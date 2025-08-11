"""Configuration constants for Amazon order history processing."""

# Input CSV column mappings
INPUT_COLUMNS = {
    'WEBSITE': 'Website',
    'ORDER_ID': 'Order ID',
    'ORDER_DATE': 'Order Date',
    'SHIP_DATE': 'Ship Date',
    'CURRENCY': 'Currency',
    'UNIT_PRICE': 'Unit Price',
    'SHIPMENT_SUBTOTAL': 'Shipment Item Subtotal',
    'PRODUCT_NAME': 'Product Name',
    'QUANTITY': 'Quantity',
    'ORDER_STATUS': 'Order Status'
}

# Output CSV column names
OUTPUT_COLUMNS = [
    'Ship Date',
    'Order ID', 
    'Transaction Amount',
    'Product Names',
    'Order URL'
]

# Amazon URL template
AMAZON_ORDER_URL_TEMPLATE = 'https://amazon.com/gp/your-account/order-details?orderID={}'

# Data type specifications for pandas - use object for mixed/problematic columns
PANDAS_DTYPES = {
    'Website': 'string',
    'Order ID': 'string', 
    'Currency': 'string',
    'Unit Price': 'object',  # Handle 'Not Available' values
    'Shipment Item Subtotal': 'object',  # Handle 'Not Available' values  
    'Product Name': 'string',
    'Quantity': 'object',  # Handle 'Not Available' values
    'Order Status': 'string'
}

# Date parsing parameters
DATE_PARSER_KWARGS = {
    'format': 'ISO8601',
    'utc': True
}