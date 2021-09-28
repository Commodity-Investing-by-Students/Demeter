from os import linesep
import feedparser
from datetime import datetime
from time import mktime
import requests
from bs4 import BeautifulSoup
# maximo xavier deleon


import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 



def main():
    DEBUG = False
    publication_data = getRSS(RSS_FILE='rssFeedURLS.txt',verbose=DEBUG)
    publication_data = sortList(publication_data,0)
    #nltk.download('stopwords')
    #nltk.download('punkt')



    for i in range(len(publication_data)):
        print('Date: {}\nTitle: {}\nURL: {}'.format(publication_data[i][0],publication_data[i][2],publication_data[i][1]))
        print('------------------')

# reads a text file and returns an array
def parseFile(filename:str):
    f = open(filename, "r")
    lines = []
    for line in f:
        line = line.rstrip()
        line = line.split(',')
        lines.append(line)
    return lines

def getRSS(RSS_FILE:str,verbose=True):
    publications = []
    file_data = parseFile(filename=RSS_FILE) # parse file data into array
    for i in range(len(file_data)): # iterate through array
        current_news_feed = feedparser.parse(file_data[i][1]) # get rss feed url
        for entry in current_news_feed.entries[::-1]: # iterate through all the entries in the rss feed
            publication = [datetime.fromtimestamp(mktime(entry.updated_parsed)),
                            entry.link,
                            entry.title,
                            file_data[i][1]]
            publications.append(publication)
            # print out news stuff for each entry in each rss feed
            if verbose:
                print('Date: {}'.format(publication[0])) 
                print("Link: {}".format(publication[1]))
                print('-----------')
                print('Source:{}\nTitle: {}'.format(file_data[i][4],publication[2]))
                print('Summary: \n{}'.format(publication[3]))
                print('===========')
    return publications # return data


def getTextFromArticle(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output


def summarize(text):
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 
    
    # Creating a frequency table to keep the  
    # score of each word 
    
    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1
    
    # Creating a dictionary to keep the score 
    # of each sentence 
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 
    
    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq  
    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 
    
    # Average value of a sentence from the original text 
    
    average = int(sumValues / len(sentenceValue)) 
    
    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)): 
            summary += " " + sentence 
    return summary


def sortList(sub_li,index):
  
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[index])
    return sub_li


if __name__ == "__main__":
    main()