Convert exported Amazon order and return history into something close to credit card transactions.

## Why
To better track my finances, I wanted to figure out what Amazon orders / products each of my credit card transactions corresponded to so I could categorize the transactions and figure out where my spending is going.

Amazon has a [transactions page](https://www.amazon.com/cpe/yourpayments/transactions), but it does not allow navigating directly to specific time periods, instead requiring you to hit the 'Next' page button as many times as needed to go back in time. Worse, you cannot link to transactions pages as they do not modify the URL, so if you lose your place (or Amazon gives the dreaded "you have no transactions" error) you have to start all over again.

There are other tools like the Chrome extension [Amazon Order History Reporter (Azad)](https://github.com/philipmulcahy/azad) which can export your order history by scraping Amazon pages, but I found them all to output lots of missing data to the point of being nearly unusable. To be fair, Amazon order history and transacions pages are an ever moving target. 

Working directly with official Amazon exported data like this script does is much easier and in principle fully complete. Plus it comes in a convenient CSV format that you may find useful for your own quick lookups and analysis.

I personally use this tool to track my spending with [Lunch Money](https://lunchmoney.app/), categorizing Amazon transactions based on what I bought. In the near future I plan to create a tool that makes use of the exported data from this tool to directly update corresponding transactions in Lunch Money since it has an open API.

## Quick Start

1. Export your Amazon order history (may take an hour or longer): https://www.amazon.com/hz/privacy-central/data-requests/preview.html
1. While you wait, install this script using `pipx install .`, `uv tool install .`, or a similar Python app manager.
1. Once export is complete, download the resulting ZIP file and extract the `Retail.OrderHistory.1.csv` and `Retail.OrdersReturned.Payments.1.csv` files, ideally to the same location as the script to avoid specifiying paths.
1. Run the script, pointing it to your files and desired output filename (see [Usage](#usage)).
1. Done! Your transactions CSV file will not perfectly match 

## Usage

Order transactions only:

```
amazon-order-history-to-transactions Retail.OrderHistory.1.csv transactions.csv
```

Orders + returns combined:

```
amazon-order-history-to-transactions Retail.OrderHistory.1.csv transactions.csv --returns Retail.OrdersReturned.Payments.1.csv
```
