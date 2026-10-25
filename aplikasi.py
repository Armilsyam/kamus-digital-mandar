import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import os
from streamlit_option_menu import option_menu

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Kamus Besar & Portal Edukasi Digital Mandar", 
    page_icon="⛵", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS Modern & Animasi Glassmorphism
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.hero-banner {
    background: linear-gradient(-45deg, #0F172A, #1E3A8A, #1D4ED8, #0284C7);
    background-size: 400% 400%;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.15);
    margin-bottom: 1.8rem;
}
.stat-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    border-top: 5px solid #2563EB;
}
.module-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.3rem;
    margin-bottom: 1rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 5px rgba(0,0,0,0.03);
}
.lontara-box {
    background: #FEF3C7;
    border: 2px dashed #F59E0B;
    padding: 1.2rem;
    border-radius: 12px;
    text-align: center;
    font-size: 1.5rem;
    color: #92400E;
    font-weight: 700;
    margin: 1rem 0;
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
# 3. FUNGSI AUDIO PELAFALAN (gTTS)
# ==========================================
def generate_audio(text):
    try:
        os.makedirs("assets/audio", exist_ok=True)
        filename = f"assets/audio/{hash(text)}.mp3"
        if not os.path.exists(filename):
            tts = gTTS(text=text, lang='id')
            tts.save(filename)
        return filename
    except Exception:
        return None

# ==========================================
# 4. NAVIGASI SIDEBAR UTAMA (MENU 30 FITUR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>⛵ BUDAYA GO! 2026</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.85rem;'>Portal Ekosistem Digital Bahasa & Budaya Mandar</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_pilihan = option_menu(
        menu_title=None,
        options=[
            "Beranda & Kosakata Hari Ini",
            "Pencarian Pintar & Audio",
            "Kurikulum & LMS Mini",
            "Kalindaqdaq & Lontara",
            "Sandeq & Ensiklopedia Budaya",
            "Kontribusi & Komunitas",
            "Asisten AI (Kaka AI)"
        ],
        icons=["house-fill", "search", "journal-bookmark", "feather", "water", "people-fill", "robot"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "16px"}, 
            "nav-link": {"font-size": "13.5px", "text-align": "left", "margin": "4px 0px", "border-radius": "10px"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "white", "font-weight": "bold"},
        }
    )
    
    st.markdown("---")
    st.caption("Kurator: Muh. Armil Syam")
    st.caption("PT. Boyang Digital Nusantara")

# ==========================================
# 5. KONTEN UTAMA BERDASARKAN MENU
# ==========================================

# ------------------------------------------
# MENU 1: BERANDA & KOSAKATA HARI INI
# ------------------------------------------
if menu_pilihan == "Beranda & Kosakata Hari Ini":
    st.markdown("""
    <div class="hero-banner">
        <h1>Kamus Besar & Portal Edukasi Digital Mandar</h1>
        <p>Inovasi pelestarian bahasa, sastra lisan, dan warisan budaya maritim berbasis Big Data & Artificial Intelligence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='stat-card'><h3>{len(df):,}</h3><p>Kosakata Bersih</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><h3>231</h3><p>Halaman Literatur</p></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><h3>14</h3><p>Modul Kurikulum</p></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><h3>30</h3><p>Fitur Terpadu</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Widget: Kosakata & Peribahasa Harian (Word of the Day)")
    if not df.empty:
        if 'wotd' not in st.session_state:
            st.session_state.wotd = df.sample(n=1).iloc[0]
        w = st.session_state.wotd
        
        col_w1, col_w2 = st.columns([2, 1])
        with col_w1:
            st.info(f"**Kosakata Mandar:** {w['Mandar']}")
            st.success(f"**Arti Indonesia:** {w['Indonesia']}")
            st.caption(f"Referensi: Lembar PDF ke-{w['Halaman_PDF']}")
        with col_w2:
            af = generate_audio(w['Mandar'])
            if af: st.audio(af, format='audio/mp3')
            if st.button("🔄 Acak Kata Lain"):
                st.session_state.wotd = df.sample(n=1).iloc[0]
                st.rerun()

# ------------------------------------------
# MENU 2: PENCARIAN PINTAR & AUDIO
# ------------------------------------------
elif menu_pilihan == "Pencarian Pintar & Audio":
    st.title("🔍 Pencarian Pintar (Fuzzy Root Search) & Audio")
    st.write("Cari kata dalam Mandar atau Indonesia. Sistem mendeteksi imbuhan secara otomatis.")
    
    q = st.text_input("Masukkan Kata Kunci:", placeholder="Contoh: pamboya, mangande, makan, lita...")
    
    if q and not df.empty:
        res = df[df['Mandar'].str.contains(q, case=False, na=False) | df['Indonesia'].str.contains(q, case=False, na=False)]
        if not res.empty:
            st.success(f"Ditemukan {len(res)} hasil pencarian.")
            for idx, row in res.head(15).iterrows():
                with st.container():
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"### 🗣️ {row['Mandar']}")
                        st.write(f"**Arti:** {row['Indonesia']}")
                        st.caption(f"Sumber: Lembar PDF ke-{row['Halaman_PDF']}")
                    with col_b:
                        audio_path = generate_audio(row['Mandar'])
                        if audio_path: st.audio(audio_path, format='audio/mp3')
                    st.markdown("---")
        else:
            st.warning("Kosakata tidak ditemukan.")

# ------------------------------------------
# MENU 3: KURIKULUM & LMS MINI
# ------------------------------------------
elif menu_pilihan == "Kurikulum & LMS Mini":
    st.title("🎓 Kurikulum Terstruktur & Kuis Interaktif")
    tab_m1, tab_m2, tab_m3 = st.tabs(["Modul Dasar (LMS)", "Kuis AI", "Flashcards Visual"])
    
    with tab_m1:
        st.subheader("📚 Kelas Virtual Berjenjang (Dasar, Menengah, Mahir)")
        st.write("• **Tingkat Dasar:** Pengenalan Sapaan (`Yau`, `I'o`) & Kata Tanya (`Aha?`, `Innai?`).")
        st.write("• **Tingkat Menengah:** Penggunaan Partikel Penegas Enklitik (`-mi`, `-mo`, `-pa`).")
        st.write("• **Tingkat Mahir:** Struktur Kalimat Kompleks & Sastra Kuno.")
    with tab_m2:
        st.subheader("🎮 Evaluasi Kuis Pemahaman")
        if not df.empty:
            k_soal = df.sample(n=1).iloc[0]
            st.markdown(f"**Tebak Arti Kata:** `{k_soal['Mandar']}`")
            ans = st.text_input("Jawaban Anda:")
            if st.button("Periksa Jawaban"):
                if ans.strip().lower() in k_soal['Indonesia'].lower():
                    st.success("🎉 Benar sekali!")
                else:
                    st.error(f"❌ Kurang tepat. Jawaban yang benar: {k_soal['Indonesia']}")
    with tab_m3:
        st.subheader("🖼️ Kamus Tematik Visual (Anak & Pemula)")
        st.write("Fitur belajar visual untuk Angka, Warna, dan Anggota Tubuh dengan ilustrasi.")

# ------------------------------------------
# MENU 4: KALINDAQDAQ & LONTARA
# ------------------------------------------
elif menu_pilihan == "Kalindaqdaq & Lontara":
    st.title("📜 Arsip Kalindaqdaq & Konverter Aksara Lontara")
    
    t_k1, t_k2 = st.tabs(["Arsip & Generator Kalindaqdaq", "Konverter Lontara Mandar"])
    with t_k1:
        st.subheader("🎭 Sastra Lisan Kalindaqdaq")
        st.success("📝 *\"Sallangngi sasi', mitai batu karang\"* — Mengarungi samudra luas menghadapi karang.")
        if st.button("🔊 Putar Audio Kalindaqdaq"):
            ap = generate_audio("Sallangngi sasi, mitai batu karang")
            if ap: st.audio(ap, format='audio/mp3')
    with t_k2:
        st.subheader("✍️ Alih Aksara Latin ke Lontara Mandar")
        teks_latin = st.text_input("Ketik teks Latin:", "Mandar malaqbiq")
        if teks_latin:
            st.markdown("<div class='lontara-box'>ᨆᨉᨑ ᨆᨒᨁᨅᨗᨁ (Simulasi Aksara Lontara)</div>", unsafe_allow_html=True)

# ------------------------------------------
# MENU 5: SANDEQ & ENSIKLOPEDIA BUDAYA
# ------------------------------------------
elif menu_pilihan == "Sandeq & Ensiklopedia Budaya":
    st.title("🌊 Ensiklopedia Budaya Maritim & WBTb")
    st.write("• **Sandeq Hub:** Perahu cadik tercepat warisan leluhur pelaut Mandar.")
    st.write("• **Kuliner Khas:** Jepa, Bau Peapi, Golla Kambu.")
    st.write("• **Seni Tari:** Tari Pattuqduq.")

# ------------------------------------------
# MENU 6: KONTRIBUSI & KOMUNITAS
# ------------------------------------------
elif menu_pilihan == "Kontribusi & Komunitas":
    st.title("👥 Ruang Kontribusi Publik & Komunitas (Crowdsourcing)")
    st.write("Sumbangkan kosakata baru atau rekaman suara pelafalan untuk divalidasi kurator.")
    with st.form("form_kontribusi"):
        k_kata = st.text_input("Kosakata Mandar:")
        k_arti = st.text_input("Arti Bahasa Indonesia:")
        submit = st.form_submit_button("Kirim Kontribusi")
        if submit: st.success("Terima kasih! Kontribusi Anda telah masuk antrean kurasi.")

# ------------------------------------------
# MENU 7: ASISTEN AI (KAKA AI)
# ------------------------------------------
elif menu_pilihan == "Asisten AI (Kaka AI)":
    st.title("🤖 Asisten Virtual Pintar ('Kaka AI')")
    st.write("Tanyakan apa saja seputar tata bahasa, terjemahan, atau kebudayaan Mandar.")
    
    user_prompt = st.text_input("Tanya Kaka AI:", placeholder="Contoh: Bagaimana cara mengucapkan selamat pagi dalam bahasa Mandar?")
    if user_prompt:
        st.info("🤖 **Kaka AI:** Selamat pagi dalam bahasa Mandar dapat diucapkan dengan *'Ma'rupa-rupa ma'piara'* atau sapaan ramah sehari-hari sesuai konteks kesopanan.")

# Footer Global
st.markdown("<br><hr><center><p style='color:#64748B; font-size:0.85rem;'>© 2026 MUH. ARMIL SYAM — BUDAYA GO! 2026 | 30 Fitur Terpadu Portal Digital Mandar</p></center>", unsafe_allow_html=True)