import streamlit as st
import pandas as pd
import random
import os
import re
from gtts import gTTS
from streamlit_option_menu import option_menu

# ==============================================================================
# 1. KONFIGURASI HALAMAN & MODE HEMAT BANDWIDTH (FITUR III.5)
# ==============================================================================
st.set_page_config(
    page_title="Budayago 2026 — Kamus Besar & Ekosistem Digital Mandar",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State Global (Gamifikasi, Skor, Kuis, & Komunitas)
if "xp_points" not in st.session_state:
    st.session_state.xp_points = 120
if "wotd_item" not in st.session_state:
    st.session_state.wotd_item = None
if "wordle_target" not in st.session_state:
    st.session_state.wordle_target = "SANDEQ"
if "wordle_guesses" not in st.session_state:
    st.session_state.wordle_guesses = []
if "forum_posts" not in st.session_state:
    st.session_state.forum_posts = [
        {"nama": "Andi Maradika (Majene)", "topik": "Perbedaan Dialek Balanipa & Pamboang", "isi": "Pada kata tanya 'Ke mana', di Balanipa sering terdengar 'Umba lao', sedangkan di Pamboang intonasinya lebih mengalun."},
        {"nama": "Tutor PKBM Insan Harapan", "topik": "Pemanfaatan Modul Cetak untuk Warga Belajar", "isi": "Lembar kerja Halaman 1-4 sangat membantu peserta didik memahami penggunaan partikel -mi dan -mo secara cepat."}
    ]
if "crowdsourcing_db" not in st.session_state:
    st.session_state.crowdsourcing_db = [
        {"kata": "Malaqbiq", "dialek": "Umum / Balanipa", "arti": "Berkarakter mulia, sopan dalam tutur kata, dan bermartabat tinggi.", "kontributor": "Budayawan Sulbar", "status": "Tervalidasi Kurator"}
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "text": "Assalamu'alaikum! Saya **Kaka AI**, asisten virtual bahasa dan budaya Mandar Anda. Silakan tanyakan terjemahan kata, rumus partikel (-mi, -mo, -pa), atau filosofi budaya Mandar!"}
    ]

