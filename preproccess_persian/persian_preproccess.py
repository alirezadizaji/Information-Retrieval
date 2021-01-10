import nltk
from hazm import Normalizer, word_tokenize, Stemmer, WordTokenizer, stopwords_list ,Lemmatizer
import re
import pandas as pd
from preproccess_persian import xml_to_csv


def conversion(filename):
    persian_wiki_xml_data_dir = filename
    xml_to_csv.xml_to_csv_method(persian_wiki_xml_data_dir, ',')
    PERSIAN_DIR = "../datasets/phase1/Persian.csv"

def listToString(lst):
    string = []
    for x in lst:
        x = x.split(" ")
        st = ' '.join(map(str, x))
        string.append(st)
    return string


def extract_data_as_string():
    df = pd.read_csv("/Users/atena/phase_1_part1/Persion_preproccess/Persian.csv" )
    titles=listToString(df["page_title"])
    text = listToString(df["text"])
    return  titles , text ,df["page_id"]

def preprocess(text):
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
    pre_text = ' '.join(words)

    return pre_text

def pre_proccess(textlst,titlelst):
    print("Start preproccessing ...")
    pre_title =[]
    pre_text=[]

    for title in titlelst:
       pre_title.append(preprocess(title))

    for text in textlst:
       pre_text.append(preprocess(text))
    print("Done preproccessing.")
    return pre_text,pre_title




def most_freq_words():
    title , text, ids = extract_data_as_string()

    listToStr = ' '.join(map(str, title+ text))
    listToStr = word_tokenize(listToStr)
    word_count = nltk.FreqDist(listToStr)
    return word_count.most_common(30)

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
punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`؟،{|}؛~"""


def PreProccess():
    title , text, ids = extract_data_as_string()

    conversion("/Users/atena/phase_1_part1/Persion_preproccess/Persian.xml")
    final_text,final_title = pre_proccess(text,title)
    # most_freq_words(title,text)

    d = {'id':ids,'title': final_title, 'text':final_text}
    for i in range(len(d['title'])):
        if len(d['title'][i]) == 0:
            d['title'][i] = "No title"

    for i in range(len(d['text'])):
        if len(d['text'][i]) == 0:
            d['text'][i] = "No text"

    df_ = pd.DataFrame(d)
    df_.to_csv(r'prepared_persian.csv')
