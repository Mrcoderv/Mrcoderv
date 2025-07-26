"""
Technical Analysis module for NEPSE stocks
Implements various technical indicators and analysis tools
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Tuple

class TechnicalAnalysis:
    """Class for calculating technical indicators"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data
        Expected columns: Open, High, Low, Close, Volume
        """
        self.data = data.copy()
        self.close = data['Close']
        self.high = data['High']
        self.low = data['Low']
        self.open = data['Open']
        self.volume = data['Volume']
    
    def calculate_sma(self, period: int = 20) -> pd.Series:
        """Calculate Simple Moving Average"""
        return self.close.rolling(window=period).mean()
    
    def calculate_ema(self, period: int = 20) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return self.close.ewm(span=period).mean()
    
    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        return ta.momentum.RSIIndicator(self.close, window=period).rsi()
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        macd_indicator = ta.trend.MACD(self.close, window_slow=slow, window_fast=fast, window_sign=signal)
        return {
            'macd': macd_indicator.macd(),
            'signal': macd_indicator.macd_signal(),
            'histogram': macd_indicator.macd_diff()
        }
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: int = 2) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands"""
        bb_indicator = ta.volatility.BollingerBands(self.close, window=period, window_dev=std_dev)
        return {
            'upper': bb_indicator.bollinger_hband(),
            'middle': bb_indicator.bollinger_mavg(),
            'lower': bb_indicator.bollinger_lband()
        }
    
    def calculate_stochastic(self, k_period: int = 14, d_period: int = 3) -> Dict[str, pd.Series]:
        """Calculate Stochastic Oscillator"""
        stoch_indicator = ta.momentum.StochasticOscillator(
            self.high, self.low, self.close, 
            window=k_period, smooth_window=d_period
        )
        return {
            'k': stoch_indicator.stoch(),
            'd': stoch_indicator.stoch_signal()
        }
    
    def calculate_atr(self, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        return ta.volatility.AverageTrueRange(self.high, self.low, self.close, window=period).average_true_range()
    
    def calculate_volume_indicators(self) -> Dict[str, pd.Series]:
        """Calculate volume-based indicators"""
        return {
            'volume_sma': self.volume.rolling(window=20).mean(),
            'volume_ratio': self.volume / self.volume.rolling(window=20).mean()
        }
    
    def identify_support_resistance(self, window: int = 20) -> Dict[str, List[float]]:
        """Identify potential support and resistance levels"""
        # Find local minima (support) and maxima (resistance)
        supports = []
        resistances = []
        
        for i in range(window, len(self.data) - window):
            # Check for local minima (support)
            if self.low.iloc[i] == self.low.iloc[i-window:i+window+1].min():
                supports.append(self.low.iloc[i])
            
            # Check for local maxima (resistance)
            if self.high.iloc[i] == self.high.iloc[i-window:i+window+1].max():
                resistances.append(self.high.iloc[i])
        
        return {
            'support_levels': list(set(supports)),
            'resistance_levels': list(set(resistances))
        }
    
    def calculate_trend_direction(self, short_period: int = 10, long_period: int = 30) -> str:
        """Determine overall trend direction"""
        short_ma = self.calculate_sma(short_period).iloc[-1]
        long_ma = self.calculate_sma(long_period).iloc[-1]
        current_price = self.close.iloc[-1]
        
        if current_price > short_ma > long_ma:
            return "Strong Uptrend"
        elif current_price > short_ma and short_ma > long_ma:
            return "Uptrend"
        elif current_price < short_ma < long_ma:
            return "Strong Downtrend"
        elif current_price < short_ma and short_ma < long_ma:
            return "Downtrend"
        else:
            return "Sideways"
    
    def generate_trading_signals(self) -> Dict[str, str]:
        """Generate basic trading signals based on multiple indicators"""
        signals = {}
        
        # RSI signals
        rsi = self.calculate_rsi().iloc[-1]
        if rsi > 70:
            signals['rsi'] = "Overbought - Consider Sell"
        elif rsi < 30:
            signals['rsi'] = "Oversold - Consider Buy"
        else:
            signals['rsi'] = "Neutral"
        
        # MACD signals
        macd_data = self.calculate_macd()
        if macd_data['macd'].iloc[-1] > macd_data['signal'].iloc[-1]:
            signals['macd'] = "Bullish"
        else:
            signals['macd'] = "Bearish"
        
        # Moving Average signals
        sma_20 = self.calculate_sma(20).iloc[-1]
        current_price = self.close.iloc[-1]
        if current_price > sma_20:
            signals['moving_average'] = "Above SMA-20 - Bullish"
        else:
            signals['moving_average'] = "Below SMA-20 - Bearish"
        
        return signals
    
    def calculate_volatility(self, period: int = 20) -> float:
        """Calculate price volatility"""
        returns = self.close.pct_change().dropna()
        return returns.rolling(window=period).std().iloc[-1] * np.sqrt(252)  # Annualized volatility

class PatternRecognition:
    """Class for identifying chart patterns"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.high = data['High']
        self.low = data['Low']
        self.close = data['Close']
        self.open = data['Open']
    
    def identify_doji(self, threshold: float = 0.1) -> List[int]:
        """Identify Doji candlestick patterns"""
        doji_indices = []
        
        for i in range(len(self.data)):
            body_size = abs(self.close.iloc[i] - self.open.iloc[i])
            range_size = self.high.iloc[i] - self.low.iloc[i]
            
            if range_size > 0 and (body_size / range_size) < threshold:
                doji_indices.append(i)
        
        return doji_indices
    
    def identify_hammer(self, threshold: float = 0.3) -> List[int]:
        """Identify Hammer candlestick patterns"""
        hammer_indices = []
        
        for i in range(len(self.data)):
            open_price = self.open.iloc[i]
            close_price = self.close.iloc[i]
            high_price = self.high.iloc[i]
            low_price = self.low.iloc[i]
            
            body_size = abs(close_price - open_price)
            lower_shadow = min(open_price, close_price) - low_price
            upper_shadow = high_price - max(open_price, close_price)
            
            if (lower_shadow > 2 * body_size and 
                upper_shadow < body_size * threshold and
                body_size > 0):
                hammer_indices.append(i)
        
        return hammer_indices
    
    def identify_engulfing_patterns(self) -> Dict[str, List[int]]:
        """Identify bullish and bearish engulfing patterns"""
        bullish_engulfing = []
        bearish_engulfing = []
        
        for i in range(1, len(self.data)):
            prev_open = self.open.iloc[i-1]
            prev_close = self.close.iloc[i-1]
            curr_open = self.open.iloc[i]
            curr_close = self.close.iloc[i]
            
            # Bullish engulfing: prev candle bearish, current bullish and engulfs previous
            if (prev_close < prev_open and  # Previous candle is bearish
                curr_close > curr_open and  # Current candle is bullish
                curr_open < prev_close and  # Current opens below previous close
                curr_close > prev_open):    # Current closes above previous open
                bullish_engulfing.append(i)
            
            # Bearish engulfing: prev candle bullish, current bearish and engulfs previous
            if (prev_close > prev_open and  # Previous candle is bullish
                curr_close < curr_open and  # Current candle is bearish
                curr_open > prev_close and  # Current opens above previous close
                curr_close < prev_open):    # Current closes below previous open
                bearish_engulfing.append(i)
        
        return {
            'bullish_engulfing': bullish_engulfing,
            'bearish_engulfing': bearish_engulfing
        }