# Improved US Stock Symbols

An aggregation of current US Stock Symbols in `json` and `txt` formats, sourced from Alpha Vantage API for accurate exchange classification.

Updated nightly at midnight, Eastern via GitHub Actions.
## Exchanges Available:

- NASDAQ
- NYSE
- AMEX


## How to use the data

Each exchange has three file types: 

`exchange_full_tickers.json` 

This contains the complete company data from Alpha Vantage, including company name, asset type, exchange, status, etc.

`exchange_tickers.json` 

This is a `json` array of just the ticker symbols on that exchange. Nothing more. 

`exchange_tickers.txt` 

This is a newline separated `txt` list of the ticker symbols on the exchange. Nothing more. 

## All Symbols
These may overlap across exchanges, be careful when using them. I highly recommend just consuming the per exchange list for your needs.

## Data Source & Accuracy

This repository uses **Alpha Vantage API** to ensure:
- ✅ Proper exchange classification (no more missing stocks like VZ, T, etc.)
- ✅ Active stocks only (delisted stocks filtered out)
- ✅ Accurate company information
- ✅ Regular updates from a reliable financial data provider

### Previous Issues Fixed:
- **Missing major stocks** (VZ, T, KO, etc.) - now included
- **Symbols with special characters** (BRK-A, BRK-B) - properly handled
- **Exchange misclassification** - accurate Alpha Vantage data
- **Incomplete datasets** - comprehensive coverage

## Manual Updates

To run the data collection manually:

### Prerequisites
1. Get a free Alpha Vantage API key: https://www.alphavantage.co/support/#api-key
2. Install Python dependencies: `pip install -r requirements.txt`

### Run the script
```bash
# Set your API key
export ALPHA_VANTAGE_API_KEY="your_api_key_here"

# Run the fetcher
python script/fetch_tickers_by_exchange.py
```

The script will:
- Fetch all active US stock listings from Alpha Vantage
- Filter by exchange (NASDAQ, NYSE, AMEX)
- Generate all file formats
- Validate results and show summary statistics
