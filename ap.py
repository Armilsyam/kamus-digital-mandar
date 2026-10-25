import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Kamus & Edukasi Digital Mandar", 
    page_icon="⛵", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS untuk mempercantik UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-bottom: 4px solid #2563EB;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

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
# 3. NAVIGASI SIDEBAR UTAMA
# ==========================================
st.sidebar.title("⛵ BUDAYA GO! 2026")
st.sidebar.markdown("Platform Literasi Mandar Terpadu")

menu_pilihan = st.sidebar.radio(
    "Pilih Fitur:",
    [
        "🏠 Beranda Utama",
        "🔍 Kamus Digital",
        "📚 Modul Pembelajaran",
        "🎮 Uji Wawasan (Kuis)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Muh. Armil Syam")
st.sidebar.caption("PT. Boyang Digital Nusantara")

# ==========================================
# 4. KONTEN BERDASARKAN MENU
# ==========================================

# ------------------------------------------
# HALAMAN 1: BERANDA (DASHBOARD)
# ------------------------------------------
if menu_pilihan == "🏠 Beranda Utama":
    st.title("Selamat Datang di Portal Mandar")
    st.markdown("Platform pelestarian bahasa dan literatur Mandar berbasis **Big Data & Artificial Intelligence**.")
    
    st.markdown("### 📊 Statistik Pangkalan Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>{len(df)}</h3><p>Total Kosakata</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>231</h3><p>Halaman Terekstrak</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>14</h3><p>Modul Edukasi</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Kosakata Hari Ini")
    if not df.empty:
        # Mengambil 1 baris data acak
        random_word = df.sample(n=1).iloc[0]
        st.info(f"**Mandar:** {random_word['Mandar']}")
        st.success(f"**Arti:** {random_word['Indonesia']}")
        st.caption(f"Sumber: Lembar PDF ke-{random_word['Halaman_PDF']}")
    else:
        st.warning("Data kamus belum dimuat.")

# ------------------------------------------
# HALAMAN 2: KAMUS (DESAIN ASLI ANDA)
# ------------------------------------------
elif menu_pilihan == "🔍 Kamus Digital":
    st.title("📚 Mesin Pencari Kamus Mandar")
    st.markdown("---")
    st.write("Jelajahi kekayaan kosakata dan literatur bahasa Mandar. Ketik kata yang ingin Anda cari di bawah ini.")

    search_query = st.text_input("🔍 Cari Kosakata Mandar:", placeholder="Contoh: pamboya, macoa, lita...")

    if search_query:
        if df.empty:
            st.error("Data kamus belum dimuat.")
        else:
            hasil = df[df['Mandar'].str.contains(search_query, case=False, na=False)]
            
            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} hasil untuk '{search_query}'")
                for index, row in hasil.iterrows():
                    with st.container():
                        st.markdown(f"### {row['Mandar']}")
                        st.write(f"**Penjelasan:** {row['Indonesia']}")
                        st.caption(f"Sumber: Lembar PDF ke-{row['Halaman_PDF']}")
                        st.markdown("---")
            else:
                st.warning(f"Kosakata '{search_query}' belum ditemukan dalam kamus.")

