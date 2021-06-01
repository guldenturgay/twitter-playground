
import unicodedata
import nltk
import re
import string
from keras.models import load_model
import numpy as np
stopword = nltk.corpus.stopwords.words('english')

model = load_model('./emotion_analysis')

def predict_emotion(text):

    def clean_text(text):
        
        # Replace or remove the characters 
        replacement_dict={"’":"'", # Replace ’ with '
                        "'s":" is", # Replace the contractions
                        "n't": " not",
                        "'m": " am",
                        "'ll": " will",
                        "'d": " would",
                        "'ve": " have",
                        "'re": " are",
                        "\W+": " "} 

        for item in replacement_dict.keys():
            text=re.sub(item,replacement_dict[item], text)

        text = ''.join([char for char in text if char not in string.punctuation])
        tokens = re.split('\W+', text)
        
        # Remove stopwords
        text = ' '.join([word for word in tokens if word not in stopword])
        text=text.lower()
        return text



    emotion_label_dict = {6: 'neutral',
                            4: 'happy',
                            2: 'fear',
                            3: 'guilt',
                            0: 'anger',
                            1: 'disgust',
                            7: 'sad',
                            8: 'shame',
                            5: 'joy',
                            9: 'suprise'}

    text = clean_text(text)


    def get_emotion(text):
        probas = model.predict([text])
        pred = np.argmax(probas)
        pred = emotion_label_dict[pred]
        return pred

    predicted = get_emotion(text)
    return predicted