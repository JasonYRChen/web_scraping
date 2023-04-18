import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from collections import deque, defaultdict
from pprint import pprint


def get_link(url, path, base_url=''):
    """
        paras:
          url: str, the url to scrape descendent links.
          path: str, a series of url paths seperated by "|"
          base_url: str, the base of each url found in the function.
        return:
          new_path: list of tuples of url and paths.
    """

    new_path = defaultdict(str)
    root = bs(urlopen(url), 'html.parser')
    links = root.find('div', {'id': 'bodyContent'}).find_all('a', \
            {'href': re.compile(r'^(/wiki/)((?!:).)*$')})
    for link in links:
        href = link.attrs['href']
        if not href.startswith('http'):
            href = base_url + href
        if href not in new_path:
            new_path[href] = path + '|' + href
    
    new_path = list(new_path.items())
    return new_path


def wiki_target(target, starting_url, base_url=''):
    """
        Use breadth-first search to find the target in the title of the 
        pages traversing from 'starting_url' through its descendents.

        paras:
          target: str, the title of the wiki page to search for.
          starting_url: str, the starting url to start searching.
          base_url: str, the base page's url.

        return:
          target_path: list of str, a series of path from 'starting_url' to
                       the target. If target not found, return None instead.

        Work explanation: Pop from 'search_pool' and check if the title in 
        the popped url is equal to the target. If yes, return the path. 
        If not, append the popped tuple to 'to_scrape_pool'. If 
        'search_pool' is empty, popleft 'to_scrape_pool' and 'get_link' 
        all its descendents links, then extend them to 'search_pool'. 
        If both 'search_pool' and 'to_search_pool' are empty, the search 
        stops and returns None.
    """

    search_pool = [(starting_url, starting_url)]
    to_scrape_pool = deque()
    target = target.lower()
    
    while search_pool or to_scrape_pool:
        if search_pool:
            target_url, target_path = search_pool.pop()
            print(f'Searching {target_url}, now at {target_path}', end='\n\n')
            title = bs(urlopen(target_url), 'html.parser').head.title.get_text().lower()
            if title.find(target) != -1:
                target_path = target_path.split('|')
                return target_path

            # target not found, append current url to 'to_scrape_pool'
            to_scrape_pool.append((target_url, target_path))

        if (not search_pool) and (to_scrape_pool):
            url, path = to_scrape_pool.popleft()
            new_path = get_link(url, path, base_url)
            search_pool.extend(new_path)
    return None
        

if __name__ == '__main__':
    base = 'http://en.wikipedia.org'
    url = base + '/wiki/Kevin_Bacon'
    target = 'Tom Hanks'
    print(wiki_target(target, url, base))
