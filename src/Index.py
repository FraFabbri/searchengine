
# coding: utf-8

import nltk,csv,os
from nltk.corpus import stopwords

stemmer = nltk.SnowballStemmer('italian')
stop = stopwords.words('italian')


def make_vocabulary(folder = 'documents'):
    """
    Write the dictionary in a txt file
    
    Args:
        folder (str): name of the folder containing the ads
        
    Additional info:
        - at this time, the price and the url are discarded 
        - the dict is built without the stopwords and each term taken is then stemmed
    """
    @global listfiles
    listfiles = []
    firstvocabulary =  []
    for folder in main_folder:
        listed_ads = os.listdir('%s/%s'%(main_folder,x))
        for i in listed_ads:
            start = open('%s/%s/%s'%(main_folder,folder,i))
            ad = start.read().lower().translate(None,',.<>/?;:"’[]{}|=+-_()*&^%$#@!‘~\\\n\r'+"'").split('\t')
            del ad[2] #remove price
            del ad[-1] #remove the url
            final = reduce(lambda x,y: x+ y, map(lambda word: word.split(), ad))
            #remove stopwords
            nostopword = filter(lambda word: word not in stop, final) 
            stemmed = [stemmer.stem(term).encode('ascii','ignore') for term in nostopword]
            listfiles.append(stemmed)
            firstvocabulary += stemmed    
    @global vocabulary
    vocabulary = sorted(set(firstvocabulary))
    output = zip(range(len(set(vocabulary))), vocabulary)
    os.mkdir('index')
    with open('index/vocabulary.txt','w') as d:
        vocabulary_out = csv.writer(d, delimiter='\t')
        for row in output:
            vocabulary_out.writerow(row)

            
def make_postinglist():
    """
    Writes the posting-list on the txt file    
    """
    vocabulary = sorted(set(firstvocabulary))
    postinglist = []
    voclist = (list(vocabulary))
    for z in voclist:
        postinglist.append([z])
    for t in voclist:
        for singlead in listfiles:
            if ('%s'%t) in singlead:
                postinglist[voclist.index('%s'%t)].append(listfiles.index(singlead))
    
    for i in postinglist:
        i[0] = postinglist.index(i)
    if not os.path.exists('index'):
        os.mkdir('index')
    with open('index/postinglist.txt','w') as plfiles:
        postinglist_out = csv.writer(plfiles, delimiter='\t')
        for row in postinglist:
                postinglist_out.writerow(row)
                
                
                
