#!/usr/bin/env python3
"""
Fetch US stock symbols by exchange using Alpha Vantage API

This script retrieves comprehensive stock listings and filters them by exchange:
- NASDAQ
- NYSE 
- AMEX

Requires Alpha Vantage API key (free tier available)
Get your key at: https://www.alphavantage.co/support/#api-key
"""

import requests
import json
import csv
import os
import sys
from typing import Dict, List, Set
from pathlib import Path

class StockFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Stock-Symbol-Fetcher/1.0'
        })
    
    def fetch_all_listings(self) -> List[Dict]:
        """Fetch all active US stock listings from Alpha Vantage"""
        params = {
            'function': 'LISTING_STATUS',
            'apikey': self.api_key,
            'state': 'active'  # Only active stocks
        }
        
        print("Fetching stock listings from Alpha Vantage...")
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Alpha Vantage returns CSV data for LISTING_STATUS
            lines = response.text.strip().split('\n')
            if not lines:
                raise ValueError("Empty response from Alpha Vantage")
            
            # Parse CSV data
            reader = csv.DictReader(lines)
            stocks = list(reader)
            
            print(f"Fetched {len(stocks)} total stock listings")
            return stocks
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error parsing data: {e}")
            sys.exit(1)
    
    def filter_by_exchange(self, stocks: List[Dict]) -> Dict[str, List[Dict]]:
        """Filter stocks by exchange"""
        exchanges = {
            'nasdaq': [],
            'nyse': [],
            'amex': []
        }
        
        for stock in stocks:
            exchange = stock.get('exchange', '').upper().strip()
            symbol = stock.get('symbol', '').strip()
            
            # Skip if no symbol or exchange
            if not symbol or not exchange:
                continue
            
            # Skip delisted, ETFs, and other non-equity securities
            asset_type = stock.get('assetType', '').upper()
            if asset_type not in ['STOCK', 'EQUITY', ''] and 'EQUITY' not in asset_type:
                continue
            
            # Filter by exchange
            if exchange in ['NASDAQ', 'NASDAQ GLOBAL MARKET', 'NASDAQ CAPITAL MARKET', 'NASDAQ GLOBAL SELECT']:
                exchanges['nasdaq'].append(stock)
            elif exchange in ['NYSE', 'NEW YORK STOCK EXCHANGE']:
                exchanges['nyse'].append(stock)
            elif exchange in ['AMEX', 'NYSE AMERICAN', 'AMERICAN STOCK EXCHANGE']:
                exchanges['amex'].append(stock)
        
        # Sort each exchange by symbol
        for exchange in exchanges:
            exchanges[exchange].sort(key=lambda x: x.get('symbol', ''))
        
        return exchanges
    
    def save_exchange_data(self, exchange_data: Dict[str, List[Dict]], output_dir: str):
        """Save filtered data to files"""
        output_path = Path(output_dir)
        
        for exchange_name, stocks in exchange_data.items():
            exchange_dir = output_path / exchange_name
            exchange_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract just symbols for quick lists
            symbols = [stock['symbol'] for stock in stocks]
            
            # Save full JSON data
            full_json_path = exchange_dir / f"{exchange_name}_full_tickers.json"
            with open(full_json_path, 'w') as f:
                json.dump(stocks, f, indent=2)
            
            # Save symbols-only JSON
            symbols_json_path = exchange_dir / f"{exchange_name}_tickers.json"
            with open(symbols_json_path, 'w') as f:
                json.dump(symbols, f, indent=2)
            
            # Save symbols-only text file
            symbols_txt_path = exchange_dir / f"{exchange_name}_tickers.txt"
            with open(symbols_txt_path, 'w') as f:
                f.write('\n'.join(symbols))
            
            print(f"{exchange_name.upper()}: {len(symbols)} stocks saved")
    
    def create_combined_file(self, exchange_data: Dict[str, List[Dict]], output_dir: str):
        """Create combined file with all unique symbols"""
        all_symbols: Set[str] = set()
        
        for stocks in exchange_data.values():
            for stock in stocks:
                all_symbols.add(stock['symbol'])
        
        # Sort alphabetically
        sorted_symbols = sorted(list(all_symbols))
        
        # Save to all directory
        all_dir = Path(output_dir) / 'all'
        all_dir.mkdir(parents=True, exist_ok=True)
        
        all_txt_path = all_dir / 'all_tickers.txt'
        with open(all_txt_path, 'w') as f:
            f.write('\n'.join(sorted_symbols))
        
        print(f"Combined: {len(sorted_symbols)} unique symbols saved")
    
    def validate_results(self, exchange_data: Dict[str, List[Dict]]):
        """Validate results and check for common stocks"""
        print("\n=== VALIDATION RESULTS ===")
        
        # Check counts
        total = sum(len(stocks) for stocks in exchange_data.values())
        print(f"Total stocks: {total}")
        
        for exchange, stocks in exchange_data.items():
            print(f"{exchange.upper()}: {len(stocks)} stocks")
        
        # Check for commonly missing stocks
        print("\n=== CHECKING FOR COMMON STOCKS ===")
        all_symbols = set()
        for stocks in exchange_data.values():
            all_symbols.update(stock['symbol'] for stock in stocks)
        
        test_symbols = ['VZ', 'T', 'KO', 'PFE', 'JNJ', 'WMT', 'AAPL', 'MSFT', 'GOOGL', 'TSLA']
        for symbol in test_symbols:
            status = "✓" if symbol in all_symbols else "✗"
            print(f"{status} {symbol}")

def main():
    # Get API key from environment variable or prompt user
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("Alpha Vantage API key not found in environment variable 'ALPHA_VANTAGE_API_KEY'")
        print("Get a free key at: https://www.alphavantage.co/support/#api-key")
        api_key = input("Enter your Alpha Vantage API key: ").strip()
        
        if not api_key:
            print("No API key provided. Exiting.")
            sys.exit(1)
    
    # Determine output directory (parent of script directory)
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent
    
    print(f"Output directory: {output_dir}")
    
    # Initialize fetcher and get data
    fetcher = StockFetcher(api_key)
    
    # Fetch all listings
    all_stocks = fetcher.fetch_all_listings()
    
    # Filter by exchange
    exchange_data = fetcher.filter_by_exchange(all_stocks)
    
    # Save data
    fetcher.save_exchange_data(exchange_data, output_dir)
    
    # Create combined file
    fetcher.create_combined_file(exchange_data, output_dir)
    
    # Validate results
    fetcher.validate_results(exchange_data)
    
    print("\n✓ Stock symbol extraction completed successfully!")

if __name__ == "__main__":
    main()