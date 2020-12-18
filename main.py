from English_preproccess import preproccess
from Indexing import *
from collections import defaultdict

from Presian_preproccess import persian_preproccess
from compress import load_index, create_distance_index, compress, save_index, decompress
from proximity_search import proccess_query, CalculateOccurences
from proximity_search_persian import persian_CalculateOccurences
from retrieval import *
from spelling_correction import load_bigram, spell_correction, jaccard_dist_type2, edit_distance

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
                  "0- PreProccess\n",
                  "1- Most Freq Words\n",
                  "2- Create positional index\n",
                  "3- Save positional index\n",
                  "4- Get posting list\n",
                  "5- Create bigram\n",
                  "6- Show bigram\n",
                  "7- Compress\n",
                  "8- decompress\n",
                  "9- resolve Query\n",
                  "10- Jaccard/Edit Distance\n",
                  "11- Lnc-ltc\n",
                  "12- Proximity Search\n",
                  "13- Quit")
            cmd = input()
            if cmd =='0':
                preproccess.PreProccess()
            elif cmd =='1':
                print(preproccess.most_freq_words())
            elif cmd == '2':
                eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index(
                    "datasets/phase1/prepared_english.csv")

                print(eng_title_posting_list, "\n", eng_document_posting_list)
            elif cmd == '3':
                eng_save_index(eng_title_posting_list, eng_document_posting_list)
            elif cmd == '4':
                print("Enter Word")
                word = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                eng_get_index(word, field, eng_title_posting_list, eng_document_posting_list)
            elif cmd == '5':
                eng_title_bigram_list, eng_document_bigram_list = eng_create_bigram(eng_title_posting_list,
                                                                                    eng_document_posting_list)
            elif cmd == '6':
                print("Enter Bigram")
                bigram = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                eng_get_bigram(bigram, field, eng_title_bigram_list, eng_document_bigram_list)

            elif cmd == '7':
                print("Enter index path: ")
                path = input() #"eng_doc_positional.pkl"
                print("Enter type (vb, gc): ")
                type = input() #vb
                info = load_index(path)
                idx = info['index']
                create_distance_index(idx)
                info['index'] = compress(idx, type)
                save_index(info)
            elif cmd == '8':
                print("Enter compressed index path: ")
                path = input()
                path = "{}_compressed.pkl".format(path[:-4])
                compressed = load_index(path)['index']
                type = "vb" #just vb is implemented
                new_index = decompress(compressed, type)
            elif cmd == '9':
                print("Enter bigram index path: ")
                path = input() #eng_doc_bigram.txt"
                bg_idx = load_bigram(path)
                print("Enter query: ")
                query = input()
                query = preproccess.prepare_text(query)
                ans = spell_correction(query, bg_idx, type1=False)
                print(ans)
            elif cmd == '10':
                print("Enter Distance Type(Jacc or Edit): ")
                type = input()
                print("Enter two Words: ")
                words = input().split()
                ans = jaccard_dist_type2(*words) if type == "Jacc" else edit_distance(*words)
                print(ans)

            elif cmd == '11':
                print("Enter Query")
                query = input()
                query=preproccess.prepare_text(query)
                search(query, eng_title_posting_list, eng_document_posting_list, eng_total_documents)
            elif cmd =='12':
                print("Enter Query like : word1 /range word2")
                query = input()
                key1 , key2 , size = proccess_query(query)
                doc_id_founded = CalculateOccurences(key1,key2,size)
                print("founded from proximity search: ",doc_id_founded)
                for i in range(eng_total_documents):
                    if i not in doc_id_founded:
                        eng_title_posting_list,eng_document_posting_lis,eng_total_documents= eng_delete_index(i,eng_title_posting_list ,eng_document_posting_list,eng_total_documents)
                search(key1+' '+key2 , eng_title_posting_list,eng_document_posting_list, eng_total_documents)

            elif cmd == '13':
                break

    else:
        wiki_title_posting_list = defaultdict(lambda: defaultdict(list))
        wiki_document_posting_list = defaultdict(lambda: defaultdict(list))
        wiki_title_bigram_list = defaultdict(list)
        wiki_document_bigram_list = defaultdict(list)
        wiki_total_documents = 0
        while True:
            print(" Choose a number:\n",
                  "0- PreProccess\n",
                  "1- Most Freq Words\n",
                  "2- Create positional index\n",
                  "3- Save positional index\n",
                  "4- Get posting list\n",
                  "5- Create bigram\n",
                  "6- Show bigram\n",
                  "7- Compress\n",
                  "8- decompress\n",
                  "9- resolve Query\n",
                  "10- Jaccard/Edit Distance\n",
                  "11- Lnc-ltc\n",
                  "12- Proximity Search\n",
                  "13- Quit")
            cmd = input()
            if cmd == '0':
                persian_preproccess.PreProccess()
            elif cmd =='1':
                print(persian_preproccess.most_freq_words())
            elif cmd == '2':
                wiki_title_posting_list, wiki_document_posting_list, wiki_total_documents = wiki_create_index(
                    "datasets/phase1/prepared_persian.csv")
                print(wiki_title_posting_list, "\n", wiki_document_posting_list)
            elif cmd == '3':
                wiki_save_index(wiki_title_posting_list, wiki_document_posting_list)
            elif cmd == '4':
                print("Enter Word")
                word = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                wiki_get_index(word, field, wiki_title_posting_list, wiki_document_posting_list)
            elif cmd == '5':
                wiki_title_bigram_list, wiki_document_bigram_list = wiki_create_bigram(wiki_title_posting_list,
                                                                                       wiki_document_posting_list)
            elif cmd == '6':
                print("Enter Bigram")
                bigram = input()
                print("Enter Field: TITLE or TEXT")
                field = input()
                wiki_get_bigram(bigram, field, wiki_title_bigram_list, wiki_document_bigram_list)
            elif cmd == '7':
                print("Enter index path: ")
                path = input() #"eng_doc_positional.pkl"
                print("Enter type (vb, gc): ")
                type = input() #vb
                info = load_index(path)
                idx = info['index']
                create_distance_index(idx)
                info['index'] = compress(idx, type)
                save_index(info)
            elif cmd == '8':
                print("Enter compressed index path: ")
                path = input()
                path = "{}_compressed.pkl".format(path[:-4])
                compressed = load_index(path)['index']
                type = "vb" #just vb is implemented
                new_index = decompress(compressed, type)
            elif cmd == '9':
                print("Enter bigram index path: ")
                path = input() #eng_doc_bigram.txt"
                bg_idx = load_bigram(path)
                print("Enter query: ")
                query = input()
                query= persian_preproccess.prepare_text(query)
                query = list(query.split())
                ans = spell_correction(query, bg_idx, type1=False)
                print(ans)
            elif cmd == '10':
                print("Enter Distance Type(Jacc or Edit): ")
                type = input()
                print("Enter two Words: ")
                words = input().split()
                ans = jaccard_dist_type2(*words) if type == "Jacc" else edit_distance(*words)
                print(ans)
            elif cmd == '11':
                print("Enter Query")
                query = input()
                query=persian_preproccess.prepare_text(query)
                search(query, wiki_title_posting_list, wiki_document_posting_list, wiki_total_documents)
            elif cmd == '12':
                print("Enter Query like : word1 /range word2")
                query = input()
                key1 , key2 , size =proccess_query(query)
                doc_id_founded = persian_CalculateOccurences(key1,key2,size , "../datasets/phase1/prepared_english.csv")
                print("founded from proximity search: ",doc_id_founded)

                for i in range(wiki_total_documents):
                    if i not in doc_id_founded:
                        wiki_title_posting_list,wiki_document_posting_lis,wiki_total_documentst= wiki_delete_index(i,wiki_title_posting_list ,wiki_document_posting_list,wiki_total_documents)
                search(key1+' '+key2 ,wiki_title_posting_list, wiki_document_posting_list, wiki_total_documents)

            elif cmd == '13':
                break
