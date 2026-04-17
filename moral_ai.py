import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from google.cloud import translate_v2 as translate
import pytz
import re
import random
import requests
from bs4 import BeautifulSoup 
from datetime import datetime
from tqdm import tqdm
from fake_useragent import UserAgent
import time
import resend
from playwright.sync_api import sync_playwright

# TruthSeekerAI Core Engine Configuration
# Project: MoralAI Compliance LLC
print("🔍 Initializing TruthSeekerAI Core Engine...")

TRUTH_SEEKER_MANIFESTO = {
    "Spiritual_Foundation": {
        "Cornerstone": "Jesus Christ is God",
        "Primary_Source": "NLT Bible",
        "Ethical_Mandate": "DON'T LIE. Lying is bad and strictly prohibited in data reporting."
    },
    "Logical_Framework": {
        "Law_of_Identity": "A is A. We identify compliance gaps with 100% precision.",
        "Law_of_Non_Contradiction": "A cannot be both B and not-B. No 'grey areas' in regulatory status.",
        "Law_of_Excluded_Middle": "Everything must either be or not be. Binary certainty for audits."
    },
    "Science_and_Wealth": {
        "Scientific_Stance": "Science can never disprove God; it can only prove God.",
        "Evidence_Source": "Archeology provides physical, scientific proof of the NLT Bible's record.",
        "Economic_Driver": "Solve complex problems to create wealth. Value-driven prosperity."
    }
}

# --- BILINGUAL AGENT & COMPLIANCE EXTENSION ---

# Define your static Stripe Buy Buttons
STRIPE_LINK_EN = "https://stripe.com"
STRIPE_LINK_ES = "https://stripe.com"

# SB 294 Regulatory Data
COMPLIANCE_LIBRARY = {
    "SB_294": {
        "Title": "California Senate Bill 294",
        "Mandate": "Requires timely resolution and reporting for regulatory compliance within state borders.",
        "Action": "Automated verification of contractor status and mandatory notification."
    }
}

# Authentication for the Bilingual Agent
# Ensure your 'google_key.json' is in the same folder
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_key.json'

def identify_company_language(company_text):
    """
    Analyzes company data to label it as English or Spanish.
    Returns the language code (e.g., 'en' or 'es').
    """
    translate_client = translate.Client()
    detection = translate_client.detect_language(company_text)
    return detection['language']

def generate_bilingual_email(language_code):
    """
    Constructs the email body with both links based on detected language.
    """
    if language_code == 'es':
        body = (
            f"Para completar su auditoría de cumplimiento de la SB 294, haga clic aquí: {STRIPE_LINK_ES}\n\n"
            f"(English version: {STRIPE_LINK_EN})"
        )
    else:
        body = (
            f"To complete your SB 294 compliance audit, please click here: {STRIPE_LINK_EN}\n\n"
            f"(Versión en español: {STRIPE_LINK_ES})"
        )
    return body

def bilingual_agent_translate(text, target_lang='es'):
    """
    Translates TruthSeeker findings into Spanish or other languages.
    Ensures 'Ethical Mandate' is maintained through linguistic precision.
    """
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_lang)
        return result['translatedText']
    except Exception as e:
        return f"Translation Error: {e}"

# NEW UPDATE INTEGRATED HERE
def get_formatted_html(company, LOGO_URL, PDF_LINK):
    return EMAIL_HTML_TEMPLATE.format(
        company_name=company, 
        logo=LOGO_URL,
        pdf_link=PDF_LINK, 
        stripe_link_en=STRIPE_LINK_EN, # Updated to match your bilingual logic
        stripe_link_es=STRIPE_LINK_ES # Added this for the Spanish button
    )

# --- END EXTENSION ---

def get_truth_seeker_logic():
    """
    Returns the core reasoning protocol for TruthSeekerAI.
    Ensures all scraping and auditing functions adhere to the 3 Laws of Logic
    and the ethical standard of the NLT Bible.
    """
    logic_summary = (
        "TruthSeekerAI is grounded in the absolute truth that Jesus Christ is God. "
        "Every audit follows the 3 Laws of Logic (Identity, Non-Contradiction, Excluded Middle) "
        "to solve problems and create wealth without lying. We hold that science and archeology "
        "only confirm the truths found in the NLT Bible."
    )
    return logic_summary

