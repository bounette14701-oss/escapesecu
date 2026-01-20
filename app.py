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

# Assurez-vous que le fichier est bien nommé 'stranger_office.png'
image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DÉFIS ---
CHALLENGES = {
    "fire_bin": {
        "label": "🔥 La Poubelle Infernale",
        "question": "Des flammes sortent de la corbeille ! Quel extincteur utiliser ?",
        "options": ["Eau pulvérisée", "CO2 (Neige carbonique)", "Sable"],
        "correct": "Eau pulvérisée",
        "digit": "1",
        "myth": "L'eau pulvérisée est idéale pour les feux de classe A (solides comme le papier)."
    },
    "sparks": {
        "label": "⚡ Le Poteau Électrique",
        "question": "La multiprise crépite. Quel est le risque majeur ?",
        "options": ["Électrisation et incendie", "Simple panne", "Mauvaises ondes"],
        "correct": "Électrisation et incendie",
        "digit": "9",
        "myth": "Une prise surchargée est la cause n°1 des incendies de bureau."
    },
    "wet_floor": {
        "label": "💧 La Substance Suspecte",
        "question": "Une flaque visqueuse est au sol. Quelle est la priorité ?",
        "options": ["Balisage et zone d'exclusion", "Nettoyer avec son écharpe", "L'ignorer"],
        "correct": "Balisage et zone d'exclusion",
        "digit": "8",
        "myth": "La chute de plain-pied représente une part énorme des accidents de travail."
    },
    "exit_blocked": {
        "label": "🚪 Le Portail Obstrué",
        "question": "Des cartons bloquent l'issue de secours. Est-ce toléré ?",
        "options": ["Jamais, l'accès doit être libre", "Oui, si c'est temporaire", "Oui, si on est fort"],
        "correct": "Jamais, l'accès doit être libre",
        "digit": "3",
        "myth": "En cas d'évacuation, un obstacle même léger peut coûter des vies."
    },
    "unlocked_pc": {
        "label": "💻 Session Ouverte",
        "question": "Un PC est déverrouillé en l'absence du collègue. Que faites-vous ?",
        "options": ["Je verrouille (Win + L)", "Je ferme les onglets", "Je ne touche à rien"],
        "correct": "Je verrouille (Win + L)",
        "digit": "4",
        "myth": "Le verrouillage est la première barrière contre l'usurpation d'identité et le vol de données."
    }
}

CODE_FINAL_CORRECT = "19834"

# --- INITIALISATION SESSION STATE ---
if 'solved' not in st.session_state or set(st.session_state.solved.keys()) != set(CHALLENGES.keys()):
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
    st.session_state.current_target = None

# --- STYLE CSS (Stranger Things + Invisible Buttons) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #e2e2e2; }}
    h1 {{ color: #ff0000 !important; text-align: center; text-shadow: 0 0 10px #ff0000; font-family: 'Arial Black'; }}
    
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

    /* Positionnement des boutons invisibles */
    .st-btn-wrap {{ position: absolute; z-index: 100; }}
    .st-btn-wrap button {{
        width: 100% !important; height: 100% !important;
        background: transparent !important; color: transparent !important;
        border: none !important; cursor: pointer;
    }}
    .st-btn-wrap button:hover {{
        background: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid red !important;
    }}

    #wrap-fire {{ top: 58%; left: 58%; width: 7%; height: 14%; }}
    #wrap-elec {{ top: 75%; left: 44%; width: 10%; height: 10%; }}
    #wrap-water {{ top: 68%; left: 53%; width: 9%; height: 13%; }}
    #wrap-exit {{ top: 43%; left: 41%; width: 8%; height: 19%; }}
    #wrap-pc   {{ top: 45%; left: 68%; width: 7%; height: 9%; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.caption("Cliquez sur les anomalies dans l'image pour les neutraliser.")

# Conteneur Image avec Boutons
st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

# On place les boutons réels de Streamlit dans les div positionnées par le CSS
with st.container():
    st.markdown('<div id="wrap-fire" class="st-btn-wrap">', unsafe_allow_html=True)
    if st.button(" ", key="btn_fire"): st.session_state.current_target = "fire_bin"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="wrap-elec" class="st-btn-wrap">', unsafe_allow_html=True)
    if st.button(" ", key="btn_elec"): st.session_state.current_target = "sparks"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="wrap-water" class="st-btn-wrap">', unsafe_allow_html=True)
    if st.button(" ", key="btn_water"): st.session_state.current_target = "wet_floor"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="wrap-exit" class="st-btn-wrap">', unsafe_allow_html=True)
    if st.button(" ", key="btn_exit"): st.session_state.current_target = "exit_blocked"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="wrap-pc" class="st-btn-wrap">', unsafe_allow_html=True)
    if st.button(" ", key="btn_pc"): st.session_state.current_target = "unlocked_pc"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- ZONE DE DÉFI ---
if st.session_state.current_target:
    target = st.session_state.current_target
    data = CHALLENGES[target]
    st.divider()
    
    st.subheader(f"📍 {data['label']}")
    if st.session_state.solved[target]:
        st.success(f"✅ Menace neutralisée. Indice découvert : **{data['digit']}**")
        st.info(data['myth'])
    else:
        with st.form(key=f"f_{target}"):
            ans = st.radio(data['question'], data['options'])
            if st.form_submit_button("Appliquer la procédure"):
                if ans == data['correct']:
                    st.session_state.solved[target] = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Erreur ! Le danger s'aggrave...")

# --- INVENTAIRE ET SORTIE ---
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.write("**Indices collectés :**")
    res = ""
    found = 0
    for k, v in CHALLENGES.items():
        if st.session_state.solved[k]:
            res += f" `{v['digit']}` "
            found += 1
        else:
            res += " `?` "
    st.subheader(res)
    st.progress(found / 5)

with c2:
    code_input = st.text_input("Code final (5 chiffres)", max_chars=5)
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_input == CODE_FINAL_CORRECT:
            st.snow()
            st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
        else:
            st.error("CODE INCORRECT")
