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

image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DÉFIS ---
CHALLENGES = {
    "pc": {
        "label": "💻 Ordinateur", 
        "q": "Un PC est déverrouillé en l'absence du collègue. Que faites-vous ?", 
        "o": ["Je verrouille (Win + L)", "J'éteins l'écran", "Je ne touche à rien"], 
        "c": "Je verrouille (Win + L)", 
        "d": "4", 
        "m": "Le verrouillage est la première barrière contre le vol de données ou l'usurpation d'identité."
    },
    "fire": {
        "label": "🔥 Poubelle", 
        "q": "Début d'incendie dans la corbeille ! Quel extincteur utiliser ?", 
        "o": ["Eau pulvérisée", "CO2", "Sable"], 
        "c": "Eau pulvérisée", 
        "d": "1", 
        "m": "L'eau pulvérisée est idéale pour les feux de solides (papier, carton)."
    },
    "elec": {
        "label": "⚡ Électricité", 
        "q": "La multiprise crépite. Quel est le risque majeur ?", 
        "o": ["Électrisation et incendie", "Simple panne", "Mauvaises ondes"], 
        "c": "Électrisation et incendie", 
        "d": "9", 
        "m": "Une prise surchargée est la cause n°1 des incendies de bureau."
    },
    "water": {
        "label": "💧 Sol Mouillé", 
        "q": "Une flaque visqueuse est au sol. Quelle est la priorité ?", 
        "o": ["Balisage et zone d'exclusion", "L'essuyer avec du papier", "Sauter par-dessus"], 
        "c": "Balisage et zone d'exclusion", 
        "d": "8", 
        "m": "La chute de plain-pied est l'accident le plus fréquent au travail."
    },
    "exit": {
        "label": "🚪 Issue de secours", 
        "q": "Des cartons bloquent la sortie. Est-ce toléré ?", 
        "o": ["Jamais, l'accès doit être libre", "Oui, si c'est temporaire", "Seulement la nuit"], 
        "c": "Jamais, l'accès doit être libre", 
        "d": "3", 
        "m": "En cas d'évacuation, chaque seconde compte. Rien ne doit gêner le passage."
    }
}

CODE_SECRET = "41983"

# --- INITIALISATION SESSION STATE ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'target' not in st.session_state:
    st.session_state.target = None

# --- STYLE CSS (Stranger Things + Correction Hitboxes) ---
st.markdown(f"""
    <style>
    /* Thème Noir et Rouge */
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

    /* On cache les boutons Streamlit et on les positionne sur l'image */
    div[data-testid="stBaseButton-secondary"] {{
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        min-height: unset !important;
    }}
    
    /* Effet au survol des zones cliquables */
    div[data-testid="stBaseButton-secondary"]:hover {{
        background-color: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid red !important;
    }}

    /* Positionnement absolu des wrappers de boutons */
    .hitbox {{ position: absolute; z-index: 1000; display: block; }}

    #area-fire {{ top: 60%; left: 58%; width: 7%; height: 15%; }}
    #area-elec {{ top: 78%; left: 45%; width: 9%; height: 10%; }}
    #area-water {{ top: 70%; left: 53%; width: 9%; height: 13%; }}
    #area-exit {{ top: 40%; left: 40%; width: 9%; height: 20%; }}
    #area-pc   {{ top: 48%; left: 68%; width: 8%; height: 10%; }}

    /* Supprimer l'espace blanc sous l'image causé par les boutons */
    .stButton {{ line-height: 0; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.markdown("<p style='text-align:center;'>Cliquez sur les anomalies dans l'image pour neutraliser les menaces.</p>", unsafe_allow_html=True)

# Conteneur Image
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

# Placement des boutons "Hitbox"
# On utilise des IDs pour que le CSS les place précisément
st.markdown('<div id="area-pc" class="hitbox">', unsafe_allow_html=True)
if st.button(" ", key="btn_pc"): st.session_state.target = "pc"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="area-fire" class="hitbox">', unsafe_allow_html=True)
if st.button(" ", key="btn_fire"): st.session_state.target = "fire"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="area-elec" class="hitbox">', unsafe_allow_html=True)
if st.button(" ", key="btn_elec"): st.session_state.target = "elec"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="area-water" class="hitbox">', unsafe_allow_html=True)
if st.button(" ", key="btn_water"): st.session_state.target = "water"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="area-exit" class="hitbox">', unsafe_allow_html=True)
if st.button(" ", key="btn_exit"): st.session_state.target = "exit"
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
        st.info(data['m'])
    else:
        with st.form(key=f"form_{target}"):
            ans = st.radio(data['q'], data['o'], index=None)
            if st.form_submit_button("Appliquer la procédure"):
                if ans == data['c']:
                    st.session_state.solved[target] = True
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
    for k in ["pc", "fire", "elec", "water", "exit"]: # Ordre du code
        if st.session_state.solved[k]:
            res += f" [{CHALLENGES[k]['digit']}] "
            found += 1
        else:
            res += " [?] "
    st.subheader(res)
    st.progress(found / 5)

with c_code:
    code_in = st.text_input("Code de fermeture", max_chars=5, placeholder="XXXXX")
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_in == CODE_SECRET:
            st.snow()
            st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
        else:
            st.error("CODE INCORRECT")
