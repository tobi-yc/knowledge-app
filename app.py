import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Phanda | A Yoco Publication",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SETUP GEMINI AI ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# --- 3. SESSION STATE INITIALIZATION ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'ai_result' not in st.session_state:
    st.session_state.ai_result = None
if 'ai_visible' not in st.session_state:
    st.session_state.ai_visible = False

# --- 4. DATA & COLORS ---
CATEGORY_COLORS = {
    "Starting Your Business": "#00695c",
    "Reaching Customers": "#7b1fa2",
    "Selling Anywhere": "#e65100",
    "Managing Your Finances": "#c62828",
    "Operating Your Business": "#1565c0",
    "Growing Your Team": "#33691e",
    "Regulatory Updates": "#455a64" 
}

CONTENT_DATA = [
    # --- REGULATORY CONTENT ---
    {"category": "Regulatory Updates", "title": "SARS Announces Real-Time VAT Reporting Plans for 2027", "summary": "SARS is moving towards real-time digital VAT reporting. Understand the timeline and what software upgrades might be required.", "source": "SARS", "link": "https://www.sars.gov.za", "location": "South Africa", "type": "official notice"},
    {"category": "Regulatory Updates", "title": "New Employment Equity Targets: Sector Guide", "summary": "Department of Employment and Labour has gazetted new sectoral targets. Check if your small business falls under the designated employer scope.", "source": "Dept of Labour", "link": "https://www.labour.gov.za", "location": "South Africa", "type": "legislation"},
    
    # --- YOCO OFFICIAL ---
    {"category": "Reaching Customers", "title": "Learn how to use Instagram for your business", "summary": "A guide on switching to a business profile, optimizing bios, showcasing products, and using Reels to drive engagement.", "source": "Yoco", "link": "https://www.yoco.com/za/blog/instagram-for-your-business/", "location": "South Africa", "type": "guide"},
    {"category": "Operating Your Business", "title": "How to choose a point of sale (POS) system", "summary": "Key questions and features to look for when selecting a POS, covering cloud vs. traditional systems and integration needs.", "source": "Yoco", "link": "https://www.yoco.com/za/blog/choose-point-of-sale/", "location": "South Africa", "type": "guide"},
    {"category": "Starting Your Business", "title": "Behind the Counter with Sparkys: 5 takeaways for success", "summary": "Lessons from the Sparkys burger brand on starting small, maintaining quality, and choosing the right tech for efficiency.", "source": "Yoco", "link": "https://www.yoco.com/za/blog/yoco-meets-sparkys/", "location": "South Africa", "type": "case study"},
    {"category": "Managing Your Finances", "title": "Yoco shapes Mzansi's gratitude culture: R1 billion in tips", "summary": "How digital tipping prompts have unlocked over R1 billion in tips for service workers, boosting staff morale and income.", "source": "Yoco", "link": "https://www.yoco.com/za/blog/yoco-shapes-gratitude-culture/", "location": "South Africa", "type": "article"},
    {"category": "Selling Anywhere", "title": "Inside Yoco Counter: Your top questions answered", "summary": "A breakdown of the Yoco Counter features, payment acceptance, stock management, and cash flow tools.", "source": "Yoco", "link": "https://www.yoco.com/za/blog/articles/inside-yoco-counter", "location": "South Africa", "type": "guide"},

    # --- EXTERNAL RESOURCES ---
    {"category": "Starting Your Business", "title": "12 Most Profitable Business Ideas in SA for 2026", "summary": "Highlights high-potential ideas like boutique fitness studios and artisanal coffee shops. Helps aspiring founders validate opportunities.", "source": "Lula", "link": "https://lula.co.za/blog/sme-advice/top-12-business-ideas-in-south-africa/", "location": "South Africa", "type": "article"},
    {"category": "Starting Your Business", "title": "How to Start a Food Business in SA (7 Steps)", "summary": "A step-by-step guide covering concept definition, business registration, and food safety compliance.", "source": "ASC Consultants", "link": "https://ascconsultants.co.za/how-to-start-a-food-business-in-south-africa/", "location": "South Africa", "type": "guide"},
    {"category": "Reaching Customers", "title": "Small Business Marketing in 2026: The Ultimate Guide", "summary": "Global playbook on building marketing funnels and prioritizing digital channels like mobile and social.", "source": "Forbes Advisor", "link": "https://www.forbes.com/advisor/business/small-business-marketing/", "location": "Global", "type": "guide"},
    {"category": "Selling Anywhere", "title": "Omnichannel Shopping Is the Future of Retail in SA", "summary": "Explains how to combine online and in-store channels to improve convenience. Ideal for fashion and food merchants.", "source": "IT News Africa", "link": "https://www.itnewsafrica.com/2025/04/omnichannel-shopping-is-the-future-of-retail-in-south-africa/", "location": "South Africa", "type": "article"},
    {"category": "Managing Your Finances", "title": "Structuring Your Finances for an SME in South Africa", "summary": "Basics on separating finances, bookkeeping, and tax planning. Valuable for first-time entrepreneurs.", "source": "M&J Group", "link": "https://mjgroup.africa/structuring-your-finances-for-an-sme-in-south-africa/", "location": "South Africa", "type": "guide"},
    {"category": "Operating Your Business", "title": "SME December Outlook: Festive Season Time to Shine", "summary": "Advice for retail and hospitality on stock and staffing during peaks. Useful template for planning high-demand months.", "source": "The Citizen", "link": "https://www.citizen.co.za/business/sme-december-outlook-festive-season-time-for-small-businesses-to-shine/", "location": "South Africa", "type": "news"},
    {"category": "Growing Your Team", "title": "Ready to Grow? Here's When You Should Hire Your First Employee", "summary": "Helps solopreneurs in beauty and fitness decide when to hire.", "source": "Sourcefin", "link": "https://www.sourcefin.co.za/ready-to-grow-your-small-business-heres-when-you-should-hire-your-first-employee/", "location": "South Africa", "type": "guide"}
]

