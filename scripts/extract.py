import pdfplumber
import pandas as pd
import os

pdf_path = "data/raw/Kamus Bahasa Mandar-Indonesia.pdf"
output_path = "data/processed/kamus_mandar_mentah.csv"
data_kamus = []

if not os.path.exists(pdf_path):
    print("File PDF tidak ditemukan. Pastikan letaknya benar di data/raw/")
else:
    with pdfplumber.open(pdf_path) as pdf:
        total_lembar = len(pdf.pages)
        print("="*50)
        print(f"MEMULAI EKSTRAKSI TOTAL {total_lembar} LEMBAR PDF")
        print("Mencakup halaman Romawi (ii-xx) dan Halaman Utama (1-231)...")
        print("="*50)
        
        kata_dasar = ""
        penjelasan = ""
        
        # Menyisir seluruh lembar digital dari awal sampai akhir tanpa batas
        for index, page in enumerate(pdf.pages): 
            # Indikator progres yang lebih sering agar Anda bisa memantau
            if (index + 1) % 20 == 0 or (index + 1) == total_lembar:
                print(f"-> Menyedot data di lembar digital ke-{index + 1} dari {total_lembar}...")
                
            if not page:
                continue
                
            # keep_blank_chars=True menjaga integritas spasi dan kalimat utuh
            words = page.extract_words(extra_attrs=["fontname", "size"], keep_blank_chars=True)
            
            for word in words:
                teks = word['text']
                font = str(word['fontname']).lower()
                
                # Mendeteksi font tebal (bold) sebagai penanda entri utama
                if "bold" in font:
                    if kata_dasar.strip() != "" and penjelasan.strip() != "":
                        data_kamus.append({
                            "Mandar": kata_dasar.strip(), 
                            "Indonesia": penjelasan.strip(),
                            "Halaman_PDF": index + 1 # Menyimpan informasi asal halaman digital
                        })
                        kata_dasar = ""
                        penjelasan = ""
                    kata_dasar += teks
                
                # Mendeteksi font biasa sebagai penjelasan / kalimat
                else:
                    penjelasan += teks
                    
        # Menyelamatkan entri terakhir di halaman paling akhir
        if kata_dasar.strip() != "" or penjelasan.strip() != "":
            data_kamus.append({
                "Mandar": kata_dasar.strip(), 
                "Indonesia": penjelasan.strip(),
                "Halaman_PDF": total_lembar
            })

    # Mengubah data ke bentuk tabel Pandas
    df = pd.DataFrame(data_kamus)
    
    # Menyimpan file ke CSV
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*50)
    print(f"EKSTRAKSI TOTAL SELESAI!")
    print(f"Berhasil menyedot {len(df)} baris data dari seluruh bagian PDF.")
    print(f"Data utuh tersimpan di: {output_path}")
    print("="*50)