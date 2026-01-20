import streamlit as st
import time

def main():
    # Configuration de la page
    st.set_page_config(page_title="Flash Escape : Sécurité Bureau", page_icon="🚨", layout="centered")

    # Style CSS personnalisé pour l'ambiance
    st.markdown("""
        <style>
        .main {
            background-color: #1e1e1e; /* Fond sombre */
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px; /* Bords arrondis pour les boutons */
            height: 3.5em;
            background-color: #FF6B6B; /* Rouge vibrant */
            color: white;
            font-size: 18px;
            font-weight: bold;
            border: none;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* Légère ombre */
        }
        .stButton>button:hover {
            background-color: #FF4F4F; /* Rouge plus foncé au survol */
        }
        .success-text {
            color: #28a745;
            font-weight: bold;
            font-size: 24px;
            text-align: center;
            margin-top: 20px;
        }
        .error-text {
            color: #ff4b4b;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFD700; /* Jaune or pour les titres */
            text-align: center;
        }
        .stRadio div {
            padding: 5px 0;
        }
        .stRadio p {
            font-size: 1.1em;
        }
        .stExpander {
            border-radius: 10px;
            background-color: #2a2a2a;
            padding: 10px;
        }
        .stExpander div[role="button"] p {
            color: #ADD8E6 !important; /* Bleu clair pour le titre de l'expander */
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚨 Flash Escape : Mission Sécurité Bureau 🚨")
    st.subheader("5 minutes pour distinguer le RÉEL du MYTHO !")
    
    st.markdown(
        """
        <div style="text-align: center;">
            <p><strong>L'alarme retentit, le chrono tourne ! ⏳</strong></p>
            <p>Pour déverrouiller cette maudite porte et retrouver la liberté (et le café ☕), vous devez prouver que vous êtes les rois de la sécurité au bureau.</p>
            <p>C'est parti pour un "Réel ou Mytho" sur des fun facts sécurité !</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # --- INITIALISATION DES VARIABLES DE SESSION ---
    if 'answers' not in st.session_state:
        st.session_state.answers = [None, None, None, None]
    if 'code_tentative' not in st.session_state:
        st.session_state.code_tentative = ""

    # --- ÉNIGME 1 : LE SYNDROME DE L'ŒIL SEC ---
    st.markdown("### 👁️ Énigme 1 : Le regard fatigué de la productivité")
    st.write("**Affirmation :** 'Cligner des yeux trois fois moins souvent devant un écran est une légende urbaine pour nous forcer à faire des pauses. Personne n'y croit, c'est comme le Père Noël 🎅 !'")
    q1 = st.radio("Alors, c'est une blague ou c'est la triste réalité ?", ["Réel", "Mytho"], key="q1", index=st.session_state.answers[0])
    if q1: st.session_state.answers[0] = ["Réel", "Mytho"].index(q1)

    # --- ÉNIGME 2 : LA CHUTE FATALE (DE PLAIN-PIED) ---
    st.markdown("---")
    st.markdown("### 🚶 Énigme 2 : Le parcours du combattant du bureau")
    st.write("**Affirmation :** 'Au bureau, les chutes de plain-pied (glissades, trébuchements) représentent plus de 15% des accidents de travail. Plus dangereux que la marche sur des Lego !' 😂")
    q2 = st.radio("Info ou Intox ? Ça vaut le coup de regarder où on met les pieds ?", ["Réel", "Mytho"], key="q2", index=st.session_state.answers[1])
    if q2: st.session_state.answers[1] = ["Réel", "Mytho"].index(q2)

    # --- ÉNIGME 3 : LE CAFÉ SALVATEUR (OU PAS) ---
    st.markdown("---")
    st.markdown("### ☕ Énigme 3 : La boisson magique")
    st.write("**Affirmation :** 'Boire 5 cafés par jour réduit les risques de troubles musculosquelettiques (TMS) car la caféine détend les muscles du poignet. C'est le secret des pros, paraît-il !'")
    q3 = st.radio("Votre corps vous remerciera ou vous enverra la facture ?", ["Réel", "Mytho"], key="q3", index=st.session_state.answers[2])
    if q3: st.session_state.answers[2] = ["Réel", "Mytho"].index(q3)

    # --- ÉNIGME 4 : L'INCENDIE INVISIBLE ---
    st.markdown("---")
    st.markdown("### 🔌 Énigme 4 : La prise maléfique")
    st.write("**Affirmation :** 'Un chargeur de téléphone laissé branché à vide sur une multiprise peut s'enflammer et causer un départ de feu. Oui, même sans votre téléphone ! 😱'")
    q4 = st.radio("Simple superstition de grand-mère ou réalité effrayante ?", ["Réel", "Mytho"], key="q4", index=st.session_state.answers[3])
    if q4: st.session_state.answers[3] = ["Réel", "Mytho"].index(q4)

    st.markdown("---")

    # --- BOUTON DE VALIDATION ---
    if st.button("TENTER LE CODE DE SORTIE 🚪"):
        if all([q1, q2, q3, q4]):
            correct_q1 = (q1 == "Mytho")
            correct_q2 = (q2 == "Réel")
            correct_q3 = (q3 == "Mytho")
            correct_q4 = (q4 == "Réel")

            code = ""
            code += "4" if correct_q1 else "?"
            code += "2" if correct_q2 else "?"
            code += "9" if correct_q3 else "?"
            code += "7" if correct_q4 else "?"
            
            st.session_state.code_tentative = code # Stocker la tentative pour le rechargement

            if "?" in code:
                st.error(f"🚨 CODE INVALIDE : {code} 🚨")
                st.markdown("<p class='error-text'>Nope ! L'alarme hurle toujours... On dirait que vous avez un peu de mal avec les faits. Relisez bien !</p>", unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/efJ5i5l5zHnJ7s376e/giphy.gif", caption="Quand tu penses avoir le bon code mais non...", use_column_width=True) # Fail GIF
                
                # Feedback pédagogique détaillé pour les erreurs
                with st.expander("🤔 Indice : C'est où que ça coince ?"):
                    st.write("---")
                    if not correct_q1: 
                        st.markdown("**Énigme 1 (Yeux) :** C'est **MYTHO** que c'est une légende. On cligne *vraiment* beaucoup moins ! Faites des pauses 20-20-20 (toutes les 20 min, regarder à 20 pieds pendant 20 sec). 🤓")
                        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2JpZ2JqZHVyeXJkdXZyejlsbGF4c3AxdXBqYWx6aHByN2ZwdzZjaCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPTNFVlBqWWZkYyZjdD1n/l0Iylr03f132zG2ys/giphy.gif", caption="Prends une pause, tes yeux te remercieront !", width=200)

                    if not correct_q2: 
                        st.markdown("**Énigme 2 (Chutes) :** C'est **RÉEL** ! Les chutes de plain-pied sont un grand classique des accidents au bureau. Rangez ces câbles et essuyez vos flaques, s'il vous plaît ! 🚧")
                        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHh3a3ZvdWluamZ0NHFicTNraDk1a2Z0ZTRhY20ycG81amw5NHd3ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPUtFTHM4dThpTnlFOUkvS2F6eUFBdGcvZ2lmeQ/S8I4g5QY0yq0222q1f/giphy.gif", caption="Attention où tu marches !", width=200)

                    if not correct_q3: 
                        st.markdown("**Énigme 3 (Café) :** C'est **MYTHO** ! Le café, c'est bon pour le réveil, pas pour détendre les muscles. Une bonne ergonomie et quelques étirements, c'est mieux que 5 expressos ! 💪")
                        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDVnbzYxd3Z6N3E1aDc0MjB6azFna3h3eTZ6Z2xvcjcyZG5xYjlpaSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPVF2R09lVkJqNFFMZWZ4Z1Y0ZSZhY3Rpb249cmVmcmVzaF9jb250cm9sJnNlc3Npb249NzM1Nzc5OTI5OTM3OTA1NTgxNg/N0hQhEa92j9xL76VzT/giphy.gif", caption="Le café, c'est pour l'énergie, pas les TMS !", width=200)

                    if not correct_q4: 
                        st.markdown("**Énigme 4 (Chargeur) :** C'est **RÉEL** ! Laissez pas votre chargeur branché comme ça, même s'il est tout seul. C'est pas une légende urbaine, le risque de surchauffe est là ! 🔥")
                        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW80cW81a3BpdDlhajM0azM3bW5zdDRwczNhbGRpYWd5N3h1bTN4MCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPXQ2b3F3ajJkQnJ3ZllKdW9DVCZjdD1n/PxfA8v0qgR0C2y0t6V/giphy.gif", caption="Débranche tes chargeurs !", width=200)

            else:
                st.balloons()
                st.success(f"🔓 ALARME DÉSACTIVÉE ! CODE CORRECT : {code} 🎉")
                st.markdown("""
                    <div class='success-text'>
                    MISSION ACCOMPLIE ! Vous êtes de vrais pros de la sécurité ! 🏆
                    </div>
                """, unsafe_allow_html=True)
                st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2p2c3p5MWp3aW0wZWM1eG92eHZtNGhrdDFmNW10d29oZnN3cnZ1ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPU51R3ZJNjQ0bWp6d1M0V2pYUiZjdD1n/Kcb94FpYdI6s0/giphy.gif", caption="La liberté ! Enfin !", use_column_width=True) # Success GIF
                st.markdown("---")
                st.info("💡 **Retenons bien : la sécurité, c'est pas juste des règles, c'est aussi du bon sens et de la vigilance au quotidien !**")
        else:
            st.warning("🧐 Attention l'ami ! Réponds à toutes les questions avant de tenter la sortie. On n'est pas dans le 'Qui veut gagner des millions' ici ! ")
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjJtMnRjaXp3djl2bW5oN255bHNzY2gzaDZ1Z3M0a3Ayd3FpOWE0NiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkPUl3czF5NXZvQXV6VFlEUTlIcyZjdD1n/LqgqS6t81iP0X59PqU/giphy.gif", caption="Ah ah ah, non non non !", use_column_width=True)

if __name__ == "__main__":
    main()