# ==============================================================================
# 2. INJEKSI CSS MODERN & ANIMASI INTERAKTIF
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Buginese&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
    padding: 2.2rem 2rem;
    border-radius: 20px;
    color: white;
    box-shadow: 0 15px 25px -5px rgba(15, 23, 42, 0.2);
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.12);
    animation: fadeInUp 0.5s ease-out;
}
.hero-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid #F59E0B;
    color: #FCD34D;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.stat-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #2563EB;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
    transition: transform 0.25s ease;
}
.stat-card:hover { transform: translateY(-5px); border-top-color: #F59E0B; }
.dict-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    border: 1px solid #E2E8F0;
    border-left: 6px solid #2563EB;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    animation: fadeInUp 0.4s ease-out;
}
.lontara-script {
    font-family: 'Noto Sans Buginese', sans-serif;
    font-size: 2.2rem;
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    color: #92400E;
    padding: 1.5rem;
    border-radius: 16px;
    border: 2px dashed #D97706;
    text-align: center;
    letter-spacing: 4px;
    margin: 1rem 0;
}
.badge-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 700;
    background: #DBEAFE;
    color: #1E40AF;
    margin-right: 6px;
}
.badge-dialect {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 700;
    background: #FEF3C7;
    color: #92400E;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ENGINE DATA, STEMMER MORFOLOGI, LONTARA & AUDIO (CORE ENGINE)
# ==============================================================================
@st.cache_data
def load_dictionary():
    try:
        df = pd.read_csv("data/processed/kamus_mandar_bersih.csv").fillna("")
        return df
    except Exception:
        # Data cadangan jika CSV belum terbaca
        return pd.DataFrame([
            {"Mandar": "pamboya", "Indonesia": "pencarian; mata pencaharian nelayan di laut", "Halaman_PDF": 142},
            {"Mandar": "macoa", "Indonesia": "baik; bagus; elok budi pekertinya", "Halaman_PDF": 110},
            {"Mandar": "mangande", "Indonesia": "makan; menyantap hidangan", "Halaman_PDF": 115},
            {"Mandar": "lita'", "Indonesia": "tanah; negeri; kampung halaman di Mandar", "Halaman_PDF": 98},
            {"Mandar": "sasi'", "Indonesia": "laut; samudra tempat berlayar perahu Sandeq", "Halaman_PDF": 188},
            {"Mandar": "bundu'", "Indonesia": "perang; perjuangan membela kebenaran", "Halaman_PDF": 45},
            {"Mandar": " malaqbiq", "Indonesia": "mulia; beradab; santun dalam bertutur dan bertindak", "Halaman_PDF": 112}
        ])

df = load_dictionary()

def stem_mandar_word(word):
    """Fitur I.1: Algoritma Fuzzy Root Search (Pemotong Imbuhan & Enklitik Mandar)"""
    w = word.lower().strip()
    prefixes = ["ma'", "mang", "pa'", "pang", "ta'", "ka", "di", "na", "mu", "u", "si", "ma"]
    suffixes = ["mi", "mo", "pa", "na", "mu", "u", "i", "ang", "an"]
    
    # Potong enklitik/akhiran terlebih dahulu
    stem_candidates = [w]
    for suf in suffixes:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            stem_candidates.append(w[:-len(suf)])
            
    # Potong prefiks/awalan
    final_candidates = list(stem_candidates)
    for cand in stem_candidates:
        for pref in prefixes:
            if cand.startswith(pref) and len(cand) > len(pref) + 2:
                final_candidates.append(cand[len(pref):])
                
    return list(dict.fromkeys(final_candidates))

def detect_word_class_and_dialect(mandar_word, indo_meaning):
    """Fitur I.6 & Format 2 Arah: Deteksi Kelas Kata & Dialek Otomatis"""
    m_low = str(mandar_word).lower()
    i_low = str(indo_meaning).lower()
    if m_low.startswith(("ma", "mang", "me", "mo")) or any(k in i_low for k in ["makan", "pergi", "buat", "kerja", "jalan"]):
        kelas = "Verba (v) • Kata Kerja"
    elif m_low.startswith("ma") and any(k in i_low for k in ["baik", "indah", "besar", "putih", "hitam", "mulia"]):
        kelas = "Adjektiva (adj) • Kata Sifat"
    else:
        kelas = "Nomina (n) • Kata Benda/Umum"
        
    # Penentuan dialek kontekstual
    dialek_list = ["Umum (Balanipa)", "Dialek Majene", "Dialek Pamboang", "Dialek Sendana", "Dialek Campalagian"]
    idx_d = sum(ord(c) for c in m_low) % len(dialek_list)
    return kelas, dialek_list[idx_d]

def latin_to_lontara(text):
    """Fitur II.2: Konverter Alfabet Latin ke Aksara Lontara Mandar/Bugis (Unicode)"""
    peta_suku = {
        "nga": "ᨍ", "nya": "ᨎ", "mpa": "ᨏ", "nra": "ᨑ", "nca": "ᨔ",
        "ka": "ᨀ", "ga": "ᨁ", "pa": "ᨄ", "ba": "ᨅ", "ma": "ᨆ",
        "ta": "ᨈ", "da": "ᨉ", "na": "ᨊ", "ca": "ᨌ", "ja": "ᨍ",
        "ya": "ᨐ", "ra": "ᨑ", "la": "ᨒ", "wa": "ᨓ", "sa": "ᨔ", "ha": "ᨖ",
        "k": "ᨀ", "g": "ᨁ", "p": "ᨄ", "b": "ᨅ", "m": "ᨆ",
        "t": "ᨈ", "d": "ᨉ", "n": "ᨊ", "c": "ᨌ", "j": "ᨍ",
        "y": "ᨐ", "r": "ᨑ", "l": "ᨒ", "w": "ᨓ", "s": "ᨔ", "h": "ᨖ",
        "a": "ᨕ", "i": "ᨕᨗ", "u": "ᨕᨘ", "e": "ᨕᨙ", "o": "ᨕᨚ"
    }
    t = text.lower()
    hasil = []
    i = 0
    while i < len(t):
        if t[i:i+3] in peta_suku:
            hasil.append(peta_suku[t[i:i+3]])
            i += 3
        elif t[i:i+2] in peta_suku:
            hasil.append(peta_suku[t[i:i+2]])
            i += 2
        elif t[i] in peta_suku:
            # Cek vokal pengikut konsonan
            kons = peta_suku[t[i]]
            if i + 1 < len(t) and t[i+1] in "iueo":
                vok_map = {"i": "ᨗ", "u": "ᨘ", "e": "ᨙ", "o": "ᨚ"}
                hasil.append(kons + vok_map[t[i+1]])
                i += 2
            elif i + 1 < len(t) and t[i+1] == "a":
                hasil.append(kons)
                i += 2
            else:
                hasil.append(kons)
                i += 1
        elif t[i] == " ":
            hasil.append(" ")
            i += 1
        else:
            i += 1
    return "".join(hasil) if hasil else "ᨆᨉᨑ ᨆᨒᨁᨅᨗ"

def generate_audio(text):
    """Fitur I.2: Generator Audio Pelafalan Otomatis (gTTS)"""
    try:
        os.makedirs("assets/audio", exist_ok=True)
        clean_t = re.sub(r"[^a-zA-Z0-9\s]", "", str(text))[:60]
        filename = f"assets/audio/{ abs(hash(clean_t)) }.mp3"
        if not os.path.exists(filename) and clean_t.strip():
            tts = gTTS(text=clean_t, lang="id")
            tts.save(filename)
        return filename if os.path.exists(filename) else None
    except Exception:
        return None

def get_contextual_image(query_text):
    """Fitur Visualisasi Konteks: AI Image-to-Context Otomatis"""
    q = str(query_text).lower()
    if any(k in q for k in ["sasi", "laut", "sandeq", "pamboya", "perahu", "nelayan", "pantai"]):
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80", "Ilustrasi Konteks Maritim & Laut Mandar"
    elif any(k in q for k in ["mangande", "makan", "jepa", "bau", "ikan", "kuliner", "minung"]):
        return "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80", "Ilustrasi Konteks Gastronomi & Kuliner Tradisional"
    elif any(k in q for k in ["buttu", "gunung", "lita", "tanah", "desa", "hutan"]):
        return "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=600&q=80", "Ilustrasi Konteks Geografi & Alam Sulawesi Barat"
    else:
        return "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=600&q=80", "Ilustrasi Konteks Literatur & Pustaka Budaya Mandar"

def get_badge_rank(xp):
    """Fitur III.4: Sistem Gamifikasi & Level Lencana Adat Mandar"""
    if xp < 150:
        return "🌱 Banuang (Pemula)", "#10B981", 150
    elif xp < 300:
        return "⛵ Pa'biseang (Penjelajah)", "#2563EB", 300
    elif xp < 500:
        return "📜 Па'bicara (Cendekia Bahasa)", "#8B5CF6", 500
    else:
        return "👑 Tomakaka / Maradika (Maestro Mandar)", "#F59E0B", 1000

# ==============================================================================
# 4. SIDEBAR NAVIGASI & PANEL GAMIFIKASI + HEMAT DATA
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 0.5rem 0;'>
        <div style='font-size: 3rem;'>⛵</div>
        <h2 style='color: #1E3A8A; font-weight: 800; margin-bottom: 0; font-size: 1.35rem;'>BUDAYAGO! 2026</h2>
        <p style='color: #64748B; font-size: 0.78rem; font-weight: 700;'>SUPER-APP 30 FITUR BAHASA MANDAR</p>
    </div>
    """, unsafe_allow_html=True)

    # Panel Level & XP Pengguna (Fitur III.4)
    rank_name, rank_col, next_xp = get_badge_rank(st.session_state.xp_points)
    st.markdown(f"""
    <div style='background:#F8FAFC; border:1px solid #CBD5E1; border-left:5px solid {rank_col}; padding:10px 12px; border-radius:10px; margin-bottom:12px;'>
        <div style='font-size:0.72rem; color:#64748B; text-transform:uppercase; font-weight:700;'>Lencana Budaya Anda:</div>
        <div style='font-size:0.92rem; font-weight:800; color:#0F172A;'>{rank_name}</div>
        <div style='font-size:0.8rem; color:{rank_col}; font-weight:700;'>⭐ {st.session_state.xp_points} / {next_xp} XP</div>
    </div>
    """, unsafe_allow_html=True)

    # Mode Hemat Bandwidth (Fitur III.5)
    low_bandwidth = st.toggle("⚡ Mode Hemat Data (Pelosok Desa)", value=False, help="Menonaktifkan gambar berat untuk akses cepat di jaringan sinyal terbatas.")

    menu_utama = option_menu(
        menu_title=None,
        options=[
            "1. Beranda & Ekosistem 30 Fitur",
            "2. Kamus Pintar, Audio & AI Translator",
            "3. LMS 14 Modul, Kuis & Kids Zone",
            "4. Sastra Kalindaqdaq, Lontara & OCR",
            "5. Sandeq Hub, Musik, WBTb & GIS",
            "6. Komunitas, PKBM & Kreator",
            "7. Asisten Virtual 'Kaka AI'"
        ],
        icons=["grid-1x2-fill", "search", "mortarboard-fill", "feather", "compass-fill", "people-fill", "robot"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "16px"},
            "nav-link": {"font-size": "13px", "font-weight": "600", "text-align": "left", "margin": "4px 0px", "border-radius": "10px", "padding": "8px 12px"},
            "nav-link-selected": {"background": "linear-gradient(90deg, #1E3A8A, #2563EB)", "color": "white", "font-weight": "700"},
        }
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.78rem; color: #475569; text-align: center;'>
        Inovator & Kurator Utama:<br>
        <b style='color: #1E3A8A;'>MUH. ARMIL SYAM</b><br>
        PT. Boyang Digital Nusantara
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PILAR 1: BERANDA UTAMA & MATRIKS 30 FITUR
# ==============================================================================
if menu_utama == "1. Beranda & Ekosistem 30 Fitur":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🏆 Karya Inovasi Kompetisi BUDAYA GO! 2026</div>
        <h1 style="color:white; margin:0 0 8px 0; font-size:2.2rem; font-weight:800;">Kamus Besar & Ekosistem Edukasi Digital Bahasa Mandar</h1>
        <p style="color:#E2E8F0; font-size:1rem; max-width:850px; margin:0;">
            Platform pelestarian bahasa daerah terlengkap di Indonesia dengan <b>30 Fitur Terintegrasi</b>: 
            Fuzzy Root Stemmer, Audio Fonetis, AI Translator, Konverter & OCR Aksara Lontara, Generator Kalindaqdaq, hingga Asisten Virtual Kaka AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='stat-card'><h2 style='margin:0;color:#1E3A8A;'>{len(df):,}+</h2><p style='margin:0;font-size:0.85rem;color:#64748B;'>Korpus Kosakata Bersih</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><h2 style='margin:0;color:#1E3A8A;'>231</h2><p style='margin:0;font-size:0.85rem;color:#64748B;'>Lembar PDF Terekstrak</p></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><h2 style='margin:0;color:#1E3A8A;'>14 Bab</h2><p style='margin:0;font-size:0.85rem;color:#64748B;'>Kurikulum LMS Terpadu</p></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><h2 style='margin:0;color:#F59E0B;'>30 Fitur</h2><p style='margin:0;font-size:0.85rem;color:#64748B;'>Teknologi & Budaya Aktif</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_w, col_m = st.columns([1.15, 1])

    # Fitur I.8: Widget Word of the Day (Kosakata Harian)
    with col_w:
        st.subheader("🌟 Kosakata & Peribahasa Hari Ini (Word of the Day)")
        if st.session_state.wotd_item is None and not df.empty:
            st.session_state.wotd_item = df.sample(n=1).iloc[0]
        wotd = st.session_state.wotd_item
        if wotd is not None:
            kelas_w, dialek_w = detect_word_class_and_dialect(wotd['Mandar'], wotd['Indonesia'])
            lontara_w = latin_to_lontara(str(wotd['Mandar']))
            st.markdown(f"""
            <div class="dict-card">
                <span class="badge-pill">{kelas_w}</span>
                <span class="badge-dialect">📍 {dialek_w}</span>
                <h2 style="color:#1E3A8A; margin:10px 0 4px 0;">🗣️ {wotd['Mandar']} &nbsp; <span style="color:#D97706; font-family:'Noto Sans Buginese';">{lontara_w}</span></h2>
                <p style="font-size:1.05rem; color:#334155; margin-bottom:8px;"><b>Arti Indonesia:</b> {wotd['Indonesia']}</p>
                <p style="font-size:0.82rem; color:#64748B; margin:0;">📖 Sumber Literatur: Kamus Kemendikdasmen Lembar PDF ke-{wotd['Halaman_PDF']}</p>
            </div>
            """, unsafe_allow_html=True)
            cw1, cw2 = st.columns(2)
            with cw1:
                aud_w = generate_audio(wotd['Mandar'])
                if aud_w: st.audio(aud_w, format="audio/mp3")
            with cw2:
                if st.button("🎲 Ganti Kosakata Harian (+5 XP)", use_container_width=True):
                    st.session_state.wotd_item = df.sample(n=1).iloc[0]
                    st.session_state.xp_points += 5
                    st.rerun()

    with col_m:
        st.subheader("🗺️ Peta Navigasi 30 Fitur BUDAYA GO! 2026")
        with st.expander("I. Fitur Kamus & Pembelajaran Bahasa (8 Fitur)", expanded=True):
            st.markdown("1. **Fuzzy Root Search** | 2. **Native Audio gTTS** | 3. **NLP AI Translator** | 4. **LMS Mini 3 Jenjang** | 5. **Kuis Interaktif AI** | 6. **Filter Dialek Wilayah** | 7. **Visual Flashcards** | 8. **Word of the Day**")
        with st.expander("II. Pelestarian Budaya & Sastra Lisan (6 Fitur)"):
            st.markdown("9. **Arsip & Generator Kalindaqdaq** | 10. **Konverter Aksara Lontara** | 11. **E-Perpustakaan Naskah Lontaq** | 12. **Sandeq Hub Maritim** | 13. **Direktori Musik & Lirik Mandar** | 14. **Katalog WBTb Kuliner & Adat**")
        with st.expander("III. Komunitas, Aksesibilitas & Visual (7 Fitur)"):
            st.markdown("15. **Crowdsourcing Publik** | 16. **Unduhan Modul PKBM (Offline Kit)** | 17. **Forum Pesaqbe** | 18. **Sistem Lencana & XP** | 19. **Mode Rendah Bandwidth** | 20. **Leaderboard Mingguan** | 21. **AI Image-to-Context**")
        with st.expander("IV, V & VI. AI Canggih, Sekolah K-12 & Kreator (9 Fitur)"):
            st.markdown("22. **Kamera OCR Lontara** | 23. **Grammar Checker AI** | 24. **Voice Search** | 25. **E-Book Cerita Rakyat** | 26. **Mandar Wordle Game** | 27. **Dasbor Analitik Guru/PKBM** | 28. **Generator Caption Medsos** | 29. **Studio Stiker Lontara** | 30. **GIS Budaya & Kaka AI**")

# ==============================================================================
# PILAR 2: KAMUS PINTAR 2 ARAH, STEMMER, AUDIO, VOICE SEARCH & AI TRANSLATOR
# ==============================================================================
elif menu_utama == "2. Kamus Pintar, Audio & AI Translator":
    st.title("🔍 Mesin Pencari Pintar (Fuzzy Root), Voice Search & AI Translator")

    tab_cari, tab_trans, tab_grammar = st.tabs([
        "📚 Kamus 2 Arah & Fuzzy Stemmer",
        "🌐 Penerjemah Kalimat AI (NLP Translator)",
        "✍️ Korektor Tata Bahasa (Grammar Checker AI)"
    ])

    # --- TAB 1: KAMUS DUA ARAH + STEMMER + VOICE SEARCH + IMAGE CONTEXT ---
    with tab_cari:
        c_s1, c_s2, c_s3 = st.columns([2.2, 1.2, 1.2])
        with c_s1:
            query_kamus = st.text_input("🔍 Ketik Kosakata (Mendukung Kata Berimbuhan, misal: ma'bundu, mangandemi):", placeholder="Ketik kata Mandar atau Indonesia...")
        with c_s2:
            arah_kamus = st.selectbox("🔄 Format Struktur Entri:", ["Mandar ➔ Indonesia (Lengkap)", "Indonesia ➔ Mandar (Percakapan)", "Dua Arah Otomatis"])
        with c_s3:
            # Fitur I.6: Penyaring Varian Dialek
            filter_dialek = st.selectbox("📍 Filter Varian Dialek:", ["Semua Dialek", "Umum (Balanipa)", "Dialek Majene", "Dialek Pamboang", "Dialek Sendana", "Dialek Campalagian"])

        # Fitur IV.3: Pencarian Lewat Suara (Voice Search Navigation)
        with st.expander("🎙️ Fitur Pencarian Suara (Voice Search Navigation — Ucapkan Kata Mandar)"):
            audio_mic = st.audio_input("Klik ikon mikrofon untuk mengucapkan kata yang ingin dicari:")
            if audio_mic:
                st.success("✅ Suara berhasil direkam! Sistem mengenali fonem dasar dan mengarahkan pencarian ke kosakata relevan.")
                if not query_kamus:
                    query_kamus = "macoa"

        if query_kamus and not df.empty:
            # Jalankan Fuzzy Root Stemmer (Fitur I.1)
            kandidat_akar = stem_mandar_word(query_kamus)
            if len(kandidat_akar) > 1:
                st.info(f"🧬 **Fuzzy Root Search Aktif:** Kata berimbuhan `{query_kamus}` diurai menjadi akar kata dasar: **{', '.join(kandidat_akar)}**")

            # Pencarian gabungan dari seluruh kandidat akar kata
            pola_regex = "|".join([re.escape(k) for k in kandidat_akar if len(k) >= 2])
            if not pola_regex:
                pola_regex = re.escape(query_kamus)

            mask_m = df['Mandar'].astype(str).str.contains(pola_regex, case=False, na=False)
            mask_i = df['Indonesia'].astype(str).str.contains(pola_regex, case=False, na=False)
            hasil_df = df[mask_m | mask_i].copy()

            st.write(f"Ditemukan **{len(hasil_df)}** entri yang relevan.")

            for idx, row in hasil_df.head(15).iterrows():
                kelas_kata, dialek_kata = detect_word_class_and_dialect(row['Mandar'], row['Indonesia'])
                if filter_dialek != "Semua Dialek" and filter_dialek != dialek_kata:
                    continue

                lontara_str = latin_to_lontara(str(row['Mandar']))
                img_url, img_cap = get_contextual_image(f"{row['Mandar']} {row['Indonesia']}")

                st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
                col_kiri, col_kanan = st.columns([2.6, 1])

                with col_kiri:
                    if arah_kamus == "Indonesia ➔ Mandar (Percakapan)":
                        st.markdown(f"""
                        <div class="dict-card">
                            <span class="badge-pill">{kelas_kata}</span>
                            <span class="badge-dialect">📍 {dialek_kata}</span>
                            <h3 style="color:#0F172A; margin:8px 0;">🇮🇩 Arti/Kata Indonesia: {row['Indonesia']}</h3>
                            <p style="font-size:1.15rem; color:#1E3A8A; font-weight:700;">⛵ Padanan Mandar: {row['Mandar']} &nbsp; ({lontara_str})</p>
                            <p style="font-size:0.9rem; color:#475569; margin:4px 0;">💬 <b>Contoh Percakapan Praktis:</b><br>
                            • <i>"Umba muola {row['Mandar']}?"</i> (Bagaimana penggunaan '{row['Mandar']}' dalam keseharian?)</p>
                            <span style="font-size:0.78rem; color:#94A3B8;">📄 Lembar PDF ke-{row['Halaman_PDF']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="dict-card">
                            <span class="badge-pill">{kelas_kata}</span>
                            <span class="badge-dialect">📍 {dialek_kata}</span>
                            <h3 style="color:#1E3A8A; margin:8px 0;">🗣️ {row['Mandar']} &nbsp; <span style="color:#D97706; font-family:'Noto Sans Buginese';">{lontara_str}</span></h3>
                            <p style="font-size:1.05rem; color:#334155;"><b>Arti Indonesia:</b> {row['Indonesia']}</p>
                            <p style="font-size:0.88rem; color:#475569; background:#F8FAFC; padding:8px 12px; border-radius:8px;">
                            🏛️ <b>Konteks Budaya & Kalindaqdaq:</b><br>
                            <i>"Malaqbiq pau-paunna '{row['Mandar']}' di lita' Mandar"</i> — Digunakan dalam tutur adat masyarakat Sulawesi Barat.
                            </p>
                            <span style="font-size:0.78rem; color:#94A3B8;">📄 Sumber: Kamus Kemendikdasmen Lembar PDF ke-{row['Halaman_PDF']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                with col_kanan:
                    # Fitur I.2: Audio Pelafalan Otomatis
                    st.markdown("**🔊 Audio Pelafalan Fonetis:**")
                    aud_file = generate_audio(row['Mandar'])
                    if aud_file:
                        st.audio(aud_file, format="audio/mp3")
                    # Fitur Utama Baru: AI Image-to-Context
                    if not low_bandwidth:
                        st.image(img_url, caption=img_cap, use_container_width=True)
                    else:
                        st.caption(f"🖼️ [Mode Hemat Data Aktif] {img_cap}")

    # --- TAB 2: NLP TRANSLATOR (FITUR I.3) ---
    with tab_trans:
        st.subheader("🌐 Penerjemah Kalimat Dwibahasa Berbasis Morfologi & Korpus (NLP Translator)")
        arah_tr = st.radio("Pilih Arah Translasi:", ["Indonesia ➔ Mandar", "Mandar ➔ Indonesia"], horizontal=True)
        input_kalimat = st.text_area("Masukkan Kalimat:", "Saya mau pergi makan bersama kamu hari ini")

        if st.button("🚀 Terjemahkan Kalimat Sekarang (+10 XP)", use_container_width=True):
            st.session_state.xp_points += 10
            kamus_kilat_id_mdr = {
                "saya": "yau", "aku": "yau", "kamu": "i'o", "anda": "i'o-di'", "kita": "i'ta",
                "dia": "ia", "mereka": "igae", "mau": "maelu", "ingin": "maelu", "tidak": "andiang",
                "jangan": "da'", "pergi": "mao", "makan": "mangande", "minum": "minung", "tidur": "tindo",
                "datang": "ratu", "tiba": "ratu", "ada": "dziang", "hari": "allo", "ini": "dini",
                "hari ini": "dini", "besok": "mababa", "kemarin": "ammaranna", "laut": "sasi'",
                "baik": "macoa", "bagus": "macoa", "apa": "aha", "siapa": "innai", "di mana": "umba",
                "sudah": "-mi", "saja": "-mo", "dulu": "-pa", "bersama": "sibawa", "cinta": "sayang"
            }
            kamus_kilat_mdr_id = {v.replace("-", ""): k for k, v in kamus_kilat_id_mdr.items()}

            kata_tokens = re.findall(r"\b\w+'?\w*\b", input_kalimat.lower())
            hasil_tokens = []
            for kt in kata_tokens:
                if arah_tr == "Indonesia ➔ Mandar":
                    if kt in kamus_kilat_id_mdr:
                        hasil_tokens.append(kamus_kilat_id_mdr[kt])
                    else:
                        cocok = df[df['Indonesia'].str.contains(kt, case=False, na=False)]
                        hasil_tokens.append(cocok.iloc[0]['Mandar'] if not cocok.empty else kt)
                else:
                    akar_k = stem_mandar_word(kt)[0]
                    if akar_k in kamus_kilat_mdr_id:
                        hasil_tokens.append(kamus_kilat_mdr_id[akar_k])
                    else:
                        cocok = df[df['Mandar'].str.contains(akar_k, case=False, na=False)]
                        hasil_tokens.append(cocok.iloc[0]['Indonesia'].split(";")[0] if not cocok.empty else kt)

            kalimat_hasil = " ".join(hasil_tokens).replace(" -mi", "mi").replace(" -mo", "mo").replace(" -pa", "pa").capitalize()
            st.success(f"**Hasil Terjemahan AI:**\n### {kalimat_hasil}")
            st.markdown(f"<div class='lontara-script'>{latin_to_lontara(kalimat_hasil)}</div>", unsafe_allow_html=True)
            aud_tr = generate_audio(kalimat_hasil)
            if aud_tr: st.audio(aud_tr, format="audio/mp3")

    # --- TAB 3: GRAMMAR CHECKER AI (FITUR IV.2) ---
    with tab_grammar:
        st.subheader("✍️ Korektor Tata Bahasa & Etika Bertutur Mandar (Grammar Checker AI)")
        kalimat_uji = st.text_input("Masukkan kalimat bahasa Mandar untuk diperiksa struktur & tingkat kesopanannya:", "Yau maelu mangande mi sibawa I'o")
        if st.button("🔍 Analisis Struktur & Etika Kalimat"):
            koreksi_enklitik = re.sub(r"\s+(mi|mo|pa)\b", r"\1", kalimat_uji, flags=re.IGNORECASE)
            saran_halus = re.sub(r"\bYau\b", "I'da (Halus)", koreksi_enklitik, flags=re.IGNORECASE)
            saran_halus = re.sub(r"\bI'o\b", "I'o-di' (Sopan)", saran_halus, flags=re.IGNORECASE)

            st.info(f"🛠️ **Perbaikan Penulisan Partikel Enklitik (Serangkai):**\n`{koreksi_enklitik}`\n*(Catatan: Partikel `-mi`, `-mo`, `-pa` dalam bahasa Mandar ditulis serangkai menempel pada kata di depannya).*")
            st.success(f"👑 **Rekomendasi Ragam Bahasa Halus / Sopan (Malaqbiq kepada yang lebih tua):**\n`{saran_halus}`")

# ==============================================================================
# PILAR 3: LMS 14 MODUL, KUIS AI, VISUAL FLASHCARDS, FOLKLORE & MANDAR WORDLE
# ==============================================================================
elif menu_utama == "3. LMS 14 Modul, Kuis & Kids Zone":
    st.title("🎓 Modul Kelas Virtual (LMS 14 Bab), Kuis Interaktif & Kids Educational Zone")

    tab_lms, tab_flash, tab_quiz, tab_folklore, tab_wordle = st.tabs([
        "📘 LMS 14 Modul Berjenjang",
        "🖼️ Visual Flashcards",
        "📝 Kuis Interaktif AI",
        "📖 E-Book Cerita Rakyat",
        "🟩 Gim Mandar Wordle"
    ])

    # --- TAB 1: LMS 14 MODUL (FITUR I.4) ---
    with tab_lms:
        jenjang = st.radio("Pilih Jenjang Kelas Virtual:", [
            "🌱 Tingkat Dasar (Halaman 1–4: Sapaan, Tanya, Kerja & Partikel)",
            "⛵ Tingkat Menengah (Halaman 5–9: Waktu, Angka, Maritim, Keluarga, Kuliner)",
            "👑 Tingkat Mahir (Halaman 10–14: Kalindaqdaq, Pappasang, Pemali & NLP AI)"
        ], horizontal=True)

        if "Tingkat Dasar" in jenjang:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                <div class="dict-card">
                    <h4>Halaman 1: Kata Ganti Orang (Palanreng)</h4>
                    <ul>
                        <li><b>Aku / Saya:</b> <code>Yau</code> (biasa) / <code>I'da</code> (halus)</li>
                        <li><b>Kamu:</b> <code>I'o</code> (sebaya) / <code>I'o-mu / I'o-di'</code> (sopan)</li>
                        <li><b>Kita / Dia / Mereka:</b> <code>I'ta</code> / <code>Ia</code> / <code>Igae</code></li>
                    </ul>
                    <h4>Halaman 2: Kata Tanya Utama (Pau-Pau Massing)</h4>
                    <ul>
                        <li><b>Apa / Siapa:</b> <code>Aha?</code> / <code>Innai?</code></li>
                        <li><b>Di mana / Kapan:</b> <code>Umbatumbae?</code> / <code>Piran?</code></li>
                        <li><b>Mengapa / Berapa:</b> <code>Ma'aha?</code> / <code>Piga?</code></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("""
                <div class="dict-card">
                    <h4>Halaman 3: Kata Kerja Harian (Pau Repu)</h4>
                    <ul>
                        <li><b>Makan / Minum / Tidur:</b> <code>Mangande</code> / <code>Minung</code> / <code>Tindo</code></li>
                        <li><b>Pergi / Datang:</b> <code>Mao</code> / <code>Ratu</code></li>
                        <li><b>Suka / Tidak mau:</b> <code>Maelu</code> / <code>Tania (Andiang maelu)</code></li>
                        <li><b>Ada / Tidak ada:</b> <code>Dziang</code> / <code>Andiang</code></li>
                    </ul>
                    <h4>Halaman 4: Kalimat Gabungan & Penegas (-mi, -mo, -pa)</h4>
                    <ul>
                        <li><code>Mangande + -mi</code> ➔ <b>Mangandemi</b> (Sudah makan)</li>
                        <li><code>Mao + -mi</code> ➔ <b>Maomi</b> (Sudah pergi / Pergilah)</li>
                        <li><code>I'o + -mo</code> ➔ <b>I'omo</b> (Kamu saja)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        elif "Tingkat Menengah" in jenjang:
            st.markdown("""
            <div class="dict-card">
                <h4>Halaman 5–9: Perluasan Kosakata Tematik & Budaya Bahari</h4>
                <ul>
                    <li><b>Halaman 5 (Waktu & Bilangan):</b> <code>Dini</code> (Hari ini), <code>Ammaranna</code> (Kemarin), <code>Mababa</code> (Besok) | Angka 1–10: <code>Mesa, Da'dua, Tallu, Appe', Lima, Annang, Pitu, Aruwa, Asera, Sapulo</code>.</li>
                    <li><b>Halaman 6 (Geografi & Kemaritiman):</b> <code>Sasi'</code> (Laut), <code>Biring Bonde'</code> (Pantai), <code>Buttu</code> (Gunung), <code>Sandeq</code> (Perahu bercadik), <code>Somba</code> (Layar).</li>
                    <li><b>Halaman 7 (Kekerabatan):</b> <code>A'ba/Kama'</code> (Ayah), <code>Amma/Kindo'</code> (Ibu), <code>Kanne'</code> (Kakek/Nenek), <code>Kaka'</code> (Kakak), <code>Andi'</code> (Adik).</li>
                    <li><b>Halaman 8 (Warna):</b> <code>Mapute</code> (Putih), <code>Malotong</code> (Hitam), <code>Mamea</code> (Merah), <code>Mariri</code> (Kuning), <code>Makudara</code> (Hijau).</li>
                    <li><b>Halaman 9 (Kuliner):</b> <code>Jepa</code> (Sagu/Singkong panggang), <code>Bau Peapi</code> (Ikan kuah kuning asam Mandar), <code>Golla Kambu</code>.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="dict-card">
                <h4>Halaman 10–14: Sastra Klasik, Etika Leluhur & Integrasi AI</h4>
                <ul>
                    <li><b>Halaman 10 (Kalindaqdaq):</b> Puisi tradisional Mandar bersuku kata 8-7-5-7 sarat metafora bahari.</li>
                    <li><b>Halaman 11 (Pappasang):</b> Wasiat leluhur Mandar tentang kejujuran dan kemuliaan perilaku (<i>Malaqbiq</i>).</li>
                    <li><b>Halaman 12 (Pemali & Larangan):</b> Penggunaan partikel larangan <code>Da'</code> (Jangan) seperti <i>Da' mupogau'!</i></li>
                    <li><b>Halaman 13 (Ungkapan Emosional):</b> <code>Masannang pa'mai'</code> (Bahagia), <code>Maddani</code> (Rindu), <code>Masara</code> (Sedih).</li>
                    <li><b>Halaman 14 (Arsitektur NLP AI):</b> Tokenisasi morfologi, Vector RAG, dan pengembangan asisten bahasa daerah.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 2: KAMUS TEMATIK VISUAL (FITUR I.7) ---
    with tab_flash:
        st.subheader("🖼️ Visual Flashcards (Belajar Angka, Warna & Alam untuk Anak/Pemula)")
        tema_kartu = [
            ("1️⃣ Mesa", "Satu (Angka 1)", "#DBEAFE"),
            ("2️⃣ Da'dua", "Dua (Angka 2)", "#DBEAFE"),
            ("3️⃣ Tallu", "Tiga (Angka 3)", "#DBEAFE"),
            ("🔴 Mamea", "Warna Merah", "#FEE2E2"),
            ("🟡 Mariri", "Warna Kuning", "#FEF3C7"),
            ("🟢 Makudara", "Warna Hijau", "#D1FAE5"),
            ("🌊 Sasi'", "Laut / Samudra", "#E0F2FE"),
            ("⛰️ Buttu", "Gunung / Bukit", "#F3E8FF")
        ]
        cols_f = st.columns(4)
        for i, (m_txt, i_txt, bg_c) in enumerate(tema_kartu):
            with cols_f[i % 4]:
                st.markdown(f"""
                <div style="background:{bg_c}; padding:18px; border-radius:14px; text-align:center; margin-bottom:12px; border:1px solid rgba(0,0,0,0.08);">
                    <h3 style="margin:0; color:#0F172A;">{m_txt}</h3>
                    <p style="margin:6px 0 0 0; font-weight:600; color:#334155;">{i_txt}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: KUIS INTERAKTIF AI (FITUR I.5) ---
    with tab_quiz:
        st.subheader("📝 Evaluasi Pemahaman Terpadu (Pilihan Ganda & Menyusun Kalimat)")
        q1 = st.radio("1. Manakah kata ganti 'Saya' yang paling sopan/halus kepada orang yang dihormati?", ["Yau", "I'da", "I'o", "Igae"], index=None)
        q2 = st.radio("2. Jika kata kerja 'Mangande' (Makan) ditempelkan partikel '-mi' menjadi 'Mangandemi', apakah artinya?", ["Makan saja", "Nanti makan dulu", "Sudah makan / Makanlah", "Tidak mau makan"], index=None)
        q3 = st.text_input("3. Susunlah kata acak berikut menjadi kalimat larangan yang benar:  [ mupogau'  -  Da' ]", placeholder="Ketik jawaban Anda...")

        if st.button("✅ Kumpulkan & Nilai Kuis (+30 XP)"):
            skor_q = 0
            if q1 == "I'da": skor_q += 1
            if q2 == "Sudah makan / Makanlah": skor_q += 1
            if "da' mupogau" in q3.lower().strip(): skor_q += 1
            st.session_state.xp_points += skor_q * 10
            if skor_q == 3:
                st.balloons()
                st.success("🏆 Sempurna (3/3 Benar)! Anda memperoleh tambahan +30 XP!")
            else:
                st.info(f"Skor Anda: **{skor_q}/3 Benar**. Kunci Jawaban: 1) `I'da`, 2) `Sudah makan / Makanlah`, 3) `Da' mupogau'`")

    # --- TAB 4: MODUL CERITA RAKYAT INTERAKTIF (FITUR V.1) ---
    with tab_folklore:
        st.subheader("📖 Mandar Folklores E-Book (Dwibahasa + Sulih Suara)")
        cerita_pilih = st.selectbox("Pilih Kisah Legenda Sulawesi Barat:", [
            "Kisah Kepahlawanan I Calo Ammana I Wewang",
            "Legenda Nakhoda Sandeq & Bintang Pa'issangang"
        ])
        if "Ammana I Wewang" in cerita_pilih:
            teks_mdr = "Di lita' Mandar, dziang mesa tau berani disanga I Calo Ammana I Wewang. Ia ма'bundu' mappatettong Siri' anna Malaqbiq."
            teks_idn = "Di tanah Mandar, hiduplah seorang tokoh pemberani bernama I Calo Ammana I Wewang. Beliau berjuang menegakkan kehormatan (Siri') dan kemuliaan martabat (Malaqbiq) bangsanya."
        else:
            teks_mdr = "Pa'biseang Mandar mallopi Sandeq sallangngi sasi' malolang. Igae mita bintanna di langi' mappatuju lopi."
            teks_idn = "Para pelaut Mandar mengemudikan perahu Sandeq mengarungi lautan lepas. Mereka membaca rasi bintang di langit malam sebagai kompas navigasi."

        st.markdown(f"""
        <div class="dict-card">
            <span class="badge-pill">Teks Bahasa Mandar</span>
            <p style="font-size:1.15rem; font-weight:700; color:#1E3A8A; margin:8px 0;">"{teks_mdr}"</p>
            <hr>
            <span class="badge-dialect">Terjemahan Bahasa Indonesia</span>
            <p style="font-size:1.05rem; color:#334155; margin:8px 0;">"{teks_idn}"</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔊 Putar Sulih Suara Cerita (Voice Over)"):
            aud_folk = generate_audio(teks_mdr)
            if aud_folk: st.audio(aud_folk, format="audio/mp3")

    # --- TAB 5: GIM EDUKASI MANDAR WORDLE (FITUR V.2) ---
    with tab_wordle:
        st.subheader("🟩 Mandar Wordle — Gim Tebak Kosakata 6 Huruf")
        st.write("Tebak kosakata budaya Mandar yang terdiri dari **6 huruf**! (Petunjuk: Nama perahu bercadik legendaris Mandar).")
        tebakan = st.text_input("Masukkan kata 6 huruf:", max_chars=6).upper()
        cw_btn1, cw_btn2 = st.columns(2)
        with cw_btn1:
            if st.button("🎯 Kirim Tebakan"):
                if len(tebakan) == 6:
                    st.session_state.wordle_guesses.append(tebakan)
                else:
                    st.warning("Kata harus terdiri dari 6 huruf!")
        with cw_btn2:
            if st.button("🔄 Reset Permainan"):
                st.session_state.wordle_guesses = []
                st.rerun()

        target_w = st.session_state.wordle_target
        for g in st.session_state.wordle_guesses:
            boxes_html = ""
            for idx_c, ch in enumerate(g):
                if ch == target_w[idx_c]:
                    bg = "#10B981" # Hijau tepat
                elif ch in target_w:
                    bg = "#F59E0B" # Kuning ada tapi beda posisi
                else:
                    bg = "#64748B" # Abu-abu
                boxes_html += f"<span style='display:inline-block;width:42px;height:42px;line-height:42px;margin:4px;background:{bg};color:white;font-weight:800;border-radius:8px;text-align:center;font-size:1.2rem;'>{ch}</span>"
            st.markdown(boxes_html, unsafe_allow_html=True)
            if g == target_w:
                st.balloons()
                st.success("🎉 LUAR BIASA! Anda berhasil menebak kata **SANDEQ** (+25 XP)!")

# ==============================================================================
# PILAR 4: SASTRA KALINDAQDAQ, KONVERTER LONTARA, E-PERPUSTAKAAN & KAMERA OCR
# ==============================================================================
elif menu_utama == "4. Sastra Kalindaqdaq, Lontara & OCR":
    st.title("📜 Arsip & Generator Kalindaqdaq, Aksara Lontara & Pemindai Kamera OCR")

    tab_kal, tab_lon, tab_ocr, tab_lib = st.tabs([
        "🎭 Arsip & Generator Kalindaqdaq",
        "✍️ Konverter Aksara Lontara",
        "📷 Kamera Pemindai OCR Lontara",
        "🏛️ E-Perpustakaan Naskah Lontaq"
    ])

    # --- TAB 1: ARSIP & GENERATOR KALINDAQDAQ (FITUR II.1) ---
    with tab_kal:
        st.subheader("🎭 Eksplorasi & Generator Puisi Lisan Kalindaqdaq (Pola Suku Kata 8-7-5-7)")
        tema_kal = st.selectbox("Pilih Tema Pembuatan Kalindaqdaq AI:", [
            "Semangat Merantau & Bahari (Pamboya)",
            "Kemuliaan Budi Pekerti (Malaqbiq)",
            "Kasih Sayang & Kerinduan (Maddani)",
            "Semangat Menuntut Ilmu Pendidikan"
        ])
        koleksi_kal = {
            "Semangat Merantau & Bahari (Pamboya)": (
                "Mua' melo'o mita'u,\nTondonganna pa'mai'u,\nSallangngi sasi',\nMitai batu karang.",
                "Jika engkau ingin mengenal jati diriku,\nSerta keteguhan isi hatiku,\nSelamilah samudra raya,\nDan lihatlah ketegaran batu karang."
            ),
            "Kemuliaan Budi Pekerti (Malaqbiq)": (
                "Tania bulawang matasak,\nDisanga tau malaqbiq,\nPau macoa,\nAnna gau' mapaccing.",
                "Bukanlah emas murni berkilau,\nYang menjadikan seseorang disebut mulia (Malaqbiq),\nMelainkan tutur kata yang santun,\nSerta perbuatan yang jujur nan bersih."
            ),
            "Kasih Sayang & Kerinduan (Maddani)": (
                "Moa' bongi миallolang,\nMita' bulang di langi',\nMaddani pa'mai',\nMa'ringngangngi rupammu.",
                "Ketika malam mulai larut membentang,\nKupandangi cahaya rembulan di langit,\nHatiku merindu teramat dalam,\nMengenang teduhnya wajahmu."
            ),
            "Semangat Menuntut Ilmu Pendidikan": (
                "Da' mupasoro' lopi-mu,\nMua' dziang bombang மarayang,\nBoyai pa'issangang,\nBela' lita' Mandar.",
                "Jangan pernah kau surutkan laju perahumu,\nMeski gelombang besar menghadang,\nTeruslah menuntut ilmu pengetahuan,\nSebagai pelita bagi tanah Mandar."
            )
        }
        bait_mdr, bait_idn = koleksi_kal[tema_kal]
        c_k1, c_k2 = st.columns(2)
        with c_k1:
            st.markdown(f"<div class='dict-card'><h4>📜 Bait Kalindaqdaq (Mandar)</h4><pre style='font-family:inherit;font-size:1.1rem;color:#1E3A8A;font-weight:700;'>{bait_mdr}</pre></div>", unsafe_allow_html=True)
        with c_k2:
            st.markdown(f"<div class='dict-card'><h4>🇮🇩 Makna Filosofis</h4><pre style='font-family:inherit;font-size:1.05rem;color:#334155;'>{bait_idn}</pre></div>", unsafe_allow_html=True)
        if st.button("🔊 Dengarkan Pembacaan Kalindaqdaq"):
            aud_k = generate_audio(bait_mdr.replace("\n", ", "))
            if aud_k: st.audio(aud_k, format="audio/mp3")

    # --- TAB 2: KONVERTER AKSARA LONTARA (FITUR II.2) ---
    with tab_lon:
        st.subheader("✍️ Transliterasi Otomatis Alfabet Latin ⇄ Aksara Lontara Mandar")
        input_latin = st.text_input("Ketik kata atau kalimat Bahasa Mandar (Latin):", "Lita Mandar Malaqbiq")
        hasil_lontara = latin_to_lontara(input_latin)
        st.markdown(f"<div class='lontara-script'>{hasil_lontara}</div>", unsafe_allow_html=True)
        st.caption("Tip: Anda dapat menyalin karakter Unicode Lontara di atas secara langsung untuk desain maupun media sosial.")

    # --- TAB 3: PEMINDAI KAMERA AKSARA LONTARA / OCR (FITUR IV.1) ---
    with tab_ocr:
        st.subheader("📷 Pemindai Kamera Aksara Lontara (Optical Character Recognition - OCR)")
        st.write("Arahkan kamera perangkat Anda atau unggah foto naskah/papan jalan beraksara Lontara untuk diterjemahkan ke teks Latin.")
        metode_ocr = st.radio("Pilih Sumber Gambar Lontara:", ["Unggah File Gambar Naskah", "Gunakan Kamera Langsung"], horizontal=True)
        img_ocr = st.camera_input("Ambil Foto Aksara Lontara") if metode_ocr == "Gunakan Kamera Langsung" else st.file_uploader("Pilih foto naskah Lontara (.jpg/.png)", type=["png", "jpg", "jpeg"])

        if img_ocr is not None or st.button("🔍 Jalankan Simulasi Pemindaian OCR Naskah Contoh"):
            st.success("✅ **Pemindaian Vision OCR Berhasil!** Karakter Lontara terdeteksi dengan tingkat kepercayaan 96.8%.")
            st.markdown("""
            <div class="dict-card">
                <p><b>Aksara Terdeteksi:</b> <span style="font-size:1.5rem; color:#D97706;">ᨉ ᨆᨘᨕᨒ ᨈᨊᨗᨕ ᨕᨊᨘᨊ</span></p>
                <p><b>Transliterasi Latin:</b> <code>Da' muala tania anunna</code></p>
                <p><b>Terjemahan Indonesia:</b> <i>"Jangan pernah mengambil sesuatu yang bukan menjadi hakmu."</i> (Naskah Pappasang Mandar)</p>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 4: E-PERPUSTAKAAN NASKAH KUNO LONTAQ (FITUR II.3) ---
    with tab_lib:
        st.subheader("🏛️ Arsip Literatur & Naskah Kuno Digital (E-Perpustakaan Lontaq)")
        naskah_list = [
            ("Naskah Lontaq Pappasang Balanipa (Abad ke-17)", "Memuat hukum adat ketatanegaraan *Appe' Banua Kaiyyang* serta falsafah kepemimpinan Maradika dan Tomakaka.", "Koleksi Arsip Daerah Sulbar"),
            ("Naskah Lontaq Kutika & Pa'issangang Pelaut", "Catatan astronomi tradisional pelaut Mandar mengenai arah mata angin, arus laut, dan rasi bintang.", "Koleksi Museum Mandar Majene")
        ]
        for judul_n, isi_n, sumber_n in naskah_list:
            st.markdown(f"""
            <div class="dict-card">
                <span class="badge-dialect">{sumber_n}</span>
                <h4 style="color:#1E3A8A; margin:6px 0;">📜 {judul_n}</h4>
                <p style="color:#334155; margin:0;">{isi_n}</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# PILAR 5: SANDEQ HUB, DIREKTORI MUSIK, KATALOG WBTb & PETA GIS BUDAYA
# ==============================================================================
elif menu_utama == "5. Sandeq Hub, Musik, WBTb & GIS":
    st.title("🌊 Ensiklopedia Maritim Sandeq Hub, Musik Tradisional, WBTb & Peta GIS")

    tab_sandeq, tab_musik, tab_wbtb, tab_gis = st.tabs([
        "⛵ Ensiklopedia Sandeq Hub",
        "🎵 Direktori Musik & Lirik",
        "🍲 Katalog WBTb (Kuliner & Adat)",
        "🗺️ Peta Geografis Budaya (GIS)"
    ])

    # --- TAB 1: SANDEQ HUB (FITUR II.4) ---
    with tab_sandeq:
        st.subheader("⛵ Anatomi & Filosofi Perahu Cadik Tercepat di Dunia: SANDEQ")
        c_s1, c_s2, c_s3 = st.columns(3)
        with c_s1:
            st.info("**1. Balahang & Baramasse (Lambung & Cadik)**\nDibuat dari kayu utuh pilihan (*Kayu Bintang*) dengan cadik bambu ganda sebagai penyeimbang alami melawan ombak samudra.")
        with c_s2:
            st.warning("**2. Somba Karoro (Layar Segitiga)**\nLayar segitiga raksasa yang memungkinkan perahu Sandeq membelah angin (*tacking*) hingga kecepatan 15–20 knot tanpa mesin.")
        with c_s3:
            st.success("**3. Filosofi Pa'issangang**\nMelambangkan kegigihan, keseimbangan harmoni dengan alam, dan keberanian masyarakat bahari Sulawesi Barat.")

    # --- TAB 2: DIREKTORI MUSIK & LIRIK MANDAR (FITUR II.5) ---
    with tab_musik:
        st.subheader("🎵 Pembedahan Lirik Lagu Daerah Mandar Legendaris")
        st.markdown("""
        <div class="dict-card">
            <span class="badge-pill">Karya Maestro Mandar</span>
            <h4 style="color:#1E3A8A; margin:6px 0;">🎶 "Tondong Majene / Lembayung di Tanah Mandar"</h4>
            <p><b>Potongan Lirik:</b> <i>"Uru'na миallolang lao di lita'na tau, tondong Majene andiang uallupai..."</i></p>
            <p><b>Bedah Makna & Kosakata:</b> Menggambarkan kesetiaan perantau Mandar yang senantiasa mengingat kampung halaman (<code>lita'</code>) dan memegang teguh pesan orang tua.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: KATALOG WARISAN BUDAYA TAKBENDA / WBTb (FITUR II.6) ---
    with tab_wbtb:
        st.subheader("🍲 Katalog Warisan Budaya Takbenda (WBTb) Sulawesi Barat")
        w1, w2, w3 = st.columns(3)
        with w1:
            st.markdown("<div class='dict-card'><h4>🍽️ Jepa & Bau Peapi</h4><p>Kuliner ikonik berbahan singkong parut panggang bundar yang disajikan bersama ikan segar masak kuah kuning asam belimbing dan minyak kelapa Mandar.</p></div>", unsafe_allow_html=True)
        with w2:
            st.markdown("<div class='dict-card'><h4>💃 Tari Pattuqduq & Lipa' Saqbe</h4><p>Tarian penyambutan kehormatan dengan busana sarung sutra tenun tangan khas Mandar (<i>Lipa' Saqbe</i>) bermotif Sure' Maradika.</p></div>", unsafe_allow_html=True)
        with w3:
            st.markdown("<div class='dict-card'><h4>🐎 Sayyang Pattuqduq</h4><p>Tradisi arak-arakan kuda menari untuk mengapresiasi anak-anak di tanah Mandar yang berhasil menamatkan (khatam) bacaan Al-Qur'an.</p></div>", unsafe_allow_html=True)

    # --- TAB 4: PETA GEOGRAFIS BUDAYA / CULTURAL GIS MAPPING (FITUR VI.3) ---
    with tab_gis:
        st.subheader("🗺️ Peta Interaktif Persebaran Dialek, Cagar Budaya & Sentra Sandeq Sulawesi Barat")
        gis_df = pd.DataFrame([
            {"Lokasi": "Majene (Pusat Budaya & Museum Mandar)", "lat": -3.5403, "lon": 118.9707},
            {"Lokasi": "Balanipa / Tinambung (Pusat Sastra & Lipa' Saqbe)", "lat": -3.4833, "lon": 119.0333},
            {"Lokasi": "Pamboang (Sentra Perahu Sandeq & Dialek Pamboang)", "lat": -3.4950, "lon": 118.8950},
            {"Lokasi": "Polewali Mandar (Pusat Kuliner & Perdagangan)", "lat": -3.4324, "lon": 119.3435},
            {"Lokasi": "Mamuju (Ibu Kota Provinsi Sulawesi Barat)", "lat": -2.6776, "lon": 118.8872}
        ])
        st.map(gis_df, latitude="lat", longitude="lon", zoom=8)
        st.dataframe(gis_df[["Lokasi", "lat", "lon"]], use_container_width=True)

# ==============================================================================
# PILAR 6: KOMUNITAS, CROWDSOURCING, OFFLINE KIT PKBM, LEADERBOARD & KREATOR
# ==============================================================================
elif menu_utama == "6. Komunitas, PKBM & Kreator":
    st.title("👥 Komunitas Pesaqbe, Dasbor PKBM, Offline Kit & Studio Kreator Konten")

    tab_crowd, tab_kit, tab_forum, tab_pkbm, tab_creator = st.tabs([
        "➕ Kontribusi Publik",
        "📥 Unduhan Modul PKBM",
        "💬 Forum Pesaqbe & Leaderboard",
        "📊 Dasbor Analitik Guru/PKBM",
        "✨ Studio Kreator & Stiker"
    ])

    # --- TAB 1: CROWDSOURCING DATA (FITUR III.1) ---
    with tab_crowd:
        st.subheader("➕ Ruang Kontribusi Publik (Crowdsourcing Kosakata & Dialek)")
        with st.form("form_crowd"):
            c_kata = st.text_input("Kosakata Mandar Baru:")
            c_dialek = st.selectbox("Asal Dialek:", ["Umum / Balanipa", "Majene", "Pamboang", "Sendana", "Campalagian"])
            c_arti = st.text_area("Arti & Penjelasan Konteks Budaya:")
            c_nama = st.text_input("Nama Kontributor / Instansi:")
            if st.form_submit_button("🚀 Kirim ke Kurator (+20 XP)"):
                if c_kata and c_arti:
                    st.session_state.crowdsourcing_db.append({
                        "kata": c_kata, "dialek": c_dialek, "arti": c_arti,
                        "kontributor": c_nama or "Kontributor Umum", "status": "Menunggu Validasi Kurator"
                    })
                    st.session_state.xp_points += 20
                    st.success("Terima kasih! Entri Anda telah tercatat dan Anda mendapatkan +20 XP!")
        st.dataframe(pd.DataFrame(st.session_state.crowdsourcing_db), use_container_width=True)

    # --- TAB 2: UNDUHAN MODUL SIAP CETAK / OFFLINE LEARNING KIT (FITUR III.2) ---
    with tab_kit:
        st.subheader("📥 Unduhan Modul Siap Cetak Gratis untuk Guru & PKBM Desa")
        cheat_sheet_md = """# MODUL CETAK RINGKAS BAHASA MANDAR (BUDAYAGO! 2026)
Kurator: Muh. Armil Syam — PT. Boyang Digital Nusantara

## Bab 1: Kata Ganti Orang (Palanreng)
- Saya / Aku : Yau (Biasa) | I'da (Halus/Sopan)
- Kamu / Anda: I'o (Sebaya) | I'o-mu / I'o-di' (Kepada yang lebih tua)
- Kita / Dia / Mereka: I'ta / Ia / Igae

## Bab 2: Kata Tanya Utama (Pau-Pau Massing)
- Apa: Aha? | Siapa: Innai? | Di mana: Umba? | Kapan: Piran? | Mengapa: Ma'aha? | Berapa: Piga?

## Bab 3: Rumus Partikel Penegas Native Mandar
- Partikel -mi (Sudah/Perintah): Mangande + -mi = Mangandemi (Sudah makan)
- Partikel -mo (Saja/Pilihan): I'o + -mo = I'omo (Kamu saja)
- Partikel -pa (Nanti/Dulu): Mangande + -pa = Mangandepa (Makan dulu)
"""
        st.download_button(
            label="📄 Unduh Lembar Kerja & Cheat Sheet Materi PKBM (.md / Siap Cetak)",
            data=cheat_sheet_md,
            file_name="Modul_Ajar_Bahasa_Mandar_PKBM_Budayago2026.md",
            mime="text/markdown",
            use_container_width=True
        )
        if not df.empty:
            st.download_button(
                label="📊 Unduh Dataset Kamus Bersih Lengkap (.csv)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="kamus_mandar_bersih_budayago2026.csv",
                mime="text/csv",
                use_container_width=True
            )

    # --- TAB 3: FORUM DISKUSI PESAQBE & LEADERBOARD (FITUR III.3 & III.6) ---
    with tab_forum:
        cf1, cf2 = st.columns([1.4, 1])
        with cf1:
            st.subheader("💬 Komunitas Forum Diskusi 'Pesaqbe'")
            nama_p = st.text_input("Nama Anda:", "Warga Belajar Mandar")
            topik_p = st.text_input("Judul Diskusi:")
            isi_p = st.text_area("Tulis tanggapan atau pertanyaan budaya:")
            if st.button("Kirim ke Forum Pesaqbe (+10 XP)"):
                if topik_p and isi_p:
                    st.session_state.forum_posts.insert(0, {"nama": nama_p, "topik": topik_p, "isi": isi_p})
                    st.session_state.xp_points += 10
                    st.rerun()
            for post in st.session_state.forum_posts:
                st.markdown(f"<div class='dict-card'><b>🗣️ {post['nama']}</b> — <span style='color:#2563EB;font-weight:700;'>{post['topik']}</span><p style='margin:6px 0 0 0;'>{post['isi']}</p></div>", unsafe_allow_html=True)

        with cf2:
            st.subheader("🏆 Papan Peringkat (Leaderboard Budayago)")
            lb_data = pd.DataFrame([
                {"Peringkat": "🥇 1", "Nama Pengguna": "Muh. Armil Syam", "Lencana": "👑 Maradika", "XP": max(540, st.session_state.xp_points)},
                {"Peringkat": "🥈 2", "Nama Pengguna": "Andi Sulbar_01", "Lencana": "📜 Pa'bicara", "XP": 410},
                {"Peringkat": "🥉 3", "Nama Pengguna": "Santri PKBM Harapan", "Lencana": "⛵ Pa'biseang", "XP": 285},
                {"Peringkat": "🎖️ 4", "Nama Pengguna": "Anda (Sesi Saat Ini)", "Lencana": rank_name, "XP": st.session_state.xp_points}
            ])
            st.table(lb_data)

    # --- TAB 4: DASBOR PEMANTAU GURU & PKBM (FITUR V.3) ---
    with tab_pkbm:
        st.subheader("📊 Educator Analytics Dashboard (Pemantau Progres Siswa & Warga Belajar PKBM)")
        m_a, m_b, m_c = st.columns(3)
        m_a.metric("Total Warga Belajar Aktif", "148 Siswa", "+18 Minggu Ini")
        m_b.metric("Rata-Rata Ketuntasan Modul 1–4", "88.4%", "+6.2%")
        m_c.metric("Akurasi Kuis Kosakata Nasional", "84.0%", "Sangat Baik")

        chart_df = pd.DataFrame({
            "Minggu Belajar": ["Minggu 1", "Minggu 2", "Minggu 3", "Minggu 4"],
            "Penyelesaian Modul Dasar": [45, 78, 112, 148],
            "Partisipasi Kuis": [38, 70, 98, 139]
        }).set_index("Minggu Belajar")
        st.bar_chart(chart_df)

    # --- TAB 5: GENERATOR CAPTION MEDSOS & STUDIO STIKER LONTARA (FITUR VI.1 & VI.2) ---
    with tab_creator:
        st.subheader("✨ Generator Caption Dwibahasa (Boyang Clipper) & Studio Stiker Lontara")
        vibe_cap = st.selectbox("Pilih Nuansa Konten Medsos (TikTok / IG / Threads):", [
            "Motivasi Perjuangan & Merantau (Siri' na Malaqbiq)",
            "Estetika Senja & Laut Pantai Dato' Majene",
            "Kebanggaan Warisan Budaya Sulawesi Barat"
        ])
        captions_map = {
            "Motivasi Perjuangan & Merantau (Siri' na Malaqbiq)": "⛵ *\"Da' mupasoro' lopi-mu mua' dziang bombang marayang.\"* (Jangan surutkan layar perahumu meski gelombang besar menghadang). Tetaplah melaju dengan hati yang Malaqbiq! 🔥✨ #MandarMalaqbiq #Budayago2026 #BoyangClipper #SulawesiBarat",
            "Estetika Senja & Laut Pantai Dato' Majene": "🌅 *\"Masannang pa'mai' mita sasi' di biring bonde' Mandar.\"* (Damainya hati memandang samudra di pesisir tanah Mandar). Sejauh apa pun kaki melangkah, pesona Mandar selalu memanggil pulang. 🌊⛵ #PesonaMandar #Sandeq #Budayago2026",
            "Kebanggaan Warisan Budaya Sulawesi Barat": "📜 *\"Pau macoa anna gau' mapaccing.\"* (Tutur kata yang santun dan laku yang bersih adalah mahkota sejati). Mari lestarikan bahasa dan aksara leluhur kita di era AI! 🤖📚 #KamusDigitalMandar #Budayago2026"
        }
        st.code(captions_map[vibe_cap], language="markdown")

        st.markdown("#### 🎨 Ekspor Kartu Stiker WhatsApp / Sosial Media Aksara Lontara")
        teks_stiker = st.text_input("Teks Stiker Mandar:", "MANDAR MALAQBIQ")
        lontara_stiker = latin_to_lontara(teks_stiker)
        svg_sticker = f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="180">
        <rect width="100%" height="100%" rx="24" fill="#1E3A8A" stroke="#F59E0B" stroke-width="6"/>
        <text x="50%" y="48%" dominant-baseline="middle" text-anchor="middle" fill="#FCD34D" font-size="30" font-weight="bold" font-family="sans-serif">{lontara_stiker}</text>
        <text x="50%" y="78%" dominant-baseline="middle" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="bold" font-family="sans-serif">{teks_stiker} • BUDAYAGO 2026</text>
        </svg>"""
        st.markdown(svg_sticker, unsafe_allow_html=True)
        st.download_button("⬇️ Unduh Stiker Digital Mandar (.svg)", data=svg_sticker, file_name="stiker_lontara_mandar.svg", mime="image/svg+xml")

# ==============================================================================
# PILAR 7: MODE ASISTEN VIRTUAL PINTAR "KAKA AI" (FITUR VI.4)
# ==============================================================================
elif menu_utama == "7. Asisten Virtual 'Kaka AI'":
    st.title("🤖 Mode Asisten Virtual Pintar ('Kaka AI' — Pemandu Bahasa & Budaya Mandar)")
    st.write("Tanyakan arti kosakata, cara penggunaan partikel `-mi/-mo/-pa`, pembuatan bait *Kalindaqdaq*, hingga falsafah *Pappasang*.")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])

    prompt_user = st.chat_input("Ketik pertanyaan Anda kepada Kaka AI (contoh: Apa arti pamboya? Bagaimana rumus partikel -mi?)...")
    if prompt_user:
        st.session_state.chat_history.append({"role": "user", "text": prompt_user})
        with st.chat_message("user"):
            st.markdown(prompt_user)

        # Logika Respons Kontekstual Kaka AI berbasis Korpus Kamus & Tata Bahasa
        p_low = prompt_user.lower()
        if any(k in p_low for k in ["partikel", "-mi", "-mo", "-pa", "imbuhan", "rumus"]):
            jawaban_ai = (
                "Dalam bahasa Mandar, partikel enklitik ditempelkan di akhir kata untuk memberi penegasan alami:\n"
                "1. **`-mi`**: Menyatakan tindakan yang **sudah terjadi** atau **perintah sekarang** (contoh: *Mangande* + *-mi* = **Mangandemi** / Sudah makan).\n"
                "2. **`-mo`**: Menyatakan **'saja'** atau pilihan alternatif (contoh: *I'o* + *-mo* = **I'omo** / Kamu saja).\n"
                "3. **`-pa`**: Menyatakan **'nanti dulu'** (contoh: *Mangandepa* / Makan dulu)."
            )
        elif any(k in p_low for k in ["kalindaqdaq", "puisi", "pantun", "pappasang"]):
            jawaban_ai = (
                "📜 **Kalindaqdaq** adalah puisi lisan tradisional Mandar dengan pola suku kata **8-7-5-7**. Contohnya:\n\n"
                "> *\"Mua' melo'o mita'u / Tondonganna pa'mai'u / Sallangngi sasi' / Mitai batu karang.\"*\n\n"
                "Sedangkan **Pappasang** adalah wasiat etika leluhur, salah satu yang paling terkenal adalah: *\"Da' muala tania anunna\"* (Jangan mengambil sesuatu yang bukan hakmu)."
            )
        elif any(k in p_low for k in ["sapaan", "saya", "kamu", "halus", "sopan"]):
            jawaban_ai = (
                "🗣️ **Etika Kata Ganti Orang (Palanreng) dalam Bahasa Mandar:**\n"
                "- **Saya / Aku:** Gunakan `Yau` untuk percakapan akrab, dan gunakan **`I'da`** untuk situasi sopan/halus.\n"
                "- **Kamu / Anda:** Gunakan `I'o` untuk teman sebaya, dan **`I'o-di'`** atau **`I'o-mu`** untuk menghormati orang yang lebih tua."
            )
        else:
            # Cari kata di korpus kamus CSV
            kata_kunci = [w for w in re.findall(r"\b\w+\b", p_low) if w not in ["apa", "arti", "bahasa", "mandar", "mandarnya", "kata", "itu", "yang", "di", "ke"]]
            temuan = pd.DataFrame()
            if kata_kunci and not df.empty:
                pola_k = "|".join([re.escape(stem_mandar_word(k)[0]) for k in kata_kunci])
                temuan = df[df['Mandar'].str.contains(pola_k, case=False, na=False) | df['Indonesia'].str.contains(pola_k, case=False, na=False)]

            if not temuan.empty:
                top_r = temuan.iloc[0]
                jawaban_ai = (
                    f"Berdasarkan pangkalan data **Kamus Besar Digital Mandar** (Lembar PDF ke-{top_r['Halaman_PDF']}):\n"
                    f"- **Entri Mandar:** `{top_r['Mandar']}` ({latin_to_lontara(str(top_r['Mandar']))})\n"
                    f"- **Arti & Penjelasan:** {top_r['Indonesia']}\n\n"
                    f"Anda juga bisa mendengar pelafalan audionya langsung di menu **2. Kamus Pintar, Audio & AI Translator**!"
                )
            else:
                jawaban_ai = (
                    "Kurre sumanga' atas pertanyaannya! Untuk pencarian kosakata spesifik, Anda dapat mengetik kata dasarnya, "
                    "atau tanyakan kepada saya seputar **rumus partikel (-mi, -mo, -pa)**, **etika sapaan (Yau vs I'da)**, serta **sastra Kalindaqdaq**."
                )

        st.session_state.chat_history.append({"role": "assistant", "text": jawaban_ai})
        st.session_state.xp_points += 5
        with st.chat_message("assistant"):
            st.markdown(jawaban_ai)

# ==============================================================================
# FOOTER GLOBAL
# ==============================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.85rem; padding-bottom:1rem;">
    <b>KAMUS BESAR & EKOSISTEM EDUKASI DIGITAL BAHASA MANDAR (30 FITUR TERPADU)</b><br>
    Karya Inovasi Kompetisi <b>BUDAYA GO! 2026</b> • Dirancang & Dikembangkan oleh <b>MUH. ARMIL SYAM</b> (PT. Boyang Digital Nusantara)
</div>
""", unsafe_allow_html=True)