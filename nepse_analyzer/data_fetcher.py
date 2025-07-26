"""
Data fetcher for Nepal Stock Exchange (NEPSE)
This module handles fetching real-time and historical stock data
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time
from bs4 import BeautifulSoup

class NepseDataFetcher:
    """Class to fetch NEPSE stock data from various sources"""
    
    def __init__(self):
        self.base_url = "https://www.nepalstock.com"
        self.session = requests.Session()
        
        # Headers to mimic browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session.headers.update(self.headers)
    
    def get_live_market_data(self):
        """Fetch live market data from NEPSE"""
        try:
            # This would be the actual NEPSE API endpoint
            # For now, we'll return sample data structure
            return self._get_sample_market_data()
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return None
    
    def get_stock_details(self, symbol):
        """Get detailed information for a specific stock"""
        try:
            # This would fetch from actual NEPSE API
            return self._get_sample_stock_details(symbol)
        except Exception as e:
            print(f"Error fetching stock details for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol, days=30):
        """Get historical data for a stock"""
        try:
            # This would fetch from actual NEPSE historical data API
            return self._generate_sample_historical_data(symbol, days)
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def get_market_indices(self):
        """Get market indices like NEPSE index"""
        try:
            return self._get_sample_indices()
        except Exception as e:
            print(f"Error fetching market indices: {e}")
            return None
    
    def _get_sample_market_data(self):
        """Generate sample market data for demonstration"""
        stocks = [
            {"symbol": "NABIL", "price": 1100.50, "change": 15.25, "volume": 25000},
            {"symbol": "SCB", "price": 425.75, "change": -8.50, "volume": 18000},
            {"symbol": "EBL", "price": 675.25, "change": 12.75, "volume": 32000},
            {"symbol": "BOKL", "price": 290.50, "change": -5.25, "volume": 15000},
            {"symbol": "NICA", "price": 875.25, "change": 22.50, "volume": 28000},
        ]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "stocks": stocks,
            "market_status": "OPEN"
        }
    
    def _get_sample_stock_details(self, symbol):
        """Generate sample stock details"""
        import random
        base_price = random.uniform(200, 1200)
        
        return {
            "symbol": symbol,
            "name": f"{symbol} Bank Limited",
            "current_price": base_price,
            "open": base_price * random.uniform(0.98, 1.02),
            "high": base_price * random.uniform(1.01, 1.05),
            "low": base_price * random.uniform(0.95, 0.99),
            "volume": random.randint(10000, 100000),
            "market_cap": base_price * random.randint(10000000, 50000000),
            "pe_ratio": random.uniform(8, 25),
            "sector": "Banking"
        }
    
    def _generate_sample_historical_data(self, symbol, days):
        """Generate sample historical data"""
        import numpy as np
        
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=days),
            end=datetime.now(),
            freq='D'
        )
        
        # Generate realistic price movements
        base_price = np.random.uniform(200, 1000)
        prices = [base_price]
        
        for i in range(1, len(dates)):
            # Random walk with slight upward bias
            change = np.random.normal(0.001, 0.02) * prices[-1]
            new_price = max(prices[-1] + change, 1)
            prices.append(new_price)
        
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            open_price = prices[i-1] if i > 0 else close
            high = close * np.random.uniform(1.001, 1.03)
            low = close * np.random.uniform(0.97, 0.999)
            volume = np.random.randint(5000, 50000)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close, 2),
                'volume': volume
            })
        
        return data
    
    def _get_sample_indices(self):
        """Generate sample market indices"""
        return {
            "NEPSE_INDEX": {
                "value": 2850.75,
                "change": 45.25,
                "change_percent": 1.61
            },
            "SENSITIVE_INDEX": {
                "value": 485.25,
                "change": 8.75,
                "change_percent": 1.84
            },
            "FLOAT_INDEX": {
                "value": 185.50,
                "change": 3.25,
                "change_percent": 1.78
            }
        }