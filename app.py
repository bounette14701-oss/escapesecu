import streamlit as st
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Hawkins Lab - Système de Sécurité",
    layout="centered", # Layout centré pour un focus sur l'image
    page_icon="🔦"
)

# --- CHARGEMENT DE L'IMAGE ---
# (Assurez-vous que stranger_office.png est dans le même dossier)
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        st.error(f"Image '{path}' non trouvée.")
        return ""

image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DÉFIS (Ajout du PC) ---
CHALLENGES = {
    "fire_bin": {
        "label": "🔥 La Poubelle Infernale",
        "question": "Des flammes sortent de la corbeille ! Quel extincteur utiliser pour un feu de papier/carton ?",
        "options": ["Extincteur à Eau pulvérisée", "Extincteur CO2 (Neige carbonique)", "Un seau de café"],
        "correct": "Extincteur à Eau pulvérisée",
        "digit": "1",
        "myth": "Le CO2 est excellent pour l'électrique, mais pour le papier, l'eau pulvérisée refroidit mieux le foyer."
    },
    "sparks": {
        "label": "⚡ Le Poteau Électrique",
        "question": "La multiprise au pied du poteau crépite. Quel est le risque immédiat ?",
        "options": ["Électrisation et incendie", "Simple coupure de courant", "Le Mind Flayer va sortir"],
        "correct": "Électrisation et incendie",
        "digit": "9",
        "myth": "Une multiprise surchargée ou endommagée est la première cause d'incendie de bureau."
    },
    "wet_floor": {
        "label": "💧 La Substance Suspecte",
        "question": "Une flaque visqueuse est au sol. Que faire en attendant le nettoyage ?",
        "options": ["Sauter par-dessus", "Balisage et zone d'exclusion", "Ess
