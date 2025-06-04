from google_play_scraper import reviews, Sort
import pandas as pd
import time

# Inisialisasi variabel
all_reviews = []
token = None
package_name = 'com.ruangguru.livestudents'
MAX_REVIEW = 10000

print("Mengambil review dari Google Play Store...")

while True:
    r, token = reviews(
        package_name,
        lang='id',
        country='id',
        sort=Sort.NEWEST,   # Kamu juga bisa coba Sort.MOST_RELEVANT
        count=200,          # Maksimal review per panggilan
        continuation_token=token  # Untuk ambil halaman selanjutnya
    )
    all_reviews.extend(r)
    print(f"Review terkumpul: {len(all_reviews)}")

    if not token or len(all_reviews) >= MAX_REVIEW:  # Jika tidak ada lagi halaman berikutnya atau mencapai batas maksimum
        break

    time.sleep(2)  # Delay untuk menghindari diblokir

# Buat DataFrame
df = pd.DataFrame(all_reviews)
df['source'] = 'Google Play'

# Simpan ke file CSV
df.to_csv('ruangguru_all_reviews.csv', index=False, encoding='utf-8-sig')
print("Berhasil menyimpan semua review ke 'ruangguru_all_reviews.csv'")
