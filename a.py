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
    padding: