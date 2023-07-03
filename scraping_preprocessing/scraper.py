"""
Author: Ra Cohen (ra.q.cohen@gmail.com)
Date: 5/1/2023
Purpose: Scrape TV Tropes from the graph of tropes 
"""

import requests
from bs4 import BeautifulSoup


class Page(object):
    
    def __init__(self, url):
        self.url = strip_domain(url)
        kind, name = get_info_from_url(url)
        ptype = type_from_kind(kind)
        self.kind = kind
        self.name = get_name(name)
        self.ptype = ptype
    
    def __repr__(self):
        return f'{self.ptype} : {self.name}'

def all_trope_parser(i):
    URL = "https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page="+str(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    folders = get_page_html(url).findAll('div', {'id': 'main-article'})

    related_tropes = []

    if folders:
        lis = []
        for folder in folders:
            lis.extend(folder.findAll('li'))
    else:
        lis = page.find('h2').findNext('ul').findAll('li')
    for li in lis:
        links = li.findAll('a', {'class': 'twikilink'})
        related_tropes.extend(links)
    related_tropes = set([related_trope for related_trope in related_tropes if related_trope['href'] != url])
    related_tropes = [Page(related_trope['href']) for related_trope in related_tropes]
    related_tropes = [related_trope for related_trope in related_tropes if related_trope.ptype == 'Trope']
    return related_tropes




# 

"""

get trope list:
    Get all urls from 
https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page=1
https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page=59

For url in list_tropes:
    create node
    extract 

"""