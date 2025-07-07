import os
import pandas as pd
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# Import library Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Muat variabel lingkungan dari file .env
load_dotenv()

# --- PENGATURAN ---
# Menggunakan USERNAME bukan EMAIL
USERNAME = os.getenv("MAGANG_USERNAME")
PASSWORD = os.getenv("MAGANG_PASSWORD")

# URL
LOGIN_URL = "https://simbelmawa.kemdikbud.go.id/magang/login"
BASE_URL = "https://simbelmawa.kemdikbud.go.id/magang/mahasiswa/lowongan-tersedia/{}"
TOTAL_PAGES = 344
OUTPUT_CSV = "hasil_scraping_magang_selenium.csv"
WAIT_TIMEOUT = 10 # Waktu tunggu maksimum (detik) untuk elemen muncul

def main():
    if not USERNAME or not PASSWORD:
        print("!!! PERINGATAN: Kredensial tidak ditemukan.")
        print("Pastikan Anda telah membuat file .env dan mengisinya dengan")
        print("variabel MAGANG_USERNAME dan MAGANG_PASSWORD.")
        return

    # --- Inisialisasi Selenium WebDriver ---
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Proses Login
        print("Membuka browser dan mencoba login...")
        driver.get(LOGIN_URL)

        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username.."]')))
        username_field.send_keys(USERNAME)

        password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter Password"]')))
        password_field.send_keys(PASSWORD)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        submit_button.click()

        wait.until(EC.url_contains("dashboard"))
        print("Login berhasil!")
        print(f"Memulai scraping dan mengumpulkan data mentah...")
        all_raw_data = []

        # Proses scraping halaman
        for page_num in tqdm(range(1, TOTAL_PAGES + 1), desc="Scraping Halaman"):
            try:
                page_url = BASE_URL.format(page_num)
                driver.get(page_url)
                app_div = wait.until(EC.presence_of_element_located((By.ID, "app")))
                json_string = app_div.get_attribute('data-page')
                
                if json_string:
                    all_raw_data.append({
                        'nomor_halaman': page_num,
                        'data_page_json': json_string
                    })
                else:
                    print(f"Tidak dapat menemukan data-page di halaman {page_num}. Melanjutkan...")
                    continue
            
            except Exception as e:
                print(f"Terjadi kesalahan saat memproses halaman {page_num}: {e}")
        
        if not all_raw_data:
            print("\nTidak ada data yang berhasil dikumpulkan.")
        else:
            print(f"\nProses scraping selesai. Mengonversi data ke DataFrame dan menyimpan ke {OUTPUT_CSV}...")
            df = pd.DataFrame(all_raw_data)
            df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
            print(f"Data mentah telah berhasil disimpan di {OUTPUT_CSV}")


    finally:
        print("\nProses selesai. Browser akan tetap terbuka.")
        input("Tekan Enter di terminal ini untuk menutup browser...")
        
        print("Menutup browser...")
        driver.quit()

if __name__ == "__main__":
    main()
