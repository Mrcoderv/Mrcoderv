#!/usr/bin/env python3
"""
NEPSE Command Line Interface
Advanced analysis tools for Nepal Stock Exchange
"""

import json
import random
import sys
from datetime import datetime, timedelta
from basic_app import NepseAnalyzer

class AdvancedNepseAnalyzer(NepseAnalyzer):
    """Extended analyzer with advanced features"""
    
    def __init__(self):
        super().__init__()
        self.portfolio = {}
        
    def analyze_stock(self, symbol, detailed=False):
        """Detailed stock analysis"""
        if symbol not in self.stocks:
            return {"error": f"Stock {symbol} not found"}
        
        data = self.generate_sample_data(symbol, 30)
        prices = data['prices']
        
        # Calculate technical indicators
        sma_10 = self.calculate_sma(prices, 10)
        sma_20 = self.calculate_sma(prices, 20)
        rsi = self.calculate_rsi(prices)
        
        # Calculate additional metrics
        volatility = self.calculate_volatility(prices)
        momentum = self.calculate_momentum(prices, 5)
        support_resistance = self.find_support_resistance(prices)
        
        analysis = {
            'symbol': symbol,
            'current_price': data['current_price'],
            'change': data['change'],
            'change_percent': round((data['change'] / data['current_price']) * 100, 2),
            'volume': data['volumes'][-1],
            'sma_10': sma_10[-1] if sma_10 else None,
            'sma_20': sma_20[-1] if sma_20 else None,
            'rsi': rsi,
            'volatility': volatility,
            'momentum': momentum,
            'support': support_resistance['support'],
            'resistance': support_resistance['resistance'],
            'recommendation': self.get_recommendation(data, sma_10, sma_20, rsi)
        }
        
        if detailed:
            analysis['price_history'] = prices[-10:]  # Last 10 days
            analysis['volume_history'] = data['volumes'][-10:]
            analysis['trend_analysis'] = self.analyze_trend(prices)
        
        return analysis
    
    def calculate_volatility(self, prices, period=20):
        """Calculate price volatility"""
        if len(prices) < 2:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if len(returns) < period:
            period = len(returns)
        
        recent_returns = returns[-period:]
        mean_return = sum(recent_returns) / len(recent_returns)
        
        variance = sum((r - mean_return) ** 2 for r in recent_returns) / len(recent_returns)
        volatility = (variance ** 0.5) * (252 ** 0.5)  # Annualized
        
        return round(volatility, 4)
    
    def calculate_momentum(self, prices, period=5):
        """Calculate price momentum"""
        if len(prices) < period + 1:
            return 0
        
        current = prices[-1]
        past = prices[-(period + 1)]
        momentum = ((current - past) / past) * 100
        
        return round(momentum, 2)
    
    def find_support_resistance(self, prices, window=5):
        """Find support and resistance levels"""
        if len(prices) < window * 2:
            return {'support': min(prices), 'resistance': max(prices)}
        
        supports = []
        resistances = []
        
        for i in range(window, len(prices) - window):
            # Support: local minimum
            if prices[i] == min(prices[i-window:i+window+1]):
                supports.append(prices[i])
            
            # Resistance: local maximum
            if prices[i] == max(prices[i-window:i+window+1]):
                resistances.append(prices[i])
        
        support = min(supports) if supports else min(prices)
        resistance = max(resistances) if resistances else max(prices)
        
        return {'support': round(support, 2), 'resistance': round(resistance, 2)}
    
    def analyze_trend(self, prices):
        """Analyze price trend"""
        if len(prices) < 10:
            return "Insufficient data"
        
        short_trend = prices[-5:]
        medium_trend = prices[-10:]
        
        short_slope = (short_trend[-1] - short_trend[0]) / len(short_trend)
        medium_slope = (medium_trend[-1] - medium_trend[0]) / len(medium_trend)
        
        if short_slope > 0 and medium_slope > 0:
            return "Strong Uptrend"
        elif short_slope > 0:
            return "Short-term Uptrend"
        elif short_slope < 0 and medium_slope < 0:
            return "Strong Downtrend"
        elif short_slope < 0:
            return "Short-term Downtrend"
        else:
            return "Sideways"
    
    def get_recommendation(self, data, sma_10, sma_20, rsi):
        """Generate trading recommendation"""
        current_price = data['current_price']
        signals = []
        
        # RSI signals
        if rsi:
            if rsi < 30:
                signals.append("BUY")
            elif rsi > 70:
                signals.append("SELL")
        
        # Moving average signals
        if sma_10 and sma_20:
            if sma_10[-1] > sma_20[-1] and current_price > sma_10[-1]:
                signals.append("BUY")
            elif sma_10[-1] < sma_20[-1] and current_price < sma_10[-1]:
                signals.append("SELL")
        
        # Volume analysis
        recent_volume = data['volumes'][-3:]
        avg_volume = sum(recent_volume) / len(recent_volume)
        if data['volumes'][-1] > avg_volume * 1.5:
            if data['change'] > 0:
                signals.append("STRONG_BUY")
            else:
                signals.append("STRONG_SELL")
        
        # Final recommendation
        buy_signals = signals.count("BUY") + signals.count("STRONG_BUY") * 2
        sell_signals = signals.count("SELL") + signals.count("STRONG_SELL") * 2
        
        if buy_signals > sell_signals:
            return "BUY" if buy_signals - sell_signals == 1 else "STRONG_BUY"
        elif sell_signals > buy_signals:
            return "SELL" if sell_signals - buy_signals == 1 else "STRONG_SELL"
        else:
            return "HOLD"
    
    def screen_stocks(self, criteria=None):
        """Screen stocks based on criteria"""
        if criteria is None:
            criteria = {}
        
        results = []
        
        for symbol in self.stocks:
            analysis = self.analyze_stock(symbol)
            
            # Apply screening criteria
            include = True
            
            if 'min_price' in criteria and analysis['current_price'] < criteria['min_price']:
                include = False
            if 'max_price' in criteria and analysis['current_price'] > criteria['max_price']:
                include = False
            if 'min_rsi' in criteria and (not analysis['rsi'] or analysis['rsi'] < criteria['min_rsi']):
                include = False
            if 'max_rsi' in criteria and (not analysis['rsi'] or analysis['rsi'] > criteria['max_rsi']):
                include = False
            if 'recommendation' in criteria and analysis['recommendation'] not in criteria['recommendation']:
                include = False
            
            if include:
                results.append(analysis)
        
        # Sort by recommendation strength
        recommendation_order = {"STRONG_BUY": 5, "BUY": 4, "HOLD": 3, "SELL": 2, "STRONG_SELL": 1}
        results.sort(key=lambda x: recommendation_order.get(x['recommendation'], 0), reverse=True)
        
        return results
    
    def add_to_portfolio(self, symbol, quantity, purchase_price):
        """Add stock to portfolio"""
        if symbol not in self.stocks:
            return False
        
        if symbol in self.portfolio:
            # Update existing position
            total_quantity = self.portfolio[symbol]['quantity'] + quantity
            total_cost = (self.portfolio[symbol]['quantity'] * self.portfolio[symbol]['purchase_price'] + 
                         quantity * purchase_price)
            avg_price = total_cost / total_quantity
            
            self.portfolio[symbol] = {
                'quantity': total_quantity,
                'purchase_price': avg_price,
                'date_added': self.portfolio[symbol]['date_added']
            }
        else:
            # New position
            self.portfolio[symbol] = {
                'quantity': quantity,
                'purchase_price': purchase_price,
                'date_added': datetime.now().strftime('%Y-%m-%d')
            }
        
        return True
    
    def get_portfolio_performance(self):
        """Calculate portfolio performance"""
        if not self.portfolio:
            return {"error": "Portfolio is empty"}
        
        total_investment = 0
        current_value = 0
        holdings = []
        
        for symbol, position in self.portfolio.items():
            analysis = self.analyze_stock(symbol)
            current_price = analysis['current_price']
            
            investment = position['quantity'] * position['purchase_price']
            market_value = position['quantity'] * current_price
            
            total_investment += investment
            current_value += market_value
            
            holdings.append({
                'symbol': symbol,
                'quantity': position['quantity'],
                'purchase_price': position['purchase_price'],
                'current_price': current_price,
                'investment': round(investment, 2),
                'market_value': round(market_value, 2),
                'gain_loss': round(market_value - investment, 2),
                'gain_loss_percent': round(((market_value - investment) / investment) * 100, 2),
                'recommendation': analysis['recommendation']
            })
        
        portfolio_gain_loss = current_value - total_investment
        portfolio_gain_loss_percent = (portfolio_gain_loss / total_investment) * 100
        
        return {
            'total_investment': round(total_investment, 2),
            'current_value': round(current_value, 2),
            'total_gain_loss': round(portfolio_gain_loss, 2),
            'total_gain_loss_percent': round(portfolio_gain_loss_percent, 2),
            'holdings': holdings
        }

