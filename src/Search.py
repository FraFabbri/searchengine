
# coding: utf-8

#!/usr/bin/python

import csv, nltk, os
from nltk.corpus import stopwords

def make_query(string):
    """
    
    """
    stop = stopwords.words('italian')
    stemmer = nltk.SnowballStemmer('italian')
    qs = string.translate(None,',.<>/?;:"’[]{}|=+-_()*&^%$#@!‘~\\\n\r'+"'").lower()
    querylist = qs.split() # split the query to obtain the words
    # stopwords
    nostopwordquery = filter(lambda x: x not in stop, querylist) 
    # stemming
    querystemming = map(lambda x: stemmer.stem(term).encode('ascii','ignore'), nostopwordquery)
    with open('index/vocabulary.txt', 'rb') as v:
        vocabulary = list(csv.reader(v, delimiter= '\t'))
    with open('index/postinglist.txt', 'rb') as pl:
        postinglist = (csv.reader(pl, delimiter= '\t'))
    
    for one_query in querystemming:
        filtered_tuples = filter(lambda one_tuple: one_query in one_tuple, vocabulary)
    # retrieving the indexes of the ads which contain the words in the query
    indexes_adv = map(lambda one_tuple: filter(lambda one_word_pl: one_word_pl[0] == one_tuple[0], postinglist),
                      filtered_tuples)
    list_of_id = reduce(lambda x,y : x+y, [el[1:] for el in indexes_adv])
    bag_of_words_ads = {}
    for idx in list_of_id:
        if idx not in bag_of_words_ads:
            bag_of_words_ads[idx] = 1
        else:
            bag_of_words_ads[idx] += 1
    
    checklist = filter(lambda word_idx: bag_of_words_ads[word_idx] == len(querystemming), bag_of_words_ads.keys())
    results = list(set(checklist))
    if len(checklist)!=0:
        for w in results: #loop useful to print the results
            adq = '%s.tsv'%w
            folders = os.listdir('documents')
            for k in folders:
                one_folders_ads = os.listdir('documents/%s'%(k))
                if adq in adv:
                    with open('documents/%s/%s'%(k,adq), 'rb') as v:
                        final = csv.reader(v, delimiter= '\t')
                        final = list(final)
                        print 'Title: %s'%final[0][0]
                        print 'Location: %s '%final[0][1]
                        if final[0][2].isdigit():
                            print 'Price: %s€'%final[0][2]
                        else:
                            print 'Price: %s'%final[0][2]
                        print 'Url: %s\n'%final[0][4]
    else:
        print "Announcement not found!\nPlease try again with some different keys."