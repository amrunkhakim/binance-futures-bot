# 🚀 Binance Futures Trading Bot

Bot trading otomatis untuk Binance Futures dengan analisa teknikal dan manajemen risiko yang canggih.

## ✨ Fitur Utama

### 📊 Analisa Teknikal
- **RSI (Relative Strength Index)** - Deteksi kondisi oversold/overbought
- **MACD (Moving Average Convergence Divergence)** - Analisa momentum dan trend
- **Bollinger Bands** - Identifikasi volatilitas dan level support/resistance
- **EMA (Exponential Moving Average)** - Multiple timeframe trend analysis
- **Volume Analysis** - Konfirmasi sinyal dengan analisa volume
- **Support & Resistance** - Deteksi level kunci otomatis
- **ATR (Average True Range)** - Pengukuran volatilitas market

### 🛡️ Manajemen Risiko
- **Position Sizing** - Otomatis berdasarkan persentase dari modal
- **Stop Loss & Take Profit** - Level otomatis berdasarkan ATR
- **Trailing Stop** - Mengikuti pergerakan harga yang menguntungkan
- **Daily Loss Limit** - Perlindungan dari kerugian harian berlebihan
- **Maximum Drawdown** - Monitoring drawdown maksimum
- **Risk-Reward Ratio** - Memastikan rasio risk/reward yang sehat
- **Emergency Stop** - Fitur hentikan darurat semua trading

### 📈 Strategi Trading
- **Multi-Indicator Strategy** - Kombinasi multiple indikator
- **Scalping Strategy** - Trading jangka pendek dengan profit kecil
- **Swing Strategy** - Trading jangka menengah dengan profit besar
- **Custom Strategy** - Mudah ditambah dan dikonfigurasi

### 🤖 AI Analysis (Powered by Gemini AI)
- **Intelligent Market Sentiment** - Analisa sentimen market menggunakan AI
- **AI-Enhanced Trading Signals** - Sinyal trading yang diperkuat dengan AI
- **Smart Risk Assessment** - Penilaian risiko cerdas berbasis AI
- **Market Insights** - Wawasan mendalam tentang kondisi market
- **Pattern Recognition** - Deteksi pola market yang kompleks
- **Multi-Factor Analysis** - Kombinasi analisa teknikal dengan AI reasoning
- **Adaptive Strategy** - Strategi yang beradaptasi dengan kondisi market

### 🔔 Notifikasi
- **Telegram Notifications** - Alert trading dan error
- **Discord Webhooks** - Integrasi dengan Discord server
- **Daily Reports** - Laporan harian performa trading

## 🛠️ Instalasi

### Prasyarat
- Python 3.9 atau lebih baru
- Akun Binance dengan API key yang sudah dikonfigurasi
- Modal trading (recommended minimum $100 untuk testnet)

### 1. Clone Repository
```bash
git clone https://github.com/amrunkhakim/binance-futures-bot.git
cd binance-futures-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Environment
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi Anda
```

