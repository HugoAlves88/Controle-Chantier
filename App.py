import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="PERCO - Contrôle BST", layout="wide")

# --- STYLE POUR RESSEMBLER AU PAPIER ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; }
    .stRadio label { padding: 5px 15px; background: #eee; border-radius: 5px; margin: 2px; }
    div[data-testid="stExpander"] { border: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Contrôle de Sécurité PERCO (BST)")

# --- ENTÊTE (Comme ton document) ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        chantier = st.text_input("Nom du chantier", "Ex: Rénovation Lausanne")
        chef_chantier = st.text_input("Chef de chantier (interne)", "Nom du chef")
    with col2:
        date_visite = st.date_input("Date de visite", datetime.now())
        controleur = st.text_input("Contrôleur", "Hugo Alves")

st.divider()

# --- STRUCTURE SIMPLE (NUMÉRO + CASE + OBSERVATION) ---
st.write("### Grille de contrôle")
st.caption("Cochez la case correspondante et ajoutez le chiffre/observation si nécessaire.")

# Liste des 20 points simplifiée
points_bst = [
    "1. Préparation du travail / Plan de sécurité",
    "2. Installations de chantier",
    "3. Voies de circulation / Accès",
    "4. Échelles et escabeaux",
    "5. Travaux de toiture",
    "6. Risques de chute (hauteur)",
    "7. Ouvertures dans le sol / trémies",
    "8. Grues et engins",
    "9. Plateformes de travail",
    "10. Fouilles et puits (Art. 68)",
    "11. Échafaudages de façade",
    "12. Échafaudages roulants",
    "13. EPI (Casque, chaussures, gilet)",
    "14. Électricité et coffrets",
    "15. Substances dangereuses / Amiante",
    "16. Ordre et propreté",
    "17. Protection contre les intempéries",
    "18. Levage de charges",
    "19. Mesures de premiers secours",
    "20. Coordination entre entreprises"
]

reponses = {}
observations = {}

# Création de la grille (Tableau)
for p in points_bst:
    col_num, col_check, col_obs = st.columns([2, 2, 3])
    
    with col_num:
        st.write(f"**{p}**")
    
    with col_check:
        # On utilise une croix (X) ou conforme (C) comme dans ton PDF
        reponses[p] = st.radio(f"Statut {p}", ["C", "X", "N/A"], key=f"check_{p}", label_visibility="collapsed")
    
    with col_obs:
        observations[p] = st.text_input("Observations / Mesures", key=f"obs_{p}", placeholder="Chiffre ou détail...")

# --- SIGNATURE ET GÉNÉRATION ---
st.divider()
col_sig1, col_sig2 = st.columns(2)
with col_sig1:
    signature_hugo = st.text_input("Signature du contrôleur")
with col_sig2:
    # Option photo pour la version mobile
    photo = st.camera_input("Prendre une photo d'un défaut (optionnel)")

if st.button("💾 GÉNÉRER LE RAPPORT FINAL"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="RAPPORT DE CONTRÔLE BST - PERCO", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    pdf.cell(100, 8, txt=f"Chantier: {chantier}")
    pdf.cell(100, 8, txt=f"Date: {date_visite}", ln=True)
    pdf.cell(100, 8, txt=f"Chef de chantier: {chef_chantier}")
    pdf.cell(100, 8, txt=f"Contrôleur: {controleur}", ln=True)
    pdf.ln(5)
    
    # En-tête tableau
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(100, 8, "Point de contrôle", 1, 0, 'L', True)
    pdf.cell(20, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(70, 8, "Observations", 1, 1, 'L', True)
    
    for p in points_bst:
        pdf.cell(100, 7, p[:50], 1)
        pdf.cell(20, 7, reponses[p], 1, 0, 'C')
        pdf.cell(70, 7, observations[p][:40], 1, 1)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Validé par: {signature_hugo}", ln=True)
    
    pdf_output = "Rapport_BST.pdf"
    pdf.output(pdf_output)
    
    with open(pdf_output, "rb") as f:
        st.download_button("⬇️ Télécharger le rapport PDF", f, file_name=f"BST_{chantier}_{date_visite}.pdf")
    st.success("Rapport créé avec succès !")
