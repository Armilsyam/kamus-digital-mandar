import pandas as pd
import re
import os

input_path = "data/processed/kamus_mandar_mentah.csv"
output_path = "data/processed/kamus_mandar_bersih.csv"

print("Memulai proses pencucian data (Data Cleaning)...")

if not os.path.exists(input_path):
    print(f"Error: File {input_path} tidak ditemukan!")
else:
    # 1. Membaca data mentah
    df = pd.read_csv(input_path)
    awal_baris = len(df)
    
    # 2. Menghapus baris yang kosong sama sekali
    df = df.dropna(subset=['Mandar', 'Indonesia'], how='all')
    
    # 3. Fungsi Regex untuk membersihkan teks dari karakter aneh dan spasi berlebih
    def bersihkan_teks(teks):
        if pd.isna(teks):
            return ""
        teks = str(teks)
        teks = teks.replace('\n', ' ')          # Mengganti enter/baris baru dengan spasi
        teks = re.sub(r'-\s+', '', teks)        # Menyambung kata yang terpotong tanda hubung di ujung baris
        teks = re.sub(r'\s+', ' ', teks)        # Mengubah spasi ganda/berkali-kali menjadi satu spasi saja
        return teks.strip()                     # Menghapus spasi di awal dan akhir teks

    # Terapkan fungsi pembersihan ke kedua kolom
    df['Mandar'] = df['Mandar'].apply(bersihkan_teks)
    df['Indonesia'] = df['Indonesia'].apply(bersihkan_teks)
    
    # 4. Hapus baris jika kolom 'Mandar' kosong setelah dibersihkan
    df = df[df['Mandar'] != ""]
    
    # 5. Hapus duplikat (jika ada kata yang terekstrak dua kali)
    df = df.drop_duplicates(subset=['Mandar'], keep='first')
    
    # 6. Simpan hasil akhirnya
    df.to_csv(output_path, index=False)
    
    akhir_baris = len(df)
    baris_dihapus = awal_baris - akhir_baris
    
    print("\n" + "="*50)
    print("PEMBERSIHAN DATA SELESAI!")
    print(f"Total awal: {awal_baris} baris.")
    print(f"Total akhir: {akhir_baris} baris kosakata bersih (berkurang {baris_dihapus} baris kotor).")
    print(f"File siap pakai tersimpan di: {output_path}")
    print("="*50)
    print("Preview Data Bersih:")
    print(df.head())