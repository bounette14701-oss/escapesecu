import streamlit as st

def main():
    # Configuration de la page
    st.set_page_config(page_title="Flash Escape : Sécurité Bureau", page_icon="🔒")

    # Style CSS personnalisé pour l'ambiance
    st.markdown("""
        <style>
        .main {
            background-color: #1e1e1e;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #ff4b4b;
            color: white;
        }
        .success-text {
            color: #28a745;
            font-weight: bold;
            font-size: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔒 5 Minutes pour s'échapper !")
    st.subheader("Thème : C'EST RÉEL ou C'EST MYTHO ?")
    
    st.info("L'alarme est activée ! Répondez correctement aux 4 questions pour obtenir le code de déverrouillage de la salle de réunion.")

    # --- INITIALISATION DU SCORE ---
    if 'answers' not in st.session_state:
        st.session_state.answers = [None, None, None, None]

    # --- ÉNIGME 1 ---
    st.markdown("---")
    st.markdown("### 👁️ Énigme 1")
    st.write("**Affirmation :** 'Cligner des yeux trois fois moins souvent devant un écran est une légende urbaine pour nous forcer à faire des pauses.'")
    q1 = st.radio("Verdict :", ["Réel", "Mytho"], key="q1", index=None)
    
    # --- ÉNIGME 2 ---
    st.markdown("---")
    st.markdown("### 🚶 Énigme 2")
    st.write("**Affirmation :** 'Au bureau, les chutes de plain-pied (glissades, trébuchements) représentent plus de 15% des accidents de travail.'")
    q2 = st.radio("Verdict :", ["Réel", "Mytho"], key="q2", index=None)

    # --- ÉNIGME 3 ---
    st.markdown("---")
    st.markdown("### ☕ Énigme 3")
    st.write("**Affirmation :** 'Boire 5 cafés par jour réduit les risques de TMS car la caféine détend les muscles du poignet.'")
    q3 = st.radio("Verdict :", ["Réel", "Mytho"], key="q3", index=None)

    # --- ÉNIGME 4 ---
    st.markdown("---")
    st.markdown("### 🔌 Énigme 4")
    st.write("**Affirmation :** 'Un chargeur de téléphone laissé branché à vide sur une multiprise peut s'enflammer.'")
    q4 = st.radio("Verdict :", ["Réel", "Mytho"], key="q4", index=None)

    st.markdown("---")

    # --- VALIDATION ---
    if st.button("GÉNÉRER LE CODE DE SORTIE"):
        # Réponses correctes : Mytho (4), Réel (2), Mytho (9), Réel (7)
        correct_q1 = (q1 == "Mytho")
        correct_q2 = (q2 == "Réel")
        correct_q3 = (q3 == "Mytho")
        correct_q4 = (q4 == "Réel")

        if all([q1, q2, q3, q4]):
            code = ""
            code += "4" if correct_q1 else "?"
            code += "2" if correct_q2 else "?"
            code += "9" if correct_q3 else "?"
            code += "7" if correct_q4 else "?"

            if "?" in code:
                st.error(f"Code erroné : {code}. Certaines réponses sont fausses, l'alarme sonne toujours !")
                
                # Feedback pédagogique pour les erreurs
                with st.expander("Besoin d'un indice sur vos erreurs ?"):
                    if not correct_q1: st.write("- **Oeil :** On cligne vraiment moins souvent (60% de moins) !")
                    if not correct_q2: st.write("- **Chutes :** C'est une cause majeure d'accident bien réelle.")
                    if not correct_q3: st.write("- **Café :** Attention, c'est un excitant, pas un relaxant musculaire !")
                    if not correct_q4: st.write("- **Chargeur :** Risque de surchauffe réel (effet Joule).")
            else:
                st.balloons()
                st.success(f"🔓 CODE CORRECT : {code}")
                st.markdown("""
                    <div class='success-text'>
                    Félicitations ! La porte est ouverte. <br>
                    Rappel Sécurité : Restez vigilants, même au bureau !
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Veuillez répondre à toutes les questions avant de tenter de sortir.")

if __name__ == "__main__":
    main()
