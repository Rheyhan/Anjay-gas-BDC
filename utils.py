import os
import pandas as pd
import re
from deep_translator import GoogleTranslator
from tqdm import tqdm

def create_submission(predicted, path = "submission.csv"):
    folder_loc = '/'.join([i for i in path.split("/")][:-1])
    if not os.path.exists(folder_loc) and folder_loc != '':
        os.makedirs(folder_loc)
    df = pd.read_excel("Data/Submission_Format.xlsx")
    df["label"] = predicted
    df.to_csv(path, index=False)



def cleantext(text_list,
              case1:  bool = True,
              case2: bool = False,
              case3: bool = False,
              case4: bool = False):
    '''
    returns cleaned string from messy raw string that's unreadable for the model.
    
    Case1: Removes UTF-8 encoded, number, comma, dot, etc. But keeps number on hastag
    Case2: This removes hastag entirely
    '''
    new_text = []
    for text in tqdm(text_list):
        if case1:
            # Removes '&amp;' from text, html stuff.
            text = re.sub(r'&amp;', '', text)
            text = re.sub(r' +'," ", ''.join(re.findall(r'[ a-zA-Z@0-9[\]#]',text)))
                    
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
            text = ''.join(processed_parts)
        
        # This removes 'RT ' from the text as the first word.
        text =re.sub(r'RT ', '', text)
        # Change text into lowercase
        text = text = text.lower()
        # This removes link https
        text = re.sub(r'http\S+', "", text)
        # Removes Tags  @xxxx
        text = re.sub(r'@\S+ ',"", text)
        # Removes word with 1 char
        text = re.sub(r' \w ', " ", text)
        # Removes Reply [re xxxx]
        text = re.sub(r' \[re \w+]',"", text)
        
        if case2: 
            text = re.sub(r'#\S+ ', '', text)
        
        if case3:
            text = re.sub(r'\b\w{2,3}\b', text)
        
        if case4:
            text = GoogleTranslator(source='en', target='id').translate(text)
        
        new_text.append(re.sub(" +", " ", text).strip(" "))
            
    return new_text

# a = train_data["text"][4]
# cleantext(a)