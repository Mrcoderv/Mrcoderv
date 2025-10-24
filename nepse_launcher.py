#!/usr/bin/env python3
"""
NEPSE Analysis Launcher
Quick launcher for all NEPSE analysis tools
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("🏛️  NEPAL STOCK EXCHANGE (NEPSE) REAL-TIME ANALYSIS")
    print("    by Raghav Panthi (Mrcoderv)")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print()

def print_menu():
    """Print main menu"""
    print("📋 Available Analysis Tools:")
    print()
    print("1. 🌐 Web Interface     - Interactive dashboard with charts")
    print("2. 💻 Command Line Tool - Advanced analysis CLI")
    print("3. 📊 Quick Analysis    - Quick stock analysis")
    print("4. 📈 Portfolio Demo    - Portfolio management demo")
    print("5. 🔍 Stock Screener    - Find stocks by criteria")
    print("6. 📚 Documentation     - View help and documentation")
    print("7. 🚀 Install Full      - Install all dependencies")
    print("8. ❌ Exit")
    print()

def run_web_interface():
    """Launch web interface"""
    print("🌐 Starting NEPSE Web Interface...")
    print("📝 Note: Using sample data for demonstration")
    print("🔗 Open http://localhost:8080 in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, "basic_app.py"], cwd="nepse_analyzer")
    except KeyboardInterrupt:
        print("\\n✅ Web server stopped.")

def run_cli():
    """Launch CLI tool"""
    print("💻 Starting NEPSE CLI Analysis Tool...")
    print("📝 Type 'help' for available commands")
    print()
    
    try:
        subprocess.run([sys.executable, "cli.py"], cwd="nepse_analyzer")
    except KeyboardInterrupt:
        print("\\n✅ CLI tool stopped.")

def quick_analysis():
    """Run quick analysis"""
    print("📊 NEPSE Quick Analysis")
    print("=" * 30)
    
    # Import analyzer
    sys.path.append('nepse_analyzer')
    from cli import AdvancedNepseAnalyzer
    
    analyzer = AdvancedNepseAnalyzer()
    
    # Show market summary
    summary = analyzer.get_market_summary()
    print("📈 Market Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\\n🔝 Top Performing Stocks:")
    # Quick analysis of top 5 stocks
    for symbol in analyzer.stocks[:5]:
        analysis = analyzer.analyze_stock(symbol)
        status = "📈" if analysis['change'] > 0 else "📉" if analysis['change'] < 0 else "➡️"
        print(f"  {status} {symbol}: Rs. {analysis['current_price']} ({analysis['change_percent']:+.2f}%) - {analysis['recommendation']}")

def portfolio_demo():
    """Run portfolio demo"""
    print("📈 Portfolio Management Demo")
    print("=" * 35)
    
    sys.path.append('nepse_analyzer')
    from cli import AdvancedNepseAnalyzer
    
    analyzer = AdvancedNepseAnalyzer()
    
    # Add sample portfolio
    print("💼 Creating sample portfolio...")
    analyzer.add_to_portfolio("NABIL", 100, 500)
    analyzer.add_to_portfolio("SCB", 200, 300)
    analyzer.add_to_portfolio("EBL", 150, 400)
    
    # Show performance
    performance = analyzer.get_portfolio_performance()
    print(f"\\n💰 Portfolio Value: Rs. {performance['current_value']:,}")
    print(f"📊 Total Investment: Rs. {performance['total_investment']:,}")
    print(f"💹 Gain/Loss: Rs. {performance['total_gain_loss']:,} ({performance['total_gain_loss_percent']:+.2f}%)")
    
    print("\\n📋 Holdings:")
    for holding in performance['holdings']:
        status = "📈" if holding['gain_loss'] > 0 else "📉" if holding['gain_loss'] < 0 else "➡️"
        print(f"  {status} {holding['symbol']}: {holding['quantity']} shares - {holding['recommendation']}")

def stock_screener():
    """Run stock screener"""
    print("🔍 NEPSE Stock Screener")
    print("=" * 25)
    
    sys.path.append('nepse_analyzer')
    from cli import AdvancedNepseAnalyzer
    
    analyzer = AdvancedNepseAnalyzer()
    
    print("📊 Screening stocks with RSI < 50 (potentially oversold)...")
    results = analyzer.screen_stocks({'max_rsi': 50})
    
    print(f"\\n✅ Found {len(results)} stocks:")
    for i, result in enumerate(results[:8], 1):
        print(f"  {i}. {result['symbol']}: Rs. {result['current_price']} (RSI: {result['rsi']}) - {result['recommendation']}")
    
    if len(results) > 8:
        print(f"  ... and {len(results) - 8} more")

def show_documentation():
    """Show documentation"""
    print("📚 NEPSE Analysis Documentation")
    print("=" * 35)
    print()
    print("🎯 Purpose:")
    print("  Real-time analysis and portfolio management for Nepal Stock Exchange")
    print()
    print("🚀 Features:")
    print("  • Live stock price monitoring with sample data")
    print("  • Technical analysis indicators (SMA, RSI, MACD, etc.)")
    print("  • Interactive web dashboard with charts")
    print("  • Command-line interface for advanced analysis")
    print("  • Portfolio tracking and performance analysis")
    print("  • Stock screening and filtering")
    print("  • Nepali calendar integration (BS ↔ AD conversion)")
    print()
    print("📁 Files:")
    print("  • basic_app.py      - Web interface (works without dependencies)")
    print("  • cli.py            - Command-line interface")
    print("  • app.py            - Full Streamlit app (requires dependencies)")
    print("  • data_fetcher.py   - Data fetching modules")
    print("  • technical_analysis.py - Technical indicators")
    print("  • date_utils.py     - Nepali date utilities")
    print()
    print("🔧 Installation:")
    print("  1. Basic version: No installation needed (uses built-in Python)")
    print("  2. Full version: pip install -r requirements.txt")
    print()
    print("💡 Note:")
    print("  Currently using sample data for demonstration.")
    print("  Real NEPSE API integration can be added by updating data_fetcher.py")

def install_dependencies():
    """Install full dependencies"""
    print("🚀 Installing Full NEPSE Analysis Dependencies")
    print("=" * 45)
    print()
    print("📦 Installing required packages...")
    print("⚠️  This may take a few minutes...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "nepse_analyzer/requirements.txt"
        ], check=True)
        print("✅ Installation completed successfully!")
        print("🎉 You can now use the full Streamlit version:")
        print("   cd nepse_analyzer && streamlit run app.py")
    except subprocess.CalledProcessError:
        print("❌ Installation failed. Using basic version instead.")
        print("💡 The basic version works without additional dependencies.")

def main():
    """Main launcher function"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("👉 Enter your choice (1-8): ").strip()
            print()
            
            if choice == "1":
                run_web_interface()
            elif choice == "2":
                run_cli()
            elif choice == "3":
                quick_analysis()
            elif choice == "4":
                portfolio_demo()
            elif choice == "5":
                stock_screener()
            elif choice == "6":
                show_documentation()
            elif choice == "7":
                install_dependencies()
            elif choice == "8":
                print("👋 Thank you for using NEPSE Analysis!")
                print("🌟 Star the repository if you found it useful!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-8.")
            
            input("\\n⏳ Press Enter to continue...")
            print("\\n" + "="*70 + "\\n")
            
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\\n⏳ Press Enter to continue...")

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("nepse_analyzer"):
        print("❌ Error: nepse_analyzer directory not found!")
        print("💡 Please run this script from the repository root directory.")
        sys.exit(1)
    
    main()