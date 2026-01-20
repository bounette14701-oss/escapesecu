import streamlit as st

def main():
    st.set_page_config(page_title="Escape the Office", page_icon="🏢", layout="wide")

    # Style pour transformer les boutons en "objets" du bureau
    st.markdown("""
        <style>
        .stButton>button {
            border: 2px solid #4e5d6c;
            border-radius: 15px;
            height: 150px;
            font-size: 50px;
            background-color: #f0f2f6;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            border-color: #ff4b4b;
            transform: scale(1.05);
            background-color: #e1e4e8;
        }
        .office-label {
            text-align: center;
            font-weight: bold;
            color: #4e5d6c;
            margin-top: -10px;
        }
        .challenge-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🕵️‍♂️ Escape Game : Le Bureau Piégé")
    st.write("Cliquez sur les objets du bureau pour inspecter les risques et trouver les 4 chiffres du code de sortie.")

    # Initialisation des découvertes
    if 'found' not in st.session_state:
        st.session_state.found = {"👁️": None, "🔌": None, "☕": None, "🍌": None}

    # --- VUE DU BUREAU (GRILLE D'OBJETS) ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🖥️"):
            st.session_state.current_item = "Ecran"
        st.markdown("<p class='office-label'>Le Poste de Travail</p>", unsafe_allow_html=True)

    with col2:
        if st.button("🔌"):
            st.session_state.current_item = "Multiprise"
        st.markdown("<p class='office-label'>Sous le Bureau</p>", unsafe_allow_html=True)

    with col3:
        if st.button("☕"):
            st.session_state.current_item = "Cafetière"
        st.markdown("<p class='office-label'>Le Coin Café</p>", unsafe_allow_html=True)

    with col4:
        if st.button("🍌"):
            st.session_state.current_item = "Sol"
        st.markdown("<p class='office-label'>Le Passage</p>", unsafe_allow_html=True)

    st.write("---")

    # --- ZONE DE DÉFI DYNAMIQUE ---
    if 'current_item' in st.session_state:
        item = st.session_state.current_item
        
        st.markdown(f"### 🔍 Inspection : {item}")
        
        with st.container():
            st.markdown('<div class="challenge-box">', unsafe_allow_html=True)
            
            if item == "Ecran":
                st.write("**Alerte Fatigue Visuelle !** On dit qu'on cligne 3x moins des yeux devant cet écran. Info ou Intox ?")
                choice = st.radio("Verdict :", ["C'est un Mytho total", "C'est malheureusement Réel"], key="choice1")
                if st.button("Vérifier le composant 1"):
                    if "Réel" in choice:
                        st.success("Correct ! On cligne 60% moins. Premier chiffre du code : **4**")
                        st.session_state.found["👁️"] = "4"
                    else:
                        st.error("Mauvaise analyse. L'œil s'assèche vraiment !")

            elif item == "Multiprise":
                st.write("**Risque d'Incendie !** Un chargeur branché à vide, c'est dangereux ?")
                choice = st.radio("Verdict :", ["Mytho, pas de courant consommé", "Réel, risque de surchauffe"], key="choice2")
                if st.button("Vérifier le composant 2"):
                    if "Réel" in choice:
                        st.success("Exact ! L'effet Joule ne dort jamais. Deuxième chiffre : **2**")
                        st.session_state.found["🔌"] = "2"
                    else:
                        st.error("Faux ! Un transformateur sous tension chauffe toujours.")

            elif item == "Cafetière":
                st.write("**Pause Café !** Boire 5 cafés aide-t-il à prévenir les douleurs aux poignets (TMS) ?")
                choice = st.radio("Verdict :", ["Réel, la caféine détend", "Mytho, ça n'a aucun rapport"], key="choice3")
                if st.button("Vérifier le composant 3"):
                    if "Mytho" in choice:
                        st.success("Bien vu ! Le café excite plus qu'il ne répare. Troisième chiffre : **9**")
                        st.session_state.found["☕"] = "9"
                    else:
                        st.error("Et non, trop de café peut même augmenter la tension musculaire.")

            elif item == "Sol":
                st.write("**Zone de Passage !** Les chutes de plain-pied, c'est 15% des accidents de bureau ?")
                choice = st.radio("Verdict :", ["Réel, c'est une cause majeure", "Mytho, on n'est pas si maladroits"], key="choice4")
                if st.button("Vérifier le composant 4"):
                    if "Réel" in choice:
                        st.success("Vrai ! Un sol encombré est un piège. Dernier chiffre : **7**")
                        st.session_state.found["🍌"] = "7"
                    else:
                        st.error("Détrompez-vous, c'est un des risques les plus sous-estimés !")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- CODE FINAL ---
    st.write("---")
    st.sidebar.title("🔐 Digicode de Sortie")
    code_input = st.sidebar.text_input("Entrez les 4 chiffres trouvés :", placeholder="????")
    
    if st.sidebar.button("DÉVERROUILLER LA PORTE"):
        if code_input == "4297":
            st.sidebar.success("PORTE OUVERTE !")
            st.balloons()
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y4eG9pZzRreXp4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26BGD4l9S8nAsy43C/giphy.gif")
        else:
            st.sidebar.error("CODE ERRONÉ")

    # Rappel des indices trouvés
    st.sidebar.write("Indices récoltés :")
    st.sidebar.write(st.session_state.found)

if __name__ == "__main__":
    main()
