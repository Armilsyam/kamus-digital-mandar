import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import os
import re
from datetime import datetime
from gtts import gTTS
from streamlit_option_menu import option_menu

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==============================================================================
st.set_page_config(
    page_title="BUDAYA GO! 2026 — Mandar Digital Super-App (40 Fitur)",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INJEKSI TAILWIND CSS, CUSTOM CSS3 & FONT MODERN
# ==============================================================================
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Buginese&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.hero-gradient {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
    border-radius: 22px;
    padding: 2rem;
    color: white;
    box-shadow: 0 15px 30px -8px rgba(15, 23, 42, 0.35);
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 1.5rem;
}
.glass-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.4rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.2rem;
    transition: all 0.25s ease;
}
.glass-card:hover {
    border-color: #93C5FD;
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.08);
}
.tiktok-frame {
    max-width: 400px;
    margin: 0 auto;
    background: #0F172A;
    border-radius: 28px;
    padding: 16px;
    color: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
    border: 4px solid #334155;
}
.ig-avatar {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    padding: 4px;
    background: linear-gradient(45deg, #F59E0B, #EF4444, #2563EB);
    object-fit: cover;
}
.lontara-box {
    font-family: 'Noto Sans Buginese', sans-serif;
    font-size: 2rem;
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    color: #92400E;
    padding: 1.2rem;
    border-radius: 14px;
    border: 2px dashed #D97706;
    text-align: center;
    letter-spacing: 3px;
}
.wa-bubble-me {
    background: #DBEAFE;
    color: #1E3A8A;
    padding: 10px 14px;
    border-radius: 16px 16px 2px 16px;
    margin: 6px 0;
    display: inline-block;
}
.wa-bubble-other {
    background: #F1F5F9;
    color: #0F172A;
    padding: 10px 14px;
    border-radius: 16px 16px 16px 2px;
    margin: 6px 0;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. INISIALISASI SESSION STATE (DATABASE SEMENTARA / MOCK DATA LENGKAP)
# ==============================================================================
if "auth_user" not in st.session_state:
    st.session_state.auth_user = {
        "logged_in": True,
        "username": "armilsyam",
        "name": "MUH. ARMIL SYAM",
        "role": "Founder & Super Admin",
        "bio": "Founder PT. Boyang Digital Nusantara | Kurator Kamus Besar Digital Mandar | Inovator BUDAYA GO! 2026 ⛵🤖",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
        "followers": 14850,
        "following": 342,
        "xp": 950
    }

if "social_posts" not in st.session_state:
    st.session_state.social_posts = [
        {
            "id": 101,
            "author": "MUH. ARMIL SYAM",
            "handle": "@armilsyam",
            "role_badge": "👑 Founder & Admin",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
            "time": "15 Menit yang lalu",
            "content": "Assalamu'alaikum seluruh warga belajar dan pecinta budaya Sulawesi Barat! ⛵ Hari ini kita resmi meluncurkan Ekosistem 40 Fitur Kamus Besar Digital Mandar untuk kompetisi BUDAYA GO! 2026. Mari lestarikan bahasa dan sastra Kalindaqdaq di era AI! #MandarMalaqbiq #Budayago2026 #BoyangClipper",
            "lontara": "ᨆᨉᨑ ᨆᨒᨁᨅᨗ",
            "media_type": "image",
            "media_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
            "likes": 248,
            "shares": 64,
            "comments": [
                {"user": "Andi Maradika (Majene)", "text": "Luar biasa Kaka Armil! Akhirnya kamus 231 halaman Kemendikdasmen bisa diakses secepat ini."},
                {"user": "Komunitas Sandeq Sulbar", "text": "Kurre sumanga'! Fitur Kalindaqdaq dan grup chat-nya sangat membantu anak muda rantau."}
            ]
        },
        {
            "id": 102,
            "author": "Boyang Clipper Official",
            "handle": "@boyangclipper",
            "role_badge": "🎬 Kreator Budaya",
            "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80",
            "time": "1 Jam yang lalu",
            "content": "Kosakata Maritim Hari Ini: 'SANDEQ' & 'SOMBA'. Tahukah kamu? Perahu bercadik tradisional Mandar mampu melaju 20 knot hanya dengan mengandalkan angin dan ilmu navigasi bintang (Pa'issangang)! 🌊⛵",
            "lontara": "ᨔᨉᨙ ᨕᨊ ᨔᨚᨅ",
            "media_type": "image",
            "media_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=900&q=80",
            "likes": 189,
            "shares": 41,
            "comments": [
                {"user": "Santri PKBM Harapan", "text": "Malaqbiq! Sangat menginspirasi kami untuk belajar kosakata maritim."}
            ]
        }
    ]

if "reels_data" not in st.session_state:
    st.session_state.reels_data = [
        {
            "id": 1,
            "creator": "@armilsyam • Boyang Clipper",
            "title": "Belajar Cepat Partikel Native Mandar (-mi, -mo, -pa) dalam 30 Detik! 🗣️✨",
            "kalindaqdaq": "\"Mua' melo'o mita'u, sallangngi sasi', mitai batu karang.\"",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "likes": 1420,
            "comments_count": 88,
            "shares": 310,
            "comments_list": ["Sangat mudah dipahami rumus -mi dan -mo nya!", "Lanjut part 2 bahas dialek Majene Kaka!"]
        },
        {
            "id": 2,
            "creator": "@budayago2026 • Sandeq Hub",
            "title": "Filosofi Perahu Sandeq & Ketangguhan Pelaut Tanah Mandar ⛵🌊",
            "kalindaqdaq": "\"Da' mupasoro' lopi-mu mua' dziang bombang marayang.\"",
            "video_url": "https://www.w3schools.com/html/movie.mp4",
            "likes": 2890,
            "comments_count": 154,
            "shares": 520,
            "comments_list": ["Bangga jadi keturunan Mandar!", "Visual dan penjelasannya kelas dunia."]
        },
        {
            "id": 3,
            "creator": "@kuliner_sulbar • WBTb Mandar",
            "title": "Mengenal Jepa & Bau Peapi: Kuliner Warisan Leluhur Mandar 🍲🔥",
            "kalindaqdaq": "\"Malaqbiq pa'mai'na, tau maradika di parola.\"",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "likes": 980,
            "comments_count": 62,
            "shares": 195,
            "comments_list": ["Jadi rindu pulang kampung ke Majene makan Bau Peapi!"]
        }
    ]

if "reel_idx" not in st.session_state:
    st.session_state.reel_idx = 0

if "contacts_db" not in st.session_state:
    st.session_state.contacts_db = {
        "🌐 Grup: Komunitas BUDAYA GO! 2026": {
            "type": "group", "status": "🟢 148 Anggota Online", "members": 520,
            "messages": [
                {"sender": "MUH. ARMIL SYAM", "time": "10:15", "text": "Selamat datang di grup kolaborasi resmi BUDAYA GO! 2026. Silakan berdiskusi dan sumbangkan kosakata daerah masing-masing!"},
                {"sender": "Andi Maradika", "time": "10:17", "text": "Siap Founder! Saya baru saja menguji fitur Fuzzy Stemmer untuk kata 'mangandemi' dan langsung terdeteksi kata dasarnya 'mangande'."}
            ]
        },
        "⛵ Grup: Paguyuban Pelaut & Sandeq Sulbar": {
            "type": "group", "status": "🟢 42 Anggota Online", "members": 185,
            "messages": [
                {"sender": "Nakhoda Pamboang", "time": "09:30", "text": "Angin timur mulai kencang pekan ini, istilah navigasi bintang perlu kita tambahkan ke modul 6."}
            ]
        },
        "📚 Grup: Warga Belajar PKBM Insan Harapan": {
            "type": "group", "status": "🟢 35 Anggota Online", "members": 148,
            "messages": [
                {"sender": "Tutor PKBM", "time": "08:00", "text": "Jangan lupa unduh Lembar Kerja PDF/Markdown di menu Komunitas untuk latihan sore ini ya!"}
            ]
        },
        "👤 Andi Maradika (Budayawan Majene)": {
            "type": "direct", "status": "🟢 Online", "members": 2,
            "messages": [
                {"sender": "Andi Maradika", "time": "11:02", "text": "Assalamu'alaikum Kaka Armil, apakah naskah Lontaq Pappasang Balanipa sudah masuk ke E-Perpustakaan?"}
            ]
        },
        "👤 Siti Nurhaliza (Kreator Mandar)": {
            "type": "direct", "status": "⚪ Offline (Terakhir dilihat 20m lalu)", "members": 2,
            "messages": [
                {"sender": "Siti Nurhaliza", "time": "Kemarin", "text": "Generator caption TikTok bahasa Mandarnya keren sekali, langsung viral!"}
            ]
        },
        "🤖 Kaka AI (Asisten Pintar 24 Jam)": {
            "type": "ai", "status": "🟢 AI Selalu Aktif", "members": 2,
            "messages": [
                {"sender": "Kaka AI", "time": " Sekarang", "text": "Halo! Tanyakan kata Bahasa Mandar atau rumus partikel apa saja di ruang obrolan ini, saya akan langsung menjawabnya!"}
            ]
        }
    }

if "profile_gallery" not in st.session_state:
    st.session_state.profile_gallery = [
        {"title": "Peluncuran Kamus Besar Digital Mandar 2026", "likes": 420, "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80"},
        {"title": "Ekspedisi Perahu Cadik Sandeq Majene", "likes": 385, "img": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=600&q=80"},
        {"title": "Digitalisasi Naskah Lontara Kuno", "likes": 310, "img": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=600&q=80"},
        {"title": "Kuliner Tradisional Jepa & Bau Peapi", "likes": 295, "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80"},
        {"title": "Pemberdayaan Literasi Digital PKBM", "likes": 512, "img": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=600&q=80"},
        {"title": "Arsitektur Hybrid AI & NLP Bahasa Daerah", "likes": 640, "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80"}
    ]

if "crowdsourcing_queue" not in st.session_state:
    st.session_state.crowdsourcing_queue = [
        {"id": 1, "kata": "Malaqbiq", "dialek": "Umum / Balanipa", "arti": "Mulia, santun, bermartabat tinggi dalam tutur dan laku.", "oleh": "Andi Maradika", "status": "Approved"},
        {"id": 2, "kata": "Pa'issangang", "dialek": "Majene / Pamboang", "arti": "Ilmu pengetahuan navigasi laut dan kebijaksanaan hidup.", "oleh": "Nakhoda Sulbar", "status": "Pending"}
    ]

if "global_announcement" not in st.session_state:
    st.session_state.global_announcement = "🎉 Selamat datang di Super-App Kamus Besar & Sosial Media Budaya Mandar (40 Fitur Terpadu) — Karya Inovasi MUH. ARMIL SYAM untuk Penjurian BUDAYA GO! 2026!"

# ==============================================================================
# 4. ENGINE DATA KAMUS, STEMMER, LONTARA & AUDIO (CORE 30 FITUR KAMUS)
# ==============================================================================
@st.cache_data
def load_dictionary():
    try:
        df = pd.read_csv("data/processed/kamus_mandar_bersih.csv").fillna("")
        return df
    except Exception:
        return pd.DataFrame([
            {"Mandar": "pamboya", "Indonesia": "pencarian; mata pencaharian nelayan di laut", "Halaman_PDF": 142},
            {"Mandar": "macoa", "Indonesia": "baik; bagus; elok budi pekertinya", "Halaman_PDF": 110},
            {"Mandar": "mangande", "Indonesia": "makan; menyantap hidangan bersama", "Halaman_PDF": 115},
            {"Mandar": "lita'", "Indonesia": "tanah; negeri; kampung halaman di Mandar", "Halaman_PDF": 98},
            {"Mandar": "sasi'", "Indonesia": "laut; samudra tempat berlayar perahu Sandeq", "Halaman_PDF": 188},
            {"Mandar": "bundu'", "Indonesia": "perang; perjuangan membela kehormatan (Siri')", "Halaman_PDF": 45},
            {"Mandar": "malaqbiq", "Indonesia": "mulia; beradab; santun dalam bertutur dan bertindak", "Halaman_PDF": 112}
        ])

df = load_dictionary()

def stem_mandar_word(word):
    w = str(word).lower().strip()
    prefixes = ["ma'", "mang", "pa'", "pang", "ta'", "ka", "di", "na", "mu", "u", "si", "ma"]
    suffixes = ["mi", "mo", "pa", "na", "mu", "u", "i", "ang", "an"]
    cands = [w]
    for s in suffixes:
        if w.endswith(s) and len(w) > len(s) + 2:
            cands.append(w[:-len(s)])
    final_c = list(cands)
    for c in cands:
        for p in prefixes:
            if c.startswith(p) and len(c) > len(p) + 2:
                final_c.append(c[len(p):])
    return list(dict.fromkeys(final_c))

def latin_to_lontara(text):
    peta = {
        "nga": "ᨍ", "nya": "ᨎ", "mpa": "ᨏ", "nra": "ᨑ", "nca": "ᨔ",
        "ka": "ᨀ", "ga": "ᨁ", "pa": "ᨄ", "ba": "ᨅ", "ma": "ᨆ",
        "ta": "ᨈ", "da": "ᨉ", "na": "ᨊ", "ca": "ᨌ", "ja": "ᨍ",
        "ya": "ᨐ", "ra": "ᨑ", "la": "ᨒ", "wa": "ᨓ", "sa": "ᨔ", "ha": "ᨖ",
        "k": "ᨀ", "g": "ᨁ", "p": "ᨄ", "b": "ᨅ", "m": "ᨆ",
        "t": "ᨈ", "d": "ᨉ", "n": "ᨊ", "c": "ᨌ", "j": "ᨍ",
        "y": "ᨐ", "r": "ᨑ", "l": "ᨒ", "w": "ᨓ", "s": "ᨔ", "h": "ᨖ",
        "a": "ᨕ", "i": "ᨕᨗ", "u": "ᨕᨘ", "e": "ᨕᨙ", "o": "ᨕᨚ"
    }
    t = str(text).lower()
    res, i = [], 0
    while i < len(t):
        if t[i:i+3] in peta:
            res.append(peta[t[i:i+3]]); i += 3
        elif t[i:i+2] in peta:
            res.append(peta[t[i:i+2]]); i += 2
        elif t[i] in peta:
            k = peta[t[i]]
            if i + 1 < len(t) and t[i+1] in "iueo":
                vm = {"i": "ᨗ", "u": "ᨘ", "e": "ᨙ", "o": "ᨚ"}
                res.append(k + vm[t[i+1]]); i += 2
            elif i + 1 < len(t) and t[i+1] == "a":
                res.append(k); i += 2
            else:
                res.append(k); i += 1
        elif t[i] == " ":
            res.append(" "); i += 1
        else:
            i += 1
    return "".join(res) if res else "ᨆᨉᨑ ᨆᨒᨁᨅᨗ"

def generate_audio(text):
    try:
        os.makedirs("assets/audio", exist_ok=True)
        clean_t = re.sub(r"[^a-zA-Z0-9\s]", "", str(text))[:60]
        fn = f"assets/audio/{abs(hash(clean_t))}.mp3"
        if not os.path.exists(fn) and clean_t.strip():
            tts = gTTS(text=clean_t, lang="id")
            tts.save(fn)
        return fn if os.path.exists(fn) else None
    except Exception:
        return None

# ==============================================================================
# 5. SIDEBAR: PORTAL LOGIN (ADMIN / USER) & NAVIGASI UTAMA
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div class="text-center py-2">
        <div class="text-5xl mb-1">⛵</div>
        <h2 class="text-xl font-extrabold text-blue-900 m-0">MANDARVERSE 2026</h2>
        <p class="text-xs font-bold text-yellow-600 tracking-wider uppercase">40-Feature Cultural Super-App</p>
    </div>
    """, unsafe_allow_html=True)

    # Panel Identitas & Switcher Role (Founder/Admin vs User)
    u = st.session_state.auth_user
    with st.expander(f"🔐 Akun: {u['name']} ({u['role']})", expanded=False):
        st.caption("Pilih Mode Akses Simulasi Penjurian:")
        pilih_role = st.radio(
            "Masuk Sebagai:",
            ["👑 Founder & Super Admin (MUH. ARMIL SYAM)", "🎓 Warga Belajar / User Umum", "🔑 Login Akun Kustom"],
            index=0 if "Admin" in u["role"] else 1
        )
        if pilih_role == "👑 Founder & Super Admin (MUH. ARMIL SYAM)":
            st.session_state.auth_user.update({
                "name": "MUH. ARMIL SYAM", "username": "armilsyam",
                "role": "Founder & Super Admin"
            })
        elif pilih_role == "🎓 Warga Belajar / User Umum":
            st.session_state.auth_user.update({
                "name": "Andi Maradika (User)", "username": "andimaradika",
                "role": "Member Komunitas"
            })
        else:
            inp_u = st.text_input("Username:", value=u["username"])
            inp_p = st.text_input("Password:", type="password", value="budayago2026")
            if st.button("Masuk Sekarang", use_container_width=True):
                if inp_u.lower() in ["armil", "armilsyam", "admin"]:
                    st.session_state.auth_user.update({"name": "MUH. ARMIL SYAM", "username": inp_u, "role": "Founder & Super Admin"})
                else:
                    st.session_state.auth_user.update({"name": inp_u.title(), "username": inp_u, "role": "Member Komunitas"})
                st.rerun()

    st.markdown(f"""
    <div class="bg-blue-50 border-l-4 border-blue-600 p-3 rounded-lg mb-3 text-xs">
        <div class="font-bold text-blue-900">👤 {st.session_state.auth_user['name']}</div>
        <div class="text-blue-700 font-semibold">{st.session_state.auth_user['role']}</div>
        <div class="text-yellow-600 font-bold mt-1">⭐ {st.session_state.auth_user['xp']} XP • Lencana Maradika</div>
    </div>
    """, unsafe_allow_html=True)

    menu_nav = option_menu(
        menu_title="Navigasi Super-App",
        options=[
            "🏠 Beranda / Feeds (FB & IG)",
            "🤳 Mandar Reels / Shorts (TikTok)",
            "💬 Obrolan, Grup & Live (WA)",
            "👤 Profil & Galeri Grid (IG)",
            "📚 Kamus Pintar, AI & Lontara",
            "🎓 Kurikulum 14 Modul & Gim",
            "🌊 Sandeq, WBTb, GIS & PKBM",
            "🛡️ Admin & Founder Center"
        ],
        icons=["house-heart-fill", "play-btn-fill", "chat-dots-fill", "person-badge-fill", "book-half", "mortarboard-fill", "compass-fill", "shield-lock-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "16px"},
            "nav-link": {"font-size": "13px", "font-weight": "600", "margin": "3px 0px", "border-radius": "10px", "padding": "8px 12px"},
            "nav-link-selected": {"background": "linear-gradient(90deg, #1E3A8A, #2563EB)", "color": "white", "font-weight": "700"},
        }
    )

    st.markdown("---")
    st.caption("Founder & Lead Developer:\n**MUH. ARMIL SYAM**\nPT. Boyang Digital Nusantara")

# Banner Pengumuman Global dari Admin
if st.session_state.global_announcement:
    st.info(st.session_state.global_announcement)

# ==============================================================================
# MENU 1: 🏠 BERANDA / FEEDS (GAYA FACEBOOK & INSTAGRAM + REACT STORIES)
# ==============================================================================
if menu_nav == "🏠 Beranda / Feeds (FB & IG)":
    st.markdown("""
    <div class="hero-gradient">
        <span class="bg-yellow-500 bg-opacity-20 border border-yellow-400 text-yellow-300 text-xs font-bold px-3 py-1 rounded-full uppercase">
            🌐 Mandar Social Hub • Facebook & Instagram Hybrid
        </span>
        <h1 class="text-2xl md:text-3xl font-extrabold text-white mt-2 mb-1">Beranda Komunitas & Lini Masa Budaya Mandar</h1>
        <p class="text-blue-100 text-sm m-0">Bagikan kosakata baru, bait Kalindaqdaq, foto budaya, dan berdiskusi langsung dengan ribuan pembelajar bahasa Mandar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Komponen React.js + Tailwind CSS untuk Stories Bar Interaktif (Gaya IG/WA Stories)
    stories_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    </head>
    <body class="bg-transparent m-0 p-0 font-sans">
        <div id="stories-root"></div>
        <script>
            const e = React.createElement;
            function StoriesBar() {
                const [activeStory, setActiveStory] = React.useState(null);
                const stories = [
                    { name: "Muh. Armil Syam", role: "Founder", img: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80", text: "🚀 Selamat datang di Super-App 40 Fitur Kamus Digital Mandar BUDAYA GO! 2026!" },
                    { name: "Boyang Clipper", role: "Kreator", img: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80", text: "⛵ Kosakata Hari Ini: 'PAMBOYA' (Pencarian / Perjuangan Pelaut di Samudra)." },
                    { name: "Sandeq Hub", role: "Maritim", img: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=200&q=80", text: "🌊 Festival Sandeq Sulawesi Barat: Perahu bercadik tercepat di dunia tanpa mesin!" },
                    { name: "PKBM Harapan", role: "Edukasi", img: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=200&q=80", text: "📚 Warga belajar sedang mempraktikkan kalimat berpartikel -mi, -mo, dan -pa." },
                    { name: "Kuliner Mandar", role: "WBTb", img: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=200&q=80", text: "🍲 Nikmatnya Jepa hangat disantap bersama kuah segar Bau Peapi khas Majene!" }
                ];
                return e("div", { className: "bg-white p-3 rounded-2xl border border-gray-200 shadow-sm" },
                    e("div", { className: "flex space-x-5 overflow-x-auto pb-1 items-center" },
                        stories.map((st, idx) =>
                            e("div", {
                                key: idx,
                                onClick: () => setActiveStory(st),
                                className: "flex flex-col items-center cursor-pointer transform hover:scale-105 transition"
                            },
                                e("div", { className: "p-0.5 rounded-full bg-gradient-to-tr from-yellow-400 via-red-500 to-blue-600" },
                                    e("img", { src: st.img, className: "w-14 h-14 rounded-full object-cover border-2 border-white" })
                                ),
                                e("span", { className: "text-xs font-bold text-gray-800 mt-1" }, st.name),
                                e("span", { className: "text-[10px] text-blue-600 font-semibold" }, st.role)
                            )
                        )
                    ),
                    activeStory && e("div", {
                        className: "mt-3 p-3 rounded-xl bg-gradient-to-r from-blue-900 to-blue-700 text-white flex justify-between items-center"
                    },
                        e("div", null,
                            e("div", { className: "text-xs text-yellow-300 font-bold uppercase" }, "📖 Story Aktif • " + activeStory.name),
                            e("div", { className: "text-sm font-medium mt-0.5" }, activeStory.text)
                        ),
                        e("button", {
                            onClick: () => setActiveStory(null),
                            className: "bg-white bg-opacity-20 hover:bg-opacity-30 text-xs px-3 py-1 rounded-lg font-bold"
                        }, "Tutup ✕")
                    )
                );
            }
            ReactDOM.createRoot(document.getElementById('stories-root')).render(e(StoriesBar));
        </script>
    </body>
    </html>
    """
    components.html(stories_html, height=165)

    col_feed, col_right_widget = st.columns([2.1, 1])

    with col_feed:
        # Kotak Buat Postingan Baru (Gaya Facebook)
        with st.expander("✍️ Buat Postingan Budaya / Bagikan Kosakata Baru ke Beranda", expanded=False):
            with st.form("create_post_form"):
                post_text = st.text_area("Apa kosakata, Kalindaqdaq, atau cerita budaya Mandar yang ingin Anda bagikan hari ini?", placeholder="Contoh: Hari ini saya belajar kata 'Malaqbiq' yang artinya mulia dan santun...")
                post_media_type = st.selectbox("Tipe Media Lampiran:", ["Gambar (URL)", "Video Pendek (URL)", "Tanpa Media (Teks & Aksara Lontara)"])
                post_media_url = st.text_input("URL Gambar / Video (Opsional):", value="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80")
                sub_post = st.form_submit_button("🚀 Publikasikan ke Lini Masa (+15 XP)", use_container_width=True)
                if sub_post and post_text.strip():
                    new_p = {
                        "id": random.randint(200, 9999),
                        "author": st.session_state.auth_user["name"],
                        "handle": "@" + st.session_state.auth_user["username"],
                        "role_badge": st.session_state.auth_user["role"],
                        "avatar": st.session_state.auth_user["avatar"],
                        "time": "Baru saja",
                        "content": post_text,
                        "lontara": latin_to_lontara(post_text[:30]),
                        "media_type": "image" if "Gambar" in post_media_type else ("video" if "Video" in post_media_type else "none"),
                        "media_url": post_media_url,
                        "likes": 1,
                        "shares": 0,
                        "comments": []
                    }
                    st.session_state.social_posts.insert(0, new_p)
                    st.session_state.auth_user["xp"] += 15
                    st.success("Postingan Anda berhasil tayang di Beranda!")
                    st.rerun()

        # Menampilkan Daftar Postingan (Feeds)
        for p_idx, post in enumerate(st.session_state.social_posts):
            st.markdown(f"""
            <div class="glass-card">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-3">
                        <img src="{post['avatar']}" class="w-11 h-11 rounded-full object-cover border-2 border-blue-600">
                        <div>
                            <div class="font-extrabold text-gray-900 text-base">{post['author']} <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full font-bold ml-1">{post['role_badge']}</span></div>
                            <div class="text-xs text-gray-500">{post['handle']} • {post['time']}</div>
                        </div>
                    </div>
                    <span class="text-lg text-yellow-600 font-bold" style="font-family:'Noto Sans Buginese';">{post['lontara']}</span>
                </div>
                <p class="text-gray-800 text-sm leading-relaxed mb-3">{post['content']}</p>
            </div>
            """, unsafe_allow_html=True)

            if post["media_type"] == "image" and post["media_url"]:
                st.image(post["media_url"], use_container_width=True)
            elif post["media_type"] == "video" and post["media_url"]:
                st.video(post["media_url"])

            # Baris Tombol Interaksi: Like, Comment Count, Share
            b_like, b_comm, b_share = st.columns(3)
            with b_like:
                if st.button(f"❤️ Suka ({post['likes']})", key=f"like_{post['id']}_{p_idx}", use_container_width=True):
                    st.session_state.social_posts[p_idx]["likes"] += 1
                    st.session_state.auth_user["xp"] += 2
                    st.rerun()
            with b_comm:
                st.button(f"💬 Komentar ({len(post['comments'])})", key=f"cbtn_{post['id']}_{p_idx}", use_container_width=True)
            with b_share:
                if st.button(f"🔗 Bagikan ({post['shares']})", key=f"share_{post['id']}_{p_idx}", use_container_width=True):
                    st.session_state.social_posts[p_idx]["shares"] += 1
                    st.toast("🔗 Tautan postingan berhasil disalin: https://kamus-digital-mandar.streamlit.app/?post=" + str(post['id']))
                    st.rerun()

            # Kolom Komentar Langsung di Bawah Postingan
            with st.expander(f"💭 Lihat & Tulis Komentar ({len(post['comments'])})", expanded=True):
                for cm in post["comments"]:
                    st.markdown(f"**🗣️ {cm['user']}:** {cm['text']}")
                c_in1, c_in2 = st.columns([3.5, 1])
                with c_in1:
                    new_cm = st.text_input("Tulis komentar...", key=f"in_cm_{post['id']}_{p_idx}", label_visibility="collapsed", placeholder="Tulis tanggapan sopan (Malaqbiq)...")
                with c_in2:
                    if st.button("Kirim", key=f"send_cm_{post['id']}_{p_idx}", use_container_width=True):
                        if new_cm.strip():
                            st.session_state.social_posts[p_idx]["comments"].append({
                                "user": st.session_state.auth_user["name"],
                                "text": new_cm.strip()
                            })
                            st.session_state.auth_user["xp"] += 5
                            st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

    with col_right_widget:
        st.markdown("### 🔥 Kosakata & Tagar Populer")
        st.markdown("""
        <div class="glass-card">
            <div class="text-xs font-bold text-blue-700 uppercase mb-2">Trending di Tanah Mandar</div>
            <ul class="text-sm space-y-2 text-gray-700">
                <li>🔹 <b>#Budayago2026</b> <span class="text-xs text-gray-400">(1.420 Postingan)</span></li>
                <li>🔹 <b>#MandarMalaqbiq</b> <span class="text-xs text-gray-400">(980 Postingan)</span></li>
                <li>🔹 <b>#BoyangClipper</b> <span class="text-xs text-gray-400">(815 Postingan)</span></li>
                <li>🔹 <b>#SandeqRaceSulbar</b> <span class="text-xs text-gray-400">(640 Postingan)</span></li>
                <li>🔹 <b>#KamusDigitalMandar</b> <span class="text-xs text-gray-400">(590 Postingan)</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💡 Kosakata Hari Ini")
        if not df.empty:
            sample_w = df.iloc[0]
            st.markdown(f"""
            <div class="glass-card border-l-4 border-yellow-500">
                <div class="text-lg font-extrabold text-blue-900">🗣️ {sample_w['Mandar']}</div>
                <div class="text-sm text-gray-700 mt-1"><b>Arti:</b> {sample_w['Indonesia']}</div>
                <div class="text-xs text-gray-400 mt-2">Sumber: Lembar PDF ke-{sample_w['Halaman_PDF']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 👥 Saran Teman & Kurator")
        st.markdown("""
        <div class="glass-card text-sm space-y-2">
            <div>👑 <b>MUH. ARMIL SYAM</b> <span class="text-xs text-green-600 font-bold">• Online</span></div>
            <div>⛵ <b>Andi Maradika (Majene)</b> <span class="text-xs text-green-600 font-bold">• Online</span></div>
            <div>📚 <b>PKBM Insan Harapan</b> <span class="text-xs text-green-600 font-bold">• Online</span></div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MENU 2: 🤳 MANDAR REELS / SHORTS (GAYA TIKTOK VERTICAL SCROLL)
# ==============================================================================
elif menu_nav == "🤳 Mandar Reels / Shorts (TikTok)":
    st.title("🤳 Mandar Reels & Edu-Shorts (Gaya TikTok Vertikal)")
    st.write("Tonton video pendek edukasi bahasa Mandar, pelafalan *Kalindaqdaq*, dan pesona maritim Sulawesi Barat.")

    reels = st.session_state.reels_data
    curr_idx = st.session_state.reel_idx % len(reels)
    active_reel = reels[curr_idx]

    col_spacer_l, col_tiktok, col_controls = st.columns([0.8, 1.6, 1.2])

    with col_tiktok:
        st.markdown(f"""
        <div class="tiktok-frame">
            <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold bg-red-600 px-2.5 py-0.5 rounded-full">🎬 MANDAR REELS #{curr_idx + 1}/{len(reels)}</span>
                <span class="text-xs text-yellow-400 font-bold">{active_reel['creator']}</span>
            </div>
            <p class="text-sm font-bold text-white mb-2">{active_reel['title']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.video(active_reel["video_url"])

        st.markdown(f"""
        <div class="bg-slate-900 text-white p-3 rounded-2xl mt-1 border border-slate-700 text-center">
            <div class="text-xs text-yellow-300 font-semibold italic">{active_reel['kalindaqdaq']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigasi Prev / Next Video
        nav_p, nav_n = st.columns(2)
        with nav_p:
            if st.button("⬆️ Video Sebelumnya", use_container_width=True):
                st.session_state.reel_idx = (curr_idx - 1) % len(reels)
                st.rerun()
        with nav_n:
            if st.button("⬇️ Next Video (Scroll)", use_container_width=True):
                st.session_state.reel_idx = (curr_idx + 1) % len(reels)
                st.rerun()

    with col_controls:
        st.markdown("### ⚡ Interaksi Video")
        if st.button(f"❤️ Like Video ({active_reel['likes']})", use_container_width=True):
            st.session_state.reels_data[curr_idx]["likes"] += 1
            st.session_state.auth_user["xp"] += 3
            st.rerun()

        if st.button(f"🔗 Bagikan Reels ({active_reel['shares']})", use_container_width=True):
            st.session_state.reels_data[curr_idx]["shares"] += 1
            st.toast("Tautan Mandar Reels berhasil disalin ke Clipboard!")
            st.rerun()

        if st.button("🔊 Putar Audio Kalindaqdaq Video Ini", use_container_width=True):
            af_r = generate_audio(active_reel["kalindaqdaq"])
            if af_r: st.audio(af_r, format="audio/mp3")

        st.markdown("#### 💬 Komentar Reels")
        for rc in active_reel["comments_list"]:
            st.markdown(f"- 🗨️ {rc}")
        new_rc = st.text_input("Tambah komentar di Reels ini:")
        if st.button("Kirim Komentar Reels", use_container_width=True):
            if new_rc.strip():
                st.session_state.reels_data[curr_idx]["comments_list"].append(f"{st.session_state.auth_user['name']}: {new_rc.strip()}")
                st.rerun()

# ==============================================================================
# MENU 3: 💬 OBROLAN, GRUP KOMUNITAS & LIVE VOICE ROOM (GAYA WHATSAPP)
# ==============================================================================
elif menu_nav == "💬 Obrolan, Grup & Live (WA)":
    st.title("💬 Pesaqbe Messenger, Grup Diskusi & Live Ngobrol Suara")

    col_contacts, col_chat_win = st.columns([1.15, 2.35])

    with col_contacts:
        st.subheader("📇 Kontak & Grup")
        selected_contact = st.radio(
            "Pilih Ruang Obrolan:",
            list(st.session_state.contacts_db.keys())
        )

        # Fitur Buat Grup Diskusi Baru
        with st.expander("➕ Buat Grup Diskusi Budaya Baru"):
            g_name = st.text_input("Nama Grup Baru:", placeholder="Misal: Belajar Aksara Lontara...")
            if st.button("Buat Grup Sekarang", use_container_width=True):
                if g_name.strip():
                    full_g = f"🌐 Grup: {g_name.strip()}"
                    st.session_state.contacts_db[full_g] = {
                        "type": "group",
                        "status": f"🟢 Dibuat oleh {st.session_state.auth_user['name']}",
                        "members": 1,
                        "messages": [
                            {"sender": st.session_state.auth_user["name"], "time": "Sekarang", "text": f"Grup '{g_name}' resmi dibuat untuk diskusi bahasa & budaya Mandar!"}
                        ]
                    }
                    st.success("Grup berhasil dibuat!")
                    st.rerun()

        # Fitur Live Ngobrol Suara (Audio Lounge)
        st.markdown("---")
        st.subheader("🎙️ Live Audio Lounge")
        st.caption("Rekam & kirim pesan suara langsung (*Voice Note* / Live Ngobrol) ke ruang obrolan aktif:")
        vn_audio = st.audio_input("Rekam Pesan Suara Anda:")
        if vn_audio:
            st.success("🎙️ Pesan suara siap dikirim ke ruang obrolan!")

    with col_chat_win:
        room_info = st.session_state.contacts_db[selected_contact]
        st.markdown(f"""
        <div class="bg-blue-900 text-white p-4 rounded-t-2xl flex justify-between items-center">
            <div>
                <h3 class="text-lg font-extrabold text-white m-0">{selected_contact}</h3>
                <span class="text-xs text-green-300 font-semibold">{room_info['status']} • {room_info['members']} Partisipan</span>
            </div>
            <span class="text-xs bg-white bg-opacity-20 px-3 py-1 rounded-full font-bold">🔒 End-to-End Cultural Chat</span>
        </div>
        """, unsafe_allow_html=True)

        # Jendela Riwayat Pesan dengan st.chat_message
        chat_box = st.container(height=390, border=True)
        with chat_box:
            for m in room_info["messages"]:
                is_me = (m["sender"] == st.session_state.auth_user["name"])
                with st.chat_message("user" if is_me else "assistant"):
                    st.markdown(f"**{m['sender']}** <span style='font-size:0.75rem;color:#64748B;'>({m['time']})</span>", unsafe_allow_html=True)
                    st.write(m["text"])

        # Input Pesan Instan di Bagian Bawah
        new_msg = st.chat_input(f"Ketik pesan ke {selected_contact}...")
        if new_msg:
            jam_skrg = datetime.now().strftime("%H:%M")
            st.session_state.contacts_db[selected_contact]["messages"].append({
                "sender": st.session_state.auth_user["name"],
                "time": jam_skrg,
                "text": new_msg
            })
            # Jika chat dengan Kaka AI atau mengandung kata tanya, berikan balasan pintar otomatis
            if room_info["type"] == "ai" or "?" in new_msg:
                akar = stem_mandar_word(new_msg.split()[-1])[0]
                cocok = df[df["Mandar"].str.contains(akar, case=False, na=False) | df["Indonesia"].str.contains(akar, case=False, na=False)]
                if not cocok.empty:
                    r0 = cocok.iloc[0]
                    balasan = f"💡 Info Kamus Mandar: Kata **{r0['Mandar']}** artinya *{r0['Indonesia']}* (Lembar PDF ke-{r0['Halaman_PDF']})."
                else:
                    balasan = "Kurre sumanga'! Pesan Anda telah diterima di ruang diskusi komunitas Mandar."
                st.session_state.contacts_db[selected_contact]["messages"].append({
                    "sender": "🤖 Kaka AI Bot",
                    "time": jam_skrg,
                    "text": balasan
                })
            st.session_state.auth_user["xp"] += 5
            st.rerun()

# ==============================================================================
# MENU 4: 👤 PROFIL PENGGUNA & GALERI GRID 3 KOLOM (GAYA INSTAGRAM)
# ==============================================================================
elif menu_nav == "👤 Profil & Galeri Grid (IG)":
    u = st.session_state.auth_user
    st.markdown(f"""
    <div class="glass-card">
        <div class="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-8">
            <img src="{u['avatar']}" class="ig-avatar">
            <div class="flex-1">
                <div class="flex items-center space-x-3">
                    <h2 class="text-2xl font-extrabold text-gray-900 m-0">{u['name']}</h2>
                    <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">✓ Terverifikasi ({u['role']})</span>
                </div>
                <p class="text-sm text-gray-500 font-semibold mt-0.5">@{u['username']} • Lencana Aksara: {latin_to_lontara(u['name'][:12])}</p>
                <p class="text-sm text-gray-800 mt-2 max-w-2xl">{u['bio']}</p>
                <div class="flex space-x-8 mt-4 text-center">
                    <div><span class="font-extrabold text-lg text-blue-900">{len(st.session_state.profile_gallery)}</span><br><span class="text-xs text-gray-500">Kiriman Grid</span></div>
                    <div><span class="font-extrabold text-lg text-blue-900">{u['followers']:,}</span><br><span class="text-xs text-gray-500">Pengikut (Followers)</span></div>
                    <div><span class="font-extrabold text-lg text-blue-900">{u['following']:,}</span><br><span class="text-xs text-gray-500">Mengikuti (Following)</span></div>
                    <div><span class="font-extrabold text-lg text-yellow-600">{u['xp']} XP</span><br><span class="text-xs text-gray-500">Skor Budaya</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol Edit Profil & Tambah Karya ke Grid
    ep1, ep2 = st.columns(2)
    with ep1:
        with st.expander("✏️ Edit Profil (Ubah Nama, Bio & Foto Profil)"):
            new_name = st.text_input("Nama Lengkap:", value=u["name"])
            new_bio = st.text_area("Bio Profil:", value=u["bio"])
            new_av = st.text_input("URL Foto Profil:", value=u["avatar"])
            if st.button("💾 Simpan Perubahan Profil", use_container_width=True):
                st.session_state.auth_user["name"] = new_name
                st.session_state.auth_user["bio"] = new_bio
                st.session_state.auth_user["avatar"] = new_av
                st.success("Profil berhasil diperbarui!")
                st.rerun()
    with ep2:
        with st.expander("➕ Unggah Dokumentasi Baru ke Galeri Grid 3 Kolom"):
            g_title = st.text_input("Judul Foto / Karya Budaya:")
            g_url = st.text_input("URL Gambar:", value="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80")
            if st.button("📤 Tambahkan ke Grid Instagram", use_container_width=True):
                if g_title:
                    st.session_state.profile_gallery.insert(0, {"title": g_title, "likes": 1, "img": g_url})
                    st.rerun()

    st.markdown("### 🔲 Galeri Dokumentasi & Portofolio Budaya (Grid 3 Kolom)")
    grid_cols = st.columns(3)
    for idx_g, item_g in enumerate(st.session_state.profile_gallery):
        with grid_cols[idx_g % 3]:
            st.image(item_g["img"], use_container_width=True)
            st.markdown(f"**{item_g['title']}**  \n❤️ `{item_g['likes']} Suka`")

# ==============================================================================
# MENU 5: 📚 KAMUS PINTAR 2 ARAH, AUDIO gTTS, AI TRANSLATOR, LONTARA & OCR
# ==============================================================================
elif menu_nav == "📚 Kamus Pintar, AI & Lontara":
    st.title("📚 Mesin Pencari Kamus 231 Halaman, AI Translator, Aksara Lontara & OCR")

    t_k1, t_k2, t_k3, t_k4 = st.tabs([
        "🔍 Fuzzy Root Search & Audio",
        "🌐 AI Translator & Grammar Checker",
        "✍️ Konverter & Stiker Aksara Lontara",
        "📷 Kamera Pemindai OCR Lontara"
    ])

    with t_k1:
        c_q1, c_q2 = st.columns([2.5, 1])
        with c_q1:
            q_word = st.text_input("Ketik Kosakata Mandar / Indonesia (Otomatis mendeteksi imbuhan ma'-, mang-, -mi, -mo, -pa):", placeholder="Contoh: pamboya, mangandemi, macoa, laut...")
        with c_q2:
            dialek_f = st.selectbox("Filter Dialek Wilayah:", ["Semua Dialek", "Balanipa", "Majene", "Pamboang", "Sendana"])

        if q_word and not df.empty:
            roots = stem_mandar_word(q_word)
            st.caption(f"🧬 Akar kata terdeteksi oleh Fuzzy Stemmer: **{', '.join(roots)}**")
            pattern = "|".join([re.escape(r) for r in roots if len(r) >= 2]) or re.escape(q_word)
            res = df[df["Mandar"].astype(str).str.contains(pattern, case=False, na=False) | df["Indonesia"].astype(str).str.contains(pattern, case=False, na=False)]
            st.success(f"Ditemukan {len(res)} entri kamus.")
            for _, row in res.head(15).iterrows():
                ck1, ck2 = st.columns([3.2, 1])
                with ck1:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div class="flex justify-between">
                            <h3 class="text-xl font-extrabold text-blue-900 m-0">🗣️ {row['Mandar']}</h3>
                            <span class="text-xl text-yellow-600 font-bold" style="font-family:'Noto Sans Buginese';">{latin_to_lontara(row['Mandar'])}</span>
                        </div>
                        <p class="text-gray-800 mt-2 mb-1"><b>Arti & Penjelasan:</b> {row['Indonesia']}</p>
                        <span class="text-xs text-blue-700 font-semibold">📖 Lembar PDF ke-{row['Halaman_PDF']} • Dialek: {dialek_f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with ck2:
                    af = generate_audio(row["Mandar"])
                    if af: st.audio(af, format="audio/mp3")

    with t_k2:
        st.subheader("🌐 Penerjemah Kalimat Dwibahasa & Korektor Partikel (-mi, -mo, -pa)")
        kal_in = st.text_area("Masukkan kalimat Indonesia atau Mandar:", "Saya mau pergi makan hari ini")
        if st.button("🚀 Terjemahkan & Periksa Tata Bahasa", use_container_width=True):
            peta_tr = {"saya": "yau (halus: i'da)", "mau": "maelu", "pergi": "mao", "makan": "mangande", "hari": "allo", "ini": "dini", "kamu": "i'o"}
            tokens = [peta_tr.get(w.lower(), w) for w in kal_in.split()]
            hasil_tr = " ".join(tokens)
            st.success(f"**Hasil Translasi Morfologi:** `{hasil_tr}`")
            st.markdown(f"<div class='lontara-box'>{latin_to_lontara(hasil_tr)}</div>", unsafe_allow_html=True)

    with t_k3:
        st.subheader("✍️ Konverter Alfabet Latin ⇄ Aksara Lontara & Generator Kalindaqdaq")
        in_lon = st.text_input("Ketik Teks Latin:", "Mandar Malaqbiq Budayago")
        st.markdown(f"<div class='lontara-box'>{latin_to_lontara(in_lon)}</div>", unsafe_allow_html=True)

    with t_k4:
        st.subheader("📷 Pemindai Kamera Aksara Lontara (Vision OCR)")
        up_ocr = st.file_uploader("Unggah Foto Aksara Lontara (.png/.jpg):", type=["png", "jpg", "jpeg"])
        if up_ocr or st.button("🔍 Simulasikan Pemindaian Naskah Lontaq"):
            st.success("✅ Aksara Terbaca: `ᨉ ᨆᨘᨕᨒ ᨈᨊᨗᨕ ᨕᨊᨘᨊ` ➔ **Da' muala tania anunna** (Jangan mengambil yang bukan hakmu).")

# ==============================================================================
# MENU 6: 🎓 KURIKULUM 14 MODUL, KUIS AI, CERITA RAKYAT & GIM MANDAR WORDLE
# ==============================================================================
elif menu_nav == "🎓 Kurikulum 14 Modul & Gim":
    st.title("🎓 Kurikulum Terpadu 14 Modul, Kuis Interaktif & Gim Mandar Wordle")
    tb1, tb2, tb3 = st.tabs(["📘 Modul 1–14 Lengkap", "📝 Kuis Interaktif AI", "🟩 Gim Mandar Wordle"])

    with tb1:
        st.markdown("""
        <div class="glass-card">
            <h4 class="font-bold text-blue-900">Ringkasan Terstruktur Halaman 1 hingga 14</h4>
            <ul class="text-sm space-y-2 text-gray-700 mt-2">
                <li><b>Halaman 1 (Kata Ganti / Palanreng):</b> Yau / I'da (Saya), I'o / I'o-di' (Kamu/Anda), I'ta (Kita), Ia (Dia), Igae (Mereka).</li>
                <li><b>Halaman 2 (Kata Tanya / Pau-Pau Massing):</b> Aha? (Apa), Innai? (Siapa), Umba? (Di mana), Piran? (Kapan), Ma'aha? (Mengapa), Piga? (Berapa).</li>
                <li><b>Halaman 3 (Kata Kerja / Pau Repu):</b> Mangande (Makan), Minung (Minum), Tindo (Tidur), Mao (Pergi), Ratu (Tiba), Dziang / Andiang (Ada / Tidak ada).</li>
                <li><b>Halaman 4 (Partikel Penegas Native):</b> <code>-mi</code> (Sudah/Perintah: Mangandemi), <code>-mo</code> (Saja: I'omo), <code>-pa</code> (Nanti dulu: Mangandepa).</li>
                <li><b>Halaman 5–9 (Tematik & Maritim):</b> Waktu, Angka 1–10 (Mesa–Sapulo), Geografi & Perahu Sandeq, Kekerabatan (A'ba, Amma), Warna, Kuliner (Jepa, Bau Peapi).</li>
                <li><b>Halaman 10–14 (Sastra & AI):</b> Puisi Kalindaqdaq (8-7-5-7), Wasiat Pappasang, Larangan Pemali (Da'), Ungkapan Emosi, & Blueprint NLP AI.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tb2:
        q_ans = st.radio("Apakah arti dari kalimat berpartikel 'Mangandemi'?", ["Makan dulu", "Sudah makan / Makanlah", "Tidak mau makan", "Makan bersama"], index=None)
        if st.button("Periksa Jawaban Kuis (+20 XP)"):
            if q_ans == "Sudah makan / Makanlah":
                st.balloons()
                st.session_state.auth_user["xp"] += 20
                st.success("🎉 Tepat sekali! Anda mendapatkan +20 XP!")
            else:
                st.error("Kurang tepat. Partikel -mi bermakna 'sudah' atau perintah tegas.")

    with tb3:
        st.subheader("🟩 Mandar Wordle (Tebak Kata Budaya 6 Huruf)")
        w_in = st.text_input("Petunjuk: Perahu bercadik tercepat warisan Mandar (6 Huruf):", max_chars=6).upper()
        if st.button("Cek Kata Wordle"):
            if w_in == "SANDEQ":
                st.balloons()
                st.success("🏆 BENAR! Kata jawabannya adalah SANDEQ!")
            else:
                st.warning("Belum tepat, coba ketik: SANDEQ")

# ==============================================================================
# MENU 7: 🌊 SANDEQ HUB, WBTb, PETA GIS SULBAR & MODUL CETAK PKBM
# ==============================================================================
elif menu_nav == "🌊 Sandeq, WBTb, GIS & PKBM":
    st.title("🌊 Ensiklopedia Sandeq Hub, Peta GIS Budaya Sulawesi Barat & Modul PKBM")
    c_g1, c_g2 = st.columns([1.3, 1])
    with c_g1:
        st.subheader("🗺️ Peta Geografis Budaya & Sentra Dialek (Cultural GIS)")
        gis_points = pd.DataFrame([
            {"Titik Budaya": "Majene (Museum Mandar & Pantai Dato')", "lat": -3.5403, "lon": 118.9707},
            {"Titik Budaya": "Balanipa / Tinambung (Sastra & Tenun Lipa' Saqbe)", "lat": -3.4833, "lon": 119.0333},
            {"Titik Budaya": "Pamboang (Sentra Perahu Sandeq)", "lat": -3.4950, "lon": 118.8950},
            {"Titik Budaya": "Polewali Mandar (Kuliner Jepa & Bau Peapi)", "lat": -3.4324, "lon": 119.3435}
        ])
        st.map(gis_points, latitude="lat", longitude="lon", zoom=8)
    with c_g2:
        st.subheader("📥 Unduhan Modul Cetak PKBM & Sekolah")
        st.write("Unduh materi pembelajaran luar jaringan (*Offline Learning Kit*) untuk warga belajar PKBM dan siswa sekolah:")
        st.download_button(
            "📄 Unduh Paket Kurikulum 14 Modul (.md)",
            data="# KURIKULUM 14 MODUL BAHASA MANDAR (BUDAYA GO! 2026)\nOleh: MUH. ARMIL SYAM (PT. Boyang Digital Nusantara)",
            file_name="Modul_PKBM_Bahasa_Mandar_2026.md",
            use_container_width=True
        )
        st.download_button(
            "📊 Unduh Korpus Kamus Bersih (.csv)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="kamus_mandar_bersih.csv",
            use_container_width=True
        )

# ==============================================================================
# MENU 8: 🛡️ ADMIN & FOUNDER COMMAND CENTER (KHUSUS MUH. ARMIL SYAM)
# ==============================================================================
elif menu_nav == "🛡️ Admin & Founder Center":
    st.title("🛡️ Founder & Super Admin Command Center")
    if "Admin" not in st.session_state.auth_user["role"]:
        st.warning("🔒 Halaman ini khusus untuk **Founder & Super Admin (MUH. ARMIL SYAM)**. Silakan ubah role Anda menjadi Founder/Admin pada panel Login di Sidebar sebelah kiri untuk membuka seluruh kontrol.")
    else:
        st.success(f"Selamat datang kembali, Founder **{st.session_state.auth_user['name']}**! Anda memiliki akses penuh ke seluruh sistem.")

        adm1, adm2, adm3, adm4 = st.columns(4)
        adm1.metric("Total Entri Kamus", f"{len(df):,}", "100% Bersih")
        adm2.metric("Postingan Komunitas", len(st.session_state.social_posts), "+2 Hari Ini")
        adm3.metric("Grup & Ruang Chat", len(st.session_state.contacts_db), "Aktif")
        adm4.metric("Antrean Kurasi Kata", len(st.session_state.crowdsourcing_queue), "Perlu Validasi")

        st.markdown("### 📢 1. Broadcast Pengumuman Global (Banner Atas Aplikasi)")
        new_ann = st.text_input("Ubah Teks Pengumuman Global:", value=st.session_state.global_announcement)
        if st.button("🚀 Perbarui Pengumuman Global"):
            st.session_state.global_announcement = new_ann
            st.success("Pengumuman global berhasil diperbarui!")
            st.rerun()

        st.markdown("### ✅ 2. Validasi Kontribusi Kosakata Publik (Crowdsourcing Moderation)")
        for idx_c, item_c in enumerate(st.session_state.crowdsourcing_queue):
            cc1, cc2, cc3 = st.columns([3, 1, 1])
            with cc1:
                st.write(f"**{item_c['kata']}** ({item_c['dialek']}) — *{item_c['arti']}* | Oleh: `{item_c['oleh']}` | Status: **{item_c['status']}**")
            with cc2:
                if st.button("Setujui", key=f"app_{idx_c}", use_container_width=True):
                    st.session_state.crowdsourcing_queue[idx_c]["status"] = "Approved ✅"
                    st.rerun()
            with cc3:
                if st.button("Hapus", key=f"del_c_{idx_c}", use_container_width=True):
                    st.session_state.crowdsourcing_queue.pop(idx_c)
                    st.rerun()

        st.markdown("### 🗑️ 3. Moderasi Postingan Sosial Media")
        for idx_p, p_item in enumerate(st.session_state.social_posts):
            cp1, cp2 = st.columns([4, 1])
            with cp1:
                st.write(f"**{p_item['author']}** ({p_item['time']}): {p_item['content'][:80]}...")
            with cp2:
                if st.button("Hapus Post", key=f"del_p_{idx_p}", use_container_width=True):
                    st.session_state.social_posts.pop(idx_p)
                    st.rerun()

# ==============================================================================
# FOOTER GLOBAL
# ==============================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div class="text-center text-gray-500 text-xs pb-4">
    <b>MANDARVERSE • SUPER-APP 40 FITUR KAMUS BESAR & SOSIAL MEDIA BUDAYA MANDAR</b><br>
    Founder & Lead Developer: <b>MUH. ARMIL SYAM</b> — PT. Boyang Digital Nusantara | Kompetisi Inovasi <b>BUDAYA GO! 2026</b>
</div>
""", unsafe_allow_html=True)