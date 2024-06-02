import os
import pandas as pd
import re
from deep_translator import GoogleTranslator
from tqdm import tqdm
from nlp_id.lemmatizer import Lemmatizer 
import numpy as np

def create_submission(predicted, path = "submission.csv"):
    folder_loc = '/'.join([i for i in path.split("/")][:-1])
    if not os.path.exists(folder_loc) and folder_loc != '':
        os.makedirs(folder_loc)
    df = pd.read_excel("Data/Submission_Format.xlsx")
    df["label"] = predicted
    df.to_csv(path, index=False)

def cleantextv2(list_text, translate = False):
    new_text = []
    index = 0
    for text in tqdm(list_text):
        # This removes 'RT ' from the text as the first word.
        text =re.sub(r'RT ', '', text)
        # Removes Reply [re xxxx]
        text = re.sub(r'\[re \w+]',"", text, flags=re.IGNORECASE)
        # This removes link https
        text = re.sub(r'http\S+', "", text)
        # Removes Tags  @xxxx
        text = re.sub(r'@\S+',"", text)
        # Removes '&amp;' from text, html stuff.
        text = re.sub(r'&amp;', '', text)
        # Removes \xad from text
        text = re.sub(r'\xad', '', text)
        # Change these specific chars into space
        text = re.sub(r'[,.?!\'\"()-]', " ", text)

        text = ''.join(re.findall(r'[ a-zA-Z0-9#]', text))
        text = re.sub(r' +', " ", text)

        # Split input string into parts: hashtags and non-hashtag parts
        parts = re.split(r'(#\w*)', text)

        # Pattern to match hashtags
        hashtag_pattern = re.compile(r'#\w*')
        # Apply digit replacement to non-hashtag parts
        processed_parts = [
            part if hashtag_pattern.match(part) else re.sub(r'\d', '', part)
            for part in parts
        ]
        # Reconstruct the string
        text = (''.join(processed_parts)).lower()
        # Removes word with 1 char
        text = re.sub(r'\b\w\b', " ", text)
        
        if translate:
            try:
                text = GoogleTranslator(source='en', target='id').translate(text)
            except:
                print(f'Failed, index: {index}')
            
        # Append, remove double space, remove space in the start and the end of the string
        new_text.append(re.sub(" +", " ", text).strip(" "))
        index+=1
        
    return new_text

thelemarization = Lemmatizer()
def lemarization(list_text):
    new_text = []
    for text in tqdm(list_text):
        text = thelemarization.lemmatize(text)
        new_text.append(text)
    return new_text

class encoder:
    def __init__(self, list_labels):
        self.encoder = {}
        for count, label in enumerate(np.unique(list_labels)):
            self.encoder[label] = count
    def encode(self, list_labels):
        return [self.encoder[label] for label in list_labels]