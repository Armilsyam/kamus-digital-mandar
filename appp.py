import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import os

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Kamus & Edukasi Digital Mandar", 
    page_icon="⛵", 
    layout="wide",
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
# 3. FUNGSI AUDIO PELAFALAN (TTS - TEXT TO SPEECH)
# ==========================================
def generate_audio(text, lang='id'):
    try:
        # Membuat folder audio sementara jika belum ada
        os.makedirs("assets/audio", exist_ok=True)
        filename = f"assets/audio/{hash(text)}.mp3"
        if not os.path.exists(filename):
            # Menggunakan gTTS untuk melafalkan teks
            tts = gTTS(text=text, lang='id') # Mendukung pelafalan fonetis
            tts.save(filename)
        return filename
    except Exception as e:
        return None

# ==========================================
# 4. NAVIGASI SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### ⛵ BUDAYA GO! 2026")
    st.markdown("**Kamus Digital Mandar Interaktif**")
    st.markdown("---")
    
    menu_pilihan = st.radio(
        "Pilar Fitur Utama:",
        [
            "🔍 Pencarian Pintar & Audio",
            "📜 Kalindaqdaq & Konteks Budaya",
            "🎓 Kurikulum 14 Modul",
            "🎮 Arena Kuis & Simulasi"
        ]
    )
    
    st.markdown("---")
    st.caption("Dikembangkan oleh Muh. Armil Syam")
    st.caption("PT. Boyang Digital Nusantara")

# ==========================================
# 5. KONTEN APLIKASI BERDASARKAN MENU
# ==========================================

# ------------------------------------------
# MENU 1: PENCARIAN PINTAR & AUDIO PELAFALAN
# ------------------------------------------
if menu_pilihan == "🔍 Pencarian Pintar & Audio":
    st.title("🔍 Mesin Pencari Pintar (Fuzzy & Audio Pelafalan)")
    st.markdown("Ketik kata dalam bahasa Mandar atau Indonesia. Sistem akan mendeteksi kata berimbuhan secara otomatis dan menyediakan tombol audio pelafalan 🔊.")
    
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_query = st.text_input("Cari Kosakata:", placeholder="Contoh: pamboya, mangande, makan, lita...")
    with col_s2:
        arah_cari = st.selectbox("Arah Terjemahan:", ["Dua Arah (Mandar ⇄ Indo)", "Hanya Mandar", "Hanya Indonesia"])

    if search_query:
        if df.empty:
            st.error("Data kamus belum dimuat.")
        else:
            # Logika Pencarian Pintar (Fuzzy / Partial Matching)
            q = search_query.strip()
            if arah_cari == "Hanya Mandar":
                hasil = df[df['Mandar'].str.contains(q, case=False, na=False)]
            elif arah_cari == "Hanya Indonesia":
                hasil = df[df['Indonesia'].str.contains(q, case=False, na=False)]
            else:
                m_mandar = df['Mandar'].str.contains(q, case=False, na=False)
                m_indo = df['Indonesia'].str.contains(q, case=False, na=False)
                hasil = df[m_mandar | m_indo]

            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} entri yang cocok dengan kata kunci '{search_query}'")
                st.markdown("---")
                
                # Menampilkan maksimal 20 hasil teratas agar halaman tetap ringan
                for index, row in hasil.head(20).iterrows():
                    with st.container():
                        c_w, c_a = st.columns([4, 1])
                        with c_w:
                            st.markdown(f"### 🗣️ {row['Mandar']}")
                            st.write(f"**Arti / Terjemahan:** {row['Indonesia']}")
                            st.caption(f"📁 Sumber: Lembar PDF ke-{row['Halaman_PDF']}")
                        with c_a:
                            # Tombol Audio Pelafalan Otomatis (Multimedia Wajib)
                            audio_file = generate_audio(row['Mandar'])
                            if audio_file and os.path.exists(audio_file):
                                st.audio(audio_file, format='audio/mp3')
                        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
            else:
                st.warning(f"Kata '{search_query}' belum ditemukan. Coba gunakan kata dasar lainnya.")