def print_separator(char="=", length=60):
    """Print a separator line"""
    print(char * length)

def print_stock_analysis(analysis):
    """Print formatted stock analysis"""
    print(f"\n📊 {analysis['symbol']} Analysis")
    print_separator("-", 40)
    print(f"Current Price: Rs. {analysis['current_price']}")
    print(f"Change: Rs. {analysis['change']} ({analysis['change_percent']}%)")
    print(f"Volume: {analysis['volume']:,}")
    
    if analysis['sma_10']:
        print(f"SMA(10): Rs. {analysis['sma_10']}")
    if analysis['sma_20']:
        print(f"SMA(20): Rs. {analysis['sma_20']}")
    if analysis['rsi']:
        print(f"RSI: {analysis['rsi']}")
    
    print(f"Volatility: {analysis['volatility']}")
    print(f"Momentum(5): {analysis['momentum']}%")
    print(f"Support: Rs. {analysis['support']}")
    print(f"Resistance: Rs. {analysis['resistance']}")
    print(f"📈 Recommendation: {analysis['recommendation']}")

def print_portfolio(performance):
    """Print formatted portfolio"""
    if 'error' in performance:
        print(f"❌ {performance['error']}")
        return
    
    print(f"\n💼 Portfolio Performance")
    print_separator("-", 50)
    print(f"Total Investment: Rs. {performance['total_investment']:,}")
    print(f"Current Value: Rs. {performance['current_value']:,}")
    print(f"Total Gain/Loss: Rs. {performance['total_gain_loss']:,} ({performance['total_gain_loss_percent']:.2f}%)")
    
    print(f"\n📋 Holdings:")
    for holding in performance['holdings']:
        status = "📈" if holding['gain_loss'] > 0 else "📉" if holding['gain_loss'] < 0 else "➡️"
        print(f"  {status} {holding['symbol']}: {holding['quantity']} shares")
        print(f"     Investment: Rs. {holding['investment']:,} | Current: Rs. {holding['market_value']:,}")
        print(f"     Gain/Loss: Rs. {holding['gain_loss']:,} ({holding['gain_loss_percent']:.2f}%)")
        print(f"     Recommendation: {holding['recommendation']}")

