# Aid (Automated internet downloader)

Tool written in python to download automated the actual version of specified software packages.

Software packages can be downloaded by creating a module which generates a JSON answer in recommended format. If you wnat to write a module by your self, see ![modules](doc/Modules.md).

Aid consists of some independent components, which are decribed in ![components](doc/Components.md).


## Prequisites
To run Aid you need some python libraries installed. 

### Ubuntu
THe following packes have to be installed on Ubuntu 22.04.5 LTS:
* python3-tk
* python-tk
* python3-tqdm
* python3-gnupg
* gnupg
* python3-validators

### Fedora
THe following packes have to be installed on Fedora 40:
* python3-tqdm
* python3-gnupg
* gnupg
* python3-validators