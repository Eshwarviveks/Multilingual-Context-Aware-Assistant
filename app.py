import streamlit as st
import spacy
import nltk
from nltk.wsd import lesk
from googletrans import Translator
from gtts import gTTS
import uuid
import os

# -----------------------------
# INITIAL SETUP
# -----------------------------
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

translator = Translator()
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# PAGE CONFIG & CUSTOM CSS
# -----------------------------
st.set_page_config(
    page_title="LinguaBot — Multilingual AI Assistant",
    page_icon="🌐",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root & Background ── */
:root {
    --ink:       #0d0f14;
    --surface:   #13151c;
    --card:      #1a1d27;
    --border:    #2a2e3f;
    --accent:    #5bf0c0;
    --accent2:   #ff6b6b;
    --accent3:   #ffd166;
    --muted:     #6b7280;
    --text:      #e8eaf0;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--ink);
    color: var(--text);
}

/* Kill default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem; max-width: 760px; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(91,240,192,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(91,240,192,0.35);
    background: rgba(91,240,192,0.06);
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e8eaf0 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}

/* ── Section Labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
    margin-top: 2rem;
}

/* ── Cards ── */
.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(91,240,192,0.3); }

.result-card h4 {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 0.8rem;
}

/* ── POS Tags ── */
.pos-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.pos-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.3rem 0.7rem;
    font-size: 0.82rem;
}
.pos-tag .word { color: var(--text); font-weight: 500; }
.pos-tag .pos  { color: var(--accent3); font-size: 0.7rem; font-weight: 400; }

/* ── WSD Rows ── */
.wsd-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
}
.wsd-item:last-child { border-bottom: none; }
.wsd-word { color: var(--accent); font-weight: 600; font-size: 0.9rem; }
.wsd-def  { color: var(--muted); font-size: 0.82rem; font-weight: 300; }

/* ── Intent Pill ── */
.intent-pill {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 0.45rem 1.2rem;
    border-radius: 100px;
    border: 1.5px solid var(--accent2);
    color: var(--accent2);
    background: rgba(255,107,107,0.08);
}

/* ── Response Box ── */
.response-box {
    background: linear-gradient(135deg, rgba(91,240,192,0.07), rgba(91,240,192,0.02));
    border: 1px solid rgba(91,240,192,0.3);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-size: 1.05rem;
    font-weight: 400;
    line-height: 1.65;
    color: var(--text);
    margin-bottom: 1rem;
}

/* ── Translation Note ── */
.trans-note {
    background: rgba(255,209,102,0.07);
    border-left: 3px solid var(--accent3);
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    font-size: 0.83rem;
    color: var(--accent3);
    margin-bottom: 1.25rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] > label,
div[data-testid="stTextInput"] > label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted) !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: rgba(91,240,192,0.5) !important;
    box-shadow: 0 0 0 3px rgba(91,240,192,0.08) !important;
}

