import streamlit as st
import spacy
import nltk
from nltk.wsd import lesk
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import uuid

# -----------------------------
# INITIAL SETUP
# -----------------------------
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

translator = Translator()
nlp = spacy.load("en_core_web_sm")
pygame.mixer.init()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Context AI Assistant",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --bg:          #0b0f1a;
    --bg-card:     #111827;
    --bg-lifted:   #1a2235;
    --accent:      #7c6af7;
    --accent-2:    #a78bfa;
    --accent-glow: rgba(124,106,247,0.25);
    --teal:        #2dd4bf;
    --teal-glow:   rgba(45,212,191,0.2);
    --amber:       #fbbf24;
    --green:       #34d399;
    --red:         #f87171;
    --text:        #e2e8f0;
    --text-mid:    #94a3b8;
    --text-dim:    #475569;
    --border:      rgba(255,255,255,0.07);
    --border-acc:  rgba(124,106,247,0.3);
  }

  /* ── Base ── */
  .stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    background-image:
      radial-gradient(ellipse 90% 50% at 50% -15%, rgba(124,106,247,0.12) 0%, transparent 60%),
      radial-gradient(ellipse 50% 40% at 90% 80%, rgba(45,212,191,0.06) 0%, transparent 55%) !important;
    font-family: 'Outfit', sans-serif;
    color: var(--text);
  }

  [data-testid="stHeader"], header { background: transparent !important; box-shadow: none !important; }
  .block-container { max-width: 700px !important; padding: 0 1.5rem 4rem !important; }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 3.8rem 0 0.5rem;
  }
  .hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(124,106,247,0.12);
    border: 1px solid var(--border-acc);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent-2);
    margin-bottom: 1.2rem;
  }
  .hero-chip .blink {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--teal);
    animation: blink 1.6s ease infinite;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.4rem);
    font-weight: 800;
    line-height: 1.05;
    color: var(--text);
    margin: 0;
    letter-spacing: -0.02em;
  }
  .hero-title .hi { color: var(--accent-2); }
  .hero-title .lo { color: var(--teal); }

  .hero-sub {
    font-size: 0.88rem;
    color: var(--text-mid);
    margin-top: 0.9rem;
    letter-spacing: 0.02em;
    line-height: 1.6;
  }

  .hero-dots {
    display: flex;
    justify-content: center;
    gap: 0.4rem;
    margin-top: 1.8rem;
  }
  .hero-dots span {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--border);
  }
  .hero-dots span:nth-child(3) { background: var(--accent); }

  /* ── Input Card ── */
  .input-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-top: 2rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
  }

  /* ── Streamlit widget overrides ── */
  label[data-testid="stWidgetLabel"] p, .stTextInput label p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: var(--text-mid) !important;
    margin-bottom: 0.4rem !important;
  }

  div[data-baseweb="select"] > div {
    background: var(--bg-lifted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
  }
  div[data-baseweb="select"] > div:hover {
    border-color: var(--border-acc) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
  }
  div[data-baseweb="select"] svg { color: var(--accent-2) !important; }

  div[data-baseweb="input"] > div {
    background: var(--bg-lifted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
  }
  div[data-baseweb="input"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
  }
  div[data-baseweb="input"] input {
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    background: transparent !important;
  }
  div[data-baseweb="input"] input::placeholder { color: var(--text-dim) !important; }

  /* ── Analyze Button ── */
  .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent) 0%, #9b6dff 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 1.5rem !important;
    margin-top: 0.6rem !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 20px rgba(124,106,247,0.4) !important;
    cursor: pointer !important;
  }
  .stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,106,247,0.5) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Results wrapper ── */
  .results-wrap { margin-top: 1.8rem; }

  /* ── Translation note ── */
  .trans-note {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 8px;
    padding: 0.65rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--amber);
    margin-bottom: 1.2rem;
    letter-spacing: 0.04em;
  }

  /* ── Section card ── */
  .s-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    animation: slideUp 0.35s ease both;
    position: relative;
    overflow: hidden;
  }
  .s-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
  }
  .s-card.teal-card::after { background: radial-gradient(circle, var(--teal-glow) 0%, transparent 70%); }

  @keyframes slideUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
  }
  .s-card:nth-child(2) { animation-delay: 0.07s; }
  .s-card:nth-child(3) { animation-delay: 0.14s; }
  .s-card:nth-child(4) { animation-delay: 0.21s; }

  .s-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent-2);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .s-title.teal  { color: var(--teal); }
  .s-title.green { color: var(--green); }

  /* POS pills */
  .pos-wrap { display: flex; flex-wrap: wrap; gap: 0.45rem; }
  .pos-pill {
    background: var(--bg-lifted);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.3rem 0.65rem;
    font-size: 0.8rem;
    color: var(--text);
    font-family: 'Outfit', sans-serif;
    display: flex; align-items: center; gap: 0.35rem;
  }
  .pos-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 500;
    padding: 0.12rem 0.35rem;
    border-radius: 4px;
    letter-spacing: 0.04em;
  }
  .pos-badge.N { background: rgba(124,106,247,0.2); color: var(--accent-2); }
  .pos-badge.V { background: rgba(45,212,191,0.15); color: var(--teal); }
  .pos-badge.J { background: rgba(251,191,36,0.15); color: var(--amber); }
  .pos-badge.R { background: rgba(52,211,153,0.15); color: var(--green); }
  .pos-badge.O { background: rgba(255,255,255,0.06); color: var(--text-mid); }

  /* WSD rows */
  .wsd-item {
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
  }
  .wsd-item:last-child { border-bottom: none; padding-bottom: 0; }
  .wsd-word {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--teal);
    margin-bottom: 0.2rem;
  }
  .wsd-def { font-size: 0.85rem; color: var(--text-mid); line-height: 1.5; }

  /* Intent badge */
  .intent-row { display: flex; align-items: center; gap: 0.8rem; }
  .intent-pill {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: linear-gradient(135deg, rgba(124,106,247,0.15), rgba(124,106,247,0.05));
    border: 1px solid var(--border-acc);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: 'Outfit', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--accent-2);
  }
  .confidence {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-dim);
  }

  /* Response bubble */
  .resp-wrap {
    background: linear-gradient(135deg, var(--accent) 0%, #6d5ce7 100%);
    border-radius: 12px 12px 12px 3px;
    padding: 1.1rem 1.4rem;
    font-size: 1rem;
    color: #fff;
    line-height: 1.65;
    box-shadow: 0 6px 24px rgba(124,106,247,0.35);
  }
  .resp-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.7rem;
  }
  .resp-lang {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-dim);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .resp-tts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--teal);
    display: flex; align-items: center; gap: 0.3rem;
  }

  /* Warn */
  .warn {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 8px;
    padding: 0.65rem 1rem;
    font-size: 0.83rem;
    color: var(--red);
  }

  /* Language count chip */
  .lang-count {
    display: inline-block;
    background: rgba(45,212,191,0.1);
    border: 1px solid rgba(45,212,191,0.2);
    border-radius: 999px;
    padding: 0.15rem 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--teal);
    letter-spacing: 0.1em;
    margin-left: 0.5rem;
    vertical-align: middle;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, [data-testid="stToolbar"],
  [data-testid="stDecoration"] { display: none !important; }
  .stAlert { display: none !important; }
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
        return ("Booking", "📅")
    elif "weather" in text:
        return ("Weather", "🌤")
    elif any(w in text for w in ["bank", "deposit", "withdraw"]):
        return ("Banking", "🏦")
    else:
        return ("General", "💬")

