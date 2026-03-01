import speech_recognition as sr

def get_text_input():
    return input("Enter your query: ")

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        return "Sorry, could not understand."
