# Nepal Stock Exchange (NEPSE) Real-time Chart Analysis

A comprehensive real-time stock market analysis tool for the Nepal Stock Exchange (NEPSE) built with Python and Streamlit.

## Features

### 📊 Live Charts
- Real-time stock price visualization
- Interactive candlestick charts
- Volume analysis
- Multiple timeframe support

### 🔍 Technical Analysis
- Moving Averages (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Stochastic Oscillator
- Support and Resistance identification
- Pattern recognition (Doji, Hammer, Engulfing patterns)

### 🔎 Stock Screener
- Filter stocks by various criteria
- Technical indicator screening
- Sector-wise analysis

### 💼 Portfolio Tracker
- Track your NEPSE investments
- Performance analysis
- Risk assessment

### 📅 Nepali Calendar Integration
- Built-in Bikram Sambat to Anno Domini date conversion
- Trading day calculations for Nepal
- Nepali fiscal year support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Mrcoderv/Mrcoderv.git
cd Mrcoderv/nepse_analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. **Live Charts**: Select a stock symbol to view real-time price charts and trading volume
2. **Technical Analysis**: Analyze stocks using various technical indicators
3. **Stock Screener**: Filter and screen stocks based on technical criteria
4. **Portfolio Tracker**: Track your investments and portfolio performance

## Data Sources

Currently displaying sample data for demonstration purposes. The application is designed to integrate with:
- Official NEPSE APIs (when available)
- Third-party financial data providers
- Web scraping from official NEPSE website

## Technical Indicators Supported

- **Trend Indicators**: SMA, EMA, MACD
- **Momentum Indicators**: RSI, Stochastic Oscillator
- **Volatility Indicators**: Bollinger Bands, ATR
- **Volume Indicators**: Volume SMA, Volume Ratio
- **Pattern Recognition**: Candlestick patterns

## File Structure

```
nepse_analyzer/
├── app.py                    # Main Streamlit application
├── data_fetcher.py          # Data fetching and API integration
├── technical_analysis.py    # Technical analysis calculations
├── date_utils.py           # Nepali calendar utilities
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Raghav Panthi (Mrcoderv)**
- Portfolio: [raghavpanthi.com.np](https://raghavpanthi.com.np)
- LinkedIn: [Raghav Vian Panthi](https://www.linkedin.com/in/raghav-vian-panthi/)
- GitHub: [Mrcoderv](https://github.com/Mrcoderv)

## Disclaimer

This tool is for educational and informational purposes only. It should not be considered as financial advice. Always do your own research before making investment decisions.