import streamlit as st
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="Hawkins Lab - Security System", layout="centered")

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except: return ""

# --- DONNÉES DES DÉFIS ---
CHALLENGES = {
    "pc": {"label": "💻 Ordinateur", "q": "Un PC est déverrouillé. Que faire ?", "o": ["Verrouiller (Win+L)", "Éteindre l'écran", "L'ignorer"], "c": "Verrouiller (Win+L)", "d": "4", "m": "L'usurpation d'identité est un risque majeur."},
    "fire": {"label": "🔥 Feu", "q": "Début d'incendie dans la corbeille !", "o": ["Eau pulvérisée", "Souffler dessus", "CO2"], "c": "Eau pulvérisée", "d": "1", "m": "L'eau pulvérisée refroidit les braises de papier."},
    "elec": {"label": "⚡ Électricité", "q": "Étincelles sur la multiprise !", "o": ["Couper le courant", "Verser de l'eau", "Toucher les fils"], "c": "Couper le courant", "d": "9", "m": "N'intervenez jamais sur un circuit sous tension."},
    "water": {"label": "💧 Sol Mouillé", "q": "Une flaque suspecte au sol.", "o": ["Balisage immédiat", "Sauter par-dessus", "Attendre"], "c": "Balisage immédiat", "d": "8", "m": "La chute est l'accident n°1 au bureau."},
    "exit": {"label": "🚪 Issue de secours", "q": "Cartons bloquant la sortie.", "o": ["Dégager l'issue", "Pousser plus tard", "C'est normal"], "c": "Dégager l'issue", "d": "3", "m": "Une issue de secours doit être libre 24h/24."}
}

CODE_SECRET = "41983"

# --- INITIALISATION ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'target' not in st.session_state:
    st.session_state.target = None

# --- STYLE STRANGER THINGS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');
    .stApp { background-color: #050505; color: #e2e2e2; font-family: 'Courier Prime', monospace; }
    h1 { color: #ff0000 !important; text-shadow: 0 0 15px #ff0000; text-align: center; font-size: 3rem !important; }
    .stButton>button { background-color: #1a1a1a; color: #ff0000; border: 1px solid #ff0000; width: 100%; }
    .stButton>button:hover { background-color: #ff0000; color: white; }
    .status-box { border: 1px solid #333; padding: 10px; border-radius: 5px; background: #111; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("STRANGER OFFICE")
st.write("---")

# --- INTERFACE IMAGE CLIQUABLE (HTML/JS) ---
# On utilise un composant HTML pour capturer les clics précisément
img_b64 = get_image_base64("stranger_office.png")

html_map = f"""
<div style="position: relative; width: 100%; display: inline-block;">
    <img src="data:image/png;base64,{img_b64}" style="width: 100%; border: 2px solid #444; box-shadow: 0 0 20px rgba(255,0,0,0.3);">
    
    <div onclick="window.parent.postMessage('exit', '*')" style="position: absolute; top: 43%; left: 41%; width: 8%; height: 20%; cursor: pointer; border: 1px dashed rgba(255,0,0,0.2);"></div>
    <div onclick="window.parent.postMessage('elec', '*')" style="position: absolute; top: 75%; left: 44%; width: 10%; height: 10%; cursor: pointer; border: 1px dashed rgba(255,0,0,0.2);"></div>
    <div onclick="window.parent.postMessage('water', '*')" style="position: absolute; top: 68%; left: 53%; width: 9%; height: 13%; cursor: pointer; border: 1px dashed rgba(255,0,0,0.2);"></div>
    <div onclick="window.parent.postMessage('fire', '*')" style="position: absolute; top: 58%; left: 58%; width: 7%; height: 14%; cursor: pointer; border: 1px dashed rgba(255,0,0,0.2);"></div>
    <div onclick="window.parent.postMessage('pc', '*')" style="position: absolute; top: 45%; left: 68%; width: 7%; height: 9%; cursor: pointer; border: 1px dashed rgba(255,0,0,0.2);"></div>
</div>

<script>
    // Ecouter les clics et envoyer l'info à Streamlit via un bouton caché
    const mapItems = document.querySelectorAll('div[onclick]');
    mapItems.forEach(item => {{
        item.addEventListener('mouseover', () => item.style.backgroundColor = 'rgba(255,0,0,0.1)');
        item.addEventListener('mouseout', () => item.style.backgroundColor = 'transparent');
    }});
</script>
"""

# Affichage de l'image via le composant HTML
from streamlit_gsheets import GSheetsConnection # Non requis ici, juste pour le rappel
import streamlit.components.v1 as components

# Capture du clic via un petit hack : un bouton Streamlit invisible déclenché par JS
# Pour simplifier, on garde les boutons sous l'image pour cette version si le JS est bloqué
# Mais voici la version "Select" qui s'active quand on clique
selected_zone = components.html(html_map, height=450)

# Comme le passage de données HTML -> Streamlit est complexe, 
# on ajoute des boutons de secours stylisés juste en dessous si le clic image échoue.
st.info("🔦 Cliquez sur une zone suspecte de l'image ou utilisez les boutons ci-dessous :")

cols = st.columns(5)
for i, (key, data) in enumerate(CHALLENGES.items()):
    with cols[i]:
        label = "✅" if st.session_state.solved[key] else "❓"
        if st.button(f"{label} {data['label']}", key=f"btn_{key}"):
            st.session_state.target = key

# --- ZONE DE RÉSOLUTION ---
if st.session_state.target:
    target = st.session_state.target
    data = CHALLENGES[target]
    
    st.write("---")
    st.subheader(f"Analyse de la menace : {data['label']}")
    
    if st.session_state.solved[target]:
        st.success(f"Indice trouvé : **{data['digit']}**")
        st.caption(f"Note : {data['m']}")
    else:
        with st.form(key="solve_form"):
            choice = st.radio(data['q'], data['o'])
            if st.form_submit_button("VALIDER"):
                if choice == data['c']:
                    st.session_state.solved[target] = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("ERREUR. Le danger se propage...")

# --- VERROUILLAGE FINAL ---
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.write("**INVENTAIRE DES CHIFFRES :**")
    code_display = "".join([f"[{CHALLENGES[k]['d']}]" if st.session_state.solved[k] else "[?]" for k in CHALLENGES])
    st.subheader(code_display)

with c2:
    final_input = st.text_input("CODE DE SORTIE", max_chars=5)
    if st.button("FERMER LE PORTAIL", type="primary"):
        if final_input == CODE_SECRET:
            st.snow()
            st.success("BUREAU SÉCURISÉ. PORTAIL FERMÉ.")
        else:
            st.error("CODE ERRONÉ.")
