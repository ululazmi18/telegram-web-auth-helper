# Telegram Web Auth Helper 🌐

> **Repository Name:** `telegram-web-auth-helper`
> **Main Script:** `tg_web_auth.py`

Repositori ini berisi **Skrip Utilitas Python** yang dirancang khusus untuk menangani proses otentikasi (login) ke **Telegram Web (Versi K)** secara otomatis. Tujuan utamanya adalah menghasilkan **sesi browser persisten** (Chrome User Data Profile) yang dapat digunakan kembali oleh alat otomatisasi lain (seperti bot screenshot atau scraper) tanpa perlu login manual berulang kali.

## 🧠 Konsep Inti (Cara Kerja)

Skrip ini bertindak sebagai **jembatan penghubung** antara **API Telegram (Backend)** dan **Web Browser (Frontend)**.

1.  **Backend (Pyrogram)**:
    -   Terhubung langsung ke server Telegram menggunakan sesi API yang ringan (`.session`).
    -   Memonitor pesan masuk dari **Telegram (ID 777000)** secara real-time.
    -   **Mengapa?** Untuk menangkap **Kode OTP Login** secara otomatis, sehingga Anda tidak perlu mengecek HP untuk melihat kode.

2.  **Frontend (Playwright)**:
    -   Menjalankan instance browser Chromium (Google Chrome).
    -   **FITUR KRUSIAL**: Menggunakan `user_data_dir` khusus (contoh: `./62812345678_chrome`).
    -   **Mengapa?** Browser yang dijalankan dengan direktori data user khusus akan **menyimpan cookies dan local storage selamanya**. Sekali Anda berhasil login, folder ini akan menyimpan status login Anda. Skrip otomatisasi lain di masa depan cukup diarahkan ke folder ini agar langsung dalam status "Sudah Login".

## ✨ Fitur Utama

-   **Pengambilan OTP Otomatis**: Menangkap kode login 5 digit dari Notifikasi Layanan Telegram secara instan dan menampilkannya di terminal.
-   **Persistensi Sesi**: Membuat profil Chrome yang terisolasi untuk setiap nomor telepon.
-   **Dukungan Multi-Login**:
    -   **via QR Code**: Scan QR langsung dari aplikasi HP untuk membuat sesi.
    -   **via Nomor Telepon**: Input manual nomor HP untuk membuat sesi.
-   **Tanpa Masalah Headless**: Mendukung mode `HEADLESS=False` (tampilan browser muncul) untuk interaksi manual saat login awal.

## 🛠️ Persyaratan Sistem

-   **Python 3.8+**
-   **Google Chrome** terinstall di sistem komputer.
-   **Akun Telegram Aktif** (untuk scan QR atau menerima OTP).

## 📦 Instalasi

1.  **Clone Repository Ini**:
    ```bash
    git clone https://github.com/ululazmi18/telegram-web-auth-helper.git
    cd telegram-web-auth-helper
    ```

2.  **Install Library Pendukung**:
    ```bash
    pip install pyrofork playwright
    playwright install chromium
    ```

## 🚀 Panduan Penggunaan

Jalankan skrip utama dengan perintah:

```bash
python tg_web_auth.py
```

### 🔹 Alur Logika Program
1.  **Cek Sesi**: Skrip akan mencari apakah ada file `*.session` di folder.
2.  **Jika Sesi Tidak Ditemukan**:
    -   Program akan meminta Anda **Membuat Sesi Baru**.
    -   Pilih **[1] Scan QR** atau **[2] Nomor Telepon**.
    -   Ikuti instruksi di layar untuk login ke API Pyrogram terlebih dahulu.
    -   Setelah sukses, file `.session` akan dibuat.
3.  **Jika Sesi Ditemukan**:
    -   Program memuat sesi Pyrogram yang ada (untuk memantau OTP).
    -   Program membuka **Browser Otomatis (Chrome)** menuju `web.telegram.org`.
    -   **Langkah Manual**: Anda memasukkan nomor HP Anda di browser yang terbuka.
    -   **Langkah Otomatis**: Skrip mendeteksi kode OTP yang dikirim Telegram ke akun Anda, lalu menampilkannya di terminal: `🔔 KODE LOGIN: 12345`.
    -   **Selesai**: Masukkan kode tersebut di browser. Anda sekarang sudah login. Folder data browser `*_chrome` telah dibuat/diperbarui.

## 📂 Struktur Proyek

| File / Folder | Deskripsi |
| :--- | :--- |
| `tg_web_auth.py` | **Skrip Utama**. Mengatur logika pembuatan sesi, membuka browser, dan menangkap OTP. |
| `*.session` | **Sesi Pyrogram**. Menyimpan token otentikasi API Backend. Jaga file ini agar aman! |
| `*_chrome/` | **Data Browser**. Menyimpan Cookies, LocalStorage, dan Cache. Folder inilah yang menyimpan status login browser Anda. |

## ⚠️ Catatan Penting untuk Otomatisasi

-   **Jangan menghapus** file `*.session` atau folder `*_chrome`. Jika dihapus, Anda harus login ulang dari awal.
-   **Pengguna Termux (Android)**: Library Playwright **TIDAK BISA** berjalan secara native di Termux standar. Gunakan skrip ini di Windows/Linux/Mac atau VPS dengan dukungan GUI.
-   **Keamanan**: File `.session` memberikan akses penuh ke akun Anda via API. Jangan bagikan file ini ke orang lain.

## 📜 Lisensi
*Open Source / Tujuan Edukasi.*
