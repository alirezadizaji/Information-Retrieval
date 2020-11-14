from Indexing import *
from collections import defaultdict
from retrieval import *

if __name__ == '__main__':
    print("Enter Either Eng or Wiki:")
    doc_type = input().lower()
    if doc_type == 'eng':
        eng_title_posting_list = defaultdict(lambda: defaultdict(list))
        eng_document_posting_list = defaultdict(lambda: defaultdict(list))
        eng_title_bigram_list = defaultdict(list)
        eng_document_bigram_list = defaultdict(list)
        eng_total_documents = 0
        while True:
            print(" Choose a number:\n",
                  "1- Create positional index\n",
                  "2- Save positional index\n",
                  "3- Get posting list\n",
                  "4- Create bigram\n",
                  "5- Show bigram\n",
                  "6- Lnc-ltc\n",
                  "7- Quit")
            cmd = input()
            if cmd == '1':
                eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index(
                    "English_preproccess/prepared_english.csv")
                print(eng_title_posting_list, "\n", eng_document_posting_list)
            elif cmd == '2':
                eng_save_index(eng_title_posting_list, eng_document_posting_list)
            elif cmd == '3':
                print("Enter Word")
                word = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                eng_get_index(word, field, eng_title_posting_list, eng_document_posting_list)
            elif cmd == '4':
                eng_title_bigram_list, eng_document_bigram_list = eng_create_bigram(eng_title_posting_list,
                                                                                    eng_document_posting_list)
            elif cmd == '5':
                print("Enter Bigram")
                bigram = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                eng_get_bigram(bigram, field, eng_title_bigram_list, eng_document_bigram_list)
            elif cmd == '6':
                print("Enter Query")
                query = input()
                search(query, eng_title_posting_list, eng_document_posting_list, eng_total_documents)
            elif cmd == '7':
                break

    else:
        wiki_title_posting_list = defaultdict(lambda: defaultdict(list))
        wiki_document_posting_list = defaultdict(lambda: defaultdict(list))
        wiki_title_bigram_list = defaultdict(list)
        wiki_document_bigram_list = defaultdict(list)
        wiki_total_documents = 0
        while True:
            print(" Choose a number:\n",
                  "1- Create positional index\n",
                  "2- Save positional index\n",
                  "3- Get posting list\n",
                  "4- Create bigram\n",
                  "5- Show bigram\n",
                  "6- Lnc-ltc\n",
                  "7- Quit")
            cmd = input()
            if cmd == '1':
                wiki_title_posting_list, wiki_document_posting_list, wiki_total_documents = wiki_create_index(
                    "Presian_preproccess/prepared_persian.csv")
                print(wiki_title_posting_list, "\n", wiki_document_posting_list)
            elif cmd == '2':
                wiki_save_index(wiki_title_posting_list, wiki_document_posting_list)
            elif cmd == '3':
                print("Enter Word")
                word = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                wiki_get_index(word, field, wiki_title_posting_list, wiki_document_posting_list)
            elif cmd == '4':
                wiki_title_bigram_list, wiki_document_bigram_list = wiki_create_bigram(wiki_title_posting_list,
                                                                                       wiki_document_posting_list)
            elif cmd == '5':
                print("Enter Bigram")
                bigram = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                wiki_get_bigram(bigram, field, wiki_title_bigram_list, wiki_document_bigram_list)
            elif cmd == '6':
                print("Enter Query")
                query = input()
                search(query, wiki_title_posting_list, wiki_document_posting_list, wiki_total_documents)
            elif cmd == '7':
                break
