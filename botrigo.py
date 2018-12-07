''' Botrigo Crawler.

agent
-mobile
-all browsers

print
((
>>> import imgkit
>>> imgkit.from_url('https://google.com','out.jpg')
))

json output (everything)

UUID: (full address SHA256)
page:
http_code:
time:
headers:
files: (and the http response code for all files)

{
    UUID:[
        "page": "https://XXX.com/",
        "http_code": 200,
        "1st_byte": 2.151707,
        "headers":[
            "x-frame-options": "ok",
            "strict-transport-security": "ok",
            "access-control-allow-origin": "ok",
            "content-security-policy": "ok",
            "x-xss-protection": "ok",
            "x-xss-protection": "ok",
            "x-powered-by": "ok",
            "server": "ok" 
        ],
        "objects":[
            "scripts":[ 
                "https://XXX.com/wp/wp-includes/js/jquery/jquery.js?ver=1.12.4",
                "https://XXX.com/wp/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1"],
            "images":[
                "https://XXX.com/app/uploads/2016/02/XXX.jpg",
                "https://XXX.com/app/uploads/2016/02/XXX.jpg"],
        ],
        "print_file":"UUID.png"
    ]
}


quiet mode

'''

import re
import json
from urllib.parse import urljoin, urlsplit, SplitResult
import requests
from bs4 import BeautifulSoup
import argparse
import securityheaders as SecurityHeaders
import securityscripts as SecurityScripts


class RecursiveScraper:
    ''' Scrape URLs in a recursive manner.
    '''

    def __init__(self, url,errors_only, links, check_headers, check_files):
        ''' Constructor to initialize domain name and main URL.
        '''
        self.domain = urlsplit(url).netloc
        self.mainurl = url
        self.urls = set()
        self.final_status = {}
        self.errors_only = errors_only
        self.links = links
        self.check_headers = check_headers
        self.check_files = check_files
        self.actual_URL = url

        '''Colors!'''
        self.okColor = '\033[92m'
        self.warnColor = '\033[93m'
        self.endColor = '\033[0m'

    def preprocess_url(self, referrer, url):
        ''' Clean and filter URLs before scraping.
        '''

        ignoreList = ['.pdf', '.jpg', 'tel:', '.dmg']

        if not url:
            return None

        fields = urlsplit(urljoin(referrer, url))._asdict() # convert to absolute URLs and split
        fields['path'] = re.sub(r'/$', '', fields['path']) # remove trailing /
        fields['fragment'] = '' # remove targets within a page
        fields = SplitResult(**fields)
        if fields.netloc == self.domain:
            # Scrape pages of current domain only
            if fields.scheme == 'http':
                httpurl = cleanurl = fields.geturl()
                httpsurl = httpurl.replace('http:', 'https:', 1)
            else:
                httpsurl = cleanurl = fields.geturl()
                httpurl = httpsurl.replace('https:', 'http:', 1)

            for item in ignoreList:
                if item in httpsurl or item in httpurl:
                    return None

            if httpurl not in self.urls and httpsurl not in self.urls:
                    # Return URL only if it's not already in list
                    return cleanurl

        return None


    def SecFiles(self,url):
        
        print("|=======================COMPONENTS=================================|")

        secscripts = SecurityScripts.RecursiveScraper(url)

        Scannedscripts = secscripts.scrape(url)

        print("|==================================================================|")

    def headers(self,url):
        
        print("|=======================HEADERS====================================|")

        secHeaders = SecurityHeaders.SecurityHeaders()

        ScannedHeaders = secHeaders.check(url)

        print("|==================================================================|")

    def resp_counter(self, response):

        print(" ")
        print("|=======================INFORMATION================================|")
        #print("| Source: {:s} ...".format(self.actual_URL))
        print("|------------------------------------------------------------------|")
        print("| Scraping {:s} ...".format(response.url))

        if response.history:
            print("| Request was redirected")
            for resp in response.history:
                print("| ",resp.status_code, resp.url)

        else:
            print("| Request was not redirected")

        print("| Final destination:")
        print("| ", response.status_code, response.url)
        print('| 1st byte time: ' + str(response.elapsed.total_seconds() ) )
        print("|==================================================================|")

    def links_list(self,soup,response):
        print("|=======================LINKS======================================|")
        print("| Links found on " + response.url )
        for link in soup.findAll("a"):
            childurltemp = self.preprocess_url(response.url, link.get("href"))
            if childurltemp:
                print("| " + str(childurltemp))

        print("|==================================================================|")

    def out_of_domain(self,response):

        print("|=======================OUT OF DOMAIN==============================|")
        print("| The link is out of domain..." )
        print("| From: " + self.actual_URL)
        print("| To: " + response.url)
        print("|==================================================================|")

    def scrape(self, url=None):
        ''' Scrape the URL and its outward links in a depth-first order.
            If URL argument is None, start from main page.
        '''
        if url is None:
            url = self.mainurl
        
        self.urls.add(url)
        response = requests.get(url,headers={'cache-control':'no-cache'})
        
        fields = urlsplit(response.url)._asdict()
        if fields['netloc'] != self.domain:
            self.out_of_domain(response)
            self.final_status.setdefault(000,[]).append(response.url)
            return

        if (self.errors_only and response.status_code == 404)or(self.errors_only == False):
            self.resp_counter(response)

        self.final_status.setdefault(response.status_code,[]).append(response.url)
        soup = BeautifulSoup(response.content, 'lxml')

        if check_files:
            self.SecFiles(url)

        if check_headers:
            self.headers(url)

        if links:
            self.links_list(soup,response)
            
        for link in soup.findAll("a"):
            childurl = self.preprocess_url(response.url, link.get("href"))
            if childurl:
                self.actual_URL = response.url
                self.scrape(childurl)