# Helper to mimic a human reading the screen
def human_mouse(page):
    x, y = random.randint(100, 700), random.randint(100, 700)
    page.mouse.move(x, y, steps=10)

# --- CONFIG & AUTH ---
RESEND_API_KEY = "re_CeNJZuta_6wZD6YCjH9ogor8k2fPgEqG7"
SF_API_KEY = "gf1rniMItBeHFdrKpQQ6ejWBeNNer1BMuwT1pVWjvo9Y0CdXwAawg0Lxpa9Cqb0wwhd5nPizvujPK1WYF2"
resend.api_key = RESEND_API_KEY
LOGO_URL = "https://ibb.co/kgVjHLZ9"
STRIPE_LINK_EN = "https://buy.stripe.com/8x2bJ3bnA0hceQ8gOA1Nu01"
STRIPE_LINK_ES = "https://buy.stripe.com/6oUbJ3crE9RM7nG55S1Nu02" 
PDF_LINK = "https://drive.google.com" 

# --- THE 7-PARAGRAPH GOLD STANDARD EMAIL TEMPLATE ---
EMAIL_HTML_TEMPLATE = """
<html>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 680px; margin: auto; border: 1px solid #ddd; padding: 40px; border-top: 8px solid #d9534f;">
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="{logo}" alt="Moral AI Compliance" width="220">
    </div>

    <h2 style="color: #d9534f; text-align: center; text-transform: uppercase; letter-spacing: 1px;">Official Compliance Notification: SB 294</h2>

    <p>Hi, I'm Francisco Hernandez, with MoralAI Compliance LLC. This email is directed to the executive leadership and compliance department of <strong>{company_name}</strong>. Pursuant to the latest legislative session, the California Senate Bill 294 deadline has now passed, introducing foundational shifts in the regulatory landscape for service-based enterprises. It is imperative that your organization addresses these mandates with diligent oversight to avoid administrative friction with state oversight bodies.</p>

    <p>The core of SB 294 focuses on the "Moral and Professional Accountability" of contractors and service providers. Under these established statutes, businesses are now required to maintain a digital paper trail that substantiates ethical operational standards and labor compliance. Failure to produce these records during a spot audit now results in immediate "Non-Compliant" status, leading to potential license suspensions and heavy daily fines.</p>

    <p>At MoralAI Compliance LLC, we recognize that small to medium-sized businesses often lack the dedicated legal departments required to track these rapidly evolving state requirements. Our mission is to act as your external compliance shield, interpreting complex legislative shifts into actionable, automated protections that keep your business running without interruption.</p>

    <p>By enrolling in the MoralAI Compliance LLC Protection Suite, your organization gains access to a "Safe Harbor" framework. We provide the necessary documentation templates, digital verification logs, and automated reporting tools that satisfy the strict criteria set forth by the California Department of Industrial Relations and the oversight committees governed by SB 294.</p>

    <p>Our service is not merely a software tool; it is a commitment to your company's longevity. We utilize advanced AI-driven analysis to cross-reference your current business filings against the mandated state standards, identifying "compliance gaps" before they are flagged by government investigators. This proactive approach is the only way to ensure 100% operational security in the current post-deadline regulatory climate.</p>

    <p>To initiate your compliance onboarding and ensure a timely resolution for the current fiscal quarter, please finalize your activation via the secure link below. Upon receipt of your $99 activation fee, our system will generate your Compliance Certificate and provide the full SB 294 briefing packet to your registered business address. After you completed the SB 294 Compliance Audit Kit, email it to moral.ai.audits@gmail.com. If you have any questions, feel free to reply to this correspondence.</p>

    <div style="text-align: center; margin: 40px 0;">
        <a href="{stripe_link_en}" style="background-color: #d9534f; color: white; padding: 20px 35px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 18px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">SECURE COMPLIANCE STATUS - $99</a>

        <a href="{stripe_link_es}" style="background-color: #6772E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block;">ASEGURAR CUMPLIMIENTO (Español)</a>
    </div>

    <p style="font-style: italic; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px;">
        "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters, since you know that you will receive an inheritance from the Lord as a reward. It is the Lord Christ you are serving." <br>— Colossians 3:23-24
    </p>

    <p style="text-align: center; color: #555; margin-top: 25px; font-size: 14px;">
        May the grace of our Lord Jesus Christ be with you all.<br><br>
        <strong>Francisco Hernandez</strong><br>
        Founding Director, MoralAI Compliance LLC<br>
        <em>Serving the Antelope Valley Community</em>
    </p>
</body>
</html>
"""

