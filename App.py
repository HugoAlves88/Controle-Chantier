import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="PERCO - BST", layout="wide")

# --- STYLE INTERFACE ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label { background: #f0f2f6; padding: 2px 10px; border-radius: 4px; border: 1px solid #dcdfe3; }
    .error-box { background-color: #ffe9e9; padding: 10px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 Formulaire de contrôle BST / PERCO")

# --- EN-TÊTE ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        chantier = st.text_input("Objet / Chantier", placeholder="Nom du projet")
        chef_chantier = st.text_input("Chef de chantier (CM)", placeholder="Nom du responsable")
    with col2:
        date_visite = st.date_input("Date", datetime.now())
        controleur = st.text_input("Contrôleur (CT)", value="Hugo Alves")
    with col3:
        perco_ref = st.text_input("Référence PERCO", "PERCO-2024")

st.divider()

# --- POINTS DE CONTRÔLE (LISTE OFFICIELLE BST) ---
points_bst = {
    1: "Préparation du travail / Plan de sécurité",
    2: "Voies d'accès au chantier",
    3: "Escaliers",
    4: "Échelles",
    5: "EPI",
    6: "Ordre et propreté",
    7: "Bords présentant un risque de chutes",
    8: "Différences de niveau dans le bâtiment",
    9: "Ouvertures dans les sols",
    10: "Fouilles (Art. 68 OTConst)",
    11: "Hauteur des échafaudages",
    12: "Échafaudages de façade",
    13: "Étayage du toit",
    14: "Coffrage mural",
    15: "Grue",
    16: "Talus",
    17: "Bord des fouilles",
    18: "Approvisionnement énergie / Substances dangereuses",
    19: "Organisation en cas d'urgence",
    20: "Amiante"
}

reponses = {}
mesures = {}

st.write("### Grille de contrôle (Page 2 du PDF)")
st.caption("C = Conforme | X = Non-conforme | N/A = Non applicable")

for i, desc in points_bst.items():
    col_desc, col_radio = st.columns([3, 1])
    
    with col_desc:
        st.write(f"**{i}. {desc}**")
    
    with col_radio:
        reponses[i] = st.radio(f"Statut {i}", ["C", "X", "N/A"], key=f"r_{i}", label_visibility="collapsed", index=2)

    # SI NON CONFORME (X) -> OUVRE LA LIGNE D'OBSERVATION (Comme en bas de ton image)
    if reponses[i] == "X":
        with st.container():
            st.markdown(f'<div class="error-box">', unsafe_allow_html=True)
            mesures[i] = st.text_input(f"⚠️ Mesure à mettre en œuvre pour le point {i}", key=f"m_{i}", placeholder="Action corrective, échéance, responsable...")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        mesures[i] = ""

# --- GÉNÉRATION DU RAPPORT ---
st.divider()
if st.button("📊 GÉNÉRER LE RAPPORT DE MESURES"):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "RAPPORT DE CONTRÔLE BST / PERCO", 1, 1, 'C')
    pdf.ln(5)
    
    # Infos
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, f"Chantier: {chantier}", 1)
    pdf.cell(95, 8, f"Date: {date_visite}", 1, 1)
    pdf.cell(95, 8, f"Chef de chantier: {chef_chantier}", 1)
    pdf.cell(95, 8, f"Contrôleur: {controleur}", 1, 1)
    pdf.ln(10)
    
    # Tableau des mesures (Page 3 du PDF)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, "PLANIFICATION DES MESURES (Points non-conformes)", 0, 1, 'L')
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(15, 10, "N°", 1, 0, 'C', True)
    pdf.cell(175, 10, "Mesure à mettre en œuvre / Remarques", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=9)
    count_errors = 0
    for i, m in mesures.items():
        if reponses[i] == "X":
            pdf.cell(15, 10, str(i), 1, 0, 'C')
            pdf.cell(175, 10, m if m else "Non précisé", 1, 1)
            count_errors += 1
            
    if count_errors == 0:
        pdf.cell(190, 10, "Aucune non-conformité détectée.", 1, 1, 'C')

    pdf_output = f"Rapport_BST_{chantier}.pdf"
    pdf.output(pdf_output)
    
    with open(pdf_output, "rb") as f:
        st.download_button("💾 Télécharger le rapport (PDF)", f, file_name=pdf_output)
    st.success("Tableau de mesures généré !")