### 4. Setup API Binance
1. Login ke [Binance](https://www.binance.com)
2. Pergi ke API Management
3. Create API Key baru
4. Aktifkan permissions untuk Futures Trading
5. Masukkan API Key dan Secret ke file `.env`

⚠️ **PENTING**: Gunakan testnet dulu untuk testing!

## ⚙️ Konfigurasi

Edit file `.env` dengan pengaturan Anda:

```env
# API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TESTNET=true  # Set false untuk live trading

# Risk Management
MAX_POSITION_SIZE_PERCENT=5.0  # Maksimal 5% modal per posisi
MAX_DAILY_LOSS_PERCENT=2.0     # Stop trading jika rugi 2% per hari
STOP_LOSS_PERCENT=2.0          # Stop loss 2% dari entry
TAKE_PROFIT_PERCENT=6.0        # Take profit 6% dari entry

# Trading Settings
STRATEGY_NAME=multi_indicator   # Strategi yang digunakan
TIMEFRAME=15m                   # Timeframe analisa
LEVERAGE=10                     # Leverage maksimum
```

## 🚀 Cara Menjalankan

### 🖥️ Mode GUI (Recommended)
```bash
# Install GUI dependencies
pip install -r requirements_gui.txt

# Jalankan GUI
python start_gui.py
```

### 💻 Mode Terminal/Console
```bash
# Mode Testnet (Recommended untuk pemula)
python start.py

# Atau langsung
python main.py
```

### ⚡ Mode Live Trading (Setelah testing sukses)
Edit `.env`:
```env
TESTNET=false
```

## 📊 Monitoring dan Analytics

### Dashboard (Coming Soon)
- Real-time position monitoring
- Performance analytics
- Risk metrics dashboard

### Logs
Bot akan membuat log di folder `logs/`:
- `trading_bot.log` - Log utama trading
- `errors.log` - Error logs
- `trades.log` - History semua trading

### Database
Semua data trading disimpan di SQLite database:
- Trade history
- Performance metrics
- Risk statistics

## 🤖 AI Analysis - Powered by Google Gemini

### ✨ Fitur AI yang Revolusioner

Bot ini dilengkapi dengan **Artificial Intelligence** menggunakan **Google Gemini AI** yang memberikan analisis pasar tingkat lanjut:

#### 🧠 **Intelligent Market Sentiment Analysis**
- **Deep Market Understanding**: AI menganalisis gabungan data teknikal, volume, dan pergerakan harga
- **Sentiment Classification**: BULLISH, BEARISH, atau NEUTRAL dengan tingkat kepercayaan
- **Multi-Factor Reasoning**: AI menjelaskan alasan di balik setiap analisis sentiment
- **Key Factors Identification**: Mengidentifikasi faktor-faktor kunci yang mempengaruhi market

#### 🎯 **AI-Enhanced Trading Signals**
- **Smart Signal Generation**: Kombinasi analisa teknikal tradisional dengan AI reasoning
- **Dynamic Entry/Exit Points**: AI menentukan titik entry dan exit yang optimal
- **Risk-Reward Optimization**: Otomatis menghitung dan mengoptimalkan rasio risk/reward
- **Time Horizon Analysis**: Menentukan apakah sinyal cocok untuk scalping, swing, atau long-term
- **Confidence Scoring**: Setiap sinyal dilengkapi dengan skor kepercayaan AI

#### ⚖️ **Smart Risk Assessment**
- **Dynamic Position Sizing**: AI menyesuaikan ukuran posisi berdasarkan kondisi market
- **Volatility-Based Adjustments**: Stop loss dan take profit disesuaikan dengan volatilitas
- **Market Condition Awareness**: Risk assessment berubah sesuai kondisi market (trending, ranging, volatile)
- **Real-time Risk Monitoring**: Monitoring risiko secara real-time dengan rekomendasi AI

#### 📊 **Comprehensive Market Insights**
- **Market Structure Analysis**: AI menganalisis struktur pasar dan pola yang kompleks
- **Support/Resistance Intelligence**: Identifikasi level S/R dengan reasoning yang mendalam
- **Breakout Scenario Prediction**: Prediksi skenario breakout dengan probabilitas
- **Pattern Recognition**: Mengenali pola-pola market yang sulit dideteksi manusia

### 🛠️ **Setup AI Analysis**

#### 1. Install Dependencies untuk AI
```bash
# Install AI-specific requirements
pip install -r requirements_ai.txt
```

#### 2. Konfigurasi AI (Opsional - sudah built-in)
```env
# AI Configuration (sudah default, bisa diubah jika perlu)
AI_ENABLED=true
AI_MODEL=gemini-1.5-flash
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2048
```

#### 3. Test AI Connection
```bash
# Test koneksi AI
python test_ai.py
```

### 🎮 **Menggunakan AI Analysis**

#### Via GUI:
1. **AI Analysis Tab**: Lihat analisis sentiment real-time
2. **Enhanced Signals**: Sinyal trading dengan AI enhancement
3. **Risk Dashboard**: Monitor risk assessment dari AI
4. **Market Insights**: Dapatkan insights mendalam tentang market

#### Via Console:
```python
from src.ai_analyzer import AIAnalyzer

# Initialize AI
ai = AIAnalyzer()

# Test AI connection
test_result = await ai.test_connection()
print(f"AI Status: {test_result['status']}")

# Get market sentiment
sentiment = await ai.analyze_market_sentiment(
    symbol="BTCUSDT",
    market_data=market_data,
    technical_analysis=tech_data
)
print(f"AI Sentiment: {sentiment['ai_sentiment']}")
print(f"Confidence: {sentiment['confidence']:.2f}")
print(f"Reasoning: {sentiment['reasoning']}")
```

### 📈 **AI Analysis Examples**

#### **Sentiment Analysis Result:**
```json
{
    "ai_sentiment": "BULLISH",
    "confidence": 0.78,
    "reasoning": "Strong upward momentum confirmed by RSI recovery from oversold levels, MACD bullish crossover, and increasing volume. Bollinger Bands expansion indicates potential breakout.",
    "key_factors": [
        "RSI recovery from 28 to 45",
        "MACD bullish crossover",
        "Volume increase 45%",
        "Breaking above EMA resistance"
    ],
    "recommendation": "BUY",
    "risk_level": "MEDIUM"
}
```

#### **AI Trading Signal:**
```json
{
    "action": "BUY",
    "signal_strength": 0.85,
    "entry_price": 43250.00,
    "stop_loss": 42100.00,
    "take_profit": 45500.00,
    "reasoning": "Multiple confluences: EMA golden cross, RSI divergence reversal, and volume confirmation. Market structure supports bullish continuation.",
    "risk_reward_ratio": 2.1,
    "time_horizon": "SHORT",
    "ai_confidence": 0.85
}
```

### 🚀 **Keunggulan AI vs Traditional Analysis**

| Fitur | Traditional | AI-Enhanced |
|-------|-------------|-------------|
| **Pattern Recognition** | Basic | Advanced & Complex |
| **Multi-Factor Analysis** | Limited | Comprehensive |
| **Reasoning** | Rule-based | Contextual & Adaptive |
| **Market Sentiment** | Basic indicators | Deep understanding |
| **Risk Assessment** | Static rules | Dynamic & Adaptive |
| **Signal Quality** | Good | Superior |
| **Adaptability** | Fixed | Learning & Evolving |

### ⚠️ **AI Limitations & Considerations**

- **Internet Required**: AI analysis membutuhkan koneksi internet
- **API Limits**: Google Gemini memiliki rate limits (sudah dioptimasi)
- **Not 100% Accurate**: AI membantu tapi tidak menjamin profit
- **Fallback System**: Jika AI tidak tersedia, sistem fallback otomatis aktif
- **Learning Curve**: Hasil AI perlu dipahami dan dikombinasikan dengan experience

### 💡 **Tips Menggunakan AI Analysis**

1. **Combine with Experience**: Gunakan AI sebagai tool tambahan, bukan pengganti experience
2. **Monitor Confidence Levels**: Perhatikan tingkat kepercayaan AI untuk setiap analisis
3. **Understand Reasoning**: Baca dan pahami reasoning yang diberikan AI
4. **Validate with Traditional**: Cross-check dengan analisis teknikal tradisional
5. **Track Performance**: Monitor performa sinyal AI vs traditional analysis

## 🎯 Strategi Trading

### 1. Multi-Indicator Strategy
**Best untuk**: Pemula hingga menengah
**Timeframe**: 15m - 1h
**Risk Level**: Medium

Menggabungkan:
- RSI untuk momentum
- MACD untuk trend confirmation  
- EMA untuk trend direction
- Bollinger Bands untuk entry/exit
- Volume untuk signal strength

### 2. Scalping Strategy  
**Best untuk**: Trader berpengalaman
**Timeframe**: 1m - 5m
**Risk Level**: High

Focus pada:
- Quick RSI reversals
- MACD momentum changes
- High volume confirmation
- Tight stop loss (0.3%)
- Quick profit taking (0.5%)

### 3. Swing Strategy
**Best untuk**: Conservative traders
**Timeframe**: 4h - 1d  
**Risk Level**: Low-Medium

Menggunakan:
- Strong EMA trends
- Support/Resistance levels
- MACD trend confirmation
- Wider stop loss (4%)
- Higher profit targets (8%)

## ⚠️ Peringatan Risiko

**TRADING CRYPTOCURRENCY SANGAT BERISIKO**

- ⚡ **Volatilitas Tinggi**: Crypto market sangat volatile
- 💸 **Risk of Total Loss**: Anda bisa kehilangan seluruh modal
- 🤖 **Bot Bukan Jaminan Profit**: Tidak ada jaminan keuntungan
- 📊 **Backtest ≠ Live Results**: Hasil masa lalu tidak menjamin masa depan
- 🧪 **Testing Required**: Selalu test di testnet dulu

### Saran Risk Management:
1. Mulai dengan modal kecil
2. Jangan pernah trading dengan uang yang tidak bisa Anda rugi
3. Gunakan stop loss yang ketat
4. Diversifikasi strategi
5. Monitor terus performa bot

## 🔧 Troubleshooting

### Error Umum

**1. API Key Error**
```
Error: Invalid API key
```
**Solusi**: Pastikan API key dan secret benar, dan permissions sudah diaktifkan.

**2. Insufficient Balance**
```
Error: Insufficient balance
```
**Solusi**: Pastikan balance cukup untuk minimal trade amount.

**3. Symbol Not Found**
```
Error: Invalid symbol
```
**Solusi**: Pastikan symbol trading benar (contoh: BTCUSDT).

### Performance Issues
- Reduce number of symbols if bot running slow
- Increase scan interval for less frequent analysis
- Check internet connection stability

## 📝 Development

### Struktur Kode
```
binance_futures_bot/
├── main.py                 # Entry point
├── src/
│   ├── config.py          # Configuration management
│   ├── binance_client.py  # Binance API client
│   ├── technical_analyzer.py # Technical analysis
│   ├── risk_manager.py    # Risk management
│   ├── strategy_manager.py # Trading strategies
│   ├── position_manager.py # Position management
│   └── notification_manager.py # Notifications
├── tests/                 # Unit tests
├── logs/                  # Log files
└── data/                  # Database and data files
```

### Menambah Strategi Baru
1. Buat class baru inherit dari `BaseStrategy`
2. Implement method `generate_signal()`
3. Tambahkan ke `StrategyManager`
4. Test dengan backtest

### Contributing
1. Fork repository
2. Create feature branch
3. Add tests untuk fitur baru
4. Submit pull request

## 📈 Roadmap

### ✅ Current Features (v1.0)
- [x] **Advanced Technical Analysis** - RSI, MACD, Bollinger Bands, EMA, Volume
- [x] **AI-Powered Analysis** - Google Gemini AI integration
- [x] **Intelligent Sentiment Analysis** - AI market sentiment with reasoning
- [x] **AI-Enhanced Trading Signals** - Smart signal generation
- [x] **Smart Risk Assessment** - Dynamic AI risk management
- [x] **GUI Interface** - User-friendly graphical interface
- [x] **Multi-Strategy Support** - Scalping, Swing, Multi-Indicator
- [x] **Real-time Monitoring** - Live market data and position tracking
- [x] **Risk Management** - Stop loss, take profit, position sizing
- [x] **Notifications** - Telegram and Discord integration

### 🔄 Version 1.5 (In Development)
- [ ] **Enhanced AI Models** - GPT-4 and Claude integration
- [ ] **AI Strategy Optimization** - Self-learning strategy parameters
- [ ] **Backtesting Engine** - Historical strategy testing with AI
- [ ] **Advanced Risk Metrics** - VaR, Sharpe ratio, maximum drawdown
- [ ] **Custom Alert System** - Advanced notification rules
- [ ] **Market Regime Detection** - AI-powered market condition classification
- [ ] **Sentiment from News** - News sentiment analysis integration
- [ ] **Multi-Asset Correlation** - Cross-asset analysis for better signals

### 🚀 Version 2.0 (Future)
- [ ] **Web-based Dashboard** - Cloud-based monitoring and control
- [ ] **Machine Learning Pipeline** - Custom ML model training
- [ ] **Multi-exchange Support** - Binance, Bybit, OKX integration
- [ ] **Portfolio Management** - Multi-strategy portfolio optimization
- [ ] **Social Trading** - Follow and copy successful strategies
- [ ] **Advanced AI Features:**
  - [ ] Reinforcement Learning for adaptive strategies
  - [ ] Natural Language Trading Commands
  - [ ] Predictive Market Analysis
  - [ ] Automated Strategy Creation
- [ ] **Enterprise Features:**
  - [ ] Multi-user support
  - [ ] White-label solutions
  - [ ] API for third-party integrations
  - [ ] Advanced reporting and analytics

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/amrunkhakim/binance-futures-bot.git/issues)
- **Telegram**: @your_telegram
- **Email**: support@yourbot.com

## 📜 License

MIT License - lihat file `LICENSE` untuk detail.

## ⭐ Acknowledgments

- Binance API Documentation
- TA-Lib Technical Analysis Library  
- Python Async/Await Best Practices
- Trading Strategy Research Papers

---

**Disclaimer**: Bot ini dibuat untuk tujuan edukasi dan research. Gunakan dengan risiko Anda sendiri. Developer tidak bertanggung jawab atas kerugian trading.
