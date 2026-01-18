import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="PERCO - BST Pro", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; gap: 15px; }
    .exigence { font-size: 0.85rem; color: #666; font-style: italic; margin-bottom: 10px; }
    .obs-box { background-color: #fff5f5; padding: 20px; border-left: 5px solid #d9534f; border-radius: 8px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Contrôle BST - Suivi de Sécurité")

# --- EN-TÊTE ---
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        chantier = st.text_input("Objet / Chantier", placeholder="Nom du projet")
        chef_c = st.text_input("Chef de chantier (Responsable désigné)", placeholder="Nom du responsable")
    with c2:
        date_v = st.date_input("Date du contrôle", datetime.now())
        ct = st.text_input("Contrôleur (CT)", "Hugo Alves")

st.divider()

# --- POINTS DE CONTRÔLE ---
points_officiels = {
    1: ["Préparation du travail", "Plan de sécurité et protection de la santé (art. 4 OTConst)."],
    2: ["Voies d'accès au chantier", "Passages sûrs, largeur > 1,00 m (art. 11 OTConst)."],
    3: ["Escaliers", "Main courante si plus de 5 marches (art. 11 OTConst)."],
    4: ["Échelles", "Dépassement de 1m au-dessus de la sortie (art. 20 OTConst)."],
    5: ["EPI", "Casque, chaussures, gilets (art. 5 et 7 OTConst)."],
    6: ["Ordre et propreté", "Passages dégagés, pas de risque de trébucher (art. 9 OTConst)."],
    7: ["Bords de chutes", "Garde-corps complet si chute > 2,00 m (art. 15 OTConst)."],
    8: ["Différences de niveau", "Protection si h > 0,50 m (art. 15 OTConst)."],
    9: ["Ouvertures au sol", "Couverture résistante et fixée (art. 18 OTConst)."],
    10: ["Fouilles", "Étayage si profondeur > 1,50 m (art. 68 OTConst)."],
    11: ["Hauteur échafaudages", "Garde-corps dépassant de 80 cm (art. 28 OTConst)."],
    12: ["Échafaudages façade", "Distance façade <= 30 cm, ancrages conformes."],
    13: ["Étayage du toit", "Poutrelles de coffrage avec têtes à fourche."],
    14: ["Coffrage mural", "Étais de réglage, protection antichute opposée."],
    15: ["Grue", "Formation grutier, fondations calculées (Ord. sur les grues)."],
    16: ["Talus", "Pente 2:1 ou 1:1 selon terrain (art. 73 OTConst)."],
    17: ["Bord des fouilles", "Main courante de délimitation (art. 23 OTConst)."],
    18: ["Énergie / Substances", "Installations électriques sûres, stockage produits."],
    19: ["Urgence", "Plan d'alarme visible, premiers secours assurés."],
    20: ["Amiante", "Instruction des collaborateurs (Règles de base)."]
}

reponses = {}
suivi_mesures = {}

st.subheader("Grille de contrôle")

for i, (titre, exigence) in points_officiels.items():
    col_t, col_r = st.columns([3, 1])
    with col_t:
        st.write(f"**{i}. {titre}**")
        st.markdown(f'<div class="exigence">{exigence}</div>', unsafe_allow_html=True)
    with col_r:
        reponses[i] = st.radio(f"S_{i}", ["C", "X", "N/A"], key=f"r_{i}", label_visibility="collapsed", index=2)

    if reponses[i] == "X":
        with st.container():
            st.markdown('<div class="obs-box">', unsafe_allow_html=True)
            
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                m = st.text_area(f"Mesure corrective (Point {i})", key=f"m_{i}", height=100)
                photo = st.camera_input(f"📸 Photo du défaut (Point {i})", key=f"p_{i}")
            with c_m2:
                resp = st.text_input(f"Responsable", value=chef_c, key=f"res_{i}")
                echeance = st.text_input(f"Échéance", placeholder="ex: Immédiat / 24h", key=f"ech_{i}")
                ctrl_final = st.selectbox(f"Statut Contrôle Final", ["En attente", "Fait - Conforme", "À revoir"], key=f"cf_{i}")
            
            suivi_mesures[i] = {"mesure": m, "responsable": resp, "echeance": echeance, "ctrl": ctrl_final}
            st.markdown('</div>', unsafe_allow_html=True)

# --- GÉNÉRATION DU RAPPORT ---
st.divider()
if st.button("💾 GÉNÉRER LE RAPPORT DE SUIVI"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, "PLANIFICATION ET SUIVI DES MESURES BST", 1, 1, 'C')
    
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, f"Chantier: {chantier}", 1)
    pdf.cell(95, 8, f"Date: {date_v}", 1, 1)
    pdf.cell(95, 8, f"Contrôleur: {ct}", 1)
    pdf.cell(95, 8, f"Responsable: {chef_c}", 1, 1)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(10, 10, "N°", 1, 0, 'C', True)
    pdf.cell(80, 10, "Mesure à mettre en oeuvre", 1, 0, 'C', True)
    pdf.cell(40, 10, "Responsable", 1, 0, 'C', True)
    pdf.cell(30, 10, "Échéance", 1, 0, 'C', True)
    pdf.cell(30, 10, "Ctrl Final", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=8)
    errors = 0
    for i, data in suivi_mesures.items():
        if data:
            pdf.cell(10, 10, str(i), 1, 0, 'C')
            pdf.cell(80, 10, data['mesure'][:50], 1, 0, 'L')
            pdf.cell(40, 10, data['responsable'], 1, 0, 'C')
            pdf.cell(30, 10, data['echeance'], 1, 0, 'C')
            pdf.cell(30, 10, data['ctrl'], 1, 1, 'C')
            errors += 1
            
    if errors == 0:
        pdf.cell(190, 10, "Aucune anomalie à signaler.", 1, 1, 'C')

    pdf_name = f"Suivi_BST_{chantier}.pdf"
    pdf.output(pdf_name)
    
    with open(pdf_name, "rb") as f:
        st.download_button("⬇️ Télécharger le rapport de suivi", f, file_name=pdf_name)
