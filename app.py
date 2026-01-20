import streamlit as st

def main():
    # --- CONFIGURATION DU JEU (Modifiez ici) ---
    CHALLENGES = {
        "POSTE DE TRAVAIL": {
            "icon": "🖥️",
            "titre": "L'écran qui hypnotise",
            "quest": "Est-il vrai qu'on cligne 3x moins des yeux devant un écran ?",
            "options": ["MYTHO", "RÉEL"],
            "correct": "RÉEL",
            "chiffre": "4",
            "feedback": "L'oeil s'assèche vraiment ! Rappel : La règle du 20-20-20 (toutes les 20 min, regarder à 20 pieds pendant 20 sec)."
        },
        "MULTIPRISE": {
            "icon": "🔌",
            "titre": "Le serpent électrique",
            "quest": "Un chargeur seul branché consomme et peut surchauffer ?",
            "options": ["MYTHO", "RÉEL"],
            "correct": "RÉEL",
            "chiffre": "2",
            "feedback": "C'est l'effet Joule. Un transformateur sous tension, même 'à vide', travaille."
        },
        "COIN CAFÉ": {
            "icon": "☕",
            "titre": "La potion magique",
            "quest": "Boire 5 cafés par jour réduit les risques de TMS au poignet ?",
            "options": ["MYTHO", "RÉEL"],
            "correct": "MYTHO",
            "chiffre": "9",
            "feedback": "Le café est un excitant nerveux, pas un relaxant musculaire. Rien ne vaut l'ergonomie !"
        },
        "SOL": {
            "icon": "🚧",
            "titre": "La zone de danger",
            "quest": "Les chutes de plain-pied = 15% des accidents de bureau ?",
            "options": ["MYTHO", "RÉEL"],
            "correct": "RÉEL",
            "chiffre": "7",
            "feedback": "C'est un record ! Un carton ou un câble mal rangé est un piège redoutable."
        }
    }
    CODE_FINAL = "".join([v["chiffre"] for v in CHALLENGES.values()])

    # --- STYLE PERSONNALISÉ ---
    st.set_page_config(page_title="Escape Game Sécurité", layout="wide")
    st.markdown(f"""
        <style>
        .stButton>button {{
            height: 120px;
            border-radius: 15px;
            font-size: 40px;
            transition: 0.3s;
        }}
        .card {{
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            border-left: 8px solid #ff4b4b;
            margin-bottom: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)

    # --- LOGIQUE D'ÉTAT ---
    if 'found_codes' not in st.session_state:
        st.session_state.found_codes = {k: "?" for k in CHALLENGES.keys()}
    if 'current_node' not in st.session_state:
        st.session_state.current_node = None

    # --- INTERFACE PRINCIPALE ---
    st.title("🕵️‍♂️ Escape Game : Inspection Bureau 304")
    st.write("Fouillez le bureau en cliquant sur les éléments pour récolter les 4 chiffres du digicode.")

    # Affichage des objets (Le bureau)
    cols = st.columns(len(CHALLENGES))
    for i, (name, data) in enumerate(CHALLENGES.items()):
        with cols[i]:
            if st.button(data["icon"], key=name):
                st.session_state.current_node = name
            st.caption(f"<center>{name}</center>", unsafe_allow_html=True)

    st.divider()

    # Zone de Défi
    if st.session_state.current_node:
        node = st.session_state.current_node
        data = CHALLENGES[node]
        
        st.markdown(f"""<div class="card">
            <h3>{data['icon']} {data['titre']}</h3>
            <p>{data['quest']}</p>
        </div>""", unsafe_allow_html=True)

        ans = st.radio("Votre diagnostic :", data["options"], index=None, key=f"radio_{node}")
        
        if st.button("Valider l'inspection"):
            if ans == data["correct"]:
                st.success(f"✅ BIEN JOUÉ ! Le chiffre identifié est : {data['chiffre']}")
                st.info(f"💡 Info Sécu : {data['feedback']}")
                st.session_state.found_codes[node] = data["chiffre"]
            else:
                st.error("❌ Diagnostic erroné. L'élément reste suspect. Réessayez.")

    # --- BARRE LATÉRALE (DIGICODE) ---
    with st.sidebar:
        st.header("🔐 Digicode")
        st.write("Chiffres collectés :")
        # Affichage visuel du code en cours
        code_display = " ".join(st.session_state.found_codes.values())
        st.subheader(f"`{code_display}`")
        
        st.divider()
        
        user_code = st.text_input("Saisir le code final :", max_chars=4)
        if st.button("TENTER LA SORTIE"):
            if user_code == CODE_FINAL:
                st.balloons()
                st.success("🔓 ACCÈS AUTORISÉ. Vous avez sécurisé le bureau !")
                st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y4eG9pZzRreXp4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26BGD4l9S8nAsy43C/giphy.gif")
            else:
                st.error("CODE INCORRECT. La porte reste verrouillée.")

if __name__ == "__main__":
    main()
