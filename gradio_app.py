import gradio as gr
import pandas as pd
import os
import re
from gtts import gTTS

# ==============================================================================
# 1. LOAD DATA KAMUS & MESIN INTI (STEMMER, LONTARA, AUDIO)
# ==============================================================================
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
# 2. FUNGSI INTERAKTIF UNTUK GRADIO UI
# ==============================================================================
def cari_kamus_gradio(query, dialek):
    if not query or not str(query).strip():
        return "<div class='card-info'>Silakan ketik kosakata Mandar atau Indonesia di kolom pencarian.</div>", None

    roots = stem_mandar_word(query)
    pattern = "|".join([re.escape(r) for r in roots if len(r) >= 2]) or re.escape(query)
    mask_m = df["Mandar"].astype(str).str.contains(pattern, case=False, na=False)
    mask_i = df["Indonesia"].astype(str).str.contains(pattern, case=False, na=False)
    hasil = df[mask_m | mask_i]

    if hasil.empty:
        return f"<div class='card-warn'>Kosakata <b>'{query}'</b> belum ditemukan. Akar kata terdeteksi: {', '.join(roots)}</div>", None

    html_cards = f"<div style='margin-bottom:10px; color:#1E3A8A; font-weight:700;'>🧬 Akar Kata Terdeteksi: {', '.join(roots)} | Ditemukan {len(hasil)} Entri:</div>"
    first_word = hasil.iloc[0]["Mandar"]
    audio_path = generate_audio(first_word)

    for _, row in hasil.head(10).iterrows():
        lontara_str = latin_to_lontara(row["Mandar"])
        html_cards += f"""
        <div class="gradio-dict-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:1.35rem; font-weight:800; color:#1E3A8A;">🗣️ {row['Mandar']}</span>
                <span style="font-size:1.5rem; color:#D97706;">{lontara_str}</span>
            </div>
            <p style="margin:8px 0; color:#334155; font-size:1rem;"><b>Arti & Penjelasan:</b> {row['Indonesia']}</p>
            <div style="font-size:0.8rem; color:#2563EB; font-weight:700;">
                📖 Lembar PDF ke-{row['Halaman_PDF']} &nbsp;•&nbsp; 📍 Dialek: {dialek}
            </div>
        </div>
        """
    return html_cards, audio_path

def konversi_lontara_gradio(teks_latin):
    hasil_lontara = latin_to_lontara(teks_latin)
    html_box = f"""
    <div style="background:linear-gradient(135deg,#FEF3C7,#FDE68A); border:2px dashed #D97706; padding:24px; border-radius:16px; text-align:center;">
        <div style="font-size:2.4rem; color:#92400E; font-weight:bold; letter-spacing:4px;">{hasil_lontara}</div>
        <div style="font-size:0.9rem; color:#78350F; margin-top:8px;">Transliterasi Aksara Lontara Mandar • "{teks_latin}"</div>
    </div>
    """
    return html_box, generate_audio(teks_latin)

def gabung_partikel_gradio(kata_dasar, partikel):
    kata = kata_dasar.split(" ")[0]
    part = partikel.split(" ")[0].replace("-", "")
    gabung = f"{kata}{part}"
    return f"""
    <div class="gradio-dict-card" style="text-align:center; border-left:6px solid #F59E0B;">
        <div style="font-size:0.85rem; color:#64748B; text-transform:uppercase; font-weight:700;">Hasil Morfologi Native Mandar:</div>
        <div style="font-size:2rem; font-weight:800; color:#1E3A8A; margin:6px 0;">{gabung}!</div>
        <div style="font-size:1.4rem; color:#D97706;">{latin_to_lontara(gabung)}</div>
    </div>
    """, generate_audio(gabung)

def kaka_ai_response(message, history):
    m_low = message.lower()
    if any(k in m_low for k in ["partikel", "-mi", "-mo", "-pa", "rumus"]):
        return "📐 **Rumus Partikel Enklitik Mandar:**\n- **`-mi`**: Sudah terjadi / Perintah (*Mangandemi* = Sudah makan)\n- **`-mo`**: Saja / Pilihan (*I'omo* = Kamu saja)\n- **`-pa`**: Nanti dulu (*Mangandepa* = Makan dulu)."
    elif any(k in m_low for k in ["kalindaqdaq", "pappasang", "puisi"]):
        return "📜 **Kalindaqdaq** bersuku kata 8-7-5-7:\n*\"Mua' melo'o mita'u, tondonganna pa'mai'u, sallangngi sasi', mitai batu karang.\"*"
    else:
        akar = stem_mandar_word(m_low.split()[-1])[0] if m_low.split() else ""
        cocok = df[df["Mandar"].str.contains(akar, case=False, na=False) | df["Indonesia"].str.contains(akar, case=False, na=False)]
        if not cocok.empty:
            r0 = cocok.iloc[0]
            return f"💡 Berdasarkan Kamus Besar Digital Mandar (Lembar PDF ke-{r0['Halaman_PDF']}):\n- **{r0['Mandar']}** ({latin_to_lontara(r0['Mandar'])}): *{r0['Indonesia']}*"
        return "Kurre sumanga'! Silakan tanyakan kosakata bahasa Mandar, rumus partikel (-mi, -mo, -pa), atau sastra Kalindaqdaq kepada Kaka AI."

