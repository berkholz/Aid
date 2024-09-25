import requests
from bs4 import BeautifulSoup
import urllib
from datetime import date

download_url = 'https://keepass.info/download.html'
integrity_url= 'https://keepass.info/integrity.html'
pub_key_url = 'https://keepass.info/integrity/DominikReichl.asc'

app_name = "keepass".lower()
full_name = "Keepass"
default_download = 'win64'
base_url = download_url.split('/')[0] + '//' + download_url.split('/')[1] + download_url.split('/')[2] + '/'


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


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') < 1 and url.find('sha256') < 1:
        return url


def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') < 1 and ref['href'].find('sha256') < 1

def toJSON(d):
    json_result = {
        "app_name": app_name,
        "full_name": full_name,
        "default_download": default_download,
        "app_version": app_version,
        "downloads": d,
        "last_found": date.today().isoformat(),
        "last_download": "0000-00-00",
    }
    return json_result

def get_hash_and_sig(url, filename):
    site = getWebSite(url)
    tables = site.find_all('table', class_='tablebox ra_int_table')

    for table in tables:
        file_section = None
        for row in table.find_all('tr'):
            b_tag = row.find('b')
            if b_tag and filename in b_tag.text:
                file_section = row
                break

        if file_section:
            sha256 = None
            signature_url = None

            current_row = file_section.next_sibling
            while current_row:
                if current_row.name == 'tr':
                    label = current_row.find('td')
                    if label and label.text.strip() == 'SHA-256:':
                        sha256 = current_row.find_all('td')[1].text.strip().replace(' ', '')
                    elif label and label.text.strip() == 'Sig.:':
                        signature_link = current_row.find('a', href=True)
                        if signature_link:
                            signature_url = signature_link['href']
                        break
                current_row = current_row.next_sibling

            if sha256 and signature_url:
                return sha256, signature_url

    return None, None


def run():
    downloads = list()
    website = getWebSite(download_url)
    tables = website.table.table
    global app_version
    # print(tables)
    for a in tables.find_all('a', href=True):
        # print(a)
        tmp_platform = ''
        tmp_url_bin = ''
        tmp_url_asc = ''
        tmp_url_sha256 = ''
        if isBinaryURL(a, '.exe'):
            tmp_url_bin = findPlatformInURL('.exe', a['href'])
            app_version = tmp_url_bin.split('-')[1]
            link = get_direct_url(tmp_url_bin)

            filename = tmp_url_bin.split('/')[-2]
            sha256, asc = get_hash_and_sig(integrity_url, filename)


            downloads.append(
                {"app_platform": "win64", "url_bin": link, "sig_type": 'asc_file', "sig_res": base_url+asc, "hash_type": 'string',
                 "hash_res": sha256, "url_pub_key": pub_key_url})

    return toJSON(downloads)


if __name__ == "__main__":
    import sys

    print(run())
    # run(sys.argv[1])
