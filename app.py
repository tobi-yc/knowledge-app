import streamlit as st

def render_header():
    # URL for the Yoco logo
    logo_url = "https://files.buildwithfern.com/yoco.docs.buildwithfern.com/ccc94a27f557100203d0ba7856f74a66a6db873418e282ad02238632d2091e7c/pages/docs/logos/yoco.svg"
    
    # Custom HTML/CSS for the lockup
    header_html = f"""
    <style>
        /* Import Montserrat for the 'Vuka' text to match brand style */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

        .header-container {{
            /* Yoco Blue background - ensures white text is visible */
            background-color: #00A9E0; 
            padding: 1.5rem;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .yoco-logo {{
            height: 40px;
            width: auto;
        }}

        .vuka-text {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 32px;
            color: #FFFFFF;
            text-transform: uppercase;
            letter-spacing: 1px;
            /* Fix vertical alignment visually */
            line-height: 1; 
            margin-top: 4px; 
        }}
    </style>

    <div class="header-container">
        <img src="{logo_url}" class="yoco-logo" alt="Yoco Logo">
        <span class="vuka-text">Vuka</span>
    </div>
    """

    # Render the HTML
    st.markdown(header_html, unsafe_allow_html=True)

# --- Your App Code Below ---
render_header()

st.title("Workspace Dashboard")
st.write("Welcome to the Yoco Vuka workspace.")
