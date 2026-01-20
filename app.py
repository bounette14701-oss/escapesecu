import streamlit as st

def main():
    st.set_page_config(page_title="HACK THE SAFETY", page_icon="⚡", layout="wide")

    # CSS pour un look "Terminal Hacker / Cyberpunk"
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Fira Code', monospace;
            background-color: #0d0221;
            color: #00ff41;
        }
        
        .stApp {
            background: linear-gradient(180deg, #0d0221 0%, #0f0c29 100%);
        }

        .node-box {
            border: 2px solid #00ff41;
            padding: 20px;
            border-radius: 10px;
            background: rgba(0, 255, 65, 0.05);
            margin-bottom: 20px;
            transition: all 0.3s;
        }

        .node-box:hover {
            box-shadow: 0 0 15px #00ff41;
        }

        .status-badge {
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            text-transform: uppercase;
        }

        .myth-text { color: #ff003c; text-shadow: 0 0 5px #ff003c; }
        .real-text { color: #00ff41; text-shadow: 0 0 5px #00ff41; }
        
        /* Cacher les boutons radio classiques */
        div[role="radiogroup"] {
            flex-direction: row !important;
            gap: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("⚡ SYSTEM OVERRIDE: SAFETY PROTOCOL")
    st.write("---")

    # Initialisation des états
    if 'steps' not in st.session_state:
        st.session_state.steps = {1: None, 2: None, 3: None, 4: None}

    # --- DASHBOARD DE PROGRESSION ---
    cols = st.columns(4)
    for i in range(1, 5):
        with cols[i-1]:
            status = "✅" if st.session_state.steps[i] is not None else "❌"
            st.markdown(f"**NODE 0{i}** \n{status}")

    st.write("")

    # --- GRILLE DE JEU (2x2) ---
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="node-box">', unsafe_allow_html=True)
        st.subheader("💾 DATA_STREAM_01")
        st.write("On cligne 3x moins des yeux sur écran : Légende urbaine ?")
        res1 = st.selectbox("ANALYSE :", ["En attente...", "RÉEL", "MYTHO"], key="s1")
        st.session_state.steps[1] = res1 if res1 != "En attente..." else None
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="node-box">', unsafe_allow_html=True)
        st.subheader("☕ ENERGY_CORE_03")
        st.write("5 cafés par jour préviennent les TMS (poignets).")
        res3 = st.selectbox("ANALYSE :", ["En attente...", "RÉEL", "MYTHO"], key="s3")
        st.session_state.steps[3] = res3 if res3 != "En attente..." else None
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="node-box">', unsafe_allow_html=True)
        st.subheader("⚠️ ACCIDENT_LOG_02")
        st.write("15% des accidents de bureau = chutes de plain-pied.")
        res2 = st.selectbox("ANALYSE :", ["En attente...", "RÉEL", "MYTHO"], key="s2")
        st.session_state.steps[2] = res2 if res2 != "En attente..." else None
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="node-box">', unsafe_allow_html=True)
        st.subheader("🔥 THERMAL_THREAT_04")
        st.write("Un chargeur vide branché peut créer un incendie.")
        res4 = st.selectbox("ANALYSE :", ["En attente...", "RÉEL", "MYTHO"], key="s4")
        st.session_state.steps[4] = res4 if res4 != "En attente..." else None
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TERMINAL DE VALIDATION ---
    st.write("---")
    if st.button("RUN DECRYPT_CODE.EXE"):
        # Vérification des réponses
        results = [
            st.session_state.steps[1] == "MYTHO",
            st.session_state.steps[2] == "RÉEL",
            st.session_state.steps[3] == "MYTHO",
            st.session_state.steps[4] == "RÉEL"
        ]

        if None in st.session_state.steps.values():
            st.warning("⚠️ ANALYSE INCOMPLÈTE : Remplissez tous les nodes.")
        elif all(results):
            st.balloons()
            st.success("🔓 ACCESS GRANTED | CODE: 4-2-9-7")
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y4eG9pZzRreXp4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26BGD4l9S8nAsy43C/giphy.gif")
            st.markdown("### BRAVO ! Vous avez hacké la sécurité. Mission terminée.")
        else:
            st.error("🚨 CORRUPTED DATA DETECTED - ACCÈS REFUSÉ")
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3RscW56ZzRreXp4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/VdBZ9H4s2fP099QvY/giphy.gif")
            
            # Feedback "Hacker"
            errors = []
            if not results[0]: errors.append("Node 01: On cligne vraiment moins (60% moins) !")
            if not results[1]: errors.append("Node 02: Les chutes sont une menace majeure (15%+) !")
            if not results[2]: errors.append("Node 03: La caféine n'aide pas les muscles, elle les excite.")
            if not results[3]: errors.append("Node 04: L'effet Joule sur un chargeur vide est réel !")
            
            for e in errors:
                st.write(f"> `{e}`")

if __name__ == "__main__":
    main()