EXAMPLE_PROMPTS = [
    "How do I register for VAT?",
    "Business funding options",
    "Draft a simple contract",
    "Marketing ideas on a budget",
    "Food trends for 2026"
]

# --- 5. HELPER FUNCTIONS ---

def trigger_search(query):
    """
    Updates the session state to initiate a search.
    Note: Does NOT run the API call directly. This allows the UI 
    to refresh, show the spinner in the right place, and then run the logic.
    """
    st.session_state.search_query = query
    st.session_state.ai_visible = True
    st.session_state.ai_result = None # Resetting this triggers the spinner in the main loop

def generate_ai_response(query):
    """The actual API call function."""
    if not api_key:
        return "⚠️ Please configure your Gemini API Key."
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash') 
        
        system_prompt = (
            "You are 'Phanda', a helpful business assistant for Yoco merchants in South Africa. "
            "1. Answer the user's question clearly and concisely. "
            "2. STRICTLY relevant to South Africa (ZAR, SARS, local laws). "
            "3. CITATIONS: You must include inline numbered citations in your text, like this: 'Turnover tax is available for micro-businesses [1].' "
            "4. SOURCES SECTION: At the bottom, add a section '### Sources'. "
            "   - Format: '1. [Title](URL)' "
            "   - Provide real, working URLs for official sources (SARS, Yoco, Dept of Labour). "
            f"\n\nUser question: {query}"
        )
        
        response = model.generate_content(system_prompt)
        return response.text
            
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

# --- CALLBACKS ---
def toggle_ai_visibility():
    st.session_state.ai_visible = not st.session_state.ai_visible

def handle_search_submit():
    query = st.session_state.main_search_input
    # Trigger only if query changed or forced
    trigger_search(query)

def on_filter_change():
    if st.session_state.ai_result:
        st.session_state.ai_visible = False

def explain_impact(article_title):
    # Construct the question
    query = f"Explain the practical impact of the article '{article_title}' for a small business owner in South Africa. What do I need to do?"
    
    # Update search bar for visual feedback
    st.session_state.main_search_input = query
    
    # Trigger the search state
    trigger_search(query)

