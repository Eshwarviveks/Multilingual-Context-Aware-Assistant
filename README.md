# 🧠 Multilingual Context-Aware Virtual Assistant

A multilingual AI-powered virtual assistant that performs contextual understanding using:

- Part-of-Speech (POS) Tagging
- Word Sense Disambiguation (WSD)
- Intent Detection
- Google Text-to-Speech (gTTS)

---

## 🚀 Features

✅ POS Tagging using spaCy  
✅ Word Sense Disambiguation using Lesk Algorithm  
✅ Intent Detection (Banking, Booking, Weather, etc.)  
✅ Multilingual Support (15+ languages)  
✅ Automatic Translation Pipeline  
✅ Google Text-to-Speech Voice Output  
✅ Streamlit Web Interface  

---

## 🌍 Supported Languages

- English
- Hindi
- Telugu
- Tamil
- Kannada
- Malayalam
- Marathi
- Bengali
- Gujarati
- Punjabi
- Spanish
- French
- German
- Arabic
- Chinese (Simplified)

---

## 🧠 How It Works

1. User selects language
2. Input is translated to English
3. POS tagging & WSD performed
4. Intent detected
5. Response generated
6. Response translated back
7. gTTS generates multilingual speech output

---

## 🛠 Technologies Used

- Python 3.11
- Streamlit
- spaCy
- NLTK
- Google Translate API
- Google Text-to-Speech (gTTS)
- pygame

---

## 📦 Installation

```bash
pip install streamlit spacy==3.7.2 click==8.1.7 typer==0.9.0 nltk gtts googletrans==4.0.0-rc1 pygame
python -m spacy download en_core_web_sm