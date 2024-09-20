# Aid (Automated internet downloader)

Tool written in python to download automated the actual version of specified software packages.

Siftware packages can be download by creating a module which generates a JSON answer in recommended format.

Aid has the following components:
- Crawler
- Database
- Downloader
- Packager
- Manager

## Crawler
The Crawler component crawls the websites an returns a JSON formatted answer with all package informations.

## Database
The Database component stores the information of the Crawler in a SQLite database.

## Downloader
THe Downloader component uses the SQLite database to retrieve the URLS that it downloads.

## Packager
The Packager component creates a signed package with all selected downloaded software downloads.

## Manager
This component manages all components. Here you can select the packages to download or select the software for package creation.

## Prequisites
THe following packes have to be installed on Ubuntu 22.04.5 LTS:
* python3-tk
* python-tk
* python3-tqdm
* python3-gnupg