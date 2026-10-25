import streamlit as st
import pandas as pd

# 1. Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="Kamus Digital Mandar", 
    page_icon="📚", 
    layout="centered"
)

# 2. Fungsi untuk Memuat Data (dengan Caching agar performa web cepat)
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/kamus_mandar_bersih.csv")
    df = df.fillna("") # Mencegah error jika ada baris kosong
    return df

df = load_data()

# 3. Mendesain Header UI
st.title("📚 Kamus Besar Digital Mandar")
st.markdown("---")
st.write("Jelajahi kekayaan kosakata dan literatur bahasa Mandar. Ketik kata yang ingin Anda cari di bawah ini.")

# 4. Kolom Pencarian Utama
search_query = st.text_input("🔍 Cari Kosakata Mandar:", placeholder="Contoh: pamboya, macoa, lita...")

# 5. Logika Pencarian dan Menampilkan Hasil
if search_query:
    # Mencari kata yang mengandung teks input (tidak sensitif huruf besar/kecil)
    hasil = df[df['Mandar'].str.contains(search_query, case=False, na=False)]
    
    if not hasil.empty:
        st.success(f"Ditemukan {len(hasil)} hasil untuk '{search_query}'")
        
        # Menampilkan setiap hasil dalam bentuk kontainer/kartu
        for index, row in hasil.iterrows():
            with st.container():
                st.markdown(f"### {row['Mandar']}")
                st.write(f"**Penjelasan:** {row['Indonesia']}")
                st.caption(f"Sumber: Lembar PDF ke-{row['Halaman_PDF']}")
                st.markdown("---")
    else:
        st.warning(f"Kosakata '{search_query}' belum ditemukan dalam kamus.")

# Footer
st.markdown("<br><br><center><i>© 2026 MUH. ARMIL SYAM - BUDAYA GO! 2026</i></center>", unsafe_allow_html=True)