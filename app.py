import streamlit as st
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Hawkins Lab - Système de Sécurité",
    layout="wide",
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

# Assurez-vous que le nom du fichier correspond à votre image Stranger Things
image_path = "stranger_office.png" 
img_base64 = get_image_base64(image_path)

# --- LOGIQUE DES DÉFIS ---
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
        "options": ["Sauter par-dessus", "Balisage et zone d'exclusion", "Essuyer avec ses mouchoirs"],
        "correct": "Balisage et zone d'exclusion",
        "digit": "8",
        "myth": "La chute de plain-pied est l'accident le plus fréquent au bureau."
    },
    "exit_blocked": {
        "label": "🚪 Le Portail Obstrué",
        "question": "Des cartons bloquent l'issue de secours. Sous quel prétexte est-ce autorisé ?",
        "options": ["Si c'est pour moins de 10 minutes", "Si on a la clé sur soi", "Aucun prétexte, c'est interdit"],
        "correct": "Aucun prétexte, c'est interdit",
        "digit": "3",
        "myth": "En cas de fumée, chaque seconde compte. Une issue doit être dégagée 24h/24."
    }
}

CODE_FINAL_CORRECT = "1983"

# --- INITIALISATION ET PROTECTION CONTRE KEYERROR ---
# Cette section vérifie que session_state est synchro avec le dictionnaire CHALLENGES
if 'solved' not in st.session_state or set(st.session_state.solved.keys()) != set(CHALLENGES.keys()):
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
    st.session_state.current_target = None

# --- STYLE CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #050505;
        color: #e2e2e2;
    }}
    .stMarkdown h1 {{
        color: #ff0000 !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px #ff0000;
        font-family: 'Arial Black', sans-serif;
    }}
    .image-container {{
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: cover;
        background-position: center;
        border: 2px solid #333;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.2);
    }}
    .hitbox {{
        position: absolute;
        background: rgba(255, 0, 0, 0.0);
        cursor: pointer;
        border: none;
        z-index: 100;
    }}
    .hitbox:hover {{
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid red;
    }}
    /* Positionnement des zones */
    .area-fire {{ top: 60%; left: 58%; width: 6%; height: 15%; }}
    .area-elec {{ top: 75%; left: 44%; width: 10%; height: 10%; }}
    .area-water {{ top: 70%; left: 53%; width: 8%; height: 12%; }}
    .area-exit {{ top: 45%; left: 40%; width: 8%; height: 20%; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.title("STRANGER OFFICE")
st.write("---")

col_main, col_tools = st.columns([3, 1])

with col_main:
    # Overlay interactif
    st.markdown(f"""
        <div class="image-container">
            <button class="hitbox area-fire" onclick="window.location.href='#danger'"></button>
            <button class="hitbox area-elec" onclick="window.location.href='#danger'"></button>
            <button class="hitbox area-water" onclick="window.location.href='#danger'"></button>
            <button class="hitbox area-exit" onclick="window.location.href='#danger'"></button>
        </div>
    """, unsafe_allow_html=True)
    
    # Boutons d'inspection (nécessaires pour capturer l'action dans Streamlit)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🔍 Inspecter Poubelle"): st.session_state.current_target = "fire_bin"
    with c2: 
        if st.button("🔍 Inspecter Élec"): st.session_state.current_target = "sparks"
    with c3: 
        if st.button("🔍 Inspecter Sol"): st.session_state.current_target = "wet_floor"
    with c4: 
        if st.button("🔍 Inspecter Issue"): st.session_state.current_target = "exit_blocked"

    # Zone de défi
    if st.session_state.current_target:
        target = st.session_state.current_target
        data = CHALLENGES[target]
        
        st.subheader(f"📍 {data['label']}", anchor="danger")
        
        if st.session_state.solved[target]:
            st.success(f"Défi complété ! Chiffre trouvé : {data['digit']}")
            st.info(data['myth'])
        else:
            ans = st.radio(data['question'], data['options'], key=f"radio_{target}", index=None)
            if st.button("Neutraliser le danger", key=f"btn_{target}"):
                if ans == data['correct']:
                    st.session_state.solved[target] = True
                    st.rerun()
                elif ans is not None:
                    st.error("Action incorrecte ! Le danger se propage...")

with col_tools:
    st.subheader("🕵️ Inventaire")
    progress_count = 0
    for k in CHALLENGES.keys():
        if st.session_state.solved[k]:
            st.write(f"✅ {CHALLENGES[k]['label']} : **{CHALLENGES[k]['digit']}**")
            progress_count += 1
        else:
            st.write(f"❌ {CHALLENGES[k]['label']} : ?")
    
    st.progress(progress_count / len(CHALLENGES))
    st.divider()
    
    # Digicode
    input_code = st.text_input("CODE DE DÉVERROUILLAGE", max_chars=4, placeholder="XXXX")
    if st.button("QUITTER L'UPSIDE DOWN"):
        if input_code == CODE_FINAL_CORRECT:
            st.balloons()
            st.success("BRAVO ! Portail fermé.")
        else:
            st.error("Code erroné...")
