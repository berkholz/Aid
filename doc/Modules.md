If you want to implement a [Crawler](Crawler) module it is very important to understand the basic structure of a crawler module.
Every crawler module MUST have a function "run". This function is called by the Crawler.

The basic structure of a crawler module looks like this:

```
01 import urllib.request            # import for catching the website
02 from bs4 import BeautifulSoup    # import for parsing the website via beautiful soup 4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
03 from datetime import date        # import for last_found in JSON export
04 import logging                   # import lib for LOGGING
05 import settings                  # import global settings
06
07 ################################### VARIABLES
08 LOGGER = logging.getLogger(__name__)
09 logging.basicConfig(level=settings.LogLevel)
10 # logging.basicConfig(level=logging.DEBUG)
11
12 download_url = ""
13 app_name = "example_app".lower()
14 full_name = "Example App"
15 default_download = 'win64'
16 app_version = "0"
17
18 ################################### FUNCTIONS
19 def getWebSite(url):
20     # creating request with custom user agent string
21     req = urllib.request.Request(
22             url,
23             data=None,
24             headers={
25                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
26             }
27         )
28     with urllib.request.urlopen(req) as f:
29         return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
30
31 def to_json(d):
32     """
33     Export the JSON.
34
35     @param d: Dictionary with all software informations for the downloads.
36     """
37     json_result = {
38         "app_name": app_name,
39         "full_name": full_name,
40         "default_download": default_download,
41        "app_version": app_version,
42         "downloads": d,
43         "last_found": date.today().isoformat(),
44         "last_download": "0000-00-00",
45     }
46     return json_result
47
48 def run():
49    downloads = list()
50    website = getWebSite(download_url)
51
52     # here you add your code to parse the website and extract links and information
54
55     app = {"app_platform": default_download, "url_bin": download_url, "sig_type": None, "sig_res": None,   "hash_type": None, "hash_res": None, "url_pub_key": None}
56     downloads.append(app)
57
58     return to_json(downloads)
59
60 ################################### FUNCTIONS
61 if __name__ == "__main__":
62     print(run())

```


For getting a better understanding, every block is described below:

**Line 01-05:** Here we import all python libraries that we use.

<p>
Open the details to see the corresponding lines:
<details>

```
import urllib.request            # import for catching the website
from bs4 import BeautifulSoup    # import for parsing the website via beautiful soup 4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
from datetime import date        # import for last_found in JSON export
import logging                   # import lib for LOGGING
import settings                  # import global settings
```

</details>
</p>

---

**Line 08:** To print out some debugging messages, we define a logger object


<p>
Open the details to see the corresponding lines:
<details>

```
LOGGER = logging.getLogger(__name__)
```
</details>
</p>

---

**Line 09-10:** In the global settings file is the default logging level defined. When the module is executed outside of the main.py the global settings could not be imported, application throws a not found exception. That's the reason why the line 05 (_import settings_) and the line 09 (_logging.basicConfig(level=settings.LogLevel)_) are commented out, when executed outside of main.py.

Default is the loading of the global settings like in the template.


<p>
Open the details to see the corresponding lines:
<details>

```
logging.basicConfig(level=settings.LogLevel)
# logging.basicConfig(level=logging.DEBUG)
```
</details>
</p>

---

**Line 12-16:** The application must have a identification name (app_name). This name is part of the primary key in the database and should not contain whitespaces. The full name can be used to fully describe the application. The _default_download_ specifies the default architecture that the downloader should download. This is only relevant if the application has more than one architecture.

<p>
Open the details to see the corresponding lines:
<details>

```
download_url = ""
app_name = "example_app".lower()
full_name = "Example App"
default_download = 'win64'
app_version = "0"
```
</details>
</p>

---

**Line 19-29:** THe function _getWebSite()_ opens a http request, creates an beautiful soup object and returns it. The user-agent is required, because some websites don't allow http requests without an valid user-agent.

<p>
Open the details to see the corresponding lines:
<details>

```
def getWebSite(url):
    # creating request with custom user agent string
    req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
```
</details>
</p>

---


**Line 31-46:** The function _to_json(d):_ creates the required JSON for the Crawler.

<p>
Open the details to see the corresponding lines:
<details>

```
def to_json(d):
    """
    Export the JSON.
    @param d: Dictionary with all software informations for the downloads.
    """
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
```
</details>
</p>


The JSON is in the following form:
```
{
    'app_platform': <PLATFORM>,
    'url_bin': <URL>,
    'sig_type': <SIG_TYPE>,
    'sig_res': <SIG_URL>,
    'hash_type': <HASH_TYPE>,
    'hash_res': <HASH_URL>,
    'url_pub_key': <PUBKEY_URL>
}
```

\<PLATFORM> := This field is the architecture of the software. Actually there are the following platforms:
* android
* linux
* linux-x86_64
* mac
* mac_arm
* win32
* win64

<URL> := The URL of the download of the application.

<SIG_TYPE> := Type of the signature. The following signature types exists:
* None
* asc_file
* sig_file

<SIG_URL> := The URL of the signature file.

<HASH_TYPE> := Type of the hash of the download file. The following hash types exists:
* sha1_string =
* sha256_multi =
* sha256_single =
* string =
* manual =


<HASH_URL> := The URL of the hash file. Only present if HASH_TYPE is sha256_multi or sha256_single.

<PUBKEY_URL> := The URL of the public key of the CA which signed the signature file.




---

**Line 48-58:**


<p>
Open the details to see the corresponding lines:
<details>

```
48 def run():
49    downloads = list()
50    website = getWebSite(download_url)
51
52     # here you add your code to parse the website and extract links and information
54
55     app = {"app_platform": default_download, "url_bin": download_url, "sig_type": None, "sig_res": None,   "hash_type": None, "hash_res": None, "url_pub_key": None}
56     downloads.append(app)
57
58     return to_json(downloads)

```
</details>
</p>

---

**Line 61-62:**

<p>
Open the details to see the corresponding lines:
<details>

```
61 if __name__ == "__main__":
62     print(run())

```
</details>
</p>

---
