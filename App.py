import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="PERCO - BST Officiel", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; gap: 15px; }
    .exigence { font-size: 0.85rem; color: #555; font-style: italic; margin-bottom: 10px; }
    .obs-box { background-color: #fdf2f2; padding: 15px; border-left: 5px solid #d9534f; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📋 Contrôle des postes de travail BST")

# --- EN-TÊTE ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        chantier = st.text_input("Objet / Chantier", placeholder="Ex: Immeuble A")
        chef_c = st.text_input("Chef de chantier (CM)")
    with c2:
        date_v = st.date_input("Date", datetime.now())
        ct = st.text_input("Contrôleur (CT)", "Hugo Alves")
    with c3:
        perco = st.text_input("PERCO", "Rapport n°1")

st.divider()

# --- POINTS DE CONTRÔLE AVEC EXIGENCES ---
points_complets = {
    1: ["Préparation du travail", "Plan de sécurité et protection de la santé (art. 4 OTConst)"],
    2: ["Voies d'accès au chantier", "Largeur > 1.00m, pente max 20cm sur 1m (art. 10 OTConst)"],
    3: ["Escaliers", "Main courante si plus de 5 marches (art. 11 OTConst)"],
    4: ["Échelles", "Dépassement de 1m au-dessus de la sortie (art. 20 OTConst)"],
    5: ["EPI", "Casque, chaussures, gilets haute visibilité (art. 5 OTConst)"],
    6: ["Ordre et propreté", "Pas de risque de trébucher, passages dégagés"],
    7: ["Bords de chute", "Garde-corps dès 2.00m de hauteur (art. 15 OTConst)"],
    8: ["Différences de niveau", "Protection si h > 0.50m (art. 15 OTConst)"],
    9: ["Ouvertures au sol", "Couverture résistante et fixée (art. 18 OTConst)"],
    10: ["Fouilles", "Étayage obligatoire dès 1.50m (art. 68 OTConst)"],
    11: ["Échafaudages (Hauteur)", "Garde-corps de 80cm min. (art. 11 OTConst)"],
    12: ["Échafaudages (Façade)", "Distance à la façade max 30cm"],
}

reponses = {}
details_mesures = {}

st.subheader("Grille de contrôle")

for i, (titre, exigence) in points_complets.items():
    col_t, col_r = st.columns([3, 1])
    with col_t:
        st.write(f"**{i}. {titre}**")
        st.markdown(f'<div class="exigence">{exigence}</div>', unsafe_allow_html=True)
    with col_r:
        reponses[i] = st.radio(f"S_{i}", ["C", "X", "N/A"], key=f"r_{i}", label_visibility="collapsed", index=2)

    if reponses[i] == "X":
        with st.container():
            st.markdown('<div class="obs-box">', unsafe_allow_html=True)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                obs = st.text_area(f"Mesure à mettre en œuvre (Point {i})", key=f"obs_{i}")
            with col_m2:
                ech = st.text_input(f"Échéance / Responsable", key=f"ech_{i}")
            details_mesures[i] = {"mesure": obs, "echeance": ech}
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

# --- GÉNÉRATION DU PDF ---
st.divider()
if st.button("💾 GÉNÉRER LE RAPPORT BST COMPLET"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    
    # Header
    pdf.cell(190, 10, "CONTRÔLE DES POSTES DE TRAVAIL SUR LES CHANTIERS", 1, 1, 'C')
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, f"Objet: {chantier}", 1)
    pdf.cell(95, 8, f"Date: {date_v}", 1, 1)
    pdf.cell(95, 8, f"CM: {chef_c}", 1)
    pdf.cell(95, 8, f"CT: {ct}", 1, 1)
    
    # Page 3 : Planification des mesures
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "PLANIFICATION DES MESURES", 0, 1, 'L')
    
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(10, 10, "N°", 1, 0, 'C', True)
    pdf.cell(120, 10, "Mesure à mettre en oeuvre", 1, 0, 'C', True)
    pdf.cell(60, 10, "Échéance / Responsable", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=9)
    found_x = False
    for i, data in details_mesures.items():
        if reponses[i] == "X":
            pdf.cell(10, 10, str(i), 1, 0, 'C')
            pdf.cell(120, 10, data['mesure'][:70], 1, 0, 'L')
            pdf.cell(60, 10, data['echeance'], 1, 1, 'C')
            found_x = True
            
    if not found_x:
        pdf.cell(190, 10, "Toutes les mesures sont conformes.", 1, 1, 'C')

    pdf_name = f"BST_{chantier}.pdf"
    pdf.output(pdf_name)
    
    with open(pdf_name, "rb") as f:
        st.download_button("⬇️ Télécharger le rapport final", f, file_name=pdf_name)