if __name__ == '__main__':


    print("__________        __         .__               ")
    print("\______   \ _____/  |________|__| ____   ____  ")
    print(" |    |  _//  _ \   __\_  __ \  |/ ___\ /  _ \ ")
    print(" |    |   (  <_> )  |  |  | \/  / /_/  >  <_> )")
    print(" |______  /\____/|__|  |__|  |__\___  / \____/ ")
    print("        \/                     /_____/         ")
    print(" ")

    parser = argparse.ArgumentParser(description='Botrigo link cralwer', \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help='Target URL')
    #parser.add_argument("--out404",  help='Output only the 404s')
    parser.add_argument("-o", "--out404", help="List only the 404s", action="store_true")
    parser.add_argument("-l", "--links", help="Show internal links", action="store_true")
    parser.add_argument("-c", "--check_headers", help="Check headers for all links", action="store_true")
    parser.add_argument("-x", "--check_files", help="List components", action="store_true")
    parser.add_argument("-aM", "--agent_mobile", help="Use Mobile agent", action="store_true")
    parser.add_argument("-aD", "--agent_desktop", help="Use Desktop agent", action="store_true")
    parser.add_argument("-aG", "--agent_google", help="Use fake Google agent", action="store_true")
    parser.add_argument("-p", "--print", help="Print website", action="store_true")
    parser.add_argument("-j", "--json_output", help="Print website", action="store_true")


    args = parser.parse_args()

    url = args.url
    links = args.links
    check_headers = args.check_headers
    check_files = args.check_files
    if not args.out404:
        errors_only = False
    else:
        errors_only = True


    print("Startig connection to " + url)
    print("Errors only: " + str(errors_only) )
    print("Show links: " + str(links))
    print("Check headers: " + str(check_headers) )
    print("List Components: " + str(check_files) )

    print(" ")


    rscraper = RecursiveScraper(url,errors_only, links, check_headers, check_files)

    rscraper.scrape()

    retjson = json.loads(json.dumps(rscraper.final_status))

    print(json.dumps(rscraper.final_status, sort_keys=True, indent=4))
