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

# Assurez-vous que votre image Stranger Things s'appelle 'stranger_office.png'
image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DANGERS (Basée sur l'image 6c2f47.jpg) ---
CHALLENGES = {
    "exit": {
        "name": "Issue de Secours",
        "q": "Des cartons bloquent l'issue 'EXIT BLOCKED'. Est-ce acceptable ?",
        "o": ["Jamais, l'accès doit être libre", "Seulement si c'est temporaire", "Si on a la clé"],
        "a": "Jamais, l'accès doit être libre",
        "d": "4",
        "info": "Une issue de secours doit être dégagée 24h/24 sans exception."
    },
    "elec": {
        "name": "Multiprise au sol",
        "q": "Une multiprise traîne au sol près du passage. Quel est le risque ?",
        "o": ["Incendie et chute", "Simple panne", "Aucun risque"],
        "a": "Incendie et chute",
        "d": "1",
        "info": "Les câbles au sol sont une cause majeure de chute de plain-pied et d'incendie."
    },
    "pc": {
        "name": "PC déverrouillé",
        "q": "Un ordinateur est allumé et déverrouillé sans surveillance. Que faites-vous ?",
        "o": ["Je le verrouille (Win+L)", "Je l'éteins", "Je ne fais rien"],
        "a": "Je le verrouille (Win+L)",
        "d": "9",
        "info": "Le verrouillage protège les données et votre identité numérique."
    },
    "sac": {
        "name": "Sac dans l'allée",
        "q": "Un sac à dos est posé en plein milieu de l'allée de circulation. Où doit-il être ?",
        "o": ["Sous le bureau ou dans un casier", "Dans le passage", "Sur une chaise libre"],
        "a": "Sous le bureau ou dans un casier",
        "d": "8",
        "info": "Gardez les zones de circulation libres de tout obstacle pour éviter les chutes."
    }
}

FINAL_CODE = "4198"

# --- INITIALISATION SESSION STATE ---
if 'solved' not in st.session_state:
    st.session_state.solved = set()
if 'current_target' not in st.session_state:
    st.session_state.current_target = None

# --- STYLE CSS AVANCÉ (Stranger Things + Correction Hitboxes) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #e2e2e2; font-family: 'Courier New', monospace; }}
    h1 {{ color: #ff0000 !important; text-align: center; text-shadow: 0 0 10px #ff0000; font-family: 'Arial Black'; }}
    
    /* Conteneur de l'image interactive */
    .game-box {{
        position: relative;
        width: 100%;
        aspect-ratio: 16 / 9;
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        border: 2px solid #ff0000;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
        margin-bottom: 20px;
    }}

    /* Cache totalement les boutons Streamlit mais les garde cliquables */
    div[data-testid="stButton"] button {{
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 100% !important;
        box-shadow: none !important;
        cursor: pointer;
    }}

    /* Effet au survol (Feedback visuel) */
    div[data-testid="stButton"] button:hover {{
        background: rgba(255, 0, 0, 0.15) !important;
        border: 1px dashed red !important;
    }}

    /* Positionnement des zones (Coordonnées ajustées pour 6c2f47.jpg) */
    .hitbox {{ position: absolute; z-index: 100; }}
    
    #exit {{ top: 0%; left: 3%; width: 10%; height: 22%; }}
    #elec {{ top: 74%; left: 42%; width: 14%; height: 12%; }}
    #pc   {{ top: 45%; left: 68%; width: 10%; height: 12%; }}
    #sac  {{ top: 72%; left: 71%; width: 13%; height: 18%; }}

    /* Masquer le texte parasite sous les boutons */
    .stMarkdown div p {{ margin-bottom: 0px; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.markdown("<p style='text-align:center;'>Cliquez sur les anomalies de l'image pour neutraliser les menaces.</p>", unsafe_allow_html=True)

# --- RENDU DE L'IMAGE AVEC BOUTONS SUPERPOSÉS ---
# On crée un conteneur et on y place les boutons Streamlit via des div identifiées
st.markdown('<div class="game-box">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div id="exit" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_exit"): st.session_state.current_target = "exit"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="elec" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_elec"): st.session_state.current_target = "elec"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="pc" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_pc"): st.session_state.current_target = "pc"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="sac" class="hitbox">', unsafe_allow_html=True)
    if st.button(" ", key="btn_sac"): st.session_state.current_target = "sac"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- ZONE DE RÉSOLUTION ---
if st.session_state.current_target:
    target = st.session_state.current_target
    data = CHALLENGES[target]
    st.write("---")
    st.subheader(f"🔍 Analyse : {data['name']}")
    
    if target in st.session_state.solved:
        st.success(f"✅ Menace neutralisée. Chiffre : **{data['digit']}**")
        st.info(data['info'])
    else:
        with st.form(key=f"form_{target}"):
            ans = st.radio(data['q'], data['o'], index=None)
            if st.form_submit_button("Appliquer la procédure"):
                if ans == data['a']:
                    st.session_state.solved.add(target)
                    st.balloons()
                    st.rerun()
                elif ans is not None:
                    st.error("Action incorrecte. Le danger persiste.")

# --- INVENTAIRE ET CODE FINAL ---
st.divider()
c_inv, c_code = st.columns([2, 1])

with c_inv:
    st.write("**Chiffres collectés :**")
    res = ""
    found = 0
    for k in ["exit", "elec", "pc", "sac"]:
        if k in st.session_state.solved:
            res += f" [{CHALLENGES[k]['digit']}] "
            found += 1
        else:
            res += " [?] "
    st.subheader(res)
    st.progress(found / 4)

with c_code:
    code_in = st.text_input("Code de fermeture", max_chars=4, placeholder="XXXX")
    if st.button("FERMER LE PORTAIL", type="primary", use_container_width=True):
        if code_in == FINAL_CODE:
            st.snow()
            st.success("BRAVO ! LE BUREAU EST SÉCURISÉ.")
        else:
            st.error("CODE INCORRECT")