# ------------------------------------------
# MENU 2: KALINDAQDAQ & KONTEKS BUDAYA
# ------------------------------------------
elif menu_pilihan == "📜 Kalindaqdaq & Konteks Budaya":
    st.title("📜 Integrasi Sastra Lisan (Kalindaqdaq) & Budaya")
    st.markdown("Pewarisan nilai leluhur suku Mandar melalui bait puisi tradisional dan konteks budaya maritim.")
    
    st.info("💡 **Keunggulan Digital:** Setiap entri budaya dilengkapi dengan bait sastra lisan *Kalindaqdaq* sebagai contoh penggunaan dalam konteks adat.")

    # Contoh Entri Budaya Unggulan dengan Kalindaqdaq
    entri_budaya = [
        {
            "kata": "Sandeq",
            "arti": "Perahu cadik tradisional suku Mandar yang dikenal sebagai perahu tercepat di perairan nusantara tanpa mesin.",
            "konteks": "Simbol ketangguhan pelaut Mandar mengarungi Laut Banda dan Selat Makassar.",
            "kalindaqdaq": "\"Sallangngi sasi', mitai batu karang\" (Mengarungi samudra luas, menghadapi batu karang — melambangkan keberanian nakhoda)."
        },
        {
            "kata": "Bau Peapi",
            "arti": "Kuliner khas Mandar berupa olahan ikan segar berkuah asam kunyit dengan minyak kelapa murni.",
            "konteks": "Hidangan utama dalamjamuan adat dan perhelatan keluarga besar di pesisir Majene dan Polewali Mandar.",
            "kalindaqdaq": "\"Malaqbiq pa'mai'na, tau maradika di parola\" (Hati yang mulia, menjamu tamu dengan setulus hidangan bahari)."
        },
        {
            "kata": "Pappasang",
            "arti": "Wasiat atau pesan moral leluhur Mandar yang diturunkan secara turun-temurun.",
            "konteks": "Landasan etika hidup bermasyarakat berdasarkan prinsip Malaqbiq (bermartabat).",
            "kalindaqdaq": "\"Da' muala tania anunna\" (Jangan pernah mengambil sesuatu yang bukan hakmu — prinsip kejujuran mutlak)."
        }
    ]

    for item in entri_budaya:
        with st.expander(f"🌟 Entri Budaya: {item['kata']}"):
            st.write(f"**Definisi:** {item['arti']}")
            st.write(f"**Konteks Adat:** {item['konteks']}")
            st.success(f"📜 **Contoh Kalindaqdaq:** {item['kalindaqdaq']}")
            
            # Tombol Audio untuk Kalindaqdaq
            if st.button(f"🔊 Putar Pelafalan Kalindaqdaq ({item['kata']})", key=item['kata']):
                af = generate_audio(item['kalindaqdaq'])
                if af and os.path.exists(af):
                    st.audio(af, format='audio/mp3')

# ------------------------------------------
# MENU 3: KURIKULUM 14 MODUL
# ------------------------------------------
elif menu_pilihan == "🎓 Kurikulum 14 Modul":
    st.title("🎓 Kurikulum Terpadu Bahasa Mandar (Halaman 1–14)")
    st.write("Materi pembelajaran terstruktur untuk menguasai tata bahasa dan struktur kalimat.")
    
    tab1, tab2, tab3 = st.tabs(["Sapaan & Kata Ganti", "Rumus Partikel (-mi, -mo)", "Kosakata & Sastra"])
    with tab1:
        st.subheader("🗣️ Halaman 1-3: Sapaan & Kata Kerja")
        st.write("- **Saya:** `Yau` (biasa) / `I'da` (halus)")
        st.write("- **Kamu:** `I'o` (akrab) / `I'o-mu` (sopan)")
        st.write("- **Makan/Minum:** `Mangande` / `Minung`")
    with tab2:
        st.subheader("🔗 Halaman 4: Partikel Native Mandar")
        st.success("📝 **-mi** (Sudah/Perintah): *Mangandemi* (Sudah makan)")
        st.warning("📝 **-mo** (Saja/Pilihan): *I'omo* (Kamu saja)")
    with tab3:
        st.subheader("🌟 Halaman 5-14: Budaya & NLP")
        format_teks = "Mencakup sistem bilangan, geografi maritim (Sandeq), kuliner tradisional, Kalindaqdaq, hingga blueprint kecerdasan buatan (NLP)."
        st.write(format_teks)

# ------------------------------------------
# MENU 4: ARENA KUIS & SIMULASI
# ------------------------------------------
elif menu_pilihan == "Arena Kuis & Simulasi":
    st.title("🎮 Arena Kuis Kosakata & Pelafalan")
    st.write("Uji kemampuan kosakata Mandar Anda secara interaktif.")
    if not df.empty:
        if 'kuis_item' not in st.session_state:
            st.session_state.kuis_item = df.sample(n=1).iloc[0]
        ki = st.session_state.kuis_item
        
        st.markdown(f"### Tebak Arti Kata: **{ki['Mandar']}**")
        with st.expander("👀 Lihat Kunci Jawaban & Audio"):
            st.success(f"**Arti:** {ki['Indonesia']}")
            audio_k = generate_audio(ki['Mandar'])
            if audio_k:
                st.audio(audio_k, format='audio/mp3')
        if st.button("🔄 Soal Berikutnya"):
            st.session_state.kuis_item = df.sample(n=1).iloc[0]
            st.rerun()

# Footer Global
st.markdown("<br><hr><center><p style='color:#64748B; font-size:0.85rem;'>© 2026 MUH. ARMIL SYAM — BUDAYA GO! 2026</p></center>", unsafe_allow_html=True)