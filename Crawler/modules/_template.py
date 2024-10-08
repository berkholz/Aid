import urllib.request
from bs4 import BeautifulSoup
import urllib
from datetime import date

download_url = 'https://www.url2download.com/downloads.html'
app_name = "example_app".lower()
full_name = "Example App"
default_download = 'win64'

base_url = download_url.split('/')[0] + download_url.split('/')[1] + download_url.split('/')[2]
app_version = 0


def findPlatformInURL(platform, url):
    if url.find(platform) > 0 and url.find('.asc') <1 and url.find('sha256') <1:
        return url

def isBinaryURL(ref, platform_string):
    return ref['href'].find(platform_string) > 0 and ref['href'].find('.asc') <1 and ref['href'].find('sha256') <1

def getWebSite():
    # creating request with custom user agent string
    req = urllib.request.Request(
            download_url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')

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

def run():
    downloads = list()
    #website = getWebSite()
    # tables = website.table
    # print(tables)
    # for a in tables.find_all('a', href=True):
    #     tmp_platform = ''
    #     tmp_url_bin = ''
    #     tmp_url_asc = ''
    #     tmp_url_sha256 = ''
    #     if isBinaryURL(a, 'win64'):
    #         tmp_url_bin = base_url + findPlatformInURL('win64', a['href'])
    #         app_version = tmp_url_bin.split('-')[1]
    #         downloads.append({"platform": "win64", "url_bin": tmp_url_bin, "url_asc": tmp_url_bin + ".asc", "url_sha256": tmp_url_bin + ".sha256"})
    #     elif isBinaryURL(a, 'android'):
    #         tmp_url_bin = base_url + findPlatformInURL('android', a['href'])
    #         app_version = tmp_url_bin.split('-')[1]
    #         downloads.append({"platform": "android", "url_bin": tmp_url_bin, "url_asc": tmp_url_bin + ".asc", "url_sha256": tmp_url_bin + ".sha256"})
    #     elif isBinaryURL(a, 'tar.gz'):
    #         # we have to find tar.gz, because it is a generic linux tar.gz package
    #         tmp_url_bin = base_url + findPlatformInURL('tar.gz', a['href'])
    #         downloads.append({"platform": "linux", "url_bin": tmp_url_bin, "url_asc": tmp_url_bin + ".asc", "url_sha256": tmp_url_bin + ".sha256"})
    #         #print(url_base + a['href'])
    return toJSON(downloads)

if __name__ == "__main__":
    import sys
    print(run())
    #run(sys.argv[1])
