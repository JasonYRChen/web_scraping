import re
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pprint import pprint


def getNgrams(content, n):
    content = re.split(r'\s+', content)
    content = [content[i:i+n] for i in range(len(content)-n+1)]
    return content


def getSemiSentence(content):
    content = re.split(r',\s*', content)
    return content


def getSentence(content):
    content = re.sub(r'\[.+?\]', '', content)
    content = re.split(r'\.\s*', content)
    return content
    

def getParagraph(paragragh, n_gram=2):
    for sentence in getSentence(paragragh):
        for semisentence in getSemiSentence(sentence):
            yield getNgrams(semisentence, n_gram)


url = 'http://en.wikipedia.org/wiki/Python_(programming_language)'
root = bs(urlopen(url), 'html.parser')
content = root.find('table', {'class': 'infobox vevent'}).nextSibling
for p in content.find_next_siblings('p')[:4]:
    print(p.get_text(), end='\n\n')
    for result in getParagraph(p.get_text(), 2):
        pprint(result)
