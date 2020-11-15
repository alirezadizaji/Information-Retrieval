import pandas as pd
import math

def listToString(lst):
    string = []
    for x in lst:
        if str(x) != 'nan':
            x = x.split(" ")
            st = ' '.join(map(str, x))
            string.append(st)
    return string


def CalculateOccurencesInRange(keyPositionsList, PositionToOccurencesMap, w_range, Length):


            OccurencesOfOtherKeyInRange = 0
            for keyPosition in keyPositionsList:

                rangeStart = keyPosition
                if rangeStart == Length - 1:
                    break

                rangeEnd = keyPosition + w_range
                rangeEnd = min(rangeEnd, Length- 1)
                otherKeyOccurencesAtRangeStart = PositionToOccurencesMap[rangeStart]
                otherKeyOccurencesAtRangeEnd = PositionToOccurencesMap[rangeEnd]
                # print(rangeStart , rangeEnd ,'dkfjv',otherKeyOccurencesAtRangeEnd)

                OccurencesOfOtherKeyInRange += otherKeyOccurencesAtRangeEnd - otherKeyOccurencesAtRangeStart

            return OccurencesOfOtherKeyInRange



def CalculateOccurences(keyword1 , keyword2,window_range):

    founded_result=[]
    csv_data = pd.read_csv("/Users/atena/PycharmProjects/Information-Retrieval-Project/prepared_english.csv")
    titles = csv_data['title']
    titles = listToString(titles)


    #titles
    for w in titles:
        words = w.split(' ')
        position_occurance_1 = dict()
        position_occurance_2 = dict()
        position_occurance_1[-1]=0
        position_occurance_2[-1]=0
        keyword1_positions=[]
        keyword2_positions=[]
        for i in range(len(words)):
            position = i
            word = words[i]
            OccurencesForKey1 = position_occurance_1[position-1]
            OccurencesForKey2 = position_occurance_2[position-1]
            if word == keyword1:
                        keyword1_positions.append(position)
                        OccurencesForKey1+=1
            elif word == keyword2:
                        keyword2_positions.append(position)
                        OccurencesForKey2+=1

            position_occurance_1[position]=OccurencesForKey1
            position_occurance_2[position]=OccurencesForKey2

        # if one of keys does not exists should return
        if not keyword1_positions or not keyword2_positions:
            continue

        key1Occurences = CalculateOccurencesInRange(keyword1_positions, position_occurance_2, window_range,len(words))
        key2Occurences = CalculateOccurencesInRange(keyword2_positions, position_occurance_1, window_range,len(words))
        totalOccurences_titles = key1Occurences + key2Occurences

        if totalOccurences_titles >0:
           founded_result.append(titles.index(w))
           # print(titles.index(w),w,'\n' , key1Occurences,key2Occurences,totalOccurences_titles ,'\n')


    #descriptions

    descriptions = csv_data['description']
    descriptions = listToString(descriptions)
    for w in descriptions:
            words = w.split(' ')
            position_occurance_1 = dict()
            position_occurance_2 = dict()
            position_occurance_1[-1]=0
            position_occurance_2[-1]=0
            keyword1_positions=[]
            keyword2_positions=[]
            for i in range(len(words)):
                position = i
                word = words[i]
                OccurencesForKey1 = position_occurance_1[position-1]
                OccurencesForKey2 = position_occurance_2[position-1]
                if word == keyword1:
                            keyword1_positions.append(position)
                            OccurencesForKey1+=1
                elif word == keyword2:
                            keyword2_positions.append(position)
                            OccurencesForKey2+=1

                position_occurance_1[position]=OccurencesForKey1
                position_occurance_2[position]=OccurencesForKey2

            # if one of keys does not exists should return
            if not keyword1_positions or not keyword2_positions:
                continue

            key1Occurences = CalculateOccurencesInRange(keyword1_positions, position_occurance_2, window_range,len(words))
            key2Occurences = CalculateOccurencesInRange(keyword2_positions, position_occurance_1, window_range,len(words))
            totalOccurences_des = key1Occurences + key2Occurences

            if totalOccurences_des >0:
                founded_result.append(descriptions.index(w))
               # print(descriptions.index(w),w,'\n' , key1Occurences,key2Occurences,totalOccurences_des ,'\n')

    return founded_result




def proccess_query(query):
    q = query.split(' ')
    num = q[1]
    return q[0] , q[2]  ,int(num[1:])



# CalculateOccurences('kill' , 'million' , 3)
# Indexing.eng_delete_index()
# print(founded_result)
#

