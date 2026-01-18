import streamlit as st
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="PERCO - BST avec Photos", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; gap: 15px; }
    .exigence { font-size: 0.85rem; color: #666; font-style: italic; margin-bottom: 10px; }
    .obs-box { background-color: #fff5f5; padding: 20px; border-left: 5px solid #d9534f; border-radius: 8px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Contrôle BST - Rapport Complet avec Photos")

# --- EN-TÊTE ---
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        chantier = st.text_input("Objet / Chantier", placeholder="Nom du projet")
        chef_c = st.text_input("Chef de chantier (CM)", placeholder="Nom du responsable")
    with c2:
        date_v = st.date_input("Date du contrôle", datetime.now())
        ct = st.text_input("Contrôleur (CT)", "Hugo Alves")

st.divider()

# --- POINTS DE CONTRÔLE ---
points_officiels = {
    1: ["Préparation du travail", "Plan de sécurité (art. 4 OTConst)."],
    2: ["Voies d'accès", "Passages sûrs, largeur > 1,00 m (art. 11 OTConst)."],
    3: ["Escaliers", "Main courante si > 5 marches."],
    4: ["Échelles", "Dépassement de 1m (art. 20 OTConst)."],
    5: ["EPI", "Casque, chaussures, gilets (art. 5 et 7 OTConst)."],
    6: ["Ordre et propreté", "Passages dégagés."],
    7: ["Bords de chutes", "Garde-corps si chute > 2,00 m."],
    8: ["Différences de niveau", "Protection si h > 0,50 m."],
    9: ["Ouvertures au sol", "Couverture fixée (art. 18 OTConst)."],
    10: ["Fouilles", "Étayage si prof. > 1,50 m."],
    11: ["Hauteur échafaudages", "Garde-corps > 80 cm."],
    12: ["Échafaudages façade", "Distance façade <= 30 cm."],
    13: ["Étayage du toit", "Poutrelles avec têtes à fourche."],
    14: ["Coffrage mural", "Étais de réglage."],
    15: ["Grue", "Formation et fondations conformes."],
    16: ["Talus", "Pente conforme au terrain."],
    17: ["Bord des fouilles", "Main courante de délimitation."],
    18: ["Énergie / Substances", "Installations électriques sûres."],
    19: ["Urgence", "Plan d'alarme et premiers secours."],
    20: ["Amiante", "Instruction des collaborateurs."]
}

reponses = {}
suivi_mesures = {}
photos_dict = {}

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
            c_obs, c_data = st.columns(2)
            with c_obs:
                m = st.text_area(f"Mesure corrective (Point {i})", key=f"m_{i}")
                # Le file_uploader permet d'utiliser la caméra arrière
                uploaded_photo = st.file_uploader(f"📸 Prendre/Ajouter une photo (Point {i})", type=['png', 'jpg', 'jpeg'], key=f"p_{i}")
                if uploaded_photo:
                    photos_dict[i] = uploaded_photo
                    st.image(uploaded_photo, width=200)
            with c_data:
                resp = st.text_input(f"Responsable", value=chef_c, key=f"res_{i}")
                echeance = st.text_input(f"Échéance", placeholder="ex: Immédiat", key=f"ech_{i}")
                ctrl_f = st.selectbox(f"Contrôle final", ["En attente", "Fait", "À revoir"], key=f"cf_{i}")
            
            suivi_mesures[i] = {"mesure": m, "resp": resp, "ech": echeance, "ctrl": ctrl_f}
            st.markdown('</div>', unsafe_allow_html=True)

# --- GÉNÉRATION DU RAPPORT AVEC PHOTOS ---
st.divider()
if st.button("💾 GÉNÉRER LE RAPPORT AVEC PHOTOS"):
    pdf = FPDF()
    
    # PAGE 1 & 2 : Tableau des mesures
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, "RAPPORT DE SECURITE BST - PERCO", 1, 1, 'C')
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, f"Chantier: {chantier}", 1)
    pdf.cell(95, 8, f"Date: {date_v}", 1, 1)
    pdf.cell(95, 8, f"Chef de chantier: {chef_c}", 1)
    pdf.cell(95, 8, f"Controleur: {ct}", 1, 1)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(10, 10, "N", 1, 0, 'C', True)
    pdf.cell(80, 10, "Mesure", 1, 0, 'C', True)
    pdf.cell(40, 10, "Responsable", 1, 0, 'C', True)
    pdf.cell(30, 10, "Echeance", 1, 0, 'C', True)
    pdf.cell(30, 10, "Statut", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=8)
    for i, data in suivi_mesures.items():
        pdf.cell(10, 10, str(i), 1, 0, 'C')
        pdf.cell(80, 10, data['mesure'][:50], 1, 0, 'L')
        pdf.cell(40, 10, data['resp'], 1, 0, 'C')
        pdf.cell(30, 10, data['ech'], 1, 0, 'C')
        pdf.cell(30, 10, data['ctrl'], 1, 1, 'C')

    # PAGE SUIVANTE : ANNEXE PHOTOS
    if photos_dict:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANNEXE : PHOTOS DES DEFAUTS", 0, 1, 'L')
        pdf.ln(5)
        
        for i, img_file in photos_dict.items():
            # Sauvegarde temporaire de l'image pour l'insérer dans le PDF
            img = Image.open(img_file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                img.save(tmp.name)
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(190, 10, f"Point {i} : {points_officiels[i][0]}", 0, 1)
                # On insère l'image (Largeur 80mm pour en mettre deux par page si besoin)
                pdf.image(tmp.name, x=10, w=80)
                pdf.ln(5)
                os.unlink(tmp.name) # Supprime le fichier temporaire

    pdf_name = f"Rapport_BST_{chantier}.pdf"
    pdf.output(pdf_name)
    with open(pdf_name, "rb") as f:
        st.download_button("⬇️ Télécharger le rapport final (PDF + Photos)", f, file_name=pdf_name)
