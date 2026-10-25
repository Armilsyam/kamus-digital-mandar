import streamlit as st
import pandas as pd
import random
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

# ==========================================
# 2. INJEKSI CSS TINGKAT LANJUT & ANIMASI
# ==========================================
st.markdown("""
<style>
/* Import Google Fonts Modern */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Keyframes untuk Animasi Muncul Halus (Fade In Up) */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Keyframes untuk Gradasi Bergerak */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Keyframes untuk Efek Mengambang (Floating) */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}

/* Hero Banner Utama dengan Animasi Gradasi Maritim */
.hero-banner {
    background: linear-gradient(-45deg, #0F172A, #1E3A8A, #1D4ED8, #0284C7);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite, fadeInUp 0.7s ease-out;
    padding: 2.8rem 2rem;
    border-radius: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.15);
    position: relative;
    overflow: hidden;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    color: #FFFFFF !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.hero-subtitle {
    font-size: 1.1rem;
    font-weight: 400;
    color: #E2E8F0 !important;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

.hero-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid #F59E0B;
    color: #FCD34D;
    padding: 5px 16px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Kartu Statistik Modern (Glassmorphism + Hover Lift) */
.stat-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.6rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.8s ease-out;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #2563EB, #F59E0B);
}

.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.12), 0 8px 10px -6px rgba(37, 99, 235, 0.08);
    border-color: #93C5FD;
}

.stat-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: inline-block;
    animation: float 3.5s ease-in-out infinite;
}

.stat-value {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.2rem 0;
}

.stat-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Kartu Hasil Pencarian Kosakata */
.dict-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid #E2E8F0;
    border-left: 6px solid #2563EB;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease-out;
}

.dict-card:hover {
    transform: translateX(6px);
    border-left-color: #F59E0B;
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.08);
}

.dict-word {
    font-size: 1.45rem;
    font-weight: 800;
    color: #1E3A8A;
    margin: 0 0 0.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.dict-meaning {
    font-size: 1.05rem;
    color: #334155;
    line-height: 1.65;
    margin-bottom: 0.9rem;
}

.dict-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid #BFDBFE;
}

/* Kartu Modul Pembelajaran */
.module-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out;
    height: 100%;
}

.module-card:hover {
    border-color: #3B82F6;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1);
    transform: translateY(-4px);
}

.module-tag {
    display: inline-block;
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
    color: #1E40AF;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 6px;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}

/* Kotak Rumus / Formula Bahasa */
.formula-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-left: 5px solid #1D4ED8;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    color: #1E3A8A;
    font-weight: 500;
}

/* Flashcard 3D Flip Interaktif untuk Kuis & Kosakata Hari Ini */
.flip-card {
    background-color: transparent;
    width: 100%;
    height: 230px;
    perspective: 1000px;
    margin: 1.2rem 0;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.7s cubic-bezier(0.4, 0.2, 0.2, 1);
    transform-style: preserve-3d;
    border-radius: 20px;
    box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.1);
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}

.flip-card-front {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    color: white;
    border: 2px solid #60A5FA;
}

.flip-card-back {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: #F8FAFC;
    transform: rotateY(180deg);
    border: 2px solid #F59E0B;
}

/* Kustomisasi Input Pencarian Streamlit */
div[data-baseweb="input"] > div {
    border-radius: 14px !important;
    border: 2px solid #CBD5E1 !important;
    padding: 4px 10px !important;
    transition: all 0.3s ease !important;
}

div[data-baseweb="input"] > div:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SISTEM CACHING & LOAD DATA
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
# 4. NAVIGASI SIDEBAR MODERN
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 3.5rem; animation: float 3s ease-in-out infinite;'>⛵</div>
        <h2 style='color: #1E3A8A; font-weight: 800; margin-bottom: 0; font-size: 1.4rem;'>MANDAR DIGITAL</h2>
        <p style='color: #64748B; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.08em;'>BUDAYA GO! 2026 EDITION</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu_pilihan = option_menu(
        menu_title=None,
        options=[
            "Beranda Utama", 
            "Kamus Digital", 
            "Kurikulum 14 Modul", 
            "Arena Kuis & Flashcard",
            "Arsitektur NLP & AI"
        ],
        icons=["grid-1x2-fill", "search", "journal-richtext", "trophy-fill", "cpu-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "14.5px", 
                "font-weight": "600",
                "text-align": "left", 
                "margin": "6px 0px", 
                "border-radius": "12px",
                "padding": "10px 15px",
                "transition": "all 0.25s ease"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #1E3A8A, #2563EB)", 
                "color": "white", 
                "font-weight": "700",
                "box-shadow": "0 4px 12px rgba(37, 99, 235, 0.3)"
            },
        }
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='background: #F1F5F9; padding: 12px; border-radius: 12px; font-size: 0.8rem; color: #475569; text-align: center;'>
        <b>Pengembang & Kurator:</b><br>
        <span style='color: #1E3A8A; font-weight: 700;'>MUH. ARMIL SYAM</span><br>
        PT. Boyang Digital Nusantara
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. HALAMAN 1: BERANDA UTAMA (DASHBOARD)
# ==========================================
if menu_pilihan == "Beranda Utama":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">✨ Inovasi Pelestarian Bahasa Daerah Berbasis AI</div>
        <div class="hero-title">Kamus Besar & Portal Edukasi Digital Mandar</div>
        <div class="hero-subtitle">
            Mengawinkan warisan maritim dan kesusastraan Tanah Mandar dengan teknologi 
            <b>Big Data Extraction</b> & <b>Natural Language Processing (NLP)</b> untuk generasi masa depan.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Baris Statistik dengan Animasi Hover
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📚</div>
            <div class="stat-value">{len(df):,}</div>
            <div class="stat-label">Entri Terekstrak</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-value">231</div>
            <div class="stat-label">Halaman Literatur</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🎓</div>
            <div class="stat-value">14</div>
            <div class="stat-label">Modul Kurikulum</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-value">NLP</div>
            <div class="stat-label">Siap Integrasi AI</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("### 💫 Kosakata Hari Ini (*Hover Kartu untuk Melihat Arti*)")
        if not df.empty:
            if "daily_word" not in st.session_state:
                st.session_state.daily_word = df.sample(n=1).iloc[0]
            dw = st.session_state.daily_word
            
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <span style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: #93C5FD;">Kosakata Mandar (Arahkan Kursor)</span>
                        <h2 style="color: white; font-size: 2.2rem; margin: 10px 0;">{dw['Mandar']}</h2>
                        <span style="font-size: 0.85rem; color: #E2E8F0;">🔄 Sentuh / Hover untuk membalik kartu</span>
                    </div>
                    <div class="flip-card-back">
                        <span style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: #FCD34D;">Arti & Penjelasan Bahasa Indonesia</span>
                        <p style="font-size: 1.15rem; font-weight: 600; margin: 12px 0; color: white;">{dw['Indonesia']}</p>
                        <span style="font-size: 0.75rem; color: #94A3B8;">Sumber: Lembar PDF ke-{dw['Halaman_PDF']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎲 Acak Kosakata Lainnya", use_container_width=True):
                st.session_state.daily_word = df.sample(n=1).iloc[0]
                st.rerun()
        else:
            st.warning("Data kamus belum dimuat.")

    with col_right:
        st.markdown("### 🧭 Mengapa Platform Ini Dibangun?")
        st.markdown("""
        <div class="module-card">
            <span class="module-tag">Visi BUDAYA GO! 2026</span>
            <h4 style="color: #1E3A8A; margin-top: 5px;">Digitalisasi Warisan Leluhur</h4>
            <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
                Bahasa Mandar memiliki struktur morfologi, partikel penegas, dan sastra lisan (<i>Kalindaqdaq</i> & <i>Pappasang</i>) yang sangat kaya. Platform ini hadir untuk:
            </p>
            <ul style="color: #475569; font-size: 0.92rem; line-height: 1.7;">
                <li><b>Aksesibilitas Instan:</b> Mengubah ratusan halaman PDF statis menjadi mesin pencari berkecepatan milidetik.</li>
                <li><b>Pembelajaran Terstruktur:</b> Menyediakan 14 modul bertahap dari sapaan dasar hingga sastra kuno.</li>
                <li><b>Fondasi AI Lokal:</b> Menyiapkan korpus bersih untuk pelatihan model bahasa (LLM/NLP) bahasa daerah.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. HALAMAN 2: MESIN PENCARI KAMUS DIGITAL
# ==========================================
elif menu_pilihan == "Kamus Digital":
    st.markdown("""
    <div class="hero-banner" style="padding: 2rem;">
        <div class="hero-title" style="font-size: 2.2rem;">📚 Mesin Pencari Kamus Besar Mandar</div>
        <div class="hero-subtitle">
            Pencarian pintar dua arah (Mandar ↔ Indonesia) dilengkapi filter halaman dan unduhan data.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Panel Kontrol Pencarian
    col_search, col_mode, col_limit = st.columns([2.5, 1.2, 1])
    with col_search:
        search_query = st.text_input("🔍 Masukkan Kata Kunci Pencarian:", placeholder="Ketik kata Mandar atau Indonesia (contoh: pamboya, laut, makan, macoa)...")
    with col_mode:
        mode_cari = st.selectbox("🎯 Mode Pencarian:", ["Semua Kolom (Mandar & Indo)", "Hanya Kosakata Mandar", "Hanya Terjemahan Indonesia"])
    with col_limit:
        batas_tampil = st.selectbox("📄 Tampilkan Hasil:", [10, 25, 50, 100, "Semua Hasil"], index=1)

    # Filter Abjad Cepat
    st.write("**⚡ Telusuri Cepat Berdasarkan Abjad Awal:**")
    abjad_list = ["Semua"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pilihan_abjad = st.pills("Filter Abjad", abjad_list, default="Semua", label_visibility="collapsed")

    if df.empty:
        st.error("Data kamus belum ditemukan di `data/processed/kamus_mandar_bersih.csv`.")
    else:
        hasil = df.copy()
        
        # Filter berdasarkan abjad jika dipilih
        if pilihan_abjad and pilihan_abjad != "Semua":
            hasil = hasil[hasil['Mandar'].astype(str).str.upper().str.startswith(pilihan_abjad)]
            
        # Filter berdasarkan kata kunci pencarian
        if search_query:
            if mode_cari == "Hanya Kosakata Mandar":
                hasil = hasil[hasil['Mandar'].str.contains(search_query, case=False, na=False)]
            elif mode_cari == "Hanya Terjemahan Indonesia":
                hasil = hasil[hasil['Indonesia'].str.contains(search_query, case=False, na=False)]
            else:
                mask_mandar = hasil['Mandar'].str.contains(search_query, case=False, na=False)
                mask_indo = hasil['Indonesia'].str.contains(search_query, case=False, na=False)
                hasil = hasil[mask_mandar | mask_indo]

        # Informasi jumlah hasil
        st.markdown(f"**Menampilkan `{len(hasil)}` entri yang cocok dengan kriteria Anda.**")
        st.markdown("---")
        
        if not hasil.empty:
            if batas_tampil != "Semua Hasil":
                hasil_tampil = hasil.head(int(batas_tampil))
            else:
                hasil_tampil = hasil
                
            for index, row in hasil_tampil.iterrows():
                st.markdown(f"""
                <div class="dict-card">
                    <div class="dict-word">
                        <span>🗣️ {row['Mandar']}</span>
                        <span class="dict-badge">📄 Lembar PDF ke-{row['Halaman_PDF']}</span>
                    </div>
                    <div class="dict-meaning">
                        <b>Arti / Penjelasan:</b><br>{row['Indonesia']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"Tidak ditemukan kosakata untuk pencarian `{search_query}` pada filter abjad `{pilihan_abjad}`.")

# ==========================================
# 7. HALAMAN 3: KURIKULUM LENGKAP 14 MODUL
# ==========================================
elif menu_pilihan == "Kurikulum 14 Modul":
    st.markdown("""
    <div class="hero-banner" style="padding: 2rem;">
        <div class="hero-title" style="font-size: 2.2rem;">🎓 Kurikulum Terpadu Bahasa & Budaya Mandar (Halaman 1 - 14)</div>
        <div class="hero-subtitle">
            Panduan sistematis dari tata bahasa dasar, partikel penutur asli, kemaritiman, hingga sastra klasik.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_dasar, tab_partikel, tab_ekspansi, tab_sastra = st.tabs([
        "📘 Halaman 1-3: Pondasi Bahasa",
        "🔗 Halaman 4: Rumus Partikel Native",
        "🌊 Halaman 5-9: Alam, Waktu & Kuliner",
        "🎭 Halaman 10-13: Sastra, Pappasang & Emosi"
    ])

    # --- TAB 1: HALAMAN 1 - 3 ---
    with tab_dasar:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 1 • Palanreng</span>
                <h3 style="color:#1E3A8A; margin-top:0;">🗣️ Kata Ganti Orang & Sapaan Dasar</h3>
                <p style="font-size:0.9rem; color:#64748B;"><b>Tujuan:</b> Mengetahui siapa yang berbicara dan kepada siapa Anda bicara sesuai etika Mandar.</p>
                <hr>
                <ul style="line-height:1.9; color:#334155;">
                    <li><b>Aku / Saya</b> → <code>Yau</code> (biasa) atau <code>I'da</code> (halus).</li>
                    <li><b>Kamu</b> → <code>I'o</code> (akrab/sebaya).</li>
                    <li><b>Anda (Sopan)</b> → <code>I'o-mu</code> / <code>I'o-di'</code> (kepada yang lebih tua).</li>
                    <li><b>Kita</b> → <code>I'ta</code> (sangat halus/sopan).</li>
                    <li><b>Dia</b> → <code>Ia</code>.</li>
                    <li><b>Mereka</b> → <code>Igae</code>.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 2 • Pau-Pau Massing</span>
                <h3 style="color:#1E3A8A; margin-top:0;">❓ Kata Tanya Utama Harian</h3>
                <p style="font-size:0.9rem; color:#64748B;"><b>Tujuan:</b> Menanyakan kabar, lokasi, atau keperluan sehari-hari dengan tepat.</p>
                <hr>
                <ul style="line-height:1.9; color:#334155;">
                    <li><b>Apa</b> → <code>Aha?</code></li>
                    <li><b>Siapa</b> → <code>Innai?</code></li>
                    <li><b>Di mana</b> → <code>Umbatumbae?</code> / <code>Umba?</code></li>
                    <li><b>Kapan</b> → <code>Piran?</code></li>
                    <li><b>Mengapa / Kenapa</b> → <code>Ahang mapia?</code> / <code>Ma'aha?</code></li>
                    <li><b>Berapa</b> → <code>Piga?</code></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 3 • Pau Repu</span>
                <h3 style="color:#1E3A8A; margin-top:0;">🏃 Kata Kerja Harian & Keadaan</h3>
                <p style="font-size:0.9rem; color:#64748B;"><b>Tujuan:</b> Mengungkapkan aktivitas dasar yang sedang dilakukan atau dilihat.</p>
                <hr>
                <ul style="line-height:1.8; color:#334155;">
                    <li><b>Makan / Minum</b> → <code>Mangande</code> / <code>Minung</code></li>
                    <li><b>Tidur</b> → <code>Tindo</code></li>
                    <li><b>Pergi / Tiba</b> → <code>Mao</code> / <code>Ratu</code></li>
                    <li><b>Suka</b> → <code>Maelu</code></li>
                    <li><b>Tidak mau</b> → <code>Tania</code> / <code>Andiang maelu</code></li>
                    <li><b>Ada / Tidak ada</b> → <code>Dziang</code> / <code>Andiang</code></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 2: HALAMAN 4 (RUMUS PARTIKEL & SIMULATOR) ---
    with tab_partikel:
        st.markdown("""
        <div class="module-card">
            <span class="module-tag">Halaman 4 • Morfologi & Enklitik</span>
            <h3 style="color:#1E3A8A; margin-top:0;">🔗 Kalimat Gabungan & Partikel Penegas (-mi, -mo, -pa)</h3>
            <p style="color:#475569;">
                <b>Tujuan:</b> Membuat kalimat Anda terdengar alami seperti penutur asli (<i>Native Mandar</i>). Bahasa Mandar sangat sering menempelkan partikel di akhir kata kerja atau kata ganti.
            </p>
            <div class="formula-box">
                📐 <b>RUMUS INTI:</b> &nbsp; <code>[Kata Kerja / Kata Ganti]</code> + <code>[-mi / -mo / -pa]</code> = <b>Makna Kontekstual Baru</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            st.info("**1. Partikel `-mi`**\n\nMenyatakan tindakan yang **sudah terjadi** atau **perintah sekarang**.\n- *Mangande* + *-mi* → **Mangandemi** (Sudah makan)\n- *Mao* + *-mi* → **Maomi** (Sudah pergi / Pergilah)")
        with c_p2:
            st.warning("**2. Partikel `-mo`**\n\nMenyatakan **'saja'** atau **pilihan alternatif / penegasan**.\n- *I'o* + *-mo* → **I'omo** (Kamu saja)\n- *Ia* + *-mo* → **Iamo** (Dia saja / Itu saja)")
        with c_p3:
            st.success("**3. Partikel `-pa`**\n\nMenyatakan **'nanti dulu' / 'masih akan'** (tindakan belum selesai).\n- *Mangande* + *-pa* → **Mangandepa** (Nanti setelah makan / Makan dulu)")

        st.markdown("#### 🧪 Simulator Pembentuk Kata *Native Mandar*")
        col_sim1, col_sim2, col_sim3 = st.columns([1.5, 1.5, 2])
        with col_sim1:
            kata_pilih = st.selectbox("Pilih Kata Dasar:", ["Mangande (Makan)", "Mao (Pergi)", "Tindo (Tidur)", "Ratu (Datang)", "I'o (Kamu)", "Yau (Saya)"])
        with col_sim2:
            partikel_pilih = st.selectbox("Pilih Partikel Akhir:", ["-mi (Sudah / Perintah)", "-mo (Saja / Pilihan)", "-pa (Nanti / Dulu)"])
        with col_sim3:
            kata_bersih = kata_pilih.split(" ")[0]
            part_bersih = partikel_pilih.split(" ")[0].replace("-", "")
            hasil_gabung = f"{kata_bersih}{part_bersih}"
            st.markdown(f"""
            <div class="formula-box" style="margin-top:0; text-align:center;">
                <span style="font-size:0.8rem; text-transform:uppercase;">Hasil Penggabungan Morfologi:</span><br>
                <b style="font-size:1.6rem; color:#1E3A8A;">{hasil_gabung}!</b>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 3: HALAMAN 5 - 9 ---
    with tab_ekspansi:
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 5 • Waktu & Bilangan</span>
                <h4 style="color:#1E3A8A; margin-top:0;">⏳ Keterangan Waktu & Sistem Bilangan</h4>
                <p style="font-size:0.9rem; color:#475569;"><b>Keterangan Waktu:</b> <code>Dini</code> (Hari ini), <code>Ammaranna</code> (Kemarin), <code>Mababa</code> (Besok), <code>Masigi</code> (Pagi), <code>Bongi</code> (Malam).</p>
                <p style="font-size:0.9rem; color:#475569;"><b>Bilangan Pokok (1-10):</b> <code>Mesa</code> (1), <code>Da'dua</code> (2), <code>Tallu</code> (3), <code>Appe'</code> (4), <code>Lima</code> (5), <code>Annang</code> (6), <code>Pitu</code> (7), <code>Aruwa</code> (8), <code>Aséra</code> (9), <code>Sapulo</code> (10).</p>
            </div>
            """, unsafe_allow_html=True)
        with r1_c2:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 6 • Maritim & Geografi</span>
                <h4 style="color:#1E3A8A; margin-top:0;">⛵ Kosakata Geografi & Kemaritiman</h4>
                <p style="font-size:0.9rem; color:#475569;">Sebagai bangsa pelaut ulung, Mandar kaya akan istilah bahari:</p>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.7;">
                    <li><code>Sasi'</code> (Laut), <code>Biring Bonde'</code> (Pantai), <code>Buttu</code> (Gunung/Bukit).</li>
                    <li><code>Sandeq</code> (Perahu bercadik tercepat warisan Mandar).</li>
                    <li><code>Pa'issangang</code> (Ilmu navigasi bintang & arus laut), <code>Somba</code> (Layar).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        r2_c1, r2_c2, r2_c3 = st.columns(3)
        with r2_c1:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 7 • Kekerabatan</span>
                <h4 style="color:#1E3A8A; margin-top:0;">👨‍👩‍👧‍👦 Istilah Keluarga</h4>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.7;">
                    <li><b>Ayah:</b> <code>A'ba</code> / <code>Kama'</code></li>
                    <li><b>Ibu:</b> <code>Amma</code> / <code>Kindo'</code></li>
                    <li><b>Kakek/Nenek:</b> <code>Kanne'</code></li>
                    <li><b>Kakak:</b> <code>Kaka'</code> / <code>Daeng</code></li>
                    <li><b>Adik:</b> <code>Andi'</code></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with r2_c2:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 8 • Spektrum Warna</span>
                <h4 style="color:#1E3A8A; margin-top:0;">🎨 Warna Tradisional</h4>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.7;">
                    <li><b>Putih:</b> <code>Mapute</code></li>
                    <li><b>Hitam:</b> <code>Malotong</code></li>
                    <li><b>Merah:</b> <code>Mamea</code></li>
                    <li><b>Kuning:</b> <code>Mariri</code></li>
                    <li><b>Hijau / Biru:</b> <code>Makudara</code> / <code>Mabiru</code></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with r2_c3:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 9 • Gastronomi</span>
                <h4 style="color:#1E3A8A; margin-top:0;">🍲 Istilah Kuliner Khas</h4>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.7;">
                    <li><b>Jepa:</b> Pangan bundar berbahan singkong parut.</li>
                    <li><b>Bau Peapi:</b> Ikan masak kuah asam kunyit & minyak kelapa Mandar.</li>
                    <li><b>Golla Kambu:</b> Olahan manis kelapa & gula aren.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 4: HALAMAN 10 - 13 ---
    with tab_sastra:
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 10 • Sastra Lisan</span>
                <h4 style="color:#1E3A8A; margin-top:0;">📜 Pengenalan Kalindaqdaq (Puisi Tradisional)</h4>
                <p style="font-size:0.9rem; color:#475569;"><i>Kalindaqdaq</i> adalah puisi lisan Mandar bersajak 4 baris dengan pola suku kata <b>8 - 7 - 5 - 7</b>.</p>
                <div class="formula-box" style="font-size:0.9rem;">
                    <i>"Mua' melo'o mita'u,<br>
                    Tondonganna pa'mai'u,<br>
                    Sallangngi sasi',<br>
                    Mitai batu karang."</i>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 12 • Etika & Tabu</span>
                <h4 style="color:#1E3A8A; margin-top:0;">🚫 Kalimat Larangan (Da') & Pemali</h4>
                <p style="font-size:0.9rem; color:#475569;">Gunakan kata <code>Da'</code> di awal kalimat untuk menyatakan larangan ("Jangan"):</p>
                <ul style="font-size:0.9rem; color:#334155;">
                    <li><code>Da' mupogau'!</code> → Jangan kau lakukan!</li>
                    <li><code>Da' мао!</code> → Jangan pergi!</li>
                    <li><b>Pemali:</b> Pantangan adat demi menjaga keharmonisan sosial dan alam.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 11 • Naskah Budaya</span>
                <h4 style="color:#1E3A8A; margin-top:0;">🏛️ Pappasang (Wasiat Leluhur Mandar)</h4>
                <p style="font-size:0.9rem; color:#475569;">Prinsip falsafah hidup <i>Malaqbiq</i> (bermartabat dalam tutur dan laku):</p>
                <div class="formula-box" style="font-size:0.9rem;">
                    <b>"Da' muala tania anunna"</b><br>
                    (Jangan pernah mengambil sesuatu yang bukan hakmu — Prinsip kejujuran mutlak).
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="module-card">
                <span class="module-tag">Halaman 13 • Ekspresi & Afeksi</span>
                <h4 style="color:#1E3A8A; margin-top:0;">❤️ Ungkapan Emosional & Perasaan</h4>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.8;">
                    <li><b>Bahagia / Senang:</b> <code>Masannang pa'mai'</code></li>
                    <li><b>Rindu Mendalam:</b> <code>Masse' pa'mai'</code> / <code>Маddani</code></li>
                    <li><b>Sedih / Pilu:</b> <code>Masara</code></li>
                    <li><b>Cinta / Kasih:</b> <code>Sayang</code> / <code>Asi</code></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 8. HALAMAN 4: ARENA KUIS & FLASHCARD
# ==========================================
elif menu_pilihan == "Arena Kuis & Flashcard":
    st.markdown("""
    <div class="hero-banner" style="padding: 2rem;">
        <div class="hero-title" style="font-size: 2.2rem;">🎮 Arena Uji Wawasan Bahasa Mandar</div>
        <div class="hero-subtitle">
            Uji ingatan kosakata Anda melalui kuis pilihan ganda otomatis berbasis pangkalan data kamus.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty or len(df) < 4:
        st.warning("Data kamus belum mencukupi untuk membuat kuis interaktif.")
    else:
        if "skor_benar" not in st.session_state:
            st.session_state.skor_benar = 0
        if "skor_total" not in st.session_state:
            st.session_state.skor_total = 0
        if "soal_kuis" not in st.session_state:
            sampel = df.sample(n=4).to_dict(orient="records")
            st.session_state.soal_kuis = {
                "target": sampel[0],
                "opsi": random.sample(sampel, len(sampel)),
                "sudah_jawab": False
            }

        # Statistik Skor Kuis
        ks1, ks2, ks3 = st.columns(3)
        with ks1:
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{st.session_state.skor_benar}</div><div class='stat-label'>Jawaban Benar</div></div>", unsafe_allow_html=True)
        with ks2:
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{st.session_state.skor_total}</div><div class='stat-label'>Total Soal Dijawab</div></div>", unsafe_allow_html=True)
        with ks3:
            akurasi = int((st.session_state.skor_benar / st.session_state.skor_total) * 100) if st.session_state.skor_total > 0 else 0
            st.markdown(f"<div class='stat-card'><div class='stat-value'>{akurasi}%</div><div class='stat-label'>Tingkat Akurasi</div></div>", unsafe_allow_html=True)

        soal = st.session_state.soal_kuis
        st.markdown(f"""
        <div class="dict-card" style="text-align:center; border-left:none; border-top: 6px solid #2563EB;">
            <span class="module-tag">Tebak Makna Kosakata Berikut</span>
            <h2 style="color:#1E3A8A; font-size:2.2rem; margin: 10px 0;">"{soal['target']['Mandar']}"</h2>
            <p style="color:#64748B; font-size:0.9rem;">Manakah arti atau penjelasan yang tepat untuk entri di atas?</p>
        </div>
        """, unsafe_allow_html=True)

        pilihan_teks = [o["Indonesia"][:140] + ("..." if len(o["Indonesia"]) > 140 else "") for o in soal["opsi"]]
        jawaban_user = st.radio("Pilih salah satu jawaban:", pilihan_teks, index=None)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Kunci Jawaban", use_container_width=True, disabled=soal["sudah_jawab"]):
                if jawaban_user is None:
                    st.warning("Silakan pilih salah satu opsi terlebih dahulu!")
                else:
                    st.session_state.skor_total += 1
                    st.session_state.soal_kuis["sudah_jawab"] = True
                    target_teks = soal["target"]["Indonesia"][:140] + ("..." if len(soal["target"]["Indonesia"]) > 140 else "")
                    if jawaban_user == target_teks:
                        st.session_state.skor_benar += 1
                        st.balloons()
                        st.success("🎉 Luar biasa! Jawaban Anda tepat sekali.")
                    else:
                        st.error(f"❌ Kurang tepat. Arti sebenarnya: **{soal['target']['Indonesia']}**")
        with col_btn2:
            if st.button("⏭️ Soal Berikutnya", use_container_width=True):
                sampel = df.sample(n=4).to_dict(orient="records")
                st.session_state.soal_kuis = {
                    "target": sampel[0],
                    "opsi": random.sample(sampel, len(sampel)),
                    "sudah_jawab": False
                }
                st.rerun()

# ==========================================
# 9. HALAMAN 5: MODUL 14 - ARSITEKTUR NLP & AI
# ==========================================
elif menu_pilihan == "Arsitektur NLP & AI":
    st.markdown("""
    <div class="hero-banner" style="padding: 2rem;">
        <div class="hero-badge">Halaman 14 • Blueprint Teknologi Masa Depan</div>
        <div class="hero-title" style="font-size: 2.2rem;">🤖 Integrasi Kecerdasan Buatan (NLP) Bahasa Mandar</div>
        <div class="hero-subtitle">
            Peta jalan arsitektur komputasi untuk melatih model AI memahami struktur bahasa Mandar.
        </div>
    </div>
    """, unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="module-card">
            <span class="module-tag">Tahap 1 • Data Engineering</span>
            <h4 style="color:#1E3A8A;">1. Korpus & Tokenisasi Morfologi</h4>
            <p style="font-size:0.9rem; color:#475569;">
                Mengolah 851+ entri bersih hasil ekstraksi PDF menjadi pasangan token. Memisahkan kata dasar (<i>Root Word</i>) dari partikel enklitik seperti <code>-mi</code>, <code>-mo</code>, dan <code>-pa</code> agar mesin memahami perubahan arti.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class="module-card">
            <span class="module-tag">Tahap 2 • Vector Embedding</span>
            <h4 style="color:#1E3A8A;">2. Semantic Search & RAG</h4>
            <p style="font-size:0.9rem; color:#475569;">
                Mengubah kosakata dan sastra <i>Kalindaqdaq</i> menjadi vektor multidimensi. Memungkinkan pencarian berbasis konteks makna (<i>Retrieval-Augmented Generation</i>), bukan sekadar kecocokan huruf.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div class="module-card">
            <span class="module-tag">Tahap 3 • Generative AI</span>
            <h4 style="color:#1E3A8A;">3. Asisten Tutur Virtual Mandar</h4>
            <p style="font-size:0.9rem; color:#475569;">
                Fine-tuning model bahasa untuk menerjemahkan percakapan sehari-hari secara otomatis sesuai tingkat kesopanan (<i>Yau</i> vs <i>I'da</i>) serta menganalisis sentimen ungkapan emosional bahasa Mandar.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# FOOTER GLOBAL
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1.5rem; border-top: 1px solid #E2E8F0; color: #64748B; font-size: 0.88rem;">
    <b>Kamus Besar & Portal Edukasi Digital Bahasa Mandar</b> • Karya Inovasi <b>BUDAYA GO! 2026</b><br>
    Dirancang & Dikembangkan oleh <b>MUH. ARMIL SYAM</b> — PT. Boyang Digital Nusantara
</div>
""", unsafe_allow_html=True)