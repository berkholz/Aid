import requests
from bs4 import BeautifulSoup


def getWebSite(url):
    """returns website as bs4 object"""
    # creating request with custom user agent string
    response = requests.get(url, allow_redirects=False).text
    return BeautifulSoup(response, 'html.parser')


def get_direct_url(url):
    """selects direct download url from sourceforge sites"""
    site = getWebSite(url)
    link = site.find('a', href=True)['href']
    return link
