import streamlit as st
from fpdf import FPDF
from datetime import date
from PIL import Image
import io

# Configuration pour tablette
st.set_page_config(page_title="PERCO - Contrôle BST", layout="wide")

# --- BASE DE DONNÉES BST (EXTRAITE DU PDF) ---
# [span_1](start_span)Ces points reprennent exactement les rubriques de votre document[span_1](end_span)
DONNEES_BST = {
    [span_2](start_span)"1. Préparation du travail": "Plan de sécurité (art. 4 OTConst) et protection collective déterminée[span_2](end_span).",
    "2. [span_3](start_span)Voies d'accès au chantier": "Largeur > 1.00m, pente max 20%, protection contre les glissades (art. 11 OTConst)[span_3](end_span).",
    "3. [span_4](start_span)Escaliers": "Main courante si plus de 5 marches (art. 11 OTConst)[span_4](end_span).",
    "4. [span_5](start_span)Échelles": "Sécurisées (ne glissent pas), dépassement de 1m au-dessus de la sortie (art. 20/21 OTConst)[span_5](end_span).",
    "5. [span_6](start_span)EPI": "Casque (art. 6), chaussures, vêtements haute visibilité (art. 7), lunettes, protections auditives[span_6](end_span).",
    "6. [span_7](start_span)Ordre et propreté": "Pas de risque de trébucher, passages dégagés (art. 9 OTConst)[span_7](end_span).",
    "7. [span_8](start_span)Bords risque de chute": "Garde-corps 3 parties si hauteur de chute > 2.00m (art. 22 OTConst)[span_8](end_span).",
    "8. [span_9](start_span)Différences de niveau": "Garde-corps si > 0.50m, main courante et escalier (art. 15 OTConst)[span_9](end_span).",
    "9. [span_10](start_span)Ouvertures dans sols": "Couverture résistante, sécurisée (pas de panneaux de coffrage) (art. 13 OTConst)[span_10](end_span).",
    "10. Fouilles": "Étayage si prof. > [span_11](start_span)1.50m (art. 68), bords de fouilles laissés libres (art. 71 OTConst)[span_11](end_span).",
    "11. [span_12](start_span)Hauteur échafaudages": "Garde-corps dépasse de 80cm le bord de la zone de chute (art. 26 OTConst)[span_12](end_span).",
    "12. [span_13](start_span)Échafaudages": "Fondations, ancrage, garde-corps 3 parties, distance façade < 30cm[span_13](end_span).",
    "13. [span_14](start_span)Étayage du toit": "Poutrelles de coffrage avec têtes à fourche[span_14](end_span).",
    "14. [span_15](start_span)Coffrage mural": "Étais de réglage, garde-corps 3 parties si chute > 2.00m[span_15](end_span).",
    "15. [span_16](start_span)Grue": "Grutiers/élingueurs formés, fondations calculées, éclairage sécurité aérienne[span_16](end_span).",
    "16. Talus": "2:1 terrain résistant, 1:1 ébouleux. [span_17](start_span)Justificatif ingénieur si > 4m (art. 76 OTConst)[span_17](end_span).",
    "17. [span_18](start_span)Bord des fouilles": "Délimiter le bord à l'aide d'une main courante (art. 23 OTConst)[span_18](end_span).",
    "18. [span_19](start_span)Énergie & Installations": "Électricité sûre (art. 31), hygiène WC/vestiaires, stockage produits dangereux (art. 3)[span_19](end_span).",
    "19. [span_20](start_span)Urgence": "Premiers secours assurés, plan d'alarme établi, lieu de rassemblement connu[span_20](end_span).",
    "20. [span_21](start_span)Amiante": "Instructions données avant manipulation d'amiante fortement aggloméré[span_21](end_span)."
}

st.title("🏗️ Contrôle PERCO - Standard BST")
[span_22](start_span)[span_23](start_span)st.write("Référence document : BFA-CL-011[span_22](end_span)[span_23](end_span)")

# --- EN-TÊTE DU RAPPORT (Page 1 du PDF) ---
with st.container():
    col1, col2 = st.columns(2)
    [span_24](start_span)objet = col1.text_input("Objet / Chantier[span_24](end_span)")
    [span_25](start_span)perco_nom = col2.text_input("PERCO (Responsable)[span_25](end_span)")
    
    col3, col4 = st.columns(2)
    [span_26](start_span)ct_nom = col3.text_input("CT (Chef de Travaux)[span_26](end_span)")
    [span_27](start_span)cm_nom = col4.text_input("CM (Chef de Chantier)[span_27](end_span)")

st.divider()

# --- FORMULAIRE DE CONTRÔLE ---
point_select = st.selectbox("Sélectionnez le point à contrôler", list(DONNEES_BST.keys()))

st.subheader(f"Exigence BST : {point_select}")
st.warning(DONNEES_BST[point_select])

# [span_28](start_span)Système de case à cocher du PDF[span_28](end_span)
etat = st.radio("Constat :", ["✅ Conforme", "❌ Non-conforme", "➖ Non concerné"], horizontal=True)

# [span_29](start_span)Planification des mesures (Page 3 du PDF)[span_29](end_span)
mesure_texte = ""
if etat == "❌ Non-conforme":
    st.error("🚨 PLANIFICATION DES MESURES REQUISE")
    [span_30](start_span)mesure_texte = st.text_area("Mesure à mettre en œuvre[span_30](end_span)")
    col_a, col_b = st.columns(2)
    [span_31](start_span)responsable = col_a.text_input("Responsable de la mesure[span_31](end_span)")
    [span_32](start_span)echeance = col_b.date_input("Échéance[span_32](end_span)")

photo = st.camera_input("📸 Photo pour preuve")

# --- GÉNÉRATION DU RAPPORT PDF ---
if st.button("📄 Valider et Générer le PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "RAPPORT DE CONTRÔLE SÉCURITÉ CHANTIER", ln=True, align='C')
    pdf.ln(5)

    # Infos entête
    pdf.set_font("Arial", '', 10)
    pdf.cell(95, 8, f"Objet: {objet}", border=1)
    pdf.cell(95, 8, f"Date: {date.today()}", border=1, ln=True)
    pdf.cell(63, 8, f"CT: {ct_nom}", border=1)
    pdf.cell(63, 8, f"CM: {cm_nom}", border=1)
    pdf.cell(64, 8, f"PERCO: {perco_nom}", border=1, ln=True)
    pdf.ln(10)

    # Résultat
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"Point contrôlé : {point_select}", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(190, 8, f"Exigence : {DONNEES_BST[point_select]}")
    pdf.cell(190, 10, f"Résultat : {etat}", ln=True)

    # Mesure si non-conforme
    if mesure_texte:
        pdf.ln(5)
        pdf.set_fill_color(255, 230, 230)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(190, 10, "MESURE À METTRE EN OEUVRE (PLAN D'ACTION)", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(190, 8, f"Action : {mesure_texte}\nResponsable : {responsable}\nDélai : {echeance}")

    # Image
    if photo:
        img = Image.open(photo)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        pdf.ln(5)
        pdf.image(img_byte_arr, x=10, w=120)

    pdf_out = pdf.output(dest='S').encode('latin-1')
    st.download_button("⬇️ Télécharger le rapport PDF", pdf_out, f"Rapport_{objet}.pdf")
  