# ------------------------------------------
# HALAMAN 3: MODUL EDUKASI (SISTEM TABS)
# ------------------------------------------
elif menu_pilihan == "📚 Modul Pembelajaran":
    st.title("📚 Modul Interaktif Mandar")
    st.write("Silakan pilih tab di bawah ini untuk memulai pelajaran Anda.")
    
    # Menggunakan UI Tabs agar halaman tidak berantakan
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Modul 1: Sapaan", 
        "Modul 2: Kata Tanya", 
        "Modul 3: Kata Kerja", 
        "Modul 4: Partikel", 
        "Modul 5-14: Lanjutan"
    ])
    
    with tab1:
        st.subheader("🗣️ Modul 1: Kata Ganti Orang (Palanreng)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("- **Aku / Saya** → *Yau* (biasa) atau *I'da* (halus).")
            st.write("- **Kamu** → *I'o* (akrab/sebaya).")
            st.write("- **Anda** → *I'o-mu / I'o-di'* (sopan).")
        with col2:
            st.write("- **Kita** → *I'ta* (sangat halus/sopan).")
            st.write("- **Dia** → *Ia*.")
            st.write("- **Mereka** → *Igae*.")

    with tab2:
        st.subheader("❓ Modul 2: Kata Tanya Utama")
        tanya_df = pd.DataFrame({
            "Bahasa Indonesia": ["Apa", "Siapa", "Di mana", "Kapan", "Mengapa / Kenapa", "Berapa"],
            "Bahasa Mandar": ["Aha?", "Innai?", "Umbatumbae? / Umba?", "Piran?", "Ahang mapia? / Ma'aha?", "Piga?"]
        })
        st.table(tanya_df)

    with tab3:
        st.subheader("🏃 Modul 3: Kata Kerja & Keadaan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("- **Makan:** Mangande\n- **Minum:** Minung\n- **Tidur:** Tindo")
        with c2:
            st.write("- **Pergi:** Mao\n- **Tiba:** Ratu")
        with c3:
            st.write("- **Suka:** Maelu\n- **Ada:** Dziang\n- **Tidak ada:** Andiang")

    with tab4:
        st.subheader("🔗 Modul 4: Partikel Kalimat (-mi, -mo, -pa)")
        st.success("📝 **Partikel `-mi`** : Menyatakan tindakan yang sudah terjadi/perintah tegas (Mao + mi = Maomi / Pergilah).")
        st.warning("📝 **Partikel `-mo`** : Menyatakan 'saja' atau pilihan alternatif (I'o + mo = I'omo / Kamu saja).")

    with tab5:
        st.subheader("🌟 Modul 5-14: *Roadmap* NLP AI")
        st.write("Bagian ini memuat struktur kurikulum tingkat lanjut untuk diintegrasikan dengan *Natural Language Processing* (NLP) di masa depan, meliputi:")
        st.write("1. Kosakata Geografi & Maritim (Sandeq).")
        st.write("2. Kesusastraan Lisan (*Kalindaqdaq* & *Pappasang*).")
        st.write("3. Pelatihan Model AI untuk Analisis Sentimen Bahasa Mandar.")

# ------------------------------------------
# HALAMAN 4: KUIS GAMIFIKASI (BARU!)
# ------------------------------------------
elif menu_pilihan == "🎮 Uji Wawasan (Kuis)":
    st.title("🎮 Kuis Kosakata Mandar")
    st.write("Uji kemampuan bahasa Mandar Anda dengan menebak arti dari kosakata acak berikut!")
    
    if not df.empty:
        # Menyimpan kata ke session state agar tidak berubah saat tombol ditekan
        if 'kuis_kata' not in st.session_state:
            st.session_state.kuis_kata = df.sample(n=1).iloc[0]
            
        kata_uji = st.session_state.kuis_kata
        
        st.markdown(f"<h2 style='text-align:center; color:#2563EB;'>{kata_uji['Mandar']}</h2>", unsafe_allow_html=True)
        
        with st.expander("👀 Tampilkan Jawaban"):
            st.success(f"**Arti:** {kata_uji['Indonesia']}")
            
        if st.button("🔄 Ganti Pertanyaan Baru"):
            st.session_state.kuis_kata = df.sample(n=1).iloc[0]
            st.rerun()
    else:
        st.warning("Data kamus belum tersedia.")

# ==========================================
# FOOTER GLOBAL
# ==========================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center><p style='color:#94A3B8; font-size:0.9rem;'><i>© 2026 MUH. ARMIL SYAM - BUDAYA GO! 2026 | PT. Boyang Digital Nusantara</i></p></center>", unsafe_allow_html=True)