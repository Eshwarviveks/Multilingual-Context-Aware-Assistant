import pyttsx3

engine = pyttsx3.init()

def generate_response(intent):
    if intent == "booking":
        response = "I can help you with booking."
    elif intent == "weather":
        response = "Please tell me your location for weather details."
    elif intent == "banking":
        response = "Are you looking for financial bank services?"
    else:
        response = "Can you please clarify your request?"
    
    return response

def speak_response(text):
    engine.say(text)
    engine.runAndWait()
