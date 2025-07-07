import pandas as pd
import json
import re
from tqdm import tqdm

INPUT_CSV = "hasil_scraping_magang_selenium.csv"
OUTPUT_CSV = "hasil_olahan_magang_final.csv"

def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]', '* ', text)
    text = re.sub(r'\r\n|\n|\r', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def process_kriteria(kriteria_list):
    hasil = {
        'kriteria_umum': '',
        'kriteria_teknis': '',
        'kriteria_soft_skills': '',
        'kriteria_khusus': ''
    }
    for item in kriteria_list:
        kategori = item.get('kategori', '').lower()
        deskripsi = clean_text(item.get('deskripsi', ''))
        if kategori == 'umum':
            hasil['kriteria_umum'] = deskripsi
        elif kategori == 'teknis':
            hasil['kriteria_teknis'] = deskripsi
        elif kategori == 'soft_skills':
            hasil['kriteria_soft_skills'] = deskripsi
        elif kategori == 'khusus':
            hasil['kriteria_khusus'] = deskripsi
    return hasil

def process_tanggung_jawab(tj_list):
    return "\n".join([clean_text(item.get("deskripsi", "")) for item in tj_list])


def main():
    try:
        print(f"Membaca data dari {INPUT_CSV}...")
        df_raw = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"File {INPUT_CSV} tidak ditemukan.")
        return

    processed = []

    print("Memproses data JSON...")
    for idx, row in tqdm(df_raw.iterrows(), total=len(df_raw)):
        json_str = row.get('data_page_json', '')

        try:
            data = json.loads(json_str)
            lowongan = data.get('props', {}).get('lowongan', {})
            mitra = lowongan.get('mitra', {})
            posisi = lowongan.get('posisi_magang', {})

            kriteria = process_kriteria(lowongan.get('lowongan_kriteria', []))
            tanggung_jawab = process_tanggung_jawab(lowongan.get('lowongan_tanggung_jawab', []))

            entry = {
                'posisi': clean_text(posisi.get('nama')),
                'deskripsi_posisi': clean_text(lowongan.get('deskripsi')),
                'lokasi': clean_text(lowongan.get('lokasi_penempatan')),
                'jumlah_dibutuhkan': lowongan.get('jumlah', ''),
                'tanggung_jawab': tanggung_jawab,
                'nama_mitra': mitra.get('nama', ''),
                'jenis_mitra': mitra.get('jenis', ''),
                'deskripsi_mitra': clean_text(mitra.get('deskripsi')),
                'kriteria_umum': kriteria['kriteria_umum'],
                'kriteria_teknis': kriteria['kriteria_teknis'],
                'kriteria_soft_skills': kriteria['kriteria_soft_skills'],
                'kriteria_khusus': kriteria['kriteria_khusus'],
                'url_lowongan': f"https://simbelmawa.kemdikbud.go.id/magang/mahasiswa/detail-lowongan/{lowongan.get('id_lowongan')}"
            }

            processed.append(entry)

        except json.JSONDecodeError:
            print(f"JSON tidak valid pada baris {idx+1}, dilewati.")
        except Exception as e:
            print(f"Kesalahan pada baris {idx+1}: {e}")

    if not processed:
        print("Tidak ada data berhasil diproses.")
        return

    df_final = pd.DataFrame(processed)
    df_final.drop_duplicates(subset=['url_lowongan'], inplace=True)

    df_final.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"Data berhasil disimpan ke {OUTPUT_CSV} ({len(df_final)} baris).")
    print(df_final.head())

if __name__ == "__main__":
    main()
