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

### Version 2.0
- [ ] Web-based dashboard
- [ ] More technical indicators
- [ ] Machine learning signals
- [ ] Multi-exchange support
- [ ] Portfolio management

### Version 1.5
- [ ] Backtesting engine
- [ ] Strategy optimization
- [ ] Advanced risk metrics
- [ ] Custom alert system

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