def main():
    """Main CLI function"""
    analyzer = AdvancedNepseAnalyzer()
    
    print("🏛️  NEPSE Advanced Analysis CLI")
    print_separator()
    
    while True:
        print("\n📋 Available Commands:")
        print("1. Analyze Stock (analyze <SYMBOL>)")
        print("2. Screen Stocks (screen)")
        print("3. Add to Portfolio (portfolio add <SYMBOL> <QUANTITY> <PRICE>)")
        print("4. View Portfolio (portfolio)")
        print("5. Market Summary (summary)")
        print("6. List Stocks (list)")
        print("7. Help (help)")
        print("8. Exit (exit)")
        
        command = input("\n💻 Enter command: ").strip().lower()
        
        if command.startswith('analyze '):
            symbol = command.split()[1].upper()
            analysis = analyzer.analyze_stock(symbol, detailed=True)
            if 'error' in analysis:
                print(f"❌ {analysis['error']}")
            else:
                print_stock_analysis(analysis)
                if 'trend_analysis' in analysis:
                    print(f"Trend: {analysis['trend_analysis']}")
        
        elif command == 'screen':
            print("\n🔍 Stock Screening")
            print("Available criteria: min_price, max_price, min_rsi, max_rsi")
            criteria_input = input("Enter criteria (e.g., min_rsi=30,max_rsi=70) or press Enter for all: ")
            
            criteria = {}
            if criteria_input.strip():
                for item in criteria_input.split(','):
                    if '=' in item:
                        key, value = item.split('=')
                        criteria[key.strip()] = float(value.strip())
            
            results = analyzer.screen_stocks(criteria)
            print(f"\n📊 Found {len(results)} stocks matching criteria:")
            for result in results[:10]:  # Show top 10
                print(f"  {result['symbol']}: Rs. {result['current_price']} - {result['recommendation']}")
        
        elif command.startswith('portfolio add '):
            parts = command.split()
            if len(parts) == 5:
                symbol = parts[2].upper()
                quantity = int(parts[3])
                price = float(parts[4])
                
                if analyzer.add_to_portfolio(symbol, quantity, price):
                    print(f"✅ Added {quantity} shares of {symbol} at Rs. {price}")
                else:
                    print(f"❌ Stock {symbol} not found")
            else:
                print("❌ Usage: portfolio add <SYMBOL> <QUANTITY> <PRICE>")
        
        elif command == 'portfolio':
            performance = analyzer.get_portfolio_performance()
            print_portfolio(performance)
        
        elif command == 'summary':
            summary = analyzer.get_market_summary()
            print(f"\n📈 Market Summary")
            print_separator("-", 30)
            for key, value in summary.items():
                print(f"{key}: {value}")
        
        elif command == 'list':
            print(f"\n📋 Available Stocks ({len(analyzer.stocks)}):")
            for i, symbol in enumerate(analyzer.stocks, 1):
                print(f"  {i:2d}. {symbol}")
        
        elif command == 'help':
            print("\n📚 Help:")
            print("  analyze NABIL     - Analyze NABIL stock")
            print("  screen            - Screen stocks with criteria")
            print("  portfolio add NABIL 100 500 - Add 100 NABIL shares at Rs. 500")
            print("  portfolio         - View portfolio performance")
            print("  summary           - Show market summary")
            print("  list              - List all available stocks")
        
        elif command == 'exit':
            print("👋 Thank you for using NEPSE Advanced Analysis CLI!")
            break
        
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please report this issue if it persists.")