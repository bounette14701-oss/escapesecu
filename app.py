import streamlit as st
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Hawkins Lab - Système de Sécurité",
    layout="centered", 
    page_icon="🔦"
)

# --- CHARGEMENT DE L'IMAGE ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        return ""

# Assurez-vous que l'image s'appelle 'stranger_office.png'
image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DÉFIS ---
CHALLENGES = {
    "pc": {
        "label": "💻 Ordinateur", 
        "q": "Un PC est déverrouillé. Que faites-vous ?", 
        "o": ["Je verrouille (Win + L)", "J'éteins l'écran", "Je ne touche à rien"], 
        "c": "Je verrouille (Win + L)", 
        "d": "4", 
        "m": "Le verrouillage empêche l'usurpation d'identité et le vol de données."
    },
    "fire": {
        "label": "🔥 Poubelle", 
        "q": "Début d'incendie ! Quel extincteur utiliser ?", 
        "o": ["Eau pulvérisée", "CO2", "Sable"], 
        "c": "Eau pulvérisée", 
        "d": "1", 
        "m": "L'eau pulvérisée est le meilleur choix pour les feux de solides (papier/carton)."
    },
    "elec": {
        "label": "⚡ Électricité", 
        "q": "La multiprise au sol crépite. Risque majeur ?", 
        "o": ["Électrisation et incendie", "Simple panne", "Mauvaises ondes"], 
        "c": "Électrisation et incendie", 
        "d": "9", 
        "m": "Une multiprise au sol dans une zone de passage est un danger électrique et de chute."
    },
    "water": {
        "label": "💧 Sol Mouillé", 
        "q": "Une flaque visqueuse au sol. Priorité ?", 
        "o": ["Balisage et zone d'exclusion", "L'essuyer vite", "Sauter"], 
        "c": "Balisage et zone d'exclusion", 
        "d": "8", 
        "m": "Les chutes de plain-pied sont les accidents les plus fréquents au bureau."
    },
    "exit": {
        "label": "🚪 Issue de secours", 
        "q": "Des cartons bloquent l'issue ('EXIT BLOCKED'). Est-ce toléré ?", 
        "o": ["Jamais", "Si c'est temporaire", "La nuit"], 
        "c": "Jamais", 
        "d": "3", 
        "m": "Une issue de secours doit être dégagée en permanence pour l'évacuation."
    }
}

CODE_SECRET = "41983"

# --- INITIALISATION SESSION STATE ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'target' not in st.session_state:
    st.session_state.target = None

# --- STYLE CSS (Stranger Things + Failles Lumineuses) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #e2e2e2; }}
    h1 {{ color: #ff0000 !important; text-align: center; text-shadow: 0 0 10px #ff0000; font-family: 'Arial Black'; }}
    
    /* Conteneur de l'image */
    .overlay-container {{
        position: relative;
        width: 100%;
        aspect-ratio: 16 / 9;
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        border: 2px solid #333;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
        margin-bottom: 20px;
    }}

    /* Style des boutons "Failles" */
    .stButton > button {{
        background: rgba(255, 0, 0, 0.2) !important;
        border: 2px solid #ff0000 !important;
        color: #ff0000 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        font-weight: bold !important;
        box-shadow: 0 0 15px #ff0000 !important;
        transition: 0.3s;
    }}
    .stButton > button:hover {{
        background: #ff0000 !important;
        color: white !important;
        transform: scale(1.2);
    }}

    /* Positionnement Absolu des boutons */
    div[data-testid="column"] {{ position: static !important; }}
    
    /* On utilise des classes pour placer les boutons sur l'image */
    .pos-pc    {{ position: absolute; top: 48%; left: 72%; z-index: 100; }}
    .pos-fire  {{ position: absolute; top: 60%; left: 60%; z-index: 100; }}
    .pos-elec  {{ position: absolute; top: 80%; left: 48%; z-index: 100; }}
    .pos-water {{ position: absolute; top: 72%; left: 55%; z-index: 100; }}
    .pos-exit  {{ position: absolute; top: 55%; left: 44%; z-index: 100; }}

    /* Masquer les boutons déjà résolus */
    .solved {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.markdown("<p style='text-align:center;'>Cliquez sur les <b>failles rouges</b> pour neutraliser les dangers.</p>", unsafe_allow_html=True)

# Zone Image Interactive
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

# Bouton PC
st.markdown(f'<div class="pos-pc {"solved" if st.session_state.solved["pc"] else ""}">', unsafe_allow_html=True)
if st.button("💻", key="btn_pc"): st.session_state.target = "pc"
st.markdown('</div>', unsafe_allow_html=True)

# Bouton Feu
st.markdown(f'<div class="pos-fire {"solved" if st.session_state.solved["fire"] else ""}">', unsafe_allow_html=True)
if st.button("🔥", key="btn_fire"): st.session_state.target = "fire"
st.markdown('</div>', unsafe_allow_html=True)

# Bouton Elec
st.markdown(f'<div class="pos-elec {"solved" if st.session_state.solved["elec"] else ""}">', unsafe_allow_html=True)
if st.button("⚡", key="btn_elec"): st.session_state.target = "elec"
st.markdown('</div>', unsafe_allow_html=True)

# Bouton Eau
st.markdown(f'<div class="pos-water {"solved" if st.session_state.solved["water"] else ""}">', unsafe_allow_html=True)
if st.button("💧", key="btn_water"): st.session_state.target = "water"
st.markdown('</div>', unsafe_allow_html=True)

# Bouton Exit
st.markdown(f'<div class="pos-exit {"solved" if st.session_state.solved["exit"] else ""}">', unsafe_allow_html=True)
if st.button("🚪", key="btn_exit"): st.session_state.target = "exit"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- ZONE DE RÉSOLUTION ---
if st.session_state.target:
    target = st.session_state.target
    data = CHALLENGES[target]
    st.divider()
    
    st.subheader(f"🔍 Analyse : {data['label']}")
    if st.session_state.solved[target]:
        st.success(f"✅ Menace neutralisée. Chiffre : **{data['digit']}**")
    else:
        with st.form(key=f"form_{target}"):
            ans = st.radio(data['q'], data['o'], index=None)
            if st.form_submit_button("Neutraliser"):
                if ans == data['c']:
                    st.session_state.solved[target] = True
                    st.session_state.target = None # Ferme la zone après réussite
                    st.balloons()
                    st.rerun()
                elif ans is not None:
                    st.error("Action incorrecte. Le danger se propage...")

# --- INVENTAIRE ET CODE FINAL ---
st.divider()
c_inv, c_code = st.columns([2, 1])

with c_inv:
    st.write("**Chiffres collectés :**")
    res = ""
    found = 0
    for k in ["pc", "fire", "elec", "water", "exit"]:
        if st.session_state.solved[k]:
            res += f" [{CHALLENGES[k]['digit']}] "
            found += 1
        else:
            res += " [?] "
    st.subheader(res)
    st.progress(found / 5)

with c_code:
    code_in = st.text_input("Code final", max_chars=5, placeholder="XXXXX")
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_in == CODE_SECRET:
            st.snow()
            st.success("BRAVO ! LE PORTAIL EST FERMÉ.")
        else:
            st.error("CODE INCORRECT")
