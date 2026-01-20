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
        "q": "Un PC est déverrouillé. Que faites-vous ?", 
        "o": ["Je verrouille (Win + L)", "J'éteins l'écran", "Je ne touche à rien"], 
        "c": "Je verrouille (Win + L)", 
        "d": "4", 
        "m": "Le verrouillage est essentiel pour empêcher l'usurpation d'identité."
    },
    "fire": {
        "label": "🔥 Poubelle", 
        "q": "Début d'incendie ! Quel extincteur utiliser ?", 
        "o": ["Eau pulvérisée", "CO2", "Sable"], 
        "c": "Eau pulvérisée", 
        "d": "1", 
        "m": "L'eau pulvérisée refroidit les foyers de feux solides (papier)."
    },
    "elec": {
        "label": "⚡ Électricité", 
        "q": "La multiprise crépite. Risque majeur ?", 
        "o": ["Électrisation et incendie", "Simple panne", "Mauvaises ondes"], 
        "c": "Électrisation et incendie", 
        "d": "9", 
        "m": "Une prise surchargée est la cause n°1 des incendies de bureau."
    },
    "water": {
        "label": "💧 Sol Mouillé", 
        "q": "Une flaque visqueuse au sol. Priorité ?", 
        "o": ["Balisage et zone d'exclusion", "L'essuyer vite", "Sauter"], 
        "c": "Balisage et zone d'exclusion", 
        "d": "8", 
        "m": "La chute de plain-pied est l'accident le plus fréquent."
    },
    "exit": {
        "label": "🚪 Issue de secours", 
        "q": "Des cartons bloquent la sortie. Acceptable ?", 
        "o": ["Jamais", "Si c'est temporaire", "La nuit"], 
        "c": "Jamais", 
        "d": "3", 
        "m": "Une issue doit être libre en permanence pour permettre l'évacuation."
    }
}

CODE_SECRET = "41983"

# --- INITIALISATION SESSION STATE ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'target' not in st.session_state:
    st.session_state.target = None

# --- STYLE CSS RADICAL (Stranger Things + Fix Boutons) ---
st.markdown(f"""
    <style>
    /* Global */
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
    }}

    /* Cache TOUS les conteneurs de boutons Streamlit pour qu'ils ne prennent pas de place en bas */
    div[data-testid="stButton"] {{
        position: absolute;
        margin: 0;
        padding: 0;
    }}

    /* Rend le bouton lui-même invisible mais cliquable */
    button[kind="secondary"] {{
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        width: 100% !important;
        height: 100% !important;
        min-height: unset !important;
        box-shadow: none !important;
    }}

    /* Effet au survol des zones */
    button[kind="secondary"]:hover {{
        background: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid red !important;
    }}

    /* Positionnement des zones (Ajusté selon image_6c2f47.jpg) */
    .hitbox-pc    {{ top: 44%; left: 68%; width: 8%; height: 10%; }}
    .hitbox-fire  {{ top: 58%; left: 58%; width: 6%; height: 15%; }}
    .hitbox-elec  {{ top: 76%; left: 45%; width: 9%; height: 9%; }}
    .hitbox-water {{ top: 68%; left: 53%; width: 9%; height: 12%; }}
    .hitbox-exit  {{ top: 42%; left: 40%; width: 8%; height: 20%; }}

    /* Fix pour empêcher les boutons de s'empiler en bas */
    .stVerticalBlock {{ gap: 0rem; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.markdown("<p style='text-align:center;'>Cliquez sur les anomalies de l'image pour neutraliser les menaces.</p>", unsafe_allow_html=True)

# Zone Image Interactive
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

# Les boutons sont injectés dans des divs positionnées
st.markdown('<div class="hitbox-pc">', unsafe_allow_html=True)
if st.button(" ", key="btn_pc"): st.session_state.target = "pc"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hitbox-fire">', unsafe_allow_html=True)
if st.button(" ", key="btn_fire"): st.session_state.target = "fire"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hitbox-elec">', unsafe_allow_html=True)
if st.button(" ", key="btn_elec"): st.session_state.target = "elec"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hitbox-water">', unsafe_allow_html=True)
if st.button(" ", key="btn_water"): st.session_state.target = "water"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hitbox-exit">', unsafe_allow_html=True)
if st.button(" ", key="btn_exit"): st.session_state.target = "exit"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- RÉSOLUTION DU DÉFI ---
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
    # On affiche les chiffres dans l'ordre PC-Feu-Elec-Eau-Exit
    for k in ["pc", "fire", "elec", "water", "exit"]:
        if st.session_state.solved[k]:
            res += f" [{CHALLENGES[k]['digit']}] "
            found += 1
        else:
            res += " [?] "
    st.subheader(res)
    st.progress(found / 5)

with c_code:
    code_in = st.text_input("Saisir le code", max_chars=5, placeholder="XXXXX")
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_in == CODE_SECRET:
            st.snow()
            st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
        else:
            st.error("CODE INCORRECT")
