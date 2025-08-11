# Amazon Order History Converter - Implementation Plan

## Project Overview
Convert Amazon order history CSV data (individual items per row) into consolidated transaction format (one row per order/transaction group).

## Phase 1: Core Data Processing Module
**File: `src/data_processor.py`**
- Create `OrderHistoryProcessor` class with methods:
  - `load_csv()` - Load CSV using pandas with proper encoding
  - `clean_data()` - Handle missing values, data type conversions
  - `group_transactions()` - Group by Order ID + Shipment Item Subtotal using pandas groupby
  - `aggregate_data()` - Sum amounts and combine product names with pandas agg functions
  - `generate_order_urls()` - Create Amazon URLs using vectorized operations
  - `sort_by_date()` - Sort using pandas sort_values

## Phase 2: Data Processing with Pandas
**File: `src/data_processor.py` (continued)**
- Use pandas DataFrame for all data operations:
  - `pd.read_csv()` for input with encoding detection
  - `pd.to_datetime()` for date parsing
  - `df.groupby()` for transaction grouping
  - `df.agg()` for aggregating amounts and concatenating product names
  - `df.sort_values()` for date sorting
  - `df.to_csv()` for output

## Phase 3: Configuration & Utilities
**File: `src/config.py`**
- Column mapping constants for pandas operations
- Output format specifications
- URL template patterns
- Data type specifications for pandas

## Phase 4: Main Application Logic
**File: `main.py`** (enhance existing)
- Command-line argument parsing (input file, output file)
- Error handling and logging with pandas-specific exceptions
- Progress indication using pandas chunking for large files
- Integration of pandas-based processing

## Phase 5: Testing & Validation
**File: `tests/`**
- Unit tests for pandas operations
- Integration tests with sample data
- Performance tests for large CSV files
- Data validation tests using pandas assertions

## Key Implementation Details

### Pandas-Based Grouping Logic
- Use `df.groupby(['Order ID', 'Shipment Item Subtotal'])` to handle partial refunds/charges
- Leverage pandas' efficient grouping for large datasets

### Amount Handling with Pandas
- Positive values = charges, negative = refunds
- Use `df.groupby().agg({'Shipment Item Subtotal': 'sum'})` for aggregation
- Pandas handles Decimal/float precision automatically

### Product Name Aggregation with Pandas
- Use `df.groupby().agg({'Product Name': lambda x: '; '.join(x)})` for concatenation
- Pandas handles special characters and encoding efficiently

### Date Sorting with Pandas
- Use `pd.to_datetime()` for parsing ISO format dates
- Use `df.sort_values('Order Date', ascending=False)` for descending sort

### URL Generation with Pandas
- Use pandas vectorized string operations: `df['Order URL'] = 'amazon.com/gp/your-account/order-details?orderID=' + df['Order ID']`
- Efficient for large datasets

## Output CSV Structure
1. Order Date
2. Order ID
3. Transaction Amount (aggregated subtotals)
4. Product Names (semicolon-separated)
5. Order URL

## Dependencies
- Python 3.12+ (as specified in pyproject.toml)
- pandas - Core data processing library
- Standard library: argparse, logging

## Implementation Benefits with Pandas
- **Performance**: Vectorized operations for large CSV files
- **Memory Efficiency**: Chunked processing for very large files
- **Data Types**: Automatic type inference and conversion
- **Grouping**: Efficient groupby operations with multiple aggregation functions
- **Error Handling**: Built-in handling of missing/malformed data
- **Output**: Direct CSV export with proper formatting
