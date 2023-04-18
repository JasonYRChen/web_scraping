import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pprint import pprint


def build_website_map(root_url, mapping, base='', max_level=3, *, level=1):
    """
        Recursively traverse the site starts from 'root_url' and build
        and renew the website map 'mapping'. Be very cautious of potential
        circle inside the site when recursively crawling, like a->b->c->a,
        this will cause infinite loop without finishing the crawling.

        paras:
          root_url: str, the url to start building website map with.
          mapping: dict of set, a map of each site and their links to 
                   others.
          base: str, the base to each site.
        return:
          mapping: dict of set, the same object in the arguments.
    """

    # the first statement in 'if' is to prevent infinite recursive loop
    if (root_url not in mapping) and (level <= max_level):
        mapping[root_url] = set()
        try:
            links = bs(urlopen(root_url), 'html.parser').find_all('a', \
                       href=re.compile(r'^(/wiki/)'))
        except:
            pass
        else:
            for link in links:
                href = link.attrs['href']
                if not href.startswith('http'):
                    href = base + href
                print(f'...working on adding "{href}" to node "{root_url}"')
                mapping[root_url].add(href)
                build_website_map(href, mapping, base, level=level+1)
    return mapping


if __name__ == '__main__':
    base = 'https://en.wikipedia.org'
    url = base + '/wiki/Kevin_Bacon'
    mapping = {}
    pprint(build_website_map(url, mapping, base))
