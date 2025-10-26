# Improved-US-Stock-Symbols

An improved version of https://github.com/rreichel3/US-Stock-Symbols, an unmaintained repo that had open issues due to the inner functions of the GET https://api.nasdaq.com/api/screener/stocks api for stock screening.

This repository addresses key issues https://github.com/rreichel3/US-Stock-Symbols/issues/4 and https://github.com/rreichel3/US-Stock-Symbols/issues/3, while also resolving bugs such as https://github.com/rreichel3/US-Stock-Symbols/issues/7. These issues not only affected the feature set but also the core functionality of the project, as having reliable, full data updated daily was the main purpose of the repo.

An aggregation of current US Stock Symbols in `json` and `txt` formats.  

Updated daily at midnight.
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
