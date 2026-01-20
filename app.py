import streamlit as st
import base64

# --- CONFIGURATION DE LA PAGE ET DU THÈME ---
st.set_page_config(
    page_title="Hawkins Lab - Sécurité",
    layout="wide",
    page_icon="🔦"
)

# --- FONCTION POUR CHARGER L'IMAGE EN BASE64 (Pour le CSS) ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        st.error(f"Erreur : L'image '{path}' est introuvable. Assurez-vous qu'elle est dans le dossier.")
        return ""

# Chargez votre image (assurez-vous du nom du fichier)
image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LES DÉFIS ET ÉNIGMES (Basés sur l'image) ---
CHALLENGES = {
    "fire_bin": {
        "label": "🔥 Poubelle en feu",
        "question": "ALERTE ! Une poubelle brûle. Quelle est la PREMIÈRE action ?",
        "options": ["Chercher un extincteur", "Donner l'alarme et évacuer", "Jeter de l'eau dessus"],
        "correct": "Donner l'alarme et évacuer",
        "digit": "6",
        "myth": "Le réflexe 'héroïque' de vouloir éteindre le feu seul met votre vie en danger. Alertez d'abord."
    },
    "sparks": {
        "label": "⚡ Multiprise qui étincelle",
        "question": "La multiprise près du poteau fait des étincelles. Que faire ?",
        "options": ["Couper le courant au disjoncteur si possible", "Débrancher rapidement la prise murale", "Ne rien toucher et appeler la maintenance"],
        "correct": "Couper le courant au disjoncteur si possible",
        "digit": "6",
        "myth": "Toucher une multiprise défaillante est dangereux. Isoler la source d'énergie en amont est plus sûr."
    },
    "wet_floor": {
        "label": "💧 Sol inondé",
        "question": "Il y a une grande flaque d'eau et un panneau 'Sol Glissant'.",
        "options": ["Je marche prudemment sur la pointe des pieds", "Je contourne largement la zone", "Je cours pour passer vite"],
        "correct": "Je contourne largement la zone",
        "digit": "1",
        "myth": "Même avec un panneau, le risque de chute est réel. Évitez totalement la zone."
    },
    "falling_boxes": {
        "label": "📦 Cartons instables",
        "question": "Ces cartons bloquent le passage et menacent de tomber.",
        "options": ["Je tente de les repousser avec le pied", "Je passe vite en protégeant ma tête", "Je signale le danger pour qu'ils soient rangés"],
        "correct": "Je signale le danger pour qu'ils soient rangés",
        "digit": "9",
        "myth": "Manipuler une pile instable peut provoquer l'accident que vous voulez éviter."
    }
}

CODE_FINAL_CORRECT = "6619"

# --- STYLE CSS "STRANGER THINGS" ET OVERLAY ---
st.markdown(f"""
    <style>
    /* Thème Global Dark / Stranger Things */
    .stApp {{
        background-color: #0a0a0f;
        color: #c41e3a; /* Rouge Stranger Things */
    }}
    h1, h2, h3 {{
        color: #ff3333 !important;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000;
        font-family: 'Courier New', monospace;
    }}
    .stButton button {{
        background-color: #222;
        color: #ff3333;
        border: 2px solid #ff3333;
        box-shadow: 0 0 5px #ff0000;
    }}
    .stButton button:hover {{
        background-color: #ff3333;
        color: white;
    }}

    /* --- CSS POUR L'OVERLAY D'IMAGE --- */
    /* Le conteneur principal qui détient l'image en fond */
    .image-container {{
        position: relative;
        width: 100%;
        /* Astuce pour maintenir le ratio de l'image (ex: 16/9 = 56.25%) */
        padding-bottom: 56.25%; 
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        border: 3px solid #ff3333;
        box-shadow: 0 0 20px #ff0000 inset;
        border-radius: 10px;
        overflow: hidden;
    }}

    /* Le style des boutons "invisibles" */
    .hitbox-btn {{
        position: absolute;
        opacity: 0.0; /* Rendre le bouton transparent */
        z-index: 10;
        cursor: pointer;
    }}
    /* Pour le debug : changez opacity à 0.5 pour voir les zones */
    .hitbox-btn:hover {{
        opacity: 0.3; /* Petit effet au survol pour aider le joueur */
        background-color: rgba(255, 0, 0, 0.5) !important;
        border: 2px solid red !important;
    }}

    /* --- POSITIONNEMENT DES ZONES (En % par rapport à l'image) --- */
    /* Vous devrez peut-être ajuster ces valeurs légèrement selon votre image exacte */
    .zone-fire {{ top: 58%; left: 59%; width: 5%; height: 12%; }}
    .zone-sparks {{ top: 77%; left: 45%; width: 8%; height: 8%; }}
    .zone-wet {{ top: 68%; left: 54%; width: 8%; height: 15%; }}
    .zone-boxes {{ top: 41%; left: 41%; width: 8%; height: 20%; }}

    </style>
""", unsafe_allow_html=True)

# --- GESTION DE L'ÉTAT (SESSION STATE) ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'current_inspect' not in st.session_state:
    st.session_state.current_inspect = None

# --- INTERFACE PRINCIPALE ---
st.title("🔦 L'Upside Down du Bureau")
st.markdown("### Trouvez les 4 failles de sécurité avant que le portail ne s'ouvre...")

col_game, col_sidebar = st.columns([3, 1])

with col_game:
    # C'est ici que la magie opère. On crée un conteneur HTML pour l'image,
    # et on y place des boutons Streamlit avec des classes CSS spécifiques pour le positionnement.
    
    # Conteneur de l'image
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    
    # --- LES BOUTONS INVISIBLES SUR L'IMAGE ---
    # On utilise des colonnes vides pour placer les boutons sans casser le layout, 
    # et on injecte le style via le paramètre args des boutons (hack courant).
    
    # Bouton Feu
    with st.container():
        st.markdown('<div class="hitbox-btn zone-fire">', unsafe_allow_html=True)
        if st.button("Inspecter Feu", key="btn_fire"):
             st.session_state.current_inspect = "fire_bin"
        st.markdown('</div>', unsafe_allow_html=True)

    # Bouton Étincelles
    with st.container():
        st.markdown('<div class="hitbox-btn zone-sparks">', unsafe_allow_html=True)
        if st.button("Inspecter Elec", key="btn_sparks"):
             st.session_state.current_inspect = "sparks"
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Bouton Sol Mouillé
    with st.container():
        st.markdown('<div class="hitbox-btn zone-wet">', unsafe_allow_html=True)
        if st.button("Inspecter Eau", key="btn_wet"):
             st.session_state.current_inspect = "wet_floor"
        st.markdown('</div>', unsafe_allow_html=True)

    # Bouton Cartons
    with st.container():
        st.markdown('<div class="hitbox-btn zone-boxes">', unsafe_allow_html=True)
        if st.button("Inspecter Cartons", key="btn_boxes"):
             st.session_state.current_inspect = "falling_boxes"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Fin du image-container

    # --- ZONE D'INSPECTION (S'affiche sous l'image quand on clique) ---
    if st.session_state.current_inspect:
        st.divider()
        key = st.session_state.current_inspect
        data = CHALLENGES[key]
        
        st.subheader(f"Analyse : {data['label']}")
        
        if st.session_state.solved[key]:
            st.success(f"✅ Menace neutralisée. Chiffre mémorisé : {data['digit']}")
        else:
            # Utilisation de radio avec un style personnalisé pour le thème sombre
            choice = st.radio(data["question"], options=data["options"], index=None)
            
            if st.button("Valider l'action"):
                if choice == data["correct"]:
                    st.session_state.solved[key] = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Mauvaise décision ! Le danger persiste.")
                    st.warning(data["myth"])

with col_sidebar:
    st.sidebar.title("📻 Talkie-Walkie")
    st.sidebar.markdown("Indices récupérés :")
    
    solved_count = 0
    for key, data in CHALLENGES.items():
        if st.session_state.solved[key]:
            st.sidebar.markdown(f"✅ **{data['label']}** : `{data['digit']}`")
            solved_count += 1
        else:
            st.sidebar.markdown(f"❌ {data['label']} (Inconnu)")
            
    st.sidebar.divider()
    st.sidebar.progress(solved_count / 4, text=f"Progression : {solved_count}/4")
    st.sidebar.divider()

    # Digicode Final
    st.sidebar.subheader("🔐 Fermer le Portail")
    user_code = st.sidebar.text_input("Entrez le code à 4 chiffres :", max_chars=4, type="password")
    
    if st.sidebar.button("TENTER LA FERMETURE"):
        if user_code == CODE_FINAL_CORRECT:
            st.snow() # Effet "spores" de l'upside down
            st.sidebar.success("PORTAIL FERMÉ ! Le bureau est sécurisé. Bien joué.")
        else:
            st.sidebar.error("CODE ERRONÉ. Le Mind Flayer approche...")

# --- INSTRUCTIONS POUR L'ANIMATEUR (A cacher lors de la démo) ---
# st.divider()
# with st.expander("🔧 Debug & Ajustement des Zones"):
#     st.write("Si les clics ne correspondent pas aux objets, ajustez les pourcentages (top, left, width, height) dans la section CSS '.zone-fire', '.zone-sparks', etc.")
#     st.write("Passez 'opacity: 0.0' à 'opacity: 0.5' dans la classe '.hitbox-btn' pour voir les zones rouges.")
