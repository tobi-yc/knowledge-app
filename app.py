import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Yoco Vuka",
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
    "Growing Your Team": "#33691e"
}

CONTENT_DATA = [
    {"category": "Starting Your Business", "title": "12 Most Profitable Business Ideas in SA for 2026", "summary": "Highlights high-potential ideas like boutique fitness studios and artisanal coffee shops. Helps aspiring founders validate opportunities.", "source": "Lula", "link": "https://lula.co.za/blog/sme-advice/top-12-business-ideas-in-south-africa/", "location": "South Africa", "type": "article"},
    {"category": "Starting Your Business", "title": "How to Start a Food Business in SA (7 Steps)", "summary": "A step-by-step guide covering concept definition, business registration, and food safety compliance.", "source": "ASC Consultants", "link": "https://ascconsultants.co.za/how-to-start-a-food-business-in-south-africa/", "location": "South Africa", "type": "guide"},
    {"category": "Starting Your Business", "title": "A Guide to Small Business Management (South Africa)", "summary": "Structured introduction to planning, finance, HR, and operations. Doubles as a checklist for new owners.", "source": "SME South Africa", "link": "https://smesouthafrica.co.za/a-guide-to-small-business-management/", "location": "South Africa", "type": "guide"},
    {"category": "Reaching Customers", "title": "How to Market Your Business Online in SA (10 Ways)", "summary": "Ten practical digital tactics from SEO to Google My Business tailored for SA. Ideal for merchants with no online strategy.", "source": "HostAfrica", "link": "https://hostafrica.co.za/blog/marketing/market-business-online-south-africa/", "location": "South Africa", "type": "guide"},
    {"category": "Reaching Customers", "title": "Small Business Marketing in 2026: The Ultimate Guide", "summary": "Global playbook on building marketing funnels and prioritizing digital channels like mobile and social.", "source": "Forbes Advisor", "link": "https://www.forbes.com/advisor/business/small-business-marketing/", "location": "Global", "type": "guide"},
    {"category": "Reaching Customers", "title": "7 Supermarket and Grocery Industry Trends 2026", "summary": "Explores trends like social commerce and loyalty programs. Includes actionable steps like using WhatsApp for promotions.", "source": "Gofrugal", "link": "https://www.gofrugal.com/blog/grocery-industry-trends/", "location": "Global", "type": "article"},
    {"category": "Selling Anywhere", "title": "Omnichannel Shopping Is the Future of Retail in SA", "summary": "Explains how to combine online and in-store channels to improve convenience. Ideal for fashion and food merchants.", "source": "IT News Africa", "link": "https://www.itnewsafrica.com/2025/04/omnichannel-shopping-is-the-future-of-retail-in-south-africa/", "location": "South Africa", "type": "article"},
    {"category": "Selling Anywhere", "title": "Trends Shaping SA's Food Retail and Wholesale Sector", "summary": "Insights on consumer behavior and retail competition. Helps SMBs differentiate through value and localization.", "source": "Sabinet", "link": "https://sabinet.co.za/trends-shaping-south-africas-food-retail-and-wholesale-sector/", "location": "South Africa", "type": "article"},
    {"category": "Selling Anywhere", "title": "8 Fastest-Growing Small Businesses in Food & Beverage", "summary": "Presents growing niches like online catering and urban microfarms. Adaptable ideas for SA entrepreneurs.", "source": "Stacker", "link": "https://walterborolive.com/premium/stacker/stories/the-8-fastest-growing-small-businesses-in-food-restaurants-and-beverages-for-2026", "location": "Global", "type": "article"},
    {"category": "Managing Your Finances", "title": "Structuring Your Finances for an SME in South Africa", "summary": "Basics on separating finances, bookkeeping, and tax planning. Valuable for first-time entrepreneurs.", "source": "M&J Group", "link": "https://mjgroup.africa/structuring-your-finances-for-an-sme-in-south-africa/", "location": "South Africa", "type": "guide"},
    {"category": "Managing Your Finances", "title": "SADC Strategy on Financial Inclusion and SME Finance", "summary": "Outlines barriers and solutions for SME finance in Southern Africa. Useful context for grants or development finance.", "source": "FinMark Trust", "link": "https://finmark.org.za/Publications/SADC_Strategy_on_Financial_Inclusion_and_SME_Access_to_Finance_2023_2028.pdf", "location": "Africa", "type": "update"},
    {"category": "Managing Your Finances", "title": "2025 Business Year in Review: Survival and Resilience", "summary": "Reviews how SA SMEs navigated cost pressures in 2025. Helps owners plan financially for 2026.", "source": "Vutivi Business News", "link": "https://vutivibusiness.co.za/business/2025-business-year-in-review-survival-strain-and-sme-resilience/", "location": "South Africa", "type": "article"},
    {"category": "Operating Your Business", "title": "Small Businesses Anticipate Steady Economic Gains 2026", "summary": "Commentary on inflation and interest rates for 2026. Timely for merchants planning inventory and financing.", "source": "Vutivi Business News", "link": "https://vutivibusiness.co.za/business/small-businesses-anticipate-steady-economic-gains-in-2026/", "location": "South Africa", "type": "news"},
    {"category": "Operating Your Business", "title": "SME December Outlook: Festive Season Time to Shine", "summary": "Advice for retail and hospitality on stock and staffing during peaks. Useful template for planning high-demand months.", "source": "The Citizen", "link": "https://www.citizen.co.za/business/sme-december-outlook-festive-season-time-for-small-businesses-to-shine/", "location": "South Africa", "type": "news"},
    {"category": "Operating Your Business", "title": "4 Ways to Thrive as a SA Hospitality SME in Winter", "summary": "Practical tactics for guesthouses to boost occupancy in off-peak months. Relevant for hospitality seasonality.", "source": "Bizcommunity", "link": "https://www.bizcommunity.com/article/4-ways-to-thrive-as-a-sa-hospitality-sme-in-winter-473909a", "location": "South Africa", "type": "article"},
    {"category": "Operating Your Business", "title": "What's Next for Local Small Businesses in 2026?", "summary": "Discusses operational adjustments needed to survive based on the Small Business Growth Index.", "source": "Logistics News", "link": "https://www.logisticsnews.co.za/Articles/what-s-next-for-local-small-businesses-in-2026", "location": "South Africa", "type": "article"},
    {"category": "Growing Your Team", "title": "Staffing Strategies for Small Businesses (eGuide)", "summary": "How to plan staff levels, recruit, and onboard. Helps owners align staffing with cash flow.", "source": "Measured Ability", "link": "https://measuredability.com/small-business-staffing-strategies/", "location": "Global", "type": "guide"},
    {"category": "Growing Your Team", "title": "Essential Tips for Growing Your Small Hospitality Business", "summary": "Focuses on concrete steps to grow bookings and profits while recognizing the emotional side of running guesthouses.", "source": "IOL", "link": "https://iol.co.za/dailynews/opinion/2025-06-18-essential-tips-for-growing-your-small-hospitality-business-in-south-africa/", "location": "South Africa", "type": "article"},
    {"category": "Growing Your Team", "title": "How to Grow Your Hospitality Business in South Africa", "summary": "Actionable ideas like mobile-optimized websites and sustainability. Ideal for lodges wanting to stand out.", "source": "SME South Africa", "link": "https://smesouthafrica.co.za/how-to-grow-your-hospitality-business-in-south-africa/", "location": "South Africa", "type": "guide"},
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
def run_search(query):
    """Executes the AI search and makes result visible."""
    st.session_state.search_query = query
    st.session_state.ai_visible = True
    
    if not api_key:
        st.session_state.ai_result = "⚠️ Please configure your Gemini API Key."
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash') 
        
        system_prompt = (
            "You are 'Vuka', a helpful business assistant for Yoco merchants in South Africa. "
            "Keep answers concise, practical, and strictly relevant to the SA market (ZAR currency, SARS tax laws, etc). "
            f"User question: {query}"
        )
        
        with st.spinner("Vuka is thinking..."):
            response = model.generate_content(system_prompt)
            st.session_state.ai_result = response.text
            
    except Exception as e:
        st.session_state.ai_result = f"Error communicating with AI: {str(e)}"

# --- CALLBACKS (Crucial for button stability) ---

def toggle_ai_visibility():
    """Toggles the AI visibility state directly."""
    st.session_state.ai_visible = not st.session_state.ai_visible

def handle_search_submit():
    """Handles text input changes safely."""
    query = st.session_state.main_search_input
    # Only run search if the query is different from what we already have
    if query and query != st.session_state.search_query:
        run_search(query)

def on_filter_change():
    """Hides AI result when filters change, but keeps the data ready."""
    if st.session_state.ai_result:
        st.session_state.ai_visible = False

# --- 6. CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');

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
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .logo-row {
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 15px;
    }
    .yoco-logo-img { height: 85px; width: auto; }
    .vuka-text {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700; font-size: 80px; color: #FFFFFF;
        letter-spacing: -1.5px; line-height: 1; padding-top: 10px;
    }
    .tagline {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700; font-size: 2rem; color: #FFFFFF; margin-bottom: 0.5rem;
    }
    .description {
        font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #94A3B8;
        max-width: 600px; line-height: 1.5;
    }

    /* BUTTONS & CARDS */
    .stButton button {
        border-radius: 20px; font-size: 0.8rem; background-color: white;
        color: #5c6c7f; border: 1px solid #eee; padding: 0.25rem 1rem; width: 100%;
    }
    .stButton button:hover { border-color: #009fe3; color: #009fe3; }
    
    div[data-testid="stColumn"] {
        background-color: white; border: 1px solid #eef0f2; border-radius: 12px;
        padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        height: 100%; display: flex; flex-direction: column;
    }
    div[data-testid="stColumn"]:hover {
        transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0, 159, 227, 0.15);
        border-color: #009fe3;
    }

    /* TAGS */
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
    
    /* TEXT */
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
    <div class="logo-row">
        <img src="{logo_url}" class="yoco-logo-img" alt="YOCO">
        <span class="vuka-text">Vuka</span>
    </div>
    <div class="tagline">Wake up to growth</div>
    <div class="description">Daily insights, guides, and tools for South African entrepreneurs ready to scale.</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# B. SEARCH INPUT
# Using on_change callback to trigger search safely
st.text_input("", 
              placeholder="Ask Vuka AI anything...", 
              key="main_search_input",
              value=st.session_state.search_query,
              on_change=handle_search_submit)

# C. EXAMPLE PROMPTS
cols = st.columns(len(EXAMPLE_PROMPTS))
for i, prompt_text in enumerate(EXAMPLE_PROMPTS):
    with cols[i]:
        # Clicking a button runs the search via direct call and rerun
        if st.button(prompt_text, use_container_width=True):
            run_search(prompt_text)
            st.rerun()

# D. AI RESULT SECTION (With Hide/Show Logic)
if st.session_state.ai_result:
    st.markdown("---")
    
    col_res_1, col_res_2 = st.columns([5, 1])
    with col_res_1:
        if st.session_state.ai_visible:
            st.caption(f"🤖 AI Insight for: **{st.session_state.search_query}**")
        else:
            st.caption(f"🤖 AI Insight (Hidden) for: **{st.session_state.search_query}**")
            
    with col_res_2:
        # Toggle Button using on_click CALLBACK
        btn_label = "🙈 Hide" if st.session_state.ai_visible else "👁️ Show"
        st.button(btn_label, key="toggle_ai_btn", on_click=toggle_ai_visibility)

    if st.session_state.ai_visible:
        with st.chat_message("assistant", avatar="⚡"):
            st.write(st.session_state.ai_result)

st.markdown("---")

# --- 8. FILTERS & CONTENT GRID ---

categories = list(CATEGORY_COLORS.keys())

# Filters using on_change CALLBACK
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
        
        # Color Logic
        cat_class = "cat-operating"
        for cat_name, _ in CATEGORY_COLORS.items():
            if item['category'] == cat_name:
                if "Starting" in cat_name: cat_class = "cat-starting"
                elif "Reaching" in cat_name: cat_class = "cat-reaching"
                elif "Selling" in cat_name: cat_class = "cat-selling"
                elif "Finances" in cat_name: cat_class = "cat-finances"
                elif "Operating" in cat_name: cat_class = "cat-operating"
                elif "Growing" in cat_name: cat_class = "cat-team"
        
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
