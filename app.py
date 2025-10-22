import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
import json

# ====== Traducción opcional (googletrans) ======
TRANSLATION_AVAILABLE = False
try:
    from googletrans import Translator
    translator = Translator()
    TRANSLATION_AVAILABLE = True
except Exception:
    translator = None

# ====== Lottie ======
from streamlit_lottie import st_lottie

# =======================
# Configuración de página
# =======================
st.set_page_config(
    page_title="Analizador de Texto Simple ⚽",
    page_icon="⚽",
    layout="wide"
)

# =======================
# Fondo azul futbolero
# =======================
fondo_azul = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #002b7f 0%, #0052cc 50%, #0073e6 100%);
    color: white !important;
}
[data-testid="stSidebar"] {
    background-color: #003366;
    color: white !important;
}
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: white !important;
}
.stButton>button {
    background-color: #0059b3 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 24px !important;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #0073e6 !important;
}
a, a:visited, a:hover, a:active {
    color: #cce6ff !important;
    text-decoration: none !important;
}
</style>
"""
st.markdown(fondo_azul, unsafe_allow_html=True)

# =======================
# Utilidades
# =======================
def load_lottie_json(path: str):
    """Carga un archivo .json de Lottie desde disco."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"No pude cargar la animación: {path} ({e})")
        return None

# Si tus JSON están en la misma carpeta que app.py:
LOTTIE_HAPPY = load_lottie_json("JFUBKdNqei.json")     # animación feliz
LOTTIE_SAD   = load_lottie_json("emojitriste.json")    # animación triste

POS_THRESHOLD = 0.05
NEG_THRESHOLD = -0.05

# Función para contar palabras
def contar_palabras(texto):
    stop_words = set([
        "a","ante","como","con","contra","cuando","de","del","desde","donde","durante",
        "el","ella","ellas","ellos","en","entre","era","es","esa","ese","eso","esta","este","esto",
        "ha","han","has