# --- 6. CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* COLORS */
    :root {
        --yoco-blue: #009fe3;
        --yoco-dark: #232d39;
        --text-grey: #5c6c7f;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }

    /* HEADER */
    .yoco-header-container {
        background-color: #0F172A;
        padding: 4rem 2rem 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    .phanda-title {
        font-family: 'Anton', sans-serif; font-size: 8rem; color: #FFFFFF;
        line-height: 0.9; letter-spacing: 2px; margin-bottom: 15px; text-transform: uppercase;
    }
    .sub-row {
        display: flex; align-items: center; justify-content: center; gap: 12px;
        color: #FFFFFF; font-family: 'Inter', sans-serif; font-size: 1.2rem; opacity: 0.9;
    }
    .yoco-logo-small { height: 24px; width: auto; margin-top: 2px; }
    .tagline-text {
        margin-top: 25px; font-family: 'Montserrat', sans-serif; font-weight: 700;
        font-size: 1.5rem; color: #FFFFFF;
    }
    .description-text {
        margin-top: 8px; font-family: 'Inter', sans-serif; font-size: 1rem;
        color: #94A3B8; max-width: 600px;
    }

    /* BUTTONS */
    .stButton button {
        border-radius: 20px; font-size: 0.8rem; background-color: white;
        color: #5c6c7f; border: 1px solid #eee; padding: 0.25rem 1rem; width: 100%;
    }
    .stButton button:hover { border-color: #009fe3; color: #009fe3; }
    
    /* CARDS */
    div[data-testid="stColumn"] {
        background-color: white; border: 1px solid #eef0f2; border-radius: 12px;
        padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        height: 100%; display: flex; flex-direction: column;
    }
    div[data-testid="stColumn"]:hover {
        transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0, 159, 227, 0.15);
        border-color: #009fe3;
    }

    /* PILLS & TAGS */
    .type-pill {
        font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
        padding: 6px 10px; border-radius: 6px; background: #f4f6f8; color: #5c6c7f;
        letter-spacing: 0.5px; display: inline-block; margin-bottom: 12px;
    }
    .category-pill {
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        padding: 6px 12px; border-radius: 20px; margin-top: auto; margin-bottom: 16px;
        display: inline-block; letter-spacing: 0.5px;
    }
    
    /* Category Colors */
    .cat-starting { background: #e0f2f1; color: #00695c; }
    .cat-reaching { background: #f3e5f5; color: #7b1fa2; }
    .cat-selling { background: #fff3e0; color: #e65100; }
    .cat-finances { background: #ffebee; color: #c62828; }
    .cat-operating { background: #e3f2fd; color: #1565c0; }
    .cat-team { background: #f1f8e9; color: #33691e; }
    .cat-regulatory { background: #eceff1; color: #455a64; border: 1px solid #cfd8dc; }

    h3 { font-size: 1.15rem; font-weight: 700; color: #232d39; margin: 0 0 10px 0; min-height: 3.9em; }
    p { font-size: 0.95rem; color: #5c6c7f; line-height: 1.6; margin-bottom: 20px; flex-grow: 1; }
    .source-text { font-size: 0.8rem; color: #999; border-top: 1px solid #f4f6f8; padding-top: 15px; display: flex; justify-content: space-between; align-items: center; }
    a { text-decoration: none; color: #009fe3; font-weight: 700; font-size: 0.85rem; }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 7. UI LAYOUT ---

# A. HEADER
logo_url = "https://files.buildwithfern.com/yoco.docs.buildwithfern.com/ccc94a27f557100203d0ba7856f74a66a6db873418e282ad02238632d2091e7c/pages/docs/logos/yoco.svg"

header_html = f"""
<div class="yoco-header-container">
    <div class="phanda-title">PHANDA</div>
    <div class="sub-row">
        <span>a</span>
        <img src="{logo_url}" class="yoco-logo-small" alt="YOCO">
        <span>publication</span>
    </div>
    <div class="tagline-text">Power your hustle</div>
    <div class="description-text">Practical insights, guides, and tools for the entrepreneurs making it happen.</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# B. SEARCH INPUT
st.text_input("", 
              placeholder="Ask Phanda AI anything...", 
              key="main_search_input",
              value=st.session_state.search_query,
              on_change=handle_search_submit)

# C. EXAMPLE PROMPTS
cols = st.columns(len(EXAMPLE_PROMPTS))
for i, prompt_text in enumerate(EXAMPLE_PROMPTS):
    with cols[i]:
        if st.button(prompt_text, use_container_width=True):
            trigger_search(prompt_text)
            st.rerun()

# D. AI RESULT SECTION
if st.session_state.ai_visible:
    st.markdown("---")
    
    col_res_1, col_res_2 = st.columns([5, 1])
    with col_res_1:
        st.caption(f"🤖 AI Insight for: **{st.session_state.search_query}**")
            
    with col_res_2:
        btn_label = "🙈 Hide"
        st.button(btn_label, key="toggle_ai_btn", on_click=toggle_ai_visibility)

    # LOGIC: If result is None, it means we need to fetch it (Showing Spinner)
    # This logic block runs AFTER the divider, so the spinner appears under the line.
    if st.session_state.ai_result is None:
        with st.spinner("Phanda AI is thinking..."):
            result_text = generate_ai_response(st.session_state.search_query)
            st.session_state.ai_result = result_text
        st.rerun() # Force a rerun to display the text immediately
    
    else:
        # Display the result
        with st.chat_message("assistant", avatar="⚡"):
            st.write(st.session_state.ai_result)

st.markdown("---")

# --- 8. FILTERS & CONTENT GRID ---

categories = list(CATEGORY_COLORS.keys())

selected_categories = st.pills(
    "Filter insights:", 
    categories, 
    selection_mode="multi", 
    key="cat_filter",
    on_change=on_filter_change
)

# --- DYNAMIC CSS FOR FILTERS ---
custom_pills_css = "<style>"
for i, cat_name in enumerate(categories):
    color = CATEGORY_COLORS[cat_name]
    custom_pills_css += f"""
    div[data-testid="stPills"] button:nth-of-type({i+1})[aria-selected="true"] {{
        background-color: {color} !important; border-color: {color} !important; color: white !important;
    }}
    div[data-testid="stPills"] button:nth-of-type({i+1}):hover {{
        border-color: {color} !important; color: {color} !important;
    }}
    """
custom_pills_css += "</style>"
st.markdown(custom_pills_css, unsafe_allow_html=True)

# Filter Logic
if not selected_categories:
    filtered_data = CONTENT_DATA
else:
    filtered_data = [item for item in CONTENT_DATA if item["category"] in selected_categories]

# Render Grid
cols_per_row = 3
rows = [filtered_data[i:i + cols_per_row] for i in range(0, len(filtered_data), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for i, item in enumerate(row):
        
        cat_class = "cat-operating" 
        for cat_name, _ in CATEGORY_COLORS.items():
            if item['category'] == cat_name:
                if "Starting" in cat_name: cat_class = "cat-starting"
                elif "Reaching" in cat_name: cat_class = "cat-reaching"
                elif "Selling" in cat_name: cat_class = "cat-selling"
                elif "Finances" in cat_name: cat_class = "cat-finances"
                elif "Operating" in cat_name: cat_class = "cat-operating"
                elif "Growing" in cat_name: cat_class = "cat-team"
                elif "Regulatory" in cat_name: cat_class = "cat-regulatory"
        
        with cols[i]:
            st.markdown(f"""
                <div style="height:100%;">
                    <div class="type-pill">{item['type']}</div>
                    <div style="font-size:0.7rem; float:right; color:#999;">📍 {item['location']}</div>
                    <h3>{item['title']}</h3>
                    <p>{item['summary']}</p>
                    <div class="category-pill {cat_class}">{item['category']}</div>
                    <div class="source-text">
                        {item['source']} 
                        <span style="float:right;"><a href="{item['link']}" target="_blank">Read ➜</a></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if item['category'] == "Regulatory Updates":
                st.button(
                    "🤖 Explain Impact", 
                    key=f"explain_btn_{i}_{item['title']}", 
                    on_click=explain_impact, 
                    args=(item['title'],)
                )
