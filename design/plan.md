# Amazon Order History Converter - Implementation Plan

## Project Overview
Convert Amazon order history CSV data (individual items per row) into consolidated transaction format (one row per order/transaction group).

## Phase 1: Core Data Processing Module
**File: `src/data_processor.py`**
- Create `OrderHistoryProcessor` class with methods:
  - `load_csv()` - Read Amazon CSV with proper encoding handling
  - `parse_order_data()` - Convert CSV rows to structured data objects
  - `group_by_order_and_amount()` - Group items by Order ID + Shipment Item Subtotal
  - `aggregate_transactions()` - Sum amounts and combine product names
  - `generate_order_urls()` - Create Amazon order detail URLs
  - `sort_by_date()` - Sort transactions by date (most recent first)

## Phase 2: Data Models
**File: `src/models.py`**
- `OrderItem` dataclass - Individual CSV row representation
- `Transaction` dataclass - Grouped transaction representation with fields:
  - order_date, order_id, transaction_amount, product_names, order_url

## Phase 3: CSV I/O Module
**File: `src/csv_handler.py`**
- `CSVReader` class - Handle input CSV parsing with error handling
- `CSVWriter` class - Output transaction CSV with proper formatting
- Handle edge cases: empty files, malformed data, encoding issues

## Phase 4: Main Application Logic
**File: `main.py`** (enhance existing)
- Command-line argument parsing (input file, output file)
- Error handling and logging
- Progress indication for large files
- Integration of all modules

## Phase 5: Configuration & Utilities
**File: `src/config.py`**
- Column mapping constants
- Output format specifications
- URL template patterns

## Phase 6: Testing & Validation
**File: `tests/`**
- Unit tests for each module
- Integration tests with sample data
- Edge case handling tests
- Data validation tests

## Key Implementation Details

### Grouping Logic
- Group by (Order ID, Shipment Item Subtotal) to handle partial refunds/charges
- This handles cases where orders have multiple transactions with different amounts

### Amount Handling
- Positive values = charges, negative = refunds
- Aggregate "Shipment Item Subtotal" values within each group

### Product Name Aggregation
- Semicolon-separated concatenation of all product names in the group
- Handle special characters and encoding properly

### Date Sorting
- Parse ISO format dates from "Order Date" column
- Sort final output by date descending (most recent first)

### URL Generation
- Template: `amazon.com/gp/your-account/order-details?orderID={order_id}`
- Extract Order ID from input data

## Output CSV Structure
1. Order Date
2. Order ID
3. Transaction Amount (aggregated subtotals)
4. Product Names (semicolon-separated)
5. Order URL

## Dependencies
- Python 3.9+ (as specified in pyproject.toml)
- Standard library: csv, dataclasses, datetime, argparse
- Consider pandas if data processing becomes complex
