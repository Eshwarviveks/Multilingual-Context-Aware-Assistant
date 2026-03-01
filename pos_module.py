import spacy

nlp = spacy.load("en_core_web_sm")

def pos_tagging(text):
    doc = nlp(text)
    pos_info = []
    for token in doc:
        pos_info.append((token.text, token.pos_))
    return pos_info
