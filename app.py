import streamlit as st
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="Hawkins Lab - Security System", layout="centered")

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except: return ""

# --- LOGIQUE DES DÉFIS BASÉE SUR L'IMAGE ---
# Nous intégrons les dangers réels visibles : multiprise, sortie bloquée, sac au sol et PC.
CHALLENGES = {
    "pc": {"label": "💻 Ordinateur", "q": "Un PC est déverrouillé avec une session ouverte. Que faites-vous ?", "o": ["Verrouiller (Win+L)", "Éteindre l'écran", "L'ignorer"], "c": "Verrouiller (Win+L)", "d": "4"},
    "exit": {"label": "🚪 Sortie Secours", "q": "Des cartons bloquent l'issue 'EXIT BLOCKED'. Est-ce autorisé ?", "o": ["Jamais", "Si c'est temporaire", "Seulement la nuit"], "c": "Jamais", "d": "1"},
    "elec": {"label": "⚡ Multiprise", "q": "Une multiprise traîne au sol près du passage. Quel est le risque ?", "o": ["Incendie et chute", "Aucun", "Mauvaises ondes"], "c": "Incendie et chute", "d": "9"},
    "sac": {"label": "🎒 Sac au sol", "q": "Un sac à dos est abandonné en plein milieu du passage. Que faire ?", "o": ["Le ranger sous le bureau", "Le laisser là", "Enjamber"], "c": "Le ranger sous le bureau", "d": "8"},
    "clown": {"label": "🤡 Anomalie", "q": "Un individu suspect (clown) est dans l'open space. Procédure ?", "o": ["Signaler au PC sécurité", "Lui demander un ballon", "Rien"], "c": "Signaler au PC sécurité", "d": "3"}
}

CODE_SECRET = "41983"

# --- INITIALISATION ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}

# Récupération du clic via les paramètres d'URL (astuce pour rendre l'image cliquable)
query_params = st.query_params
if "target" in query_params:
    st.session_state.current_target = query_params["target"]

# --- STYLE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e2e2e2; font-family: 'Courier New', monospace; }
    h1 { color: #ff0000 !important; text-shadow: 0 0 15px #ff0000; text-align: center; }
    . rift-btn { 
        display: inline-block; padding: 10px; margin: 5px; 
        border: 2px solid #ff0000; color: #ff0000; text-decoration: none;
        border-radius: 50%; box-shadow: 0 0 10px #ff0000;
    }
</style>
""", unsafe_allow_html=True)

st.title("STRANGER OFFICE")

# --- IMAGE CLIQUABLE (Image Map HTML) ---
# Cette partie crée des zones de clic invisibles mais réelles sur l'image
img_b64 = get_image_base64("stranger_office.png") # Assurez-vous d'avoir l'image Stranger Things

st.markdown(f"""
<div style="position: relative; width: 100%;">
    <img src="data:image/png;base64,{img_b64}" style="width: 100%; border: 2px solid #ff0000;">
    
    <a href="/?target=exit" style="position: absolute; top: 43%; left: 41%; width: 8%; height: 20%; border: 2px dashed rgba(255,0,0,0.5);"></a>
    <a href="/?target=elec" style="position: absolute; top: 75%; left: 44%; width: 10%; height: 10%; border: 2px dashed rgba(255,0,0,0.5);"></a>
    <a href="/?target=sac" style="position: absolute; top: 72%; left: 68%; width: 10%; height: 15%; border: 2px dashed rgba(255,0,0,0.5);"></a>
    <a href="/?target=pc" style="position: absolute; top: 45%; left: 68%; width: 7%; height: 9%; border: 2px dashed rgba(255,0,0,0.5);"></a>
    <a href="/?target=clown" style="position: absolute; top: 40%; left: 90%; width: 8%; height: 15%; border: 2px dashed rgba(255,0,0,0.5);"></a>
</div>
<p style="text-align:center; color: #666; font-size: 0.8em;">(Cliquez sur les zones en pointillés rouges pour inspecter)</p>
""", unsafe_allow_html=True)

# --- ZONE DE RÉSOLUTION ---
if 'current_target' in st.session_state:
    target = st.session_state.current_target
    data = CHALLENGES[target]
    
    st.write("---")
    st.subheader(f"🔍 Inspection : {data['label']}")
    
    if st.session_state.solved[target]:
        st.success(f"✅ Menace neutralisée. Chiffre trouvé : {data['digit']}")
    else:
        with st.form(key="solve_form"):
            choice = st.radio(data['q'], data['o'])
            if st.form_submit_button("VALIDER"):
                if choice == data['c']:
                    st.session_state.solved[target] = True
                    st.balloons()
                    # Reset param
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error("ERREUR. Le portail s'agrandit...")

# --- INVENTAIRE ---
st.write("---")
st.write("**CHIFFRES RÉCUPÉRÉS :**")
cols = st.columns(5)
for i, (key, data) in enumerate(CHALLENGES.items()):
    val = data['digit'] if st.session_state.solved[key] else "?"
    cols[i].metric(data['label'], val)

# --- CODE FINAL ---
final_code = st.text_input("Saisir le code à 5 chiffres pour fermer le portail", max_chars=5)
if st.button("FERMER LE PORTAIL", type="primary"):
    if final_code == CODE_SECRET:
        st.snow()
        st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
    else:
        st.error("CODE ERRONÉ.")
