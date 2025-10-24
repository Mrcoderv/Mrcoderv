#!/usr/bin/env python3
"""
Nepal Stock Exchange (NEPSE) Real-time Chart Analysis - Basic Version
Author: Raghav Panthi (Mrcoderv)

This is a basic implementation using only built-in Python libraries.
For full functionality, install the requirements from requirements.txt
"""

import json
import random
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import html
import os

class NepseAnalyzer:
    """Basic NEPSE analyzer using built-in libraries"""
    
    def __init__(self):
        self.stocks = [
            "NABIL", "SCB", "EBL", "BOKL", "NICA", "PRVU", 
            "GBIME", "CBL", "SANIMA", "MBL", "KBL", "ADBL"
        ]
        self.current_data = {}
        self.historical_data = {}
        
    def generate_sample_data(self, symbol, days=30):
        """Generate sample stock data for demonstration"""
        base_price = random.uniform(200, 1200)
        dates = []
        prices = []
        volumes = []
        
        # Generate data for the last 'days' days
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            dates.append(date.strftime('%Y-%m-%d'))
            
            # Simple random walk for price
            if i == 0:
                price = base_price
            else:
                change = random.uniform(-0.05, 0.05) * prices[-1]
                price = max(prices[-1] + change, 1)
            
            prices.append(round(price, 2))
            volumes.append(random.randint(1000, 50000))
        
        return {
            'symbol': symbol,
            'dates': dates,
            'prices': prices,
            'volumes': volumes,
            'current_price': prices[-1],
            'change': round(prices[-1] - prices[-2], 2) if len(prices) > 1 else 0
        }
    
    def calculate_sma(self, prices, period=10):
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return []
        
        sma = []
        for i in range(period - 1, len(prices)):
            avg = sum(prices[i-period+1:i+1]) / period
            sma.append(round(avg, 2))
        
        return sma
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI (simplified version)"""
        if len(prices) < period + 1:
            return None
        
        changes = []
        for i in range(1, len(prices)):
            changes.append(prices[i] - prices[i-1])
        
        gains = [max(0, change) for change in changes]
        losses = [abs(min(0, change)) for change in changes]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def get_market_summary(self):
        """Get market summary data"""
        summary = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'market_status': 'OPEN' if 10 <= datetime.now().hour <= 15 else 'CLOSED',
            'total_stocks': len(self.stocks),
            'advancing': 0,
            'declining': 0,
            'unchanged': 0
        }
        
        for symbol in self.stocks:
            data = self.generate_sample_data(symbol, 2)
            if data['change'] > 0:
                summary['advancing'] += 1
            elif data['change'] < 0:
                summary['declining'] += 1
            else:
                summary['unchanged'] += 1
        
        return summary

class WebInterface:
    """Simple web interface for the NEPSE analyzer"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def generate_html(self):
        """Generate HTML for the web interface"""
        summary = self.analyzer.get_market_summary()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEPSE Real-time Analysis</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            color: #ffffff;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .summary-card {{
            background: #2d2d2d;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        .stock-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stock-card {{
            background: #2d2d2d;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #00ff88;
        }}
        .stock-price {{
            font-size: 24px;
            font-weight: bold;
            color: #00ff88;
        }}
        .stock-change {{
            font-size: 16px;
            margin-top: 5px;
        }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4444; }}
        .neutral {{ color: #ffaa00; }}
        .chart-placeholder {{
            background: #1a1a1a;
            height: 200px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 15px;
            border: 1px solid #444;
        }}
        .refresh-btn {{
            background: #00ff88;
            color: #1e1e1e;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }}
        .refresh-btn:hover {{
            background: #00cc77;
        }}
    </style>
    <script>
        function refreshData() {{
            location.reload();
        }}
        
        function drawSimpleChart(canvasId, prices, dates) {{
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            const width = canvas.width = canvas.offsetWidth;
            const height = canvas.height = 150;
            
            // Clear canvas
            ctx.clearRect(0, 0, width, height);
            
            if (!prices || prices.length === 0) return;
            
            // Find min and max prices
            const minPrice = Math.min(...prices);
            const maxPrice = Math.max(...prices);
            const priceRange = maxPrice - minPrice || 1;
            
            // Draw grid
            ctx.strokeStyle = '#444';
            ctx.lineWidth = 1;
            for (let i = 1; i < 5; i++) {{
                const y = (height / 5) * i;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }}
            
            // Draw price line
            ctx.strokeStyle = '#00ff88';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            for (let i = 0; i < prices.length; i++) {{
                const x = (width / (prices.length - 1)) * i;
                const y = height - ((prices[i] - minPrice) / priceRange) * height;
                
                if (i === 0) {{
                    ctx.moveTo(x, y);
                }} else {{
                    ctx.lineTo(x, y);
                }}
            }}
            ctx.stroke();
            
            // Draw price points
            ctx.fillStyle = '#00ff88';
            for (let i = 0; i < prices.length; i++) {{
                const x = (width / (prices.length - 1)) * i;
                const y = height - ((prices[i] - minPrice) / priceRange) * height;
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, 2 * Math.PI);
                ctx.fill();
            }}
        }}
        
        window.onload = function() {{
            // Draw charts for all stocks
            const stockData = {json.dumps({symbol: analyzer.generate_sample_data(symbol, 10) for symbol in analyzer.stocks[:6]})};
            
            for (const symbol in stockData) {{
                const data = stockData[symbol];
                drawSimpleChart('chart-' + symbol, data.prices, data.dates);
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ Nepal Stock Exchange (NEPSE) Real-time Analysis</h1>
            <p>Real-time stock market analysis for Nepal Stock Exchange</p>
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
        </div>
        
        <div class="summary-card">
            <h2>Market Summary</h2>
            <p><strong>Last Updated:</strong> {summary['timestamp']}</p>
            <p><strong>Market Status:</strong> <span class="{'positive' if summary['market_status'] == 'OPEN' else 'neutral'}">{summary['market_status']}</span></p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 15px;">
                <div>
                    <h3 class="positive">↗ Advancing</h3>
                    <p style="font-size: 24px; margin: 0;">{summary['advancing']}</p>
                </div>
                <div>
                    <h3 class="negative">↘ Declining</h3>
                    <p style="font-size: 24px; margin: 0;">{summary['declining']}</p>
                </div>
                <div>
                    <h3 class="neutral">→ Unchanged</h3>
                    <p style="font-size: 24px; margin: 0;">{summary['unchanged']}</p>
                </div>
            </div>
        </div>
        
        <h2>Top Stocks</h2>
        <div class="stock-grid">
"""
        
        # Generate stock cards
        for symbol in self.analyzer.stocks[:6]:  # Show top 6 stocks
            data = self.analyzer.generate_sample_data(symbol, 10)
            change_class = 'positive' if data['change'] > 0 else 'negative' if data['change'] < 0 else 'neutral'
            change_symbol = '↗' if data['change'] > 0 else '↘' if data['change'] < 0 else '→'
            
            sma = self.analyzer.calculate_sma(data['prices'], 5)
            rsi = self.analyzer.calculate_rsi(data['prices'])
            
            html_content += f"""
            <div class="stock-card">
                <h3>{symbol}</h3>
                <div class="stock-price">Rs. {data['current_price']}</div>
                <div class="stock-change {change_class}">{change_symbol} Rs. {data['change']} ({(data['change']/data['current_price']*100):.2f}%)</div>
                <canvas id="chart-{symbol}" class="chart-placeholder" style="height: 150px; width: 100%;"></canvas>
                <div style="margin-top: 10px; font-size: 12px; color: #aaa;">
                    <p>Volume: {data['volumes'][-1]:,}</p>
                    <p>SMA(5): {sma[-1] if sma else 'N/A'}</p>
                    <p>RSI: {rsi if rsi else 'N/A'}</p>
                </div>
            </div>
            """
        
        html_content += """
        </div>
        
        <div class="summary-card" style="margin-top: 40px;">
            <h2>About NEPSE Real-time Analysis</h2>
            <p>This is a real-time stock market analysis tool for the Nepal Stock Exchange (NEPSE). 
            Currently displaying sample data for demonstration purposes.</p>
            <h3>Features:</h3>
            <ul>
                <li>📊 Real-time stock price monitoring</li>
                <li>📈 Interactive price charts</li>
                <li>🔍 Technical analysis indicators</li>
                <li>📅 Nepali calendar integration</li>
                <li>💼 Portfolio tracking</li>
            </ul>
            <p><strong>Note:</strong> This is a demonstration version using sample data. 
            For real NEPSE data integration, install the full requirements.</p>
        </div>
        
        <div class="summary-card">
            <h2>🗓️ Nepali Date Conversion</h2>
            <p>Integrated Bikram Sambat (BS) to Anno Domini (AD) date conversion from the existing date converter.</p>
            <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p><strong>Current Date (AD):</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
                <p><strong>Current Date (BS):</strong> {datetime.now().year + 56}-{datetime.now().month + 8:02d}-{datetime.now().day + 17:02d}</p>
                <p><em>Note: This is a simplified conversion. The original C code provides more accurate conversion.</em></p>
            </div>
        </div>
        
        <footer style="text-align: center; margin-top: 40px; padding: 20px; color: #888;">
            <p>© 2024 Raghav Panthi (Mrcoderv) - NEPSE Real-time Analysis</p>
            <p>Built with ❤️ for Nepal Stock Exchange traders and investors</p>
        </footer>
    </div>
</body>
</html>
"""
        return html_content

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the web server"""
    
    def __init__(self, analyzer, *args, **kwargs):
        self.analyzer = analyzer
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            interface = WebInterface(self.analyzer)
            html_content = interface.generate_html()
            self.wfile.write(html_content.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def create_request_handler(analyzer):
    """Create a request handler with the analyzer instance"""
    def handler(*args, **kwargs):
        return RequestHandler(analyzer, *args, **kwargs)
    return handler

def main():
    """Main function to run the NEPSE analyzer"""
    print("🏛️ Nepal Stock Exchange (NEPSE) Real-time Analysis")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = NepseAnalyzer()
    
    # Print some sample data
    print("\\nMarket Summary:")
    summary = analyzer.get_market_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\\nSample Stock Data:")
    for symbol in analyzer.stocks[:3]:
        data = analyzer.generate_sample_data(symbol)
        print(f"  {symbol}: Rs. {data['current_price']} (Change: {data['change']})")
    
    # Start web server
    print("\\n🌐 Starting web server...")
    print("Open http://localhost:8080 in your browser to view the interface")
    print("Press Ctrl+C to stop the server")
    
    try:
        server_address = ('', 8080)
        handler_class = create_request_handler(analyzer)
        httpd = HTTPServer(server_address, handler_class)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n\\n✅ Server stopped. Thank you for using NEPSE Real-time Analysis!")

if __name__ == "__main__":
    main()