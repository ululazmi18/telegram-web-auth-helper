import os
import asyncio
import glob
import re
import time
import shutil
from pathlib import Path
from pyrogram import Client, errors
from playwright.async_api import async_playwright

API_ID = 4765143
API_HASH = "780165a4b075be84420c2e44efcef5ec"

# Direktori skrip
script_dir = os.path.dirname(os.path.abspath(__file__))

async def create_session_qr():
    print("\n--- LOGIN VIA QR CODE (AUTO) ---")
    
    # Gunakan Path object untuk kompatibilitas dengan script asli
    script_path_obj = Path(script_dir)
    temp_session_name = "qr_login_temp"
    temp_session_path = script_path_obj / f"{temp_session_name}.session"
    
    # Bersihkan sesi lama
    if temp_session_path.exists():
        try:
            os.remove(temp_session_path)
        except:
            pass

    print(f"Menginisialisasi klien sementara...")
    app = Client(name=temp_session_name, api_id=API_ID, api_hash=API_HASH, workdir=str(script_path_obj))

    await app.connect()

    print("Memulai proses login dengan QR Code...")
    print("Silakan scan QR Code yang muncul menggunakan aplikasi Telegram di HP Anda.")
    print("Settings > Devices > Link Desktop Device > Scan QR Code")
    
    user = None
    try:
        while not user:
            try:
                login_token = await app.sign_in_qrcode()
                expiry = getattr(login_token, 'expires', 0)
                if not expiry:
                    expiry = time.time() + 30
                else:
                    expiry -= 10
                
                while time.time() < expiry:
                    try:
                        print(".", end="", flush=True)
                        user = await app.get_me()
                        if user:
                            print("\n✅ Scan terdeteksi!")
                            break
                    except errors.SessionPasswordNeeded:
                        raise
                    except errors.Unauthorized:
                        pass
                    except Exception as e:
                        if "SESSION_PASSWORD_NEEDED" in str(e):
                            raise errors.SessionPasswordNeeded
                        if "AUTH_TOKEN_EXPIRED" in str(e) or "expired" in str(e).lower():
                             print("\n⚠️ Token QR Code kadaluarsa. Membuat baru...")
                             break 
                        pass
                    
                    await asyncio.sleep(1)
                
                if user: break
                if not user:
                    print("\n⚠️ Waktu QR Code habis. Membuat QR Code baru...")
                    continue

            except errors.SessionPasswordNeeded:
                 print("\n🔒 Scan berhasil! Akun memiliki 2FA.")
                 while True:
                    password = input("Masukkan Password 2FA Anda: ")
                    try:
                        await app.check_password(password)
                        print("✅ Password benar!")
                        user = await app.get_me()
                        break
                    except errors.PasswordHashInvalid:
                        print("❌ Password salah. Silakan coba lagi.")
                    except Exception as e:
                        print(f"❌ Error verifikasi password: {e}")
                        break
                 if user: break

            except Exception as e:
                # Catch string-based exceptions if needed
                if "SESSION_PASSWORD_NEEDED" in str(e):
                     print("\n🔒 Scan berhasil (2FA Detected)!")
                     # Handle password input...
                     # Simplification: restart loop or handle here. 
                     # For brevity assuming standard flow caught above.
                     pass 
                
                if "AUTH_TOKEN_EXPIRED" in str(e):
                     continue

                print(f"\n❌ Terjadi kesalahan saat login QR: {e}")
                await asyncio.sleep(3)

        if not user:
            print("Gagal login.")
            return

        print(f"\nLogin BERHASIL! User: {user.first_name}")
        phone_number = user.phone_number
        if not phone_number:
            phone_number = input("Masukkan nomor telepon untuk nama file (tanpa +): ").strip()
        
        # Simpan sesi
        try:
            if hasattr(app, 'storage'):
                await app.storage.save()
        except:
            pass

        await app.disconnect()
        await asyncio.sleep(1) 
        
        # Rename session
        new_filename = f"{phone_number}.session"
        new_filepath = script_path_obj / new_filename
        
        if new_filepath.exists():
            try: os.remove(new_filepath)
            except: pass

        try:
            source_temp_path = script_path_obj / f"{temp_session_name}.session"
            if source_temp_path.exists():
                shutil.copy2(source_temp_path, new_filepath)
                print(f"✅ Sesi berhasil disimpan: {new_filename}")
                try: os.remove(source_temp_path)
                except: pass
            else:
                print("⚠️ Gagal menemukan file sesi temp.")
        except Exception as e:
            print(f"❌ Gagal menyimpan file sesi: {e}")

    except KeyboardInterrupt:
        print("\n⛔ Proses dibatalkan.")
        try: await app.disconnect()
        except: pass
    except Exception as e:
        print(f"Error: {e}")

async def create_session_phone():
    print("\n--- LOGIN VIA NOMOR TELEPON ---")
    phone_input = input("Masukkan Nomor Telepon (contoh: 6281xxx): ").strip().replace("+", "")
    
    app = Client(name=phone_input, api_id=API_ID, api_hash=API_HASH, workdir=script_dir)
    await app.connect()

    try:
        user = await app.get_me()
        print(f"Sudah login sebagai: {user.first_name}")
    except errors.Unauthorized:
        print("Belum login, mengirim kode...")
        try:
            code = await app.send_code(phone_input)
            print("Kode terkirim ke Telegram/SMS.")
            phone_code = input("Masukkan Kode OTP: ")
            
            try:
                await app.sign_in(phone_input, code.phone_code_hash, phone_code)
                print("Login berhasil!")
            except errors.SessionPasswordNeeded:
                password = input("Masukkan Password 2FA: ")
                await app.check_password(password)
                print("Login berhasil dengan 2FA!")
        except Exception as e:
            print(f"Gagal login: {e}")
    except Exception as e:
        print(f"Error: {e}")
    
    await app.disconnect()
    print(f"✅ Sesi disimpan: {phone_input}.session")

async def run_browser_helper(phone_number, session_name):
    # Gunakan absolute path agar folder selalu di tempat script berada
    session_dir = os.path.join(script_dir, f"{phone_number}_chrome")
    os.makedirs(session_dir, exist_ok=True)
    
    print(f"\n🚀 Menjalankan Browser Helper untuk: {phone_number}...")
    
    app = Client(session_name, api_id=API_ID, api_hash=API_HASH, phone_number=phone_number, workdir=script_dir)
    
    async with app:
        me = await app.get_me()
        print(f"✅ Akun Pyrogram Loaded: {me.first_name} (@{me.username})")
        
        # PLAYWRIGHT
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            
            page = await context.new_page()
            await page.goto("https://web.telegram.org/k/")
            
            print("⏳ Browser terbuka. Silakan masukkan nomor HP di browser jika diminta.")
            print("⏳ Menunggu kode login masuk ke akun Telegram ini...")
            
            last_msg_id = 0
            
            # Init last msg id
            try:
                async for msg in app.get_chat_history(777000, limit=1):
                    last_msg_id = msg.id
            except:
                pass

            # Loop wait sampai page closed + Polling pesan Telegram
            try:
                while not page.is_closed():
                    try:
                        # Cek pesan terbaru dari sistem Telegram (ID 777000)
                        async for msg in app.get_chat_history(777000, limit=1):
                            if msg.id > last_msg_id:
                                last_msg_id = msg.id
                                text = msg.text
                                # Cari kode 5 digit
                                match = re.search(r'\\b(\\d{5})\\b', text)
                                if match:
                                    print(f"\\n🔔🔔 KODE LOGIN: {match.group(1)} 🔔🔔\\n")
                                else:
                                    # Fallback jika regex gagal, print pesannya
                                    if "Login code" in text or "kode" in text.lower():
                                        print(f"\\n🔔 PESAN BARU DARI TELEGRAM: {text[:100]}...\\n")
                    except Exception:
                        pass
                    
                    await asyncio.sleep(2)
            except KeyboardInterrupt:
                pass
            
            await context.close()

async def main():
    # 1. Cek Session
    session_files = glob.glob(os.path.join(script_dir, "*.session"))
    
    selected_session = None
    selected_phone = None
    
    if not session_files:
        print("⚠️ Tidak ada file session (*.session) ditemukan di folder ini.")
        print("Silakan login terlebih dahulu untuk membuat session.")
        print("[1] Login via Scan QR Code (Mudah, via HP)")
        print("[2] Login via Nomor Telepon (Input Manual)")
        print("[3] Keluar")
        
        choice = input("Pilihan: ").strip()
        
        if choice == "1":
            await create_session_qr()
        elif choice == "2":
            await create_session_phone()
        elif choice == "3":
            return
        else:
            print("Pilihan tidak valid.")
            return
            
        # Re-check session files
        session_files = glob.glob(os.path.join(script_dir, "*.session"))
        if not session_files:
            print("❌ Belum ada session yang berhasil dibuat. Keluar.")
            return

    # 2. Pilih Session (jika ada banyak) atau ambil satu-satunya
    if len(session_files) == 1:
        filename = os.path.basename(session_files[0])
        selected_session = os.path.splitext(filename)[0] # Nama session biasanya nomor HP
        selected_phone = selected_session
        print(f"✅ Menggunakan session: {filename}")
    else:
        print("\nDaftar Session:")
        for idx, f in enumerate(session_files):
            print(f"[{idx+1}] {os.path.basename(f)}")
        
        try:
            sel_idx = int(input("Pilih nomor session: ")) - 1
            filename = os.path.basename(session_files[sel_idx])
            selected_session = os.path.splitext(filename)[0]
            selected_phone = selected_session
        except:
            print("Pilihan tidak valid.")
            return

    # 3. Jalankan Helper
    if selected_session:
        await run_browser_helper(selected_phone, selected_session)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
