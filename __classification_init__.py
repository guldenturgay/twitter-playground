
import unicodedata
import nltk
import re
import string
from keras.models import load_model
import tensorflow_hub as hub
import numpy as np
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
stopword = nltk.corpus.stopwords.words('english')


model = load_model('test.h5', custom_objects={'KerasLayer': hub.KerasLayer})

def predict_emotion(text):

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

    probas = model.predict([text])
    pred = np.argmax(probas)
    pred = emotion_label_dict[pred]
    return pred