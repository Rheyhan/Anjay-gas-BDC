import re
import pandas as pd

train_data_cleaned_lemarization_stopwords = pd.read_csv("../Temp/cleaned_datav2_translated_lemarized_stopwords.csv")

temp = train_data_cleaned_lemarization_stopwords.copy()
pattern = r"\[(.*?)\]"

for iter, text_duplicated in enumerate(list(set(temp[temp["text"].duplicated()]["text"].values))):    
    dict_labelselector = {}
    
    text_duplicated = re.sub(pattern, "", text_duplicated).strip(" ")
    temp.reset_index(drop=True, inplace=True)
    
    for index, (actual_text, actual_label) in list(enumerate(temp.values)):
        if (text_duplicated == actual_text):
            try: dict_labelselector[actual_label][0]+=1
            except: dict_labelselector[actual_label]=[1]
            dict_labelselector[actual_label].append(index)
    majorval = sorted(list(dict_labelselector.items()), key=lambda x: x[1][0], reverse=True)
    try:
        if majorval[0][1][0] == majorval[1][1][0]:
            print(text_duplicated)
            for count, i in enumerate(majorval):
                print(f'{count + 1}. {i[0]}: {i[1][0]}')
            picked = int(input("pick one "))
            majorval = sorted(majorval, key=lambda x: (x[0] != majorval[picked-1][0], majorval.index(x)))
        temp1 = []
        for item in majorval:
            temp1.extend(item[1][1:])
        temp = temp.drop(temp1[1:])
    except:
        temp = temp.drop(majorval[0][1][2:])
        
temp.to_csv("../Temp/cleaned_datav2_translated_lemarized_stopwords_handled.csv")