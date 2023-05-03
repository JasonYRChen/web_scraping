import re
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from collections import defaultdict
from pprint import pprint


def getNgrams(content, n, counter=None):
    content = re.split(r'\s+', content)
    ngram = defaultdict(int) if counter is None else counter
    for i in range(len(content)-n+1):
        ngram[tuple(content[i:i+n])] += 1
    return ngram


def getSemiSentence(content):
    content = re.split(r',\s*', content)
    return content


def getSentence(content):
    content = re.sub(r'\[.+?\]', '', content)
    content = re.split(r'\.\s*', content)
    return content
    

def getParagraph(paragragh, n_gram=2, counter=None):
    for sentence in getSentence(paragragh):
        for semisentence in getSemiSentence(sentence):
            yield getNgrams(semisentence, n_gram, counter)


counter = defaultdict(int)
url = 'http://en.wikipedia.org/wiki/Python_(programming_language)'
root = bs(urlopen(url), 'html.parser')
content = root.find('table', {'class': 'infobox vevent'}).nextSibling
for p in content.find_next_siblings('p')[:4]:
    for result in getParagraph(p.get_text(), 2, counter):
        continue
pprint(counter)
