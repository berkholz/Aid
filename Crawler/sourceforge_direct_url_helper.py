import requests
from bs4 import BeautifulSoup

def getWebSite(url):
    # creating request with custom user agent string
    response = requests.get(url,allow_redirects=False).text
    return BeautifulSoup(response, 'html.parser')

def get_direct_url(url):
    site = getWebSite(url)
    link = site.find('a', href=True)['href']
    return link

