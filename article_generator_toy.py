import re
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from random import randint, choice
from pprint import pprint


def wiki_content_retriever(url, max_paragraph=10):
    """
        Retrieve raw content from wiki url.

        paras:
          url: str, url of wiki website.
          max_paragraph: int, the maximum paragragh to retrieve.

        return:
          content: str, the raw content from the given url.
    """

    root = bs(urlopen(url), 'html.parser')
    content = root.find('table', {'class': 'infobox vevent'}).nextSibling.find_next_siblings('p')
    content = [p.get_text() for p in content[:max_paragraph]]
    content = '\n'.join(content)
    return content


def clean_content(content):
    """
        Remove something like '[x]' ,'(x)' and '"', then replace '.' and 
        ',' with ' . ' and ' , ', respectively.

        para:
          content: str, the raw content.

        return:
          content: str, the clean content.
    """

    content = re.sub(r'\[\w+?\]', '', content) # remove '[xx]'
    content = re.sub(r'\((\w+.?\w+\s?)+\)', '', content) # remove '(xx)'
    content = re.sub(r'\"', '', content) # remove "
    content = re.sub(r'(\.\s+)', ' . ', content) # identify end of sentence
    content = re.sub(r',', ' , ', content) # identity comma
    return content
    

def word_dict(content):
    """
        Arrange the input content into the form of '{current word: 
        {next word: number}}'

        para:
          content: str, the clean content offered by 'clean_content' 
                   function.

        return:
          lookup_table: dict(dict(int)), a dictionary containing the words
                        in the content, and each word contains its another
                        dictionary to make count on the word next to it in
                        the content.
    """

    content = content.split()
    lookup_table = defaultdict(lambda: defaultdict(int))
    for i in range(len(content)-1):
        word_curr, word_next = content[i], content[i+1]
        lookup_table[word_curr][word_next] += 1
    return lookup_table


def fake_article(lookup_table, sentences=10):
    """
        Using 'lookup_table' to fake an article with 'sentences' number of
        sentences.

        paras:
          lookup_table: dict(dict(int)), the object returned by 'word_dict'
          sentences: int, number of sentences to fake.

       return:
          paragraph: str, a fake paragraph.
    """

    # add up the number belongs to each key
    counter = defaultdict(int)
    for key, words in lookup_table.items():
        for value in words.values():
            counter[key] += value

    # pick a starter from the dictionary of '.'
    words = []
    words.append(choice(list(lookup_table['.'].keys())))

    number = 1
    while number < sentences:
        word = words[-1]
        count = randint(1, counter[word]) # to randomly choose next word
        # kind of 'randomly' choose the next word
        for next_word, value in lookup_table[word].items():
            count -= value
            if count <= 0:
                break # next word found

        words.append(next_word)
        if next_word == '.': # meet the end of a sentence
            number += 1

    paragraph = ' '.join(words)
    return paragraph
    

url = 'http://en.wikipedia.org/wiki/Python_(programming_language)'
print(fake_article(word_dict(clean_content(wiki_content_retriever(url)))))
