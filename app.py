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

# Assurez-vous que votre image est nommée 'stranger_office.png'
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
        "m": "Le verrouillage est la première barrière contre le vol de données."
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

# --- STYLE CSS (Thème Stranger Things) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #e2e2e2; }}
    h1 {{ color: #ff0000 !important; text-align: center; text-shadow: 0 0 10px #ff0000; font-family: 'Arial Black'; }}
    
    /* Conteneur de l'image interactive */
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

    /* Positionnement des zones cliquables invisibles */
    .hitbox {{
        position: absolute;
        background: rgba(255, 0, 0, 0.0);
        border: none;
        cursor: pointer;
        z-index: 100;
    }}
    .hitbox:hover {{
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid red;
    }}

    /* Coordonnées des zones en % */
    #area-fire {{ top: 58%; left: 58%; width: 7%; height: 14%; }}
    #area-elec {{ top: 75%; left: 44%; width: 10%; height: 10%; }}
    #area-water {{ top: 68%; left: 53%; width: 9%; height: 13%; }}
    #area-exit {{ top: 43%; left: 41%; width: 8%; height: 19%; }}
    #area-pc   {{ top: 45%; left: 68%; width: 7%; height: 9%; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.markdown("<p style='text-align:center;'>Analysez l'image et cliquez sur les anomalies pour fermer le portail.</p>", unsafe_allow_html=True)

# Affichage de l'image avec zones réactives (Hitboxes)
# Note : On utilise des boutons Streamlit invisibles superposés
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5) # Pour forcer la création des boutons dans le DOM

# On injecte les boutons Streamlit dans les zones CSS
with st.container():
    # PC
    st.markdown('<div id="area-pc" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_pc"): st.session_state.target = "pc"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FEU
    st.markdown('<div id="area-fire" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_fire"): st.session_state.target = "fire"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ELEC
    st.markdown('<div id="area-elec" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_elec"): st.session_state.target = "elec"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # EAU
    st.markdown('<div id="area-water" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_water"): st.session_state.target = "water"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # EXIT
    st.markdown('<div id="area-exit" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_exit"): st.session_state.target = "exit"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- RÉSOLUTION DU DÉFI ---
if st.session_state.target:
    target = st.session_state.target
    data = CHALLENGES[target]
    st.write("---")
    st.subheader(f"🔍 Analyse : {data['label']}")
    
    if st.session_state.solved[target]:
        st.success(f"Défi réussi ! Chiffre : **{data['digit']}**")
        st.info(data['m'])
    else:
        with st.form(key=f"form_{target}"):
            ans = st.radio(data['q'], data['o'], index=None)
            if st.form_submit_button("Valider la procédure"):
                if ans == data['c']:
                    st.session_state.solved[target] = True
                    st.balloons()
                    st.rerun()
                elif ans is not None:
                    st.error("Action incorrecte. Le danger persiste.")

# --- INVENTAIRE ET CODE FINAL ---
st.write("---")
c_inv, c_code = st.columns([2, 1])

with c_inv:
    st.write("**Chiffres du portail :**")
    # Affichage des chiffres trouvés
    display = ""
    count = 0
    for k in CHALLENGES.keys():
        if st.session_state.solved[k]:
            display += f" `{CHALLENGES[k]['digit']}` "
            count += 1
        else:
            display += " `?` "
    st.subheader(display)
    st.progress(count / 5)

with c_code:
    code_in = st.text_input("Saisir le code", max_chars=5, placeholder="XXXXX")
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_in == CODE_SECRET:
            st.snow()
            st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
        else:
            st.error("CODE ERRONÉ")
