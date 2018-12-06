''' Scraper.
'''

import re
import json
from urllib.parse import urljoin, urlsplit, SplitResult
import requests
from bs4 import BeautifulSoup
import argparse

class RecursiveScraper:
    ''' Scrape URLs in a recursive manner.
    '''
    def __init__(self, url):
        ''' Constructor to initialize domain name and main URL.
        '''
        self.domain = urlsplit(url).netloc
        self.mainurl = url

    def scrape(self, url=None):
        ''' Scrape the URL and its outward links in a depth-first order.
            If URL argument is None, start from main page.
        '''
        if url is None:
            url = self.mainurl

        response = requests.get(url)

        fields = urlsplit(response.url)._asdict()
        
        if fields['netloc'] == self.domain:

            soup = BeautifulSoup(response.content, 'lxml')

            #script
            for x in soup.find_all("script"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| script: " + x["src"])
                except KeyError:
                    pass

            #script
            for x in soup.find_all("img"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| img: " + x["src"])
                except KeyError:
                    pass

            #script
            for x in soup.find_all("link"):
                try:
                    if self.mainurl in x["href"] or "./" in x["href"] or "/" in x["href"][:1]:
                        pass
                    else:
                        print("| link: "+ x["src"])
                except KeyError:
                    pass

            #script
            for x in soup.find_all("video"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| video: " + x["src"])
                except KeyError:
                    pass        

            #script
            for x in soup.find_all("audio"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| audio" + x["src"])
                except KeyError:
                    pass        

            #script
            for x in soup.find_all("iframe"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| iframe: " + x["src"])
                except KeyError:
                    pass        

            #script
            for x in soup.find_all("embed"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| embed: " + x["src"])
                except KeyError:
                    pass        

            #script
            for x in soup.find_all("object"):
                try:
                    if self.mainurl in x["data"] or "./" in x["data"] or "/" in x["data"][:1]:
                        pass
                    else:
                        print("| object: " + x["src"])
                except KeyError:
                    pass        

            #script
            for x in soup.find_all("source"):
                try:
                    if self.mainurl in x["src"] or "./" in x["src"] or "/" in x["src"][:1]:
                        pass
                    else:
                        print("| source: " + x["src"])
                except KeyError:
                    pass        

        else:
            print("| /!\ Out of domain")
