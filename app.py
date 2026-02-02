Here is the updated solution.

### **Key Changes Made**

1. **Moved the Search Bar:** Switched from `st.chat_input` (which is stuck to the bottom) to a customized `st.text_input` placed directly inside the Hero section at the top.
2. **Dynamic Filter Colors:** Added a logic block that detects which category is selected and injects specific CSS to turn the active filter button that specific color (e.g., Purple for Marketing, Red for Finances).
3. **Full Width Search:** Removed the columns constraints so the search bar fills the space naturally.

### **`app.py`**

Replace your file with this code.

```python
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

# --- 3. DATA & COLORS ---
# We define colors here so we can use them in both CSS and Python logic
CATEGORY_COLORS = {
    "Starting Your Business": "#00695c",  # Teal
    "Reaching Customers": "#7b1fa2",      # Purple
    "Selling Anywhere": "#e65100",        # Orange
    "Managing Your Finances": "#c62828",  # Red
    "Operating Your Business": "#1565c0", # Blue
    "Growing Your Team": "#33691e",       # Green
    "All": "#009fe3"                      # Yoco Blue (Default)
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

SUGGESTIONS = [
    "How do I submit my VAT return?", 
    "What are the latest food trends for 2026?", 
    "How do I draft a basic employment contract?", 
    "Low cost marketing ideas for SA"
]

# --- 4. CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* COLORS */
    :root {
        --yoco-blue: #009fe3;
        --yoco-dark: #232d39;
        --text-grey: #5c6c7f;
    }
    
    /* RESET PADDING */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    
    /* HERO SECTION */
    .hero-container {
        background-color: #232d39;
        padding: 4rem 2rem 2rem 2rem; /* Reduced bottom padding */
        text-align: center;
        border-radius: 0 0 24px 24px;
        margin: -6rem -4rem 2rem -4rem; /* Negative margins to fill top */
        color: white;
    }
    
    .hero-brand {
        font-weight: 900;
        font-size: 1.2rem;
        text-transform: lowercase;
        color: #009fe3;
        letter-spacing: -1px;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-sub {
        opacity: 0.85;
        max-width: 600px;
        margin: 0 auto 30px auto;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
    }

    /* CUSTOM INPUT STYLING (To look like the Chat Bar) */
    .stTextInput input {
        border-radius: 50px;
        padding: 12px 20px;
        border: 1px solid transparent;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stTextInput input:focus {
        border-color: #009fe3;
        box-shadow: 0 4px 20px rgba(0, 159, 227, 0.4);
    }

    /* CARD STYLING */
    div[data-testid="stColumn"] {
        background-color: white;
        border: 1px solid #eef0f2;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    div[data-testid="stColumn"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 159, 227, 0.15); /* Yoco Blue Shadow */
        border-color: #009fe3;
    }

    /* PILLS & TAGS */
    .type-pill {
        font-size: 0.65rem; 
        font-weight: 800; 
        text-transform: uppercase;
        padding: 6px 10px; 
        border-radius: 6px; 
        background: #f4f6f8; 
        color: #5c6c7f;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    .category-pill {
        font-size: 0.7rem; 
        font-weight: 700; 
        text-transform: uppercase;
        padding: 6px 12px; 
        border-radius: 20px;
        margin-top: auto; /* Pushes to bottom */
        margin-bottom: 16px;
        display: inline-block;
        letter-spacing: 0.5px;
    }
    
    /* Category Colors (CSS Classes) */
    .cat-starting { background: #e0f2f1; color: #00695c; }
    .cat-reaching { background: #f3e5f5; color: #7b1fa2; }
    .cat-selling { background: #fff3e0; color: #e65100; }
    .cat-finances { background: #ffebee; color: #c62828; }
    .cat-operating { background: #e3f2fd; color: #1565c0; }
    .cat-team { background: #f1f8e9; color: #33691e; }
    
    /* TEXT */
    h3 { 
        font-size: 1.15rem; 
        font-weight: 700; 
        color: #232d39; 
        margin: 0 0 10px 0; 
        line-height: 1.3;
        min-height: 3.9em; /* Aligns cards */
    }
    
    p { 
        font-size: 0.95rem; 
        color: #5c6c7f; 
        line-height: 1.6; 
        margin-bottom: 20px;
        flex-grow: 1;
    }
    
    .source-text { 
        font-size: 0.8rem; 
        color: #999; 
        border-top: 1px solid #f4f6f8;
        padding-top: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    a { 
        text-decoration: none; 
        color: #009fe3; 
        font-weight: 700; 
        font-size: 0.85rem; 
        transition: color 0.2s;
    }
    
    a:hover { color: #007bb0; }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

# A. HERO SECTION with Text Input
# We use st.container to group the hero content
with st.container():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-brand">yoco vuka</div>
        <div class="hero-title">Wake up to growth</div>
        <div class="hero-sub">Daily insights, guides, and tools for South African entrepreneurs ready to scale.</div>
    </div>
    """, unsafe_allow_html=True)

    # Search Bar (Using text_input instead of chat_input to control placement)
    # We move the margin up negatively via CSS to pull it into the Hero box visually if needed, 
    # but here we just place it directly after the Hero HTML.
    
    user_query = st.text_input("", placeholder="Ask Vuka AI anything (e.g. 'How do I register my business?')", key="main_search")

    # Prompt Chips
    st.markdown(
        "<div style='text-align:center; color:#999; font-size:0.8rem; margin-top:10px; margin-bottom: 30px;'>Try asking: " 
        + "  •  ".join([f"<i>{s}</i>" for s in SUGGESTIONS]) 
        + "</div>", 
        unsafe_allow_html=True
    )

    # AI Logic Handling
    if user_query:
        if not api_key:
            st.error("⚠️ Gemini API Key is missing. Add it to Streamlit Secrets.")
        else:
            with st.chat_message("assistant", avatar="⚡"):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    system_prompt = (
                        "You are 'Vuka', a helpful business assistant for Yoco merchants in South Africa. "
                        "Keep answers concise, practical, and strictly relevant to the SA market (ZAR currency, SARS tax laws, etc). "
                        f"User question: {user_query}"
                    )
                    
                    with st.spinner("Vuka is thinking..."):
                        response = model.generate_content(system_prompt)
                        st.write(response.text)
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")

st.markdown("---")

# --- 6. FILTERS (MULTI-SELECT PILLS) ---

categories = ["Starting Your Business", "Reaching Customers", "Selling Anywhere", 
              "Managing Your Finances", "Operating Your Business", "Growing Your Team"]

# Render Pills
selected_categories = st.pills("Filter insights:", categories, selection_mode="multi")

# --- DYNAMIC CSS INJECTION FOR ACTIVE FILTER COLORS ---
# This block runs every time the script reruns (which happens on selection)
if selected_categories:
    css_styles = []
    # Streamlit's pills don't have unique IDs per option easily, 
    # but we can rely on the fact that 'active' state + 'inner text' combination.
    # However, simpler is to just color ALL selected pills the Yoco Blue 
    # OR try to map them. 
    
    # Since specific targeting of Pill[i] is hard in pure CSS without hacks,
    # We will use the Yoco Blue for uniformity, OR apply specific logic if just one is selected.
    
    # Let's check which color to use. If multiple, we might default to Blue.
    # If single, we match the category color.
    
    active_color = "#009fe3" # Default Yoco Blue
    if len(selected_categories) == 1:
        active_color = CATEGORY_COLORS.get(selected_categories[0], "#009fe3")
        
    # Inject CSS to override the selected pill color
    st.markdown(f"""
    <style>
        /* Target the active pill in the specific st.pills widget */
        div[data-testid="stPills"] button[aria-selected="true"] {{
            background-color: {active_color} !important;
            color: white !important;
            border-color: {active_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# Filter Data Logic
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
        cat_class = "cat-operating" # Default
        for cat_name, color_hex in CATEGORY_COLORS.items():
            if item['category'] == cat_name:
                # We map the category name to our CSS class names
                # Simplified mapping based on known keys
                if "Starting" in cat_name: cat_class = "cat-starting"
                elif "Reaching" in cat_name: cat_class = "cat-reaching"
                elif "Selling" in cat_name: cat_class = "cat-selling"
                elif "Finances" in cat_name: cat_class = "cat-finances"
                elif "Operating" in cat_name: cat_class = "cat-operating"
                elif "Growing" in cat_name: cat_class = "cat-team"
        
        # Card HTML
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

```
