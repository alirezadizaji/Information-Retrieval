from hazm import Normalizer, word_tokenize, Stemmer, WordTokenizer, stopwords_list ,Lemmatizer
import re
import pandas as pd
from Presian_preproccess import xml_to_csv


def conversion(filename):
    persian_wiki_xml_data_dir = filename
    xml_to_csv.xml_to_csv_method(persian_wiki_xml_data_dir, ',')
    PERSIAN_DIR = "Persian.csv"

def listToString(lst):
    string = []
    for x in lst:
        x = x.split(" ")
        st = ' '.join(map(str, x))
        string.append(st)
    return string


def extract_data_as_string():
    df = pd.read_csv("Persian.csv" )
    titles=listToString(df["page_title"])
    text = listToString(df["text"])
    return  titles , text ,df["page_id"]

def prepare_text(text):
    text = text.lower()
    text = re.sub('\d+', '', text)
    text = text.translate(str.maketrans(punctuations, ' ' * len(punctuations)))
    text = ' '.join(re.sub(r'[^ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپوئژآؤ \n]', ' ', text).split())
    text = text.strip()
    normalized_text = normalizer.normalize(text)
    words = word_tokenize(normalized_text)
    words = [w for w in words if w != '.']
    words = [w for w in words if w not in stopwords_list()]
    words = [lemmatizer.lemmatize(w) for w in words]
    words = ' '.join(words)
    return words

def pre_proccess(lst):
    print("Start preproccessing ...")
    pre_title =[]

    for title in lst:
       pre_title.append(prepare_text(title))

    print("Done preproccessing.")
    return pre_title




stemmer = Stemmer()
lemmatizer = Lemmatizer()
normalizer = Normalizer()
tokenizer = WordTokenizer(separate_emoji=True, replace_links=True,
                              replace_IDs=True, replace_emails=True,
                              replace_hashtags=True, replace_numbers=True)
tokenizer.number_int_repl = '.'
tokenizer.number_float_repl = '.'
tokenizer.email_repl = '.'
tokenizer.hashtag_repl = '.'
tokenizer.id_repl = '.'
tokenizer.emoji_repl = '.'
tokenizer.link_repl = '.'
punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`؟،{|}~"""

conversion("Persian.xml")
title , text, ids = extract_data_as_string()
final_text = pre_proccess(text)
final_title = pre_proccess(title)

d = {'title': final_title, 'id':ids,'text':final_text}
df = pd.DataFrame(d)
df.to_csv(r'prepared_persian.csv')