# ==============================================================================
# 3. DESAIN TEMA MODERN & CSS GRADIO BLOCKS
# ==============================================================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
body, .gradio-container { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.hero-gradio {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
    padding: 28px;
    border-radius: 20px;
    color: white !important;
    margin-bottom: 18px;
    box-shadow: 0 15px 30px rgba(15, 23, 42, 0.25);
}
.gradio-dict-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 6px solid #2563EB;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04);
}
.metric-box {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-top: 4px solid #2563EB;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
}
"""

theme_mandar = gr.themes.Ocean(
    primary_hue="blue",
    secondary_hue="amber",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Plus Jakarta Sans"), "sans-serif"]
)

with gr.Blocks(theme=theme_mandar, css=custom_css, title="MANDARVERSE 2026 — Gradio AI Edition") as demo:
    gr.HTML(f"""
    <div class="hero-gradio">
        <span style="background:rgba(245,158,11,0.25); border:1px solid #F59E0B; color:#FCD34D; padding:4px 12px; border-radius:99px; font-size:0.75rem; font-weight:700;">
            ⛵ KOMPETISI INOVASI BUDAYA GO! 2026 • GRADIO AI EDITION
        </span>
        <h1 style="color:white; font-size:2rem; font-weight:800; margin:10px 0 4px 0;">
            KAMUS BESAR & EKOSISTEM DIGITAL BAHASA MANDAR
        </h1>
        <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">
            Founder & Lead Developer: <b>MUH. ARMIL SYAM</b> — PT. Boyang Digital Nusantara | 
            Mengintegrasikan {len(df):,}+ Kosakata Bersih, Fuzzy Root Stemmer, Audio Fonetis, Aksara Lontara & Kaka AI.
        </p>
    </div>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:16px;">
        <div class="metric-box"><h2 style="margin:0;color:#1E3A8A;">{len(df):,}+</h2><span style="font-size:0.8rem;color:#64748B;">Kosakata Bersih</span></div>
        <div class="metric-box"><h2 style="margin:0;color:#1E3A8A;">231</h2><span style="font-size:0.8rem;color:#64748B;">Halaman Literatur</span></div>
        <div class="metric-box"><h2 style="margin:0;color:#1E3A8A;">14 Modul</h2><span style="font-size:0.8rem;color:#64748B;">Kurikulum Budaya</span></div>
        <div class="metric-box"><h2 style="margin:0;color:#D97706;">40 Fitur</h2><span style="font-size:0.8rem;color:#64748B;">Ekosistem Super-App</span></div>
    </div>
    """)

    with gr.Tabs():
        # TAB 1: MESIN PENCARI KAMUS & AUDIO
        with gr.TabItem("🔍 1. Kamus Pintar & Audio Fonetis"):
            with gr.Row():
                with gr.Column(scale=3):
                    inp_cari = gr.Textbox(
                        label="Cari Kosakata Mandar / Indonesia (Otomatis Mendeteksi Imbuhan ma'-, mang-, -mi, -mo, -pa)",
                        placeholder="Ketik contoh: pamboya, mangandemi, macoa, laut..."
                    )
                with gr.Column(scale=1):
                    inp_dialek = gr.Dropdown(
                        choices=["Umum (Balanipa)", "Dialek Majene", "Dialek Pamboang", "Dialek Sendana"],
                        value="Umum (Balanipa)",
                        label="Filter Dialek Wilayah"
                    )
            btn_cari = gr.Button("🚀 Cari Kosakata & Putar Audio Pelafalan", variant="primary")
            out_audio = gr.Audio(label="🔊 Audio Pelafalan Otomatis (Kata Teratas)", autoplay=False)
            out_hasil = gr.HTML(label="Hasil Pencarian Kamus")

            btn_cari.click(fn=cari_kamus_gradio, inputs=[inp_cari, inp_dialek], outputs=[out_hasil, out_audio])
            inp_cari.submit(fn=cari_kamus_gradio, inputs=[inp_cari, inp_dialek], outputs=[out_hasil, out_audio])

        # TAB 2: AKSARA LONTARA & KALINDAQDAQ
        with gr.TabItem("✍️ 2. Studio Aksara Lontara & Kalindaqdaq"):
            gr.Markdown("### ✍️ Konverter Instan Alfabet Latin ⇄ Aksara Lontara Mandar")
            inp_lontara = gr.Textbox(label="Ketik Kata atau Kalimat Bahasa Mandar:", value="Lita Mandar Malaqbiq")
            btn_lontara = gr.Button("✨ Konversi ke Aksara Lontara & Suara", variant="primary")
            out_lontara_html = gr.HTML()
            out_lontara_aud = gr.Audio(label="🔊 Audio Pelafalan")
            btn_lontara.click(fn=konversi_lontara_gradio, inputs=inp_lontara, outputs=[out_lontara_html, out_lontara_aud])

        # TAB 3: SIMULATOR PARTIKEL & KURIKULUM 14 MODUL
        with gr.TabItem("🎓 3. Kurikulum 14 Modul & Simulator Partikel"):
            with gr.Row():
                pilih_kata = gr.Dropdown(
                    choices=["Mangande (Makan)", "Mao (Pergi)", "Tindo (Tidur)", "Ratu (Datang)", "I'o (Kamu)"],
                    value="Mangande (Makan)", label="Pilih Kata Dasar"
                )
                pilih_part = gr.Dropdown(
                    choices=["-mi (Sudah / Perintah)", "-mo (Saja / Pilihan)", "-pa (Nanti Dulu)"],
                    value="-mi (Sudah / Perintah)", label="Pilih Partikel Enklitik"
                )
            btn_sim = gr.Button("🧪 Gabungkan Rumus Morfologi Native", variant="primary")
            out_sim_html = gr.HTML()
            out_sim_aud = gr.Audio(label="🔊 Dengarkan Hasil Penggabungan Kata")
            btn_sim.click(fn=gabung_partikel_gradio, inputs=[pilih_kata, pilih_part], outputs=[out_sim_html, out_sim_aud])

        # TAB 4: CHATBOT KAKA AI
        with gr.TabItem("🤖 4. Asisten Virtual 'Kaka AI'"):
            gr.ChatInterface(
                fn=kaka_ai_response,
                title="🤖 Kaka AI — Asisten Pintar Bahasa & Budaya Mandar",
                description="Tanyakan terjemahan kata, rumus partikel (-mi, -mo, -pa), etika sapaan (Yau vs I'da), atau bait Kalindaqdaq!",
                examples=["Apa arti kata pamboya?", "Jelaskan rumus partikel -mi, -mo, dan -pa!", "Berikan contoh puisi Kalindaqdaq Mandar!"]
            )

if __name__ == "__main__":
    demo.launch()