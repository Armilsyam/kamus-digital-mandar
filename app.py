import streamlit as st
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Kamus Digital Mandar", 
    page_icon="📚", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SISTEM CACHING & LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/kamus_mandar_bersih.csv")
        df = df.fillna("") 
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Mandar", "Indonesia", "Halaman_PDF"])

df = load_data()

# ==========================================
# 3. NAVIGASI SIDEBAR
# ==========================================
st.sidebar.title("🧭 Navigasi Edukasi")
st.sidebar.markdown("Pilih menu pembelajaran:")

menu_pilihan = st.sidebar.radio(
    "",
    [
        "🔍 Mesin Pencari Kamus",
        "🗣️ Modul 1: Kata Ganti & Sapaan",
        "❓ Modul 2: Kata Tanya Utama",
        "🏃 Modul 3: Kata Kerja & Keadaan",
        "🔗 Modul 4: Partikel Kalimat",
        "🌟 Modul 5-14: Budaya & NLP AI"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Dibangun untuk BUDAYA GO! 2026")
st.sidebar.caption("Oleh: Muh. Armil Syam")

# ==========================================
# 4. KONTEN HALAMAN BERDASARKAN NAVIGASI
# ==========================================

# ------------------------------------------
# HALAMAN: MESIN PENCARI (DESAIN ASLI KEMBALI)
# ------------------------------------------
if menu_pilihan == "🔍 Mesin Pencari Kamus":
    st.title("📚 Kamus Besar Digital Mandar")
    st.markdown("---")
    st.write("Jelajahi kekayaan kosakata dan literatur bahasa Mandar. Ketik kata yang ingin Anda cari di bawah ini.")

    search_query = st.text_input("🔍 Cari Kosakata Mandar:", placeholder="Contoh: pamboya, macoa, lita...")

    if search_query:
        if df.empty:
            st.error("Data kamus belum dimuat. Pastikan file CSV tersedia di folder data/processed/")
        else:
            hasil = df[df['Mandar'].str.contains(search_query, case=False, na=False)]
            
            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} hasil untuk '{search_query}'")
                
                # Menampilkan setiap hasil dalam bentuk kontainer asli
                for index, row in hasil.iterrows():
                    with st.container():
                        st.markdown(f"### {row['Mandar']}")
                        st.write(f"**Penjelasan:** {row['Indonesia']}")
                        st.caption(f"Sumber: Lembar PDF ke-{row['Halaman_PDF']}")
                        st.markdown("---")
            else:
                st.warning(f"Kosakata '{search_query}' belum ditemukan dalam kamus.")

# ------------------------------------------
# HALAMAN: MODUL 1
# ------------------------------------------
elif menu_pilihan == "🗣️ Modul 1: Kata Ganti & Sapaan":
    st.title("🗣️ Modul 1: Kata Ganti Orang (Palanreng) & Sapaan Dasar")
    st.info("**Tujuan Pembelajaran:** Mengetahui siapa yang berbicara dan kepada siapa Anda bicara sesuai dengan tingkat kesopanan budaya Mandar.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 Orang Pertama & Kedua")
        st.write("- **Aku / Saya** → *Yau* (biasa) atau *I'da* (halus).")
        st.write("- **Kamu** → *I'o* (akrab/sebaya).")
        st.write("- **Anda** → *I'o-mu / I'o-di'* (sopan, kepada yang lebih tua).")
    with col2:
        st.markdown("### 👥 Orang Ketiga & Jamak")
        st.write("- **Kita** → *I'ta* (sangat halus/sopan).")
        st.write("- **Dia** → *Ia*.")
        st.write("- **Mereka** → *Igae*.")

# ------------------------------------------
# HALAMAN: MODUL 2
# ------------------------------------------
elif menu_pilihan == "❓ Modul 2: Kata Tanya Utama":
    st.title("❓ Modul 2: Kata Tanya Utama (Pau-Pau Massing)")
    st.info("**Tujuan Pembelajaran:** Menguasai kemampuan dasar untuk menanyakan kabar, lokasi, atau keperluan sehari-hari.")
    
    st.markdown("### Kosakata Inti Pertanyaan")
    tanya_df = pd.DataFrame({
        "Bahasa Indonesia": ["Apa", "Siapa", "Di mana", "Kapan", "Mengapa / Kenapa", "Berapa"],
        "Bahasa Mandar": ["Aha?", "Innai?", "Umbatumbae? / Umba?", "Piran?", "Ahang mapia? / Ma'aha?", "Piga?"]
    })
    st.table(tanya_df)

# ------------------------------------------
# HALAMAN: MODUL 3
# ------------------------------------------
elif menu_pilihan == "🏃 Modul 3: Kata Kerja & Keadaan":
    st.title("🏃 Modul 3: Kata Kerja Harian & Keadaan (Pau Repu)")
    st.info("**Tujuan Pembelajaran:** Bisa mengungkapkan aktivitas dasar yang Anda lakukan atau lihat di sekitar Anda.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🍽️ Aktivitas Fisik")
        st.write("- **Makan:** Mangande")
        st.write("- **Minum:** Minung")
        st.write("- **Tidur:** Tindo")
    with c2:
        st.markdown("#### 🚶 Mobilitas")
        st.write("- **Pergi:** Mao")
        st.write("- **Datang/Tiba:** Ratu")
    with c3:
        st.markdown("#### 💭 Keadaan & Emosi")
        st.write("- **Suka:** Maelu")
        st.write("- **Tidak mau:** Tania / Andiang maelu")
        st.write("- **Ada:** Dziang")
        st.write("- **Tidak ada:** Andiang")

# ------------------------------------------
# HALAMAN: MODUL 4
# ------------------------------------------
elif menu_pilihan == "🔗 Modul 4: Partikel Kalimat":
    st.title("🔗 Modul 4: Kalimat Gabungan & Penegas (-mi, -mo, -pa)")
    st.info("**Tujuan Pembelajaran:** Membuat kalimat Anda terdengar alami seperti penutur asli (Native Mandar). Bahasa Mandar sangat sering menempelkan partikel di akhir kata kerja.")
    
    st.markdown("### Aturan Praktis (Rumus Imbuhan)")
    st.success("📝 **Partikel `-mi`** : Ditempelkan untuk menyatakan tindakan yang sudah terjadi atau perintah tegas (sekarang).")
    st.warning("📝 **Partikel `-mo`** : Ditempelkan untuk menyatakan 'saja' atau sebagai pilihan alternatif.")
    
    st.markdown("### 💡 Contoh Penerapan")
    st.write("1. **Mangande + mi** → *Mangandemi* (Sudah makan).")
    st.write("2. **Mao + mi** → *Maomi* (Sudah pergi / Pergilah).")
    st.write("3. **I'o + mo** → *I'omo* (Kamu saja).")

# ------------------------------------------
# HALAMAN: MODUL 5-14
# ------------------------------------------
elif menu_pilihan == "🌟 Modul 5-14: Budaya & NLP AI":
    st.title("🌟 Modul 5-14: Perluasan Kosakata & Struktur Bahasa")
    
    st.markdown("""
    Halaman ini merupakan *roadmap* (peta jalan) pengembangan literasi budaya Mandar tingkat lanjut. Modul ini sedang dalam tahap pengembangan struktur (*Work in Progress*) yang akan mencakup:
    """)
    
    with st.expander("📚 Ekspansi Kosakata (Modul 5 - 9)"):
        st.write("- **Modul 5:** Kata Keterangan Waktu (Piran-piran) & Sistem Bilangan.")
        st.write("- **Modul 6:** Kosakata Geografi & Kemaritiman (Mandar sebagai suku pelaut/Sandeq).")
        st.write("- **Modul 7:** Istilah Kekerabatan (Hubungan keluarga) & Hierarki Sosial.")
        st.write("- **Modul 8:** Penamaan Warna dalam tradisi lokal.")
        st.write("- **Modul 9:** Istilah Kuliner tradisional & bahan pangan lokal.")
        
    with st.expander("🎭 Sastra & Warisan Lisan (Modul 10 - 12)"):
        st.write("- **Modul 10:** Pengenalan *Kalindaqdaq* (Puisi lisan/pantun Mandar).")
        st.write("- **Modul 11:** *Pappasang* (Naskah budaya/Pesan leluhur yang sarat makna).")
        st.write("- **Modul 12:** Kalimat Larangan/Tabu (*Pemali*) dalam kehidupan sehari-hari.")
        
    with st.expander("🤖 Integrasi Kecerdasan Buatan (Modul 13 - 14)"):
        st.write("- **Modul 13:** Ungkapan Emosional tingkat lanjut untuk analisis sentimen (*Sentiment Analysis*).")
        st.write("- **Modul 14: NLP Artificial Intelligence.** Panduan integrasi pemrosesan bahasa alami (Natural Language Processing) untuk melatih model AI memahami sintaksis, partikel, dan morfologi bahasa Mandar agar *platform* edukasi ini dapat merespons secara otomatis layaknya asisten virtual penutur asli.")

# ==========================================
# FOOTER GLOBAL
# ==========================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center><p style='color:#94A3B8; font-size:0.9rem;'><i>© 2026 MUH. ARMIL SYAM - BUDAYA GO! 2026 | PT. Boyang Digital Nusantara</i></p></center>", unsafe_allow_html=True)