from nltk.wsd import lesk
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

def get_word_sense(sentence, word):
    sense = lesk(sentence.split(), word)
    if sense:
        return sense.definition()
    return None
