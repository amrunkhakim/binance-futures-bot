# Premium Subscription System

Sistem berlangganan premium untuk Binance Futures Trading Bot dengan pembayaran QRIS dan pembatasan fitur.

## 🚀 Fitur

### Fitur Free (Gratis)
- ✅ Dashboard basic
- ✅ Manual trading
- ✅ Basic logs
- ✅ Price monitoring

### Fitur Premium (Berbayar)
- 🔥 Bot trading otomatis 24/7
- 🤖 AI analysis & machine learning
- 📊 Advanced analytics & reporting
- 🛡️ Risk management lanjutan
- 🎯 Multi-strategy trading
- 📱 Telegram alerts real-time
- 📈 Backtesting & optimasi strategi
- 💼 Portfolio management
- 🔧 Custom indicators
- 🔌 API access untuk integrasi

## 💰 Harga Berlangganan

- **Bulanan**: Rp 99.000 per bulan
- **Tahunan**: Rp 999.000 per tahun (hemat 17%)

## 🏛️ Metode Pembayaran

Semua pembayaran menggunakan sistem **QRIS** untuk kemudahan dan keamanan:

- 🏛️ Bank Transfer / Mobile Banking
- 💳 E-Wallet (GoPay, OVO, DANA, LinkAja)
- 📱 QRIS (Scan & Pay)
- 🛒 Virtual Account

## 📱 Kontak & Support

- **WhatsApp**: 081391782567
- **Email**: support@binancebot.com
- **Waktu Layanan**: 24/7

## 🔧 Instalasi

### 1. Install Dependencies
```bash
python install_premium_deps.py
```

### 2. Manual Installation (jika diperlukan)
```bash
pip install qrcode[pil] Pillow
```

## 💻 Penggunaan

### 1. Akses Menu Premium
- Buka aplikasi trading bot
- Klik menu **💎 Premium** di sidebar
- Lihat status berlangganan Anda

### 2. Berlangganan Premium
1. Pilih paket berlangganan (Bulanan/Tahunan)
2. Klik tombol "Berlangganan"
3. Scan QR code QRIS yang muncul
4. Lakukan pembayaran sesuai nominal
5. Screenshot bukti pembayaran
6. Kirim ke WhatsApp: **081391782567** dengan Transaction ID

### 3. Aktivasi Manual
Setelah pembayaran:
1. Simpan Transaction ID
2. Screenshot bukti pembayaran
3. Kirim ke WhatsApp dengan format:
   ```
   Halo, saya telah melakukan pembayaran untuk Binance Bot Premium.
   Transaction ID: [ID_TRANSAKSI]
   Mohon aktivasi akun premium saya.
   
   [Lampirkan screenshot bukti pembayaran]
   ```

## 🔐 Sistem Feature Gating

### Struktur Fitur
```python
# Free features
free_features = [
    "basic_dashboard",
    "manual_trading", 
    "basic_logs",
    "price_monitoring"
]

# Premium features
premium_features = [
    "automated_trading",
    "ai_analysis", 
    "advanced_analytics",
    "risk_management",
    "multi_strategy",
    "telegram_alerts",
    "backtesting",
    "portfolio_management",
    "custom_indicators",
    "api_access"
]
```

### Penggunaan dalam Kode
```python
from src.feature_gate import premium_feature

@premium_feature("automated_trading")
def start_bot(self):
    # Bot hanya dapat dijalankan oleh pengguna premium
    pass
```

## 📁 File Structure

```
src/
├── subscription_manager.py    # Manajemen berlangganan
├── feature_gate.py           # Sistem pembatasan fitur
gui/
├── premium_panel.py          # Interface berlangganan
config/
├── license.json              # Data lisensi (auto-generated)
```

## 🔄 Alur Berlangganan

1. **Pengguna Free**
   - Akses terbatas ke fitur basic
   - Melihat pesan upgrade untuk fitur premium

2. **Generate QRIS**
   - Sistem generate QR code unik
   - Transaction ID dibuat otomatis
   - Nominal sesuai paket yang dipilih

3. **Pembayaran**
   - Pengguna scan QR code
   - Lakukan pembayaran via e-wallet/bank
   - Simpan bukti pembayaran

4. **Verifikasi Manual**
   - Admin menerima notifikasi pembayaran
   - Verifikasi bukti pembayaran
   - Aktivasi akun premium

5. **Pengguna Premium**
   - Akses penuh ke semua fitur
   - Bot trading otomatis aktif
   - Fitur advanced tersedia

## ⚙️ Konfigurasi

### Subscription Manager
```python
payment_info = {
    "phone": "081391782567",
    "name": "Binance Bot Premium",
    "monthly_price": 99000,
    "yearly_price": 999000,
    "currency": "IDR"
}
```

### License File
File `config/license.json` dibuat otomatis dengan struktur:
```json
{
    "subscription_type": "premium",
    "expiry_date": "2024-12-31T23:59:59",
    "license_key": "ABC123DEF456",
    "features": [...],
    "payment_verified": true,
    "transaction_id": "TXN123456"
}
```

## 🛠️ Development

### Menambah Fitur Premium Baru
1. Tambahkan ke `premium_features` di `SubscriptionManager`
2. Gunakan decorator `@premium_feature("feature_name")`
3. Atau check manual: `feature_gate.check_feature_access("feature_name")`

### Custom Feature Gate
```python
from src.feature_gate import FeatureGate

gate = FeatureGate(subscription_manager)

if gate.check_feature_access("custom_feature"):
    # Jalankan fitur premium
    pass
else:
    # Tampilkan pesan upgrade
    pass
```

## ⚠️ Catatan Penting

1. **Keamanan**: Sistem tidak menyimpan data pembayaran sensitif
2. **Verifikasi**: Aktivasi premium memerlukan verifikasi manual via WhatsApp
3. **Backup**: File lisensi disimpan lokal di `config/license.json`
4. **Ekspirasi**: Sistem otomatis check masa berlangganan
5. **Support**: Tim support tersedia 24/7 via WhatsApp

## 🚨 Troubleshooting

### QR Code Tidak Muncul
```bash
pip install qrcode[pil] Pillow --force-reinstall
```

### Error Import
```bash
python install_premium_deps.py
```

### Subscription Tidak Aktif
1. Check file `config/license.json`
2. Hubungi support dengan Transaction ID
3. Kirim screenshot bukti pembayaran

### Reset Subscription (Development)
```python
subscription_manager.deactivate_subscription()
```

## 📞 Support & Help

Jika mengalami kendala:

1. **Check dokumentasi** di atas
2. **WhatsApp support**: 081391782567
3. **Email**: support@binancebot.com

Tim support akan membantu:
- ✅ Aktivasi akun premium
- ✅ Troubleshooting teknis
- ✅ Bantuan penggunaan fitur
- ✅ Migrasi data
- ✅ Refund (sesuai kebijakan)
