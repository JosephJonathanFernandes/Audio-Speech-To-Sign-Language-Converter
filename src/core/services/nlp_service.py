import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from django.contrib.staticfiles import finders

class NLPService:
    """
    Service class to handle Natural Language Processing tasks.
    It takes an input sentence, tokenizes it, removes stop words,
    determines the tense, lemmatizes words, and maps them to available video assets.
    """
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set([
            "mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', 
            "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", 
            "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 
            'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 
            'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', 
            "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 
            'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 
            'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 
            'ma', 't', 'having', 'mightn', 've', "isn't", "won't"
        ])

    def get_tense(self, tagged_words):
        """Determine the tense of the sentence based on POS tags."""
        tense = {
            "future": len([word for word in tagged_words if word[1] == "MD"]),
            "present": len([word for word in tagged_words if word[1] in ["VBP", "VBZ", "VBG"]]),
            "past": len([word for word in tagged_words if word[1] in ["VBD", "VBN"]]),
            "present_continuous": len([word for word in tagged_words if word[1] in ["VBG"]])
        }
        return tense

    def lemmatize_word(self, word, pos_tag):
        """Lemmatize a single word based on its POS tag."""
        if pos_tag in ['VBG', 'VBD', 'VBZ', 'VBN', 'NN']:
            return self.lemmatizer.lemmatize(word, pos='v')
        elif pos_tag in ['JJ', 'JJR', 'JJS', 'RBR', 'RBS']:
            return self.lemmatizer.lemmatize(word, pos='a')
        else:
            return self.lemmatizer.lemmatize(word)

    def process_text(self, text):
        """
        Main processing function.
        Returns a list of words or characters that correspond to available video assets.
        """
        if not text:
            return []

        # Tokenize the sentence
        words = word_tokenize(text.lower())
        tagged = nltk.pos_tag(words)
        
        tense = self.get_tense(tagged)
        
        # Remove stopwords and apply lemmatization
        filtered_text = []
        for w, p in zip(words, tagged):
            if w not in self.stop_words:
                lemmatized_word = self.lemmatize_word(w, p[1])
                filtered_text.append(lemmatized_word)

        # Basic pronoun swap and capitalization matching
        temp = []
        for w in filtered_text:
            if w.lower() == 'i':
                temp.append('Me')
            else:
                # Capitalizing the first letter to match file names (e.g., 'Hello.mp4')
                # Alternatively, preserve original casing if needed. 
                # The original code did temp.append(w), but checking for 'I'.
                temp.append(w.capitalize())

        words = temp
        
        # Tense adjustment keywords
        if tense:
            probable_tense = max(tense, key=tense.get)
            if probable_tense == "past" and tense["past"] >= 1:
                words = ["Before"] + words
            elif probable_tense == "future" and tense["future"] >= 1:
                if "Will" not in words:
                    words = ["Will"] + words
            elif probable_tense == "present":
                if tense["present_continuous"] >= 1:
                    words = ["Now"] + words

        # Map to available videos or break down into characters
        final_animation_sequence = []
        for w in words:
            path = w + ".mp4"
            f = finders.find(path)
            
            # Splitting the word into characters if its animation is not present in database
            if not f:
                for c in w:
                    final_animation_sequence.append(c.capitalize())
            else:
                final_animation_sequence.append(w)

        return final_animation_sequence
