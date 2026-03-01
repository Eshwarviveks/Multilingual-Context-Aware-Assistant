def detect_intent(text):
    text = text.lower()
    
    if "book" in text:
        return "booking"
    elif "weather" in text:
        return "weather"
    elif "bank" in text:
        return "banking"
    elif "withdraw" in text or "deposit" in text:
        return "banking"
    else:
        return "general"
