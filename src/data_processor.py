"""Core data processing module using pandas for Amazon order history conversion."""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

from .config import (
    INPUT_COLUMNS, 
    OUTPUT_COLUMNS, 
    AMAZON_ORDER_URL_TEMPLATE,
    PANDAS_DTYPES,
    DATE_PARSER_KWARGS
)


class OrderHistoryProcessor:
    """Processes Amazon order history CSV data into consolidated transactions."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.df: Optional[pd.DataFrame] = None
        self.processed_df: Optional[pd.DataFrame] = None
    
    def load_csv(self, file_path: str | Path) -> pd.DataFrame:
        """Load Amazon order history CSV with proper encoding and data types."""
        try:
            self.logger.info(f"Loading CSV from {file_path}")
            
            # Load CSV with pandas, handling encoding automatically
            self.df = pd.read_csv(
                file_path,
                dtype=PANDAS_DTYPES,
                encoding='utf-8-sig',  # Handle BOM if present
                low_memory=False
            )
            
            self.logger.info(f"Loaded {len(self.df)} rows from CSV")
            return self.df
            
        except Exception as e:
            self.logger.error(f"Failed to load CSV: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and prepare data for processing."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_csv() first.")
        
        self.logger.info("Cleaning data...")
        
        # Parse ship dates, handling 'Not Available' values
        self.df[INPUT_COLUMNS['SHIP_DATE']] = pd.to_datetime(
            self.df[INPUT_COLUMNS['SHIP_DATE']], 
            errors='coerce',  # Convert invalid dates to NaT
            **DATE_PARSER_KWARGS
        )
        
        # Convert 'Not Available' and similar strings to NaN for numeric columns
        numeric_columns = [INPUT_COLUMNS['SHIPMENT_SUBTOTAL'], INPUT_COLUMNS['SHIPMENT_SUBTOTAL_TAX'], 'Unit Price', 'Quantity']
        for col in numeric_columns:
            if col in self.df.columns:
                # Replace non-numeric strings with NaN, then convert to numeric
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove any rows with missing critical data
        required_columns = [
            INPUT_COLUMNS['ORDER_ID'],
            INPUT_COLUMNS['SHIP_DATE'],
            INPUT_COLUMNS['SHIPMENT_SUBTOTAL'],
            INPUT_COLUMNS['SHIPMENT_SUBTOTAL_TAX'],
            INPUT_COLUMNS['PRODUCT_NAME']
        ]
        
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=required_columns)
        dropped_count = initial_count - len(self.df)
        
        if dropped_count > 0:
            self.logger.warning(f"Dropped {dropped_count} rows with missing critical data")
        
        return self.df
    
    def group_transactions(self) -> pd.DataFrame:
        """Group items by Order ID and Shipment Item Subtotal."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_csv() first.")
        
        self.logger.info("Grouping transactions...")
        
        # Calculate total transaction amount (subtotal + tax) for each row
        self.df['Transaction Amount'] = (
            self.df[INPUT_COLUMNS['SHIPMENT_SUBTOTAL']].fillna(0) + 
            self.df[INPUT_COLUMNS['SHIPMENT_SUBTOTAL_TAX']].fillna(0)
        )
        
        # Group by Order ID and Shipment Item Subtotal to handle partial refunds/charges
        grouped = self.df.groupby([
            INPUT_COLUMNS['ORDER_ID'],
            INPUT_COLUMNS['SHIPMENT_SUBTOTAL']
        ]).agg({
            INPUT_COLUMNS['SHIP_DATE']: 'first',  # Take first occurrence ship date
            INPUT_COLUMNS['PRODUCT_NAME']: lambda x: '; '.join(x.astype(str)),  # Concatenate product names
            'Transaction Amount': 'first'  # Transaction amount is the same within group (subtotal + tax)
        }).reset_index()
        
        self.logger.info(f"Grouped into {len(grouped)} transactions")
        return grouped
    
    def generate_order_urls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate Amazon order URLs using vectorized operations."""
        df = df.copy()
        df['Order URL'] = AMAZON_ORDER_URL_TEMPLATE.format(
            df[INPUT_COLUMNS['ORDER_ID']].iloc[0] if len(df) > 0 else ''
        )
        
        # Use vectorized string operation for all rows
        df['Order URL'] = df[INPUT_COLUMNS['ORDER_ID']].apply(
            lambda x: AMAZON_ORDER_URL_TEMPLATE.format(x)
        )
        
        return df
    
    def sort_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort transactions by date (most recent first)."""
        return df.sort_values(
            INPUT_COLUMNS['SHIP_DATE'], 
            ascending=False
        ).reset_index(drop=True)
    
    def process(self, input_file: str | Path) -> pd.DataFrame:
        """Complete processing pipeline."""
        self.logger.info("Starting order history processing...")
        
        # Load and clean data
        self.load_csv(input_file)
        self.clean_data()
        
        # Process transactions
        grouped_df = self.group_transactions()
        
        # Generate URLs
        url_df = self.generate_order_urls(grouped_df)
        
        # Sort by date
        final_df = self.sort_by_date(url_df)
        
        # Rename columns for output
        output_df = final_df.rename(columns={
            INPUT_COLUMNS['SHIP_DATE']: 'Ship Date',
            INPUT_COLUMNS['ORDER_ID']: 'Order ID',
            INPUT_COLUMNS['PRODUCT_NAME']: 'Product Names'
            # 'Transaction Amount' already has the correct name
        })
        
        # Select only output columns
        self.processed_df = output_df[OUTPUT_COLUMNS]
        
        self.logger.info(f"Processing complete. Generated {len(self.processed_df)} transactions")
        return self.processed_df
    
    def save_csv(self, output_file: str | Path) -> None:
        """Save processed data to CSV."""
        if self.processed_df is None:
            raise ValueError("No processed data available. Call process() first.")
        
        self.logger.info(f"Saving results to {output_file}")
        
        self.processed_df.to_csv(
            output_file,
            index=False,
            encoding='utf-8'
        )
        
        self.logger.info("Save complete")