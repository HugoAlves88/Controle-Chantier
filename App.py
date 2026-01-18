import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="PERCO - Contrôle BST", layout="centered")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stRadio > label { font-weight: bold; color: #1f77b4; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Contrôle de Sécurité PERCO")
st.subheader("Rapport de visite de chantier (BST)")

# --- INFORMATIONS GÉNÉRALES ---
with st.expander("📌 Informations du chantier", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        chantier = st.text_input("Nom du chantier", "Chantier exemple")
        chef = st.text_input("Responsable", "Hugo Alves")
    with col2:
        date_visite = st.date_input("Date de visite", datetime.now())
        meteo = st.selectbox("Météo", ["Soleil", "Pluie", "Vent", "Neige"])

# --- LES 20 POINTS DE CONTRÔLE ---
st.write("### 📝 Liste de contrôle")

sections = {
    "1. Organisation": [
        "1.1 Plan de sécurité (art. 4 OTConst)",
        "1.2 Installation de chantier (art. 7 OTConst)",
        "1.3 Sorties de secours / Premiers secours"
    ],
    "2. Fouilles et Travaux spéciaux": [
        "2.1 Étayage des fouilles > 1.50m (art. 68)",
        "2.2 Accès aux fouilles (échelles, rampes)",
        "2.3 Stockage des déblais (distance de 60cm)"
    ],
    "3. Échafaudages": [
        "3.1 Garde-corps complet (80cm - art. 11)",
        "3.2 Fixations et stabilité",
        "3.3 Accès sécurisés aux étages"
    ],
    "4. Travaux en hauteur": [
        "4.1 Protection contre les chutes (art. 15)",
        "4.2 Échelles: dépassement de 1m (art. 20)",
        "4.3 Utilisation de nacelles / PEMP"
    ],
    "5. Équipements et Électricité": [
        "5.1 Armoires électriques de chantier conformes",
        "5.2 Matériel électrique (câbles, prises)",
        "5.3 Grues et engins de terrassement"
    ],
    "6. Hygiène et EPI": [
        "6.1 Port du casque et chaussures (EPI)",
        "6.2 Vestiaires et réfectoires propres",
        "6.3 Élimination des déchets"
    ]
}

reponses = {}
observations = {}

for section, items in sections.items():
    with st.expander(f"🔵 {section}"):
        for item in items:
            col_q, col_obs = st.columns([2, 1])
            with col_q:
                reponses[item] = st.radio(item, ["Conforme", "Non-conforme", "N/A"], horizontal=True)
            with col_obs:
                observations[item] = st.text_input("Obs.", key=f"obs_{item}")

# --- SIGNATURE ET VALIDATION ---
st.divider()
signature = st.text_input("Signature (Nom pour validation)")

if st.button("🚀 GÉNÉRER ET TÉLÉCHARGER LE RAPPORT"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="RAPPORT DE CONTRÔLE BST - PERCO", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Chantier: {chantier} | Date: {date_visite}", ln=True)
    pdf.cell(200, 10, txt=f"Responsable: {chef} | Météo: {meteo}", ln=True)
    pdf.ln(5)
    
    for item, status in reponses.items():
        obs_text = f" | Obs: {observations[item]}" if observations[item] else ""
        pdf.cell(200, 8, txt=f"- {item}: {status}{obs_text}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Validé par: {signature}", ln=True)
    
    pdf_output = "Rapport_Chantier.pdf"
    pdf.output(pdf_output)
    
    with open(pdf_output, "rb") as f:
        st.download_button("⬇️ Télécharger le PDF", f, file_name=f"Rapport_{chantier}.pdf")
    st.success("Le rapport est prêt !")
    
