import streamlit as st

def render_yoco_header():
    """
    Renders the custom YOCO Vuka header.
    Includes styles for a dark background container to ensure 
    both the Blue Logo and White Text are visible.
    """
    
    # The provided Yoco Logo URL
    logo_url = "https://files.buildwithfern.com/yoco.docs.buildwithfern.com/ccc94a27f557100203d0ba7856f74a66a6db873418e282ad02238632d2091e7c/pages/docs/logos/yoco.svg"
    
    header_html = f"""
    <style>
        /* Import a font similar to Yoco's proprietary font (Geometric Sans) */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

        .yoco-header-container {{
            /* Dark background: Necessary to see both Blue Logo and White Text */
            background-color: #0F172A; /* Deep Navy/Black */
            padding: 2.5rem 2rem;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 25px; /* Spacing between Logo and Text */
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .yoco-logo-img {{
            height: 85px; /* Large Header Size */
            width: auto;
        }}

        .vuka-text {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700; /* Bold */
            font-size: 80px; /* Large Header Size */
            color: #FFFFFF; /* White Text */
            letter-spacing: -1.5px;
            line-height: 1;
            /* Minor adjustment to align text baseline with the logo */
            padding-top: 10px; 
        }}
    </style>

    <div class="yoco-header-container">
        <img src="{logo_url}" class="yoco-logo-img" alt="YOCO">
        
        <span class="vuka-text">Vuka</span>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

# --- App Execution ---

# Optional: Set page to wide mode for better header spacing
st.set_page_config(page_title="Yoco Vuka", layout="wide")

# 1. Render the Header
render_yoco_header()

# 2. Your App Content Below
st.write("### Welcome to the internal workspace.")