/* ── Button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #3dd9a8) !important;
    color: var(--ink) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(91,240,192,0.25) !important;
    margin-top: 0.5rem;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# NLP FUNCTIONS
# -----------------------------
def pos_tagging(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

def word_sense_disambiguation(sentence):
    words = sentence.split()
    senses = {}
    for word in words:
        sense = lesk(words, word)
        if sense:
            senses[word] = sense.definition()
    return senses

def detect_intent(text):
    text = text.lower()
    if "book" in text:
        return "Booking"
    elif "weather" in text:
        return "Weather"
    elif "bank" in text or "deposit" in text or "withdraw" in text:
        return "Banking"
    else:
        return "General"

def generate_response(intent):
    responses = {
        "Booking":  "I can help you with booking services. Please share the details — date, destination, or service type.",
        "Weather":  "Please provide your location and I'll fetch the latest weather details for you.",
        "Banking":  "Sure! Are you looking for balance info, a recent transaction, or something else?",
        "General":  "Could you clarify your request? I'm here to help with bookings, weather, banking, and more.",
    }
    return responses.get(intent, "Could you please clarify your request?")

def speak(text, lang_code):
    try:
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filename)
        with open(filename, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        os.remove(filename)
    except Exception as e:
        st.error(f"Speech generation failed: {e}")

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">Powered by NLP + gTTS</div>
    <h1>LinguaBot</h1>
    <p>Context-aware multilingual assistant — speak in any language, understand everything.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# -----------------------------
# LANGUAGE OPTIONS
# -----------------------------
language_options = {
    "🇬🇧  English": "en",
    "🇮🇳  Hindi": "hi",
    "🇮🇳  Telugu": "te",
    "🇮🇳  Tamil": "ta",
    "🇮🇳  Kannada": "kn",
    "🇮🇳  Malayalam": "ml",
    "🇮🇳  Marathi": "mr",
    "🇮🇳  Bengali": "bn",
    "🇮🇳  Gujarati": "gu",
    "🇮🇳  Punjabi": "pa",
    "🇪🇸  Spanish": "es",
    "🇫🇷  French": "fr",
    "🇩🇪  German": "de",
    "🇸🇦  Arabic": "ar",
    "🇨🇳  Chinese (Simplified)": "zh-cn",
}

col1, col2 = st.columns([1, 2])
with col1:
    selected_language = st.selectbox("Language", list(language_options.keys()))
language_code = language_options[selected_language]

with col2:
    user_input = st.text_input("Your query", placeholder="e.g. I want to book a flight to Delhi...")

analyze = st.button("⚡  Analyze Query")

# -----------------------------
# ANALYSIS
# -----------------------------
if analyze:
    if not user_input.strip():
        st.warning("Please enter a query first.")
    else:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # Translation
        if language_code != "en":
            translated_input = translator.translate(user_input, dest="en").text
            st.markdown(f"""
            <div class="trans-note">
                ↳ Translated to English: <strong>{translated_input}</strong>
            </div>""", unsafe_allow_html=True)
        else:
            translated_input = user_input

        # ── POS Tagging ──
        st.markdown('<div class="section-label">POS Tagging</div>', unsafe_allow_html=True)
        pos_results = pos_tagging(translated_input)
        tags_html = '<div class="result-card"><h4>Part-of-Speech Tags</h4><div class="pos-row">'
        for word, pos in pos_results:
            tags_html += f'<span class="pos-tag"><span class="word">{word}</span><span class="pos">{pos}</span></span>'
        tags_html += '</div></div>'
        st.markdown(tags_html, unsafe_allow_html=True)

        # ── WSD ──
        st.markdown('<div class="section-label">Word Sense Disambiguation</div>', unsafe_allow_html=True)
        senses = word_sense_disambiguation(translated_input)
        if senses:
            wsd_html = '<div class="result-card"><h4>Detected Word Senses</h4>'
            for word, meaning in senses.items():
                wsd_html += f'<div class="wsd-item"><span class="wsd-word">{word}</span><span class="wsd-def">{meaning}</span></div>'
            wsd_html += '</div>'
        else:
            wsd_html = '<div class="result-card"><h4>Detected Word Senses</h4><span style="color:var(--muted);font-size:0.85rem;">No ambiguous words detected.</span></div>'
        st.markdown(wsd_html, unsafe_allow_html=True)

        # ── Intent ──
        st.markdown('<div class="section-label">Intent Detection</div>', unsafe_allow_html=True)
        intent = detect_intent(translated_input)
        intent_icons = {"Booking": "✈️", "Weather": "⛅", "Banking": "🏦", "General": "💬"}
        st.markdown(f"""
        <div class="result-card">
            <h4>Detected Intent</h4>
            <span class="intent-pill">{intent_icons.get(intent,'')} &nbsp;{intent}</span>
        </div>""", unsafe_allow_html=True)

        # ── Response ──
        response = generate_response(intent)
        if language_code != "en":
            response = translator.translate(response, dest=language_code).text

        st.markdown('<div class="section-label">Assistant Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="response-box">🤖 &nbsp;{response}</div>', unsafe_allow_html=True)

        # ── Audio ──
        st.markdown('<div class="section-label">Voice Output</div>', unsafe_allow_html=True)
        speak(response, language_code)