
# coding: utf-8

import requests as rs
import time
from bs4 import BeautifulSoup
import csv, os, shutil


def retrieve_data(string,lst):
    """
    
    """
    if string == 'description':
        results = soup.find_all(class_ = string)
        map(lambda one_res: lst.append((res.get_text().encode('ascii','ignore').replace('\n',' '))), results)

    elif string == 'url':
        results = soup.find_all(class_ = string)
        map(lambda one_res: lst.append(one_res['href']), results)
    else:
        results = soup.find_all(class_ = string)
        map(lambda one_res: lst.append((one_res.get_text().encode('ascii','ignore'))), results)
        
    
def addAds(url):
    """
    
    """
    if not os.path.exists('temporary'):
        os.mkdir('temporary')
    r = rs.get(url)
    soup = BeautifulSoup(r.content)
    parsed_classes = ['title', 'locale','price', 'description', 'cta']
    conversion_categories = {'title':'title',
                             'locale':'locations',
                             'price': 'price',
                             'description': 'description',
                             'cta': 'url'}
    @global extracted_info
    extracted_info = {}
    for category in conversion_categories:
        extracted_info[conversion_categories[category]] = []
        retrieve_data(category,extracted_info[conversion_categories[category]])
            
    results = soup.find_all(class_='cta')
    for res in results:
        urls.append(res['href'])
    
    all_ads = [list(i) for i in zip(titles, locations, prices, descriptions, urls)]
    
    count = 0
    while os.path.isfile('temporary/%s.tsv'%(count)):
        count += 1
    else:
        for ad in all_ads:
            output = open(('temporary/%s.tsv'%(all_ads.index(ad)+count)), 'wb')
            adv = csv.writer(output, delimiter='\t')
            adv.writerow(ad)
            output.close()

            
def collect(n):
    """
    
    """
    Nfolder = 32*n
    if (Nfolder < 500):
        os.makedirs('documents/0-%s'%(Nfolder-1))
        numrange = Nfolder
        for i in range(numrange):
            shutil.move('temporary/%s.tsv'%(i),'documents/0-%s'%(Nfolder-1)) #move the files to the right folders
    else:
        TOTfolder = Nfolder/500
        for i in range(1, TOTfolder+1):
            inf = (i)*500 - 500
            sup = (i)*500
            os.makedirs('documents/%s-%s'%((i)*500 - 500,(i)*500-1))
            for y in range(inf,sup):
                shutil.move('temporary/%s.tsv'%y,'documents/%s-%s'%(inf, sup-1))
        if (Nfolder%500 != 0):
            liminf = ((Nfolder/500)*500)
            limsup = (Nfolder/500)*500+(Nfolder%500)
            os.makedirs('documents/%s-%s'%((Nfolder/500)*500, (Nfolder/500)*500+(Nfolder%500)-1))
            for x in range(liminf,limsup):
                shutil.move('temporary/%s.tsv'%x, 'documents/%s-%s'%(liminf,limsup-1))

def processAllPages(baseURL, minPage=1, maxPage=1, delay=2,):
    """
    
    """
    for i in range(minPage, maxPage+1):
        print "Processing page: " + str(i)
        print
        addAds(baseURL + "?p=" + str(i))
        time.sleep(delay)
    collect(maxPage)  
    os.rmdir('temporary')