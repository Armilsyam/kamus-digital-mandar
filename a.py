import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Kamus & Edukasi Digital Mandar", 
    page_icon="⛵", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS Tambahan untuk Kartu UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #F1F5F9;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-bottom: 5px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    h1, h2, h3 {
        color: #1E3A8A;
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
# 3. NAVIGASI SIDEBAR PROFESIONAL
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3389/3389081.png", width=120)
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>BUDAYA GO! 2026</h2>", unsafe_allow_html=True)
    
    # Menu UI Interaktif yang elegan
    menu_pilihan = option_menu(
        menu_title=None,
        options=["Beranda Utama", "Kamus Digital", "Modul Pembelajaran", "Uji Wawasan"],
        icons=["house-fill", "book-half", "journal-bookmark-fill", "controller"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px 0px", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "white", "font-weight": "bold"},
        }
    )
    
    st.markdown("---")
    st.caption("© 2026 Muh. Armil Syam")
    st.caption("PT. Boyang Digital Nusantara")

# ==========================================
# 4. KONTEN BERDASARKAN MENU
# ==========================================

if menu_pilihan == "Beranda Utama":
    st.title("⛵ Selamat Datang di Portal Mandar")
    st.write("Platform pelestarian bahasa dan literatur Mandar berbasis **Big Data & Artificial Intelligence**.")
    
    st.markdown("### 📊 Statistik Pangkalan Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h2>{len(df)}</h2><p>Total Kosakata</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h2>231</h2><p>Halaman Ekstrak</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h2>14</h2><p>Modul Edukasi</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Kosakata Hari Ini")
    if not df.empty:
        random_word = df.sample(n=1).iloc[0]
        st.info(f"**Mandar:** {random_word['Mandar']}")
        st.success(f"**Arti:** {random_word['Indonesia']}")
    else:
        st.warning("Data kamus belum dimuat.")

elif menu_pilihan == "Kamus Digital":
    st.title("📚 Mesin Pencari Kamus Mandar")
    st.write("Ketik kata yang ingin Anda cari di bawah ini.")
    search_query = st.text_input("🔍 Cari Kosakata Mandar:", placeholder="Contoh: pamboya, macoa, lita...")

    if search_query:
        if not df.empty:
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

elif menu_pilihan == "Modul Pembelajaran":
    st.title("📚 Modul Interaktif Mandar")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sapaan", "Kata Tanya", "Kata Kerja", "Partikel", "Lanjutan"])
    
    with tab1:
        st.subheader("🗣️ Modul 1: Kata Ganti & Sapaan")
        st.write("- **Aku/Saya:** Yau / I'da\n- **Kamu:** I'o / I'o-mu\n- **Kita:** I'ta\n- **Dia:** Ia\n- **Mereka:** Igae")
    with tab2:
        st.subheader("❓ Modul 2: Kata Tanya Utama")
        st.table(pd.DataFrame({"Mandar": ["Aha?", "Innai?", "Umba?", "Piran?", "Ma'aha?", "Piga?"], "Indonesia": ["Apa", "Siapa", "Di mana", "Kapan", "Kenapa", "Berapa"]}))
    with tab3:
        st.subheader("🏃 Modul 3: Kata Kerja")
        st.write("- **Makan:** Mangande\n- **Minum:** Minung\n- **Tidur:** Tindo\n- **Pergi:** Mao")
    with tab4:
        st.subheader("🔗 Modul 4: Partikel (-mi, -mo)")
        st.success("📝 **-mi** : Sudah terjadi/Perintah (Mao+mi = Maomi / Pergilah).")
        st.warning("📝 **-mo** : Pilihan/Saja (I'o+mo = I'omo / Kamu saja).")
    with tab5:
        st.subheader("🌟 Modul 5-14: Roadmap")
        st.write("Segera Hadir: Kosakata Maritim, Kesusastraan Lisan (Kalindaqdaq), dan Integrasi Analisis Sentimen NLP.")

elif menu_pilihan == "Uji Wawasan":
    st.title("🎮 Kuis Kosakata Mandar")
    if not df.empty:
        if 'kuis_kata' not in st.session_state:
            st.session_state.kuis_kata = df.sample(n=1).iloc[0]
        kata_uji = st.session_state.kuis_kata
        
        st.markdown(f"<div class='metric-card'><h1>{kata_uji['Mandar']}</h1></div>", unsafe_allow_html=True)
        
        with st.expander("👀 Tampilkan Jawaban"):
            st.success(f"**Arti:** {kata_uji['Indonesia']}")
            
        if st.button("🔄 Ganti Pertanyaan Baru", use_container_width=True):
            st.session_state.kuis_kata = df.sample(n=1).iloc[0]
            st.rerun()