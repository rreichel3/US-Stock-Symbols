# US-Stock-Symbols

An aggregation of current US Stock Symbols in `json` and `txt` formats.  

Updated nightly at midnight, Eastern.
## Exchanges Available:

- NASDAQ
- NYSE
- AMEX


## How to use the data

Each exchange has three file types: 

`exchange_full_ticker.json` 

This is the raw data from NASDAQ list.  It is not a simple list of ticker symbols and contains full company name, etc.

`exchange_tickers.json` 

This is a `json` list of the ticker symbols on that exchange. Nothing more. 

`exchange_tickers.txt` 

This is a newline separated `txt` list of the ticker symbols on the exchange. Nothing more. 
## All Symbols
These may overlap across exchanges, be careful when using them. I highly recommend just consuming the per exchange list for your needs.
