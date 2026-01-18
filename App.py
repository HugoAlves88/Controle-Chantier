import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="PERCO - BST Complet", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; gap: 15px; }
    .exigence { font-size: 0.85rem; color: #666; font-style: italic; margin-bottom: 10px; line-height: 1.2; }
    .obs-box { background-color: #fff5f5; padding: 15px; border-left: 5px solid #d9534f; border-radius: 4px; margin-bottom: 20px; }
    h3 { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("📋 Contrôle des postes de travail")

# --- EN-TÊTE ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        chantier = st.text_input("Objet / Chantier", placeholder="Nom du projet")
        chef_c = st.text_input("CM (Chef de chantier / Maître d'œuvre)")
    with c2:
        date_v = st.date_input("Date", datetime.now())
    with c3:
        perco = st.text_input("PERCO", "Hugo Alves")

st.divider()

# --- LES 20 POINTS OFFICIELS BST ---
points_officiels = {
    1: ["Préparation du travail", "Un plan de sécurité et de protection de la santé (art. 4 OTConst) pour le bâtiment / la maçonnerie a-t-il été défini ? La protection collective a-t-elle été déterminée avec les maîtres d'ouvrage ?"],
    2: ["Voies d'accès au chantier", "Passages (art. 11 OTConst) sûrs et libres d'obstacles. Largeur > 1,00 m, pente (max. 20 cm sur 1 m), protection contre les glissades."],
    3: ["Escaliers", "Main courante si plus de 5 marches -> garde-corps périphérique (art. 11 OTConst)."],
    4: ["Échelles", "Échelles adaptées (art. 20 OTConst) et sécurisées de façon à ne pouvoir ni glisser, ni basculer, à au moins 1 m au-dessus de la surface de sortie. Travaux à partir d'échelles portables (art. 21 OTConst)."],
    5: ["EPI", "Casque (art. 5 OTConst), chaussures de sécurité, vêtements de signalisation à haute visibilité (art. 7 OTConst), lunettes de protection (BST info Protection des yeux), protections auditives ou voir BST info Protection contre les chutes, en cas d'absence de garde-corps périphérique."],
    6: ["Ordre et propreté", "Pas de risque de trébucher ou de tomber (à cause de matériaux, de détritus, de déchets, etc.). Les passages doivent être dégagés (art. 9 OTConst)."],
    7: ["Bords présentant un risque de chutes", "Garde-corps périphérique en trois parties si hauteur de chute > 2,00 m (art. 15 OTConst) ou voir BST info Protection contre les chutes de hauteur."],
    8: ["Différences de niveau dans le bâtiment", "Garde-corps périphérique si différences de niveau > 0,50 m, main courante et escalier (art. 15 OTConst)."],
    9: ["Ouvertures dans les sols", "Garde-corps périphérique ou couverture résistante à la rupture et sécurisée de façon à ne pas glisser (pas de panneaux de coffrage) (art. 18 OTConst)."],
    10: ["Fouilles", "Étayage si profondeur > 1,50 m (art. 68 OTConst). Les bords de fouilles doivent être laissés libres (art. 71 OTConst)."],
    11: ["Hauteur des échafaudages", "En cas de hauteur de chute > 3,00 m, la lisse haute du garde-corps périphérique de l'échafaudage doit dépasser de 80 cm au moins le bord de la zone la plus élevée présentant un risque de chutes (art. 28 OTConst)."],
    12: ["Échafaudages", "Fondations et ancrage, garde-corps périphériques en trois parties, distance par rapport à la façade <= 30 cm (FAQ: Foire aux questions - Échafaudages de façade)."],
    13: ["Étayage du toit", "Poutrelles de coffrage avec têtes à fourche."],
    14: ["Coffrage mural", "Coffrage mural avec étais de réglage. Garde-corps périphérique toujours en trois parties si hauteur de chute > 2,00 m, si hauteur de chute > 2,00 m protection antichute opposée."],
    15: ["Grue", "Les grutiers et les élingueurs sont formés, les fondations de la grue sont calculées, l'éclairage pour la sécurité aérienne et des substances dangereuses (art. 76 OTConst) (Ordonnance sur les grues)."],
    16: ["Talus", "2:1 pour les terrains résistants, 1:1 pour les terrains ébouleux ainsi qu'un justificatif de la sécurité établi par un ingénieur pour les talus de plus de 4,00 m (art. 73 OTConst)."],
    17: ["Bord des fouilles", "Délimiter le bord des fouilles à l'aide d'une main courante (art. 23 OTConst)."],
    18: ["Approvisionnement en énergie, installations et substances dangereuses", "Installations et équipements électriques sûrs (art. 31 OTConst), hygiène et propreté des installations sanitaires et des vestiaires, manipulation sûre et stockage approprié des substances dangereuses (art. 32 OTConst)."],
    19: ["Organisation en cas d'urgence", "Les premiers secours sont assurés, le plan d'alarme est établi (y compris la suppléance) et bien visible, le comportement à adopter en cas d'urgence a fait l'objet d'une instruction et le lieu de rassemblement est connu de tous (BST info Premiers secours sur le chantier)."],
    20: ["Amiante", "Les collaborateurs ont-ils été instruits avant de travailler avec de l'amiante fortement aggloméré (BST info Règles de base pour la manipulation de l'amiante) ?"]
}

reponses = {}
details_mesures = {}

st.subheader("Liste de contrôle (Grille BST)")
st.caption("C = Conforme | X = Non-conforme | N/A = Non applicable")

for i, (titre, exigence) in points_officiels.items():
    col_t, col_r = st.columns([3, 1])
    with col_t:
        st.write(f"**{i}. {titre}**")
        st.markdown(f'<div class="exigence">{exigence}</div>', unsafe_allow_html=True)
    with col_r:
        reponses[i] = st.radio(f"S_{i}", ["C", "X", "N/A"], key=f"r_{i}", label_visibility="collapsed", index=2)

    # Ligne d'observation qui s'ouvre si Non-conforme
    if reponses[i] == "X":
        with st.container():
            st.markdown('<div class="obs-box">', unsafe_allow_html=True)
            c_mes, c_ech = st.columns([2, 1])
            with c_mes:
                m = st.text_area(f"Mesure à mettre en œuvre (Point {i})", key=f"m_{i}", height=70)
            with c_ech:
                e = st.text_input(f"Échéance / Responsable", key=f"e_{i}")
            details_mesures[i] = {"mesure": m, "echeance": e}
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        details_mesures[i] = None

# --- GÉNÉRATION DU PDF ---
st.divider()
if st.button("💾 GÉNÉRER LE RAPPORT BST (PDF)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    
    # Titre Rapport
    pdf.cell(190, 10, "CONTRÔLE DES POSTES DE TRAVAIL (BST)", 1, 1, 'C')
    pdf.ln(5)
    
    # Infos Entête
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 8, f"Objet: {chantier}", 1)
    pdf.cell(95, 8, f"Date: {date_v}", 1, 1)
    pdf.cell(95, 8, f"CM (Chef de chantier): {chef_c}", 1)
    pdf.cell(95, 8, f"CT (Contrôleur): {ct}", 1, 1)
    pdf.cell(190, 8, f"Référence PERCO: {perco}", 1, 1)
    
    # Section Planification des mesures (Page 3 du PDF)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(190, 10, "PLANIFICATION DES MESURES (Points non-conformes)", 0, 1, 'L', True)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(10, 10, "N°", 1, 0, 'C')
    pdf.cell(120, 10, "Mesure à mettre en oeuvre / Remarques", 1, 0, 'C')
    pdf.cell(60, 10, "Échéance / Responsable", 1, 1, 'C')
    
    pdf.set_font("Arial", size=9)
    errors = 0
    for i, data in details_mesures.items():
        if data:
            # Calcul de la hauteur de cellule pour le texte long
            pdf.cell(10, 10, str(i), 1, 0, 'C')
            pdf.cell(120, 10, data['mesure'][:80], 1, 0, 'L')
            pdf.cell(60, 10, data['echeance'], 1, 1, 'C')
            errors += 1
            
    if errors == 0:
        pdf.cell(190, 10, "Aucune mesure corrective requise. Chantier conforme.", 1, 1, 'C')

    pdf_name = f"Rapport_BST_{chantier}_{date_v}.pdf"
    pdf.output(pdf_name)
    
    with open(pdf_name, "rb") as f:
        st.download_button("⬇️ Télécharger le rapport final", f, file_name=pdf_name)
    st.success("Rapport généré avec succès !")