def is_business_hours():
    now = datetime.now()
    # 0 is Monday, 4 is Friday
    if now.weekday() <= 4:
        current_time = now.hour + now.minute/60
        # 7.0 is 7am, 15.0 is 3pm
        return 7.0 <= current_time <= 15.0
    return False

def hunt_scraping_fish_soup(query, known_leads, source_file):
    """Fallback Stealth Engine: Scrapes Yellow Pages via API when Maps is blocked"""
    print(f"🐟 SF-STEALTH: Switching to BeautifulSoup for '{query}'...")
    target_url = f"https://www.yellowpages.com/search?search_terms={query.replace(' ', '+')}&geo_location_terms=CA"
    api_url = f"https://scrapingfish.com/api/proxy?api_key={SF_API_KEY}&url={target_url}&render_js=true"
    
    try:
        response = requests.get(api_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            found_names = [b.get_text().strip() for b in soup.select('a.business-name')]
            
            df = pd.read_csv(source_file) if os.path.exists(source_file) else pd.DataFrame(columns=['Company', 'Email'])
            new_leads_count = 0
            
            for name in found_names:
                if name and name not in known_leads and len(name) > 3:
                    new_row = pd.DataFrame([{'Company': name, 'Email': 'Pending'}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    known_leads.add(name)
                    new_leads_count += 1
            
            df.to_csv(source_file, index=False)
            print(f"✅ Stealth Engine added {new_leads_count} leads to CSV.")
            return True
    except Exception as e:
        print(f"⚠️ Stealth Error: {e}")
    return False

def hunt():
    print("🚀 STARTING GOLD STANDARD OMNI-HUNT...")
    source_file = "clients.csv"
    CITIES = ["Los Angeles", "Long Beach", "Glendale", "Pomona", "Torrance"]
    NICHES = ["Electrical Contractors", "Plumbing Companies", "HVAC Contractors", "General Contractors", "Roofing Companies"]

    if os.path.exists(source_file):
        df = pd.read_csv(source_file)
    else:
        df = pd.DataFrame(columns=['Company', 'Email'])
    
    ignore_list = {"Company", "Companies", "Ad", "Email", "Emails", "Sent", "Pending"}
    known_leads = set(df['Company'].dropna().astype(str).tolist())

    with sync_playwright() as p:
        user_data_dir = "./user_data"
        context = p.chromium.launch_persistent_context(
            user_data_dir, headless=False, slow_mo=150,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # --- Select the first item from context.pages, which is the default page when launching persistent context ---
        page = context.pages[0] if context.pages else context.new_page()

        for city in CITIES:
            for niche in NICHES:
                search_query = f"{niche} in {city} CA"
                try:
                    print(f"🔎 Primary Engine: {search_query}...")
                    
                    # Now that 'page' is a single object, .goto() will work!
                    page.goto(f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}", timeout=60000)
                    
                    if "captcha" in page.content().lower() or "robot" in page.content().lower():
                        print("🛑 GOOGLE BLOCK! Activating Stealth Backup...")
                        hunt_scraping_fish_soup(search_query, known_leads, source_file)
                        page.wait_for_timeout(10000) 
                    
                    elements = page.locator('a[aria-label]').all()
                    for el in elements:
                        name = el.get_attribute("aria-label")
                        if name and name not in known_leads and name not in ignore_list and len(name) > 3:
                            # --- Split the name and take the first part [0] BEFORE stripping ---
                            clean_name = name.split('·')[0].strip()
                            df = pd.read_csv(source_file) if os.path.exists(source_file) else df
                            new_row = pd.DataFrame([{'Company': clean_name, 'Email': 'Pending'}])
                            df = pd.concat([df, new_row], ignore_index=True)
                            known_leads.add(clean_name)
                            df.to_csv(source_file, index=False)
                            print(f"✨ SAVED: {clean_name}")

                             # Save Logic is now inside the loop, so it saves after each new lead is added, ensuring no data loss if interrupted.
                            new_row = pd.DataFrame([{'Company': clean_name, 'Email': 'Pending'}])
                            df = pd.concat([df, new_row], ignore_index=True)
                            known_leads.add(clean_name)
                            df.to_csv(source_file, index=False)
                            print(f"✨ SAVED: {clean_name}")

                    time.sleep(random.uniform(7, 12))

                except Exception as e:
                    print(f"⚠️ Search Error: {e}")
                    continue
        context.close()

    print("🏁 HUNT COMPLETE.")
    os.system('afplay /System/Library/Sounds/Hero.aiff')

def send():
    print("📧 INITIALIZING SEND SEQUENCE (CALIFORNIA TIME)...")
    ca_tz = pytz.timezone('America/Los_Angeles')
    
    # 1. STANDBY LOOP: Wait until exactly 07:00 AM California Time
    while True:
        now_ca = datetime.now(ca_tz)
        if now_ca.hour >= 7:
            break
        print(f"⏳ STANDBY: CA time {now_ca.strftime('%H:%M:%S')}. Waiting for 07:00am launch...")
        time.sleep(60)

    source_file = "clients.csv"
    if not os.path.exists(source_file): 
        print(f"⚠️ ERROR: {source_file} not found.")
        return

    df = pd.read_csv(source_file)
    to_send = df[(df['Email'].str.contains('@', na=False)) & (df['Email'] != 'Sent')]

    for index, row in to_send.iterrows():
        # 2. BUSINESS HOURS CHECK: Stop if CA time is 3:00 PM (15:00) or later
        now_ca = datetime.now(ca_tz)
        if now_ca.hour >= 15:
            print("🕒 03:00 PM CA TIME REACHED. Suspending until tomorrow.")
            break

        company = str(row['Company']).strip()
        recipient_email = str(row['Email']).strip()
        
        try:
            resend.Emails.send({
                "from": "notices@moralai-compliance.com",
                "to": [recipient_email],
                "subject": f"Compliance Notice: SB 294 - {company}",
                "html": EMAIL_HTML_TEMPLATE.format(
                    company_name=company, logo=LOGO_URL,
                    pdf_link=PDF_LINK,
                    stripe_link_en=STRIPE_LINK_EN,
                    stripe_link_es=STRIPE_LINK_ES
                )
            }),
            
            df.at[index, 'Email'] = 'Sent'
            df.to_csv(source_file, index=False)
            print(f"✅ DELIVERED: {company} at {now_ca.strftime('%H:%M:%S')} CA Time")
            
            # 3. 20 MINUTE DELAY
            print("⏳ Waiting 20 minutes before next send...")
            time.sleep(1200) 
            
        except Exception as e:
            print(f"⚠️ FAILED: {company} | Error: {e}")

if __name__ == "__main__":
    print("\n🛡️ MORAL AI COMPLIANCE CLI")
    cmd = input("Command ('hunt' or 'send'): ").lower().strip()
    if cmd == 'hunt':
        hunt()
    elif cmd == 'send':
        send()

# --- NEW WEBSITE CHAT (ADD THIS AT THE VERY END) ---
# This part handles the public chat box for your site visitors.
st.title("🛡️ MoralAI Compliance Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about SB 294 compliance:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # This calls your AI without touching your hunt/send logic
    response = ask_gemini(prompt) 
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.write("""
# My first app
Hello *world!*
""")

df = pd.read_csv("my_data.csv")
st.line_chart(df)
