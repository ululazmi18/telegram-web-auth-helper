# Telegram Web Auth Helper 🌐

Skrip Python sederhana untuk membantu proses login ke **Telegram Web (K Version)** secara otomatis dan persisten. Skrip ini bertindak sebagai "jembatan" antara API Telegram (Backend) dan Browser (Frontend).

## ✨ Fitur Utama

1.  **Auto OTP Fetcher 📩**:
    *   Tidak perlu buka HP! Skrip akan memonitor pesan masuk dari Telegram (ID 777000).
    *   Begitu ada kode login, skrip langsung menampilkannya di terminal.
    
2.  **Sesi Browser Persisten 🍪**:
    *   Menggunakan profil Chrome khusus untuk setiap nomor.
    *   Login sekali, **awet selamanya** (selama session valid). Tidak perlu scan ulang setiap kali menjalankan tool.

3.  **Multi-Metode Login 🔑**:
    *   Mendukung login via **Scan QR Code** (langsung dari terminal/window).
    *   Mendukung login via **Nomor Telepon** (input kode manual).
    *   Jika belum punya file `.session`, skrip akan memandu untuk membuatnya.

## 🛠️ Persyaratan Sistem

-   Python 3.8+
-   Google Chrome (terinstall di sistem)

## 📦 Instalasi

1.  **Clone repository ini**:

```bash
git clone https://github.com/ululazmi18/telegram-web-auth-helper.git
cd telegram-web-auth-helper
```

2.  **Install Library** yang dibutuhkan:

```bash
pip install pyrofork playwright
playwright install chromium
```

> **Catatan:** Kami menggunakan `pyrofork` sebagai fork modern dari Pyrogram.

## 🚀 Cara Penggunaan

Cukup jalankan satu file skrip ini:

```bash
python tg_web_auth.py
```

### Skenario 1: Belum Punya Sesi (Pengguna Baru)
1.  Jalankan skrip.
2.  Skrip akan mendeteksi tidak ada file `.session`.
3.  Pilih metode login:
    *   **[1] Scan QR Code:** Akan muncul QR Code (atau instruksi), scan pakai HP.
    *   **[2] Nomor Telepon:** Masukkan nomor, tunggu kode SMS/Telegram di HP, masukkan ke terminal.
4.  Setelah sukses, file `.session` akan dibuat otomatis.

### Skenario 2: Sudah Punya Sesi
1.  Jalankan skrip.
2.  Skrip otomatis mendeteksi file `.session` di folder.
3.  Browser Chrome akan terbuka otomatis menuju `web.telegram.org`.
4.  Jika diminta login manual di browser, masukkan nomor HP Anda.
5.  **Tunggu kode!** Lihat terminal, kode OTP dari Telegram akan muncul otomatis di sana.
6.  Ketik kode di browser. Selesai!

## 📂 Struktur File

*   `tg_web_auth.py`: Script utama.
*   `*.session`: File sesi Pyrogram (JANGAN DISEBARKAN/DIUPLOAD).
*   `*_chrome/`: Folder data browser Chrome (Cache, Cookies, Local Storage).

## ⚠️ Disclaimer

Alat ini dibuat untuk tujuan edukasi dan mempermudah manajemen akun sendiri. Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini. Gunakan dengan bijak dan sesuai ToS Telegram.