def generate_response(intent):
    return {
        "Booking":  "I can help you with booking services.",
        "Weather":  "Please provide your location for weather details.",
        "Banking":  "Are you referring to a financial bank?",
        "General":  "Could you please clarify your request?",
    }.get(intent, "Could you please clarify your request?")

def get_pos_class(pos):
    if pos.startswith("N"): return "N"
    if pos.startswith("V"): return "V"
    if pos.startswith("J"): return "J"
    if pos.startswith("R"): return "R"
    return "O"

def speak(text, lang_code):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang_code)
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


# -----------------------------
# LANGUAGE OPTIONS (15 languages)
# -----------------------------
language_options = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "Kannada": "kn", "Malayalam": "ml", "Marathi": "mr", "Bengali": "bn",
    "Gujarati": "gu", "Punjabi": "pa", "Spanish": "es", "French": "fr",
    "German": "de", "Arabic": "ar", "Chinese (Simplified)": "zh-cn",
}


# -----------------------------
# HERO
# -----------------------------
st.markdown(f"""
<div class="hero">
  <div class="hero-chip">
    <div class="blink"></div>
    NLP · Intent · Voice
  </div>
  <h1 class="hero-title">Context <span class="hi">AI</span><br><span class="lo">Assistant</span></h1>
  <p class="hero-sub">
    Multilingual context-aware intelligence<br>
    Powered by spaCy · WordNet · Google TTS
    <span class="lang-count">{len(language_options)} languages</span>
  </p>
  <div class="hero-dots">
    <span></span><span></span><span></span><span></span><span></span>
  </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# INPUT CARD
# -----------------------------
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    selected_language = st.selectbox("🌍 Language", list(language_options.keys()))
with col2:
    language_code = language_options[selected_language]
    st.markdown(
        f'<div style="padding-top:2rem;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:0.65rem;color:#475569;letter-spacing:0.14em;text-align:center;">'
        f'{language_code.upper()}</div>',
        unsafe_allow_html=True
    )

user_input = st.text_input(
    "✍ Query",
    placeholder="e.g. I want to book a hotel in Hyderabad..."
)

analyze = st.button("⚡  Analyze Query")
st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# ANALYSIS OUTPUT
# -----------------------------
if analyze:
    if not user_input.strip():
        st.markdown('<div class="warn">⚠ Please enter a query before analyzing.</div>', unsafe_allow_html=True)
    else:
        if language_code != "en":
            translated_input = translator.translate(user_input, dest="en").text
            st.markdown(
                f'<div class="trans-note">⟳ Translated → English &nbsp;|&nbsp; <strong>{translated_input}</strong></div>',
                unsafe_allow_html=True
            )
        else:
            translated_input = user_input

        st.markdown('<div class="results-wrap">', unsafe_allow_html=True)

        # ── POS Tagging ──
        pos_results = pos_tagging(translated_input)
        pills = "".join([
            f'<div class="pos-pill">{w} '
            f'<span class="pos-badge {get_pos_class(p)}">{p}</span></div>'
            for w, p in pos_results
        ])
        st.markdown(f"""
        <div class="s-card">
          <div class="s-title">🔍 &nbsp;Part-of-Speech Tagging</div>
          <div class="pos-wrap">{pills}</div>
          <div style="margin-top:0.9rem;display:flex;gap:0.8rem;flex-wrap:wrap;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#a78bfa;">■ Noun</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#2dd4bf;">■ Verb</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#fbbf24;">■ Adjective</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#34d399;">■ Adverb</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#475569;">■ Other</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── WSD ──
        senses = word_sense_disambiguation(translated_input)
        if senses:
            wsd_rows = "".join([
                f'<div class="wsd-item"><div class="wsd-word">{w}</div>'
                f'<div class="wsd-def">{m}</div></div>'
                for w, m in senses.items()
            ])
        else:
            wsd_rows = '<div class="wsd-item"><div class="wsd-def" style="font-style:italic;color:#475569;">No ambiguous words detected.</div></div>'

        st.markdown(f"""
        <div class="s-card teal-card">
          <div class="s-title teal">📖 &nbsp;Word Sense Disambiguation</div>
          {wsd_rows}
        </div>
        """, unsafe_allow_html=True)

        # ── Intent + Response ──
        intent, icon = detect_intent(translated_input)
        response = generate_response(intent)
        if language_code != "en":
            response = translator.translate(response, dest=language_code).text

        st.markdown(f"""
        <div class="s-card">
          <div class="s-title green">🎯 &nbsp;Intent Detection &amp; Response</div>
          <div class="intent-row">
            <div class="intent-pill">{icon} &nbsp;{intent}</div>
            <div class="confidence">NLP CLASSIFIER</div>
          </div>
          <div style="margin-top:1.1rem">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                        letter-spacing:0.18em;color:#475569;text-transform:uppercase;
                        margin-bottom:0.5rem;">🤖 Assistant Response</div>
            <div class="resp-wrap">{response}</div>
            <div class="resp-footer">
              <span class="resp-lang">Language: {selected_language}</span>
              <span class="resp-tts">🔊 Speaking via TTS</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Speak
        speak(response, language_code)