
# coding: utf-8

# In[19]:

from Collect import *
from Index import *
from Search import *
import os


#Set pages of announcements:
if not os.path.exists('documents'):
    print "Please, select how many pages you want to scan:"
    Num_pages = raw_input()
    Num_pages = int(Num_pages)
    processAllPages('http://www.kijiji.it/case/vendita/roma-annunci-roma',1,Num_pages,2)
    #Index
    print "Just few seconds to search"
    make_vocabulary('documents')
    make_postinglist('documents')
#Query
print "Now, write your query without accented characters:"
Query = raw_input()
make_query(Query)

