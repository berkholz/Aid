from bs4 import BeautifulSoup
import urllib
import datetime 
import requests                 # for getting http ressources
import re                       #import for filtering Links via RegExp
from datetime import date       # for generating dates in JSON

downloads = list()

app_name = "adobe_enterprise".lower()
full_name = "Adobe Reader Enterprise"
default_architecture = 'win32'
app_version = 0

def build_download_link():
    """Generate the url to the download page."""
    year = str(datetime.datetime.now().year)
    month = datetime.datetime.now()
    month_number = datetime.datetime.now().month
    month_name = ""
    if month_number == 6 or month_number == 7:
        month_name = month.strftime("%B").lower()[0:4]
    else: 
        month_name = month.strftime("%B").lower()[0:3]

    # return link with month and year 
    return "https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/continuous/dccontinuous" + month_name + year + ".html"


def getWebSite(download_url):
    """creating request with custom user agent string"""
    response = requests.get(download_url).text
    return BeautifulSoup(response, 'html.parser')

def toJSON(d):
    """convert result as JSON"""
    json_result = {
        "app_name": app_name,
        "full_name": full_name,
        "default_download": default_architecture,
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00",
    }
    return json_result

def extract_links(table, architecture):
    """Extract download url for the given architecture from the HTML table from the download page."""
    for link in table.find_all('a'):
        if re.search('.*AcroRdrDC[0-9A-Za-z]+(\\.msp|_MUI\\.dmg)$', link.get('href')) != None:
            download_link = link.get('href')
            return {"app_platform": architecture, "url_bin": download_link, "sig_type": None, "sig_res": None, "hash_type": None, "hash_res": None, "url_pub_key": None}

def extract_version(download_website):
    """Extract version from dwonload page from website."""
    return download_website.h1.text.split(' ')[0]

def run():
    global downloads  
    global app_version  
    
    website = getWebSite(build_download_link())

    app_version = extract_version(website)
    
    # get all tables with downloads of any architecture
    tables = website.find_all('table')
    
    # iterate over tables by architecture
    for table in tables:
        if table['id'] == 'id1': # win32
            downloads.append(extract_links(table, "win32"))
        if table['id'] == 'id2': # win64
            downloads.append(extract_links(table, "win64"))
        if table['id'] == 'id3': # mac
            downloads.append(extract_links(table, "mac"))
    return toJSON(downloads)

if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
