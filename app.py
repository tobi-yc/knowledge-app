import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Yoco Vuka | Merchant Insights",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SETUP GEMINI AI ---
# Try to get the key from Streamlit Secrets (Cloud) or Environment (Local)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# --- 3. DATA CONTENT ---
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

# --- 4. CSS STYLING (YOCO THEME) ---
st.markdown("""
<style>
    /* Global Font & Colors */
    :root { --yoco-blue: #009fe3; --yoco-dark: #232d39; }
    
    /* Hero Section */
    .hero {
        background-color: #232d39;
        color: white;
        padding: 3rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: white; }
    .hero p { opacity: 0.9; font-size: 1.1rem; }
    
    /* Tiles/Cards */
    div[data-testid="stColumn"] > div {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s;
    }
    div[data-testid="stColumn"] > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        border-color: #009fe3;
    }
    
    /* Typography inside cards */
    .card-type { font-size: 0.7rem; font-weight: 800; text-transform:
