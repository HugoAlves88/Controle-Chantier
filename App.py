import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Contrôle PERCO", layout="wide")
st.title("📋 Contrôle de Sécurité Chantier (BST)")

# Liste simplifiée des points de contrôle
points = [
    "1. Préparation du travail: Plan de sécurité (art. 4 OTConst)",
    "4. Échelles: Dépassement de 1m (art. 20 OTConst)",
    "10. Fouilles: Étayage dès 1.50m (art. 68 OTConst)",
    "11. Échafaudages: Garde-corps de 80cm (art. 11 OTConst)",
    "13. Port des EPI: Casque, chaussures, gilet"
]

concomite = {}
for p in points:
    concomite[p] = st.radio(f"Conformité pour {p}", ["Conforme", "Non-conforme", "N/A"])

if st.button("Générer le rapport PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Rapport de Contrôle de Chantier", ln=True, align='C')
    for p, v in concomite.items():
        pdf.cell(200, 10, txt=f"{p}: {v}", ln=True)
    pdf.output("rapport.pdf")
    st.success("Rapport généré avec succès !")

