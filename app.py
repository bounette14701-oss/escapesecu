import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Le Bureau Suspect - Escape Game Sécurité", layout="wide", page_icon="🕵️")

# --- PERSONNALISATION DES DÉFIS (DICTIONNAIRE) ---
# Vous pouvez changer les questions, les réponses et les chiffres du code ici.
CHALLENGES = {
    "multiprise": {
        "label": "🔌 La Multiprise",
        "question": "Peut-on brancher une multiprise sur une autre multiprise (montage en cascade) ?",
        "options": ["Oui, si la puissance totale est faible", "Non, jamais, risque d'incendie", "Seulement si elles sont de la même marque"],
        "correct": "Non, jamais, risque d'incendie",
        "digit": "5",
        "myth": "Le mythe : 'C'est pas grave si c'est juste pour un chargeur de téléphone'."
    },
    "ecran": {
        "label": "💻 L'Écran Allumé",
        "question": "Tu pars en pause café 5 minutes. Que fais-tu de ta session ?",
        "options": ["Je laisse tel quel", "J'éteins juste l'écran", "Je verrouille ma session (Win + L)"],
        "correct": "Je verrouille ma session (Win + L)",
        "digit": "2",
        "myth": "Le mythe : 'On est entre collègues, personne ne touchera à mon PC'."
    },
    "sac": {
        "label": "👜 Le Sac au Sol",
        "question": "Où doit-on ranger son sac ou ses câbles dans l'open space ?",
        "options": ["Sous le bureau, dans le passage", "Dans un casier ou sous le bureau (hors zone de circulation)", "Peu importe"],
        "correct": "Dans un casier ou sous le bureau (hors zone de circulation)",
        "digit": "8",
        "myth": "Le mythe : 'Les gens regardent où ils marchent'."
    },
    "sortie": {
        "label": "🚪 L'Issue de Secours",
        "question": "Un carton de livraison bloque l'issue de secours 'juste pour 1 heure'. Est-ce acceptable ?",
        "options": ["Oui, c'est temporaire", "Non, une issue doit être dégagée en permanence", "Oui, si on prévient les collègues"],
        "correct": "Non, une issue doit être dégagée en permanence",
        "digit": "4",
        "myth": "Le mythe : 'En cas d'incendie, on aura le temps de le pousser'."
    }
}

CODE_FINAL_CORRECT = "".join([v["digit"] for v in CHALLENGES.values()])

# --- STYLE CSS PERSONNALISÉ ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f0f2f6; }}
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        height: 80px;
        font-weight: bold;
        font-size: 18px;
        border: 2px solid #2e4053;
    }}
    .found-digit {{
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- GESTION DE L'ÉTAT (SESSION STATE) ---
if 'solved' not in st.session_state:
    st.session_state.solved = {k: False for k in CHALLENGES.keys()}
if 'digits_collected' not in st.session_state:
    st.session_state.digits_collected = {}

# --- INTERFACE PRINCIPALE ---
st.title("🕵️ Le Bureau Suspect")
st.markdown("### Objectif : Inspectez le bureau, débusquez les risques et trouvez le code de sortie !")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("Cliquez sur un objet suspect pour l'inspecter.")
    
    # Simulation de l'Open Space avec des boutons
    c1, c2 = st.columns(2)
    
    for i, (key, data) in enumerate(CHALLENGES.items()):
        with (c1 if i % 2 == 0 else c2):
            if st.button(data["label"], key=key):
                st.session_state.current_inspect = key

    # Zone d'inspection dynamique
    if 'current_inspect' in st.session_state:
        key = st.session_state.current_inspect
        data = CHALLENGES[key]
        
        st.divider()
        st.subheader(f"Inspection : {data['label']}")
        
        if st.session_state.solved[key]:
            st.success(f"✅ Défi relevé ! Le chiffre découvert est : **{data['digit']}**")
            st.info(data["myth"])
        else:
            choice = st.radio(data["question"], options=data["options"], index=None)
            if st.button("Valider la réponse"):
                if choice == data["correct"]:
                    st.session_state.solved[key] = True
                    st.session_state.digits_collected[key] = data["digit"]
                    st.rerun()
                else:
                    st.error("Oups... Ce n'est pas la bonne pratique. Réessayez !")

with col2:
    st.sidebar.header("🎒 Votre Inventaire")
    st.sidebar.write("Indices collectés :")
    
    for key, data in CHALLENGES.items():
        if st.session_state.solved[key]:
            st.sidebar.markdown(f"<div class='found-digit'>{data['label']} → {data['digit']}</div>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"<div style='color:gray; text-align:center;'>[ {data['label']} bloqué ]</div>", unsafe_allow_html=True)

    st.sidebar.divider()
    
    # Digicode Final
    st.sidebar.subheader("🔓 Digicode Final")
    user_code = st.sidebar.text_input("Entrez les 4 chiffres :", max_chars=4)
    
    if st.sidebar.button("Tenter de sortir"):
        if user_code == CODE_FINAL_CORRECT:
            st.balloons()
            st.sidebar.success("BRAVO ! Vous avez sécurisé le bureau et terminé la réunion !")
        else:
            st.sidebar.error("Code incorrect. Continuez l'inspection.")

# --- FOOTER ---
st.divider()
st.caption("Point Sécurité Ludique - Créé pour briser les mythes de l'Open Space.")
