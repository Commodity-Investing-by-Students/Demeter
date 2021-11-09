#Python code to illustrate parsing of XML files
# importing the required modules
import requests
import xml.etree.ElementTree as ET
  
def loadRSS_USDA():
  
    # url of rss feed
    url = 'https://www.usda.gov/rss/latest-releases.xml'
    
    # creating HTTP response object from given url
    resp = requests.get(url)
    
    # saving the xml file
    with open('latest-releases.xml', 'wb') as f:
        f.write(resp.content) 

def parseXML(xmlfile):
    
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # create empty list for news items
    newsitems = []
  
    # iterate news items
    for item in root.findall('./channel/item'):
  
        # empty news dictionary
        news = {}
  
        # iterate child elements of item
        for child in item:
  
            # special checking for namespace object content:media
            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']
            else:
                news[child.tag] = child.text.encode('utf8')
  
        # append news dictionary to news items list
        newsitems.append(news)
      
    # return news items list
    return newsitems

def savetoCSV(newsitems, filename):
  
    # specifying the fields for csv file
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']
  
    # writing to csv file
    with open(filename, 'w') as csvfile:
  
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
  
        # writing headers (field names)
        writer.writeheader()
  
        # writing data rows
        writer.writerows(newsitems)

def USDA():
    # load rss from web to update existing xml file
    loadRSS_USDA()
  
    # parse xml file
    newsitems = parseXML('latest-releases.xml')

    links = list() 

    for i in newsitems:
        for j in i:
            if j == "link":
                links.append(i["link"])

    three = str(links[0])[1:] + " " + str(links[1])[1:] + " " + str(links[2])[1:]

    return three

def summary(text):
    text = "Text you want to summarize"
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    clean_text = text.lower()
    word_tokenize = clean_text.split()
    #english stopwords
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    word2count = {}
    for word in word_tokenize:
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    sent2score = {}
    for sentence in sentences:
        for word in  sentence.split():
            if word in word2count.keys():
                if len(sentence.split(' ')) < 28 and len(sentence.split(' ')) > 9:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]
    # weighted histogram
    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())  
    
    best_three_sentences = heapq.nlargest(3, sent2score, key=sent2score.get)
    return (best_three_sentences)


#integrate goose + add to discord + do write up 


from goose import Goose3
#from requests import get
from bot import text
links = USDA()
links.replace("'", "") 
links = links.split()
print(summary(text(links[0].replace("\'", ""))))

'''
response = get(str(link[0])[1:])
extractor = Goose()
article = extractor.extract(raw_html=response.content)
text = article.cleaned_text
title = article.title

print("title: ", title)
print("article:", cleaned) 
print("cleaned:", text)
'''

