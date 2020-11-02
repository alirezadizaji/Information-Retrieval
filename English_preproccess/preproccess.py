# import nltk
# import re
# import pandas as pd
#
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# def extract_data():
#     df = pd.read_csv('ted_talks.csv' , names=["title" , "description"])
#     return  df
#
#
#
#
#
# def listToString(lst):
#     string = []
#     for x in lst:
#         str1 = " "
#         string.append(str1.join(x))
#     return string
#
#
#
# def prepare_text(text):
#     text = text.lower()
#     text = re.sub('\d+', '', text)
#     text = text.translate(str.maketrans(punctuations, ' ' * len(punctuations)))
#     text = ' '.join(re.sub(r'[^ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپوئژآؤ \n]', ' ', text).split())
#     text = text.strip()
#
#
#
#
#
#
# stop_words = set(stopwords.words('english'))
# lemmatizer = nltk.WordNetLemmatizer()
# punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`؟،{|}~"""
