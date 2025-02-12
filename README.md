# Aid (Automated internet downloader)

Aid is a tool written in python to download the recent version of specific software packages/products automatically.
Software packages can be downloaded by creating a module for the Crawler component. This module  generates a JSON answer which is stored in the SQLite database. The Downloader uses it to download the software packages. Some basic software packages are actually implemented. To see which are implemented, look in folder [Crawler/modules](Crawler/modules).

If you want to write a module to extend the software products portfolio, see [modules](doc/Modules.md).

To get more informations about the different components of Aid, take a look at [components](doc/Components.md).


## Run Aid
### Windows
#### Install prerequisites
To run Aid in Windows you need some programs installed:
* [Python 3](https://www.python.org/downloads/)
* [Gpg4win](https://gpg4win.org/download.html)
* Python IDE, e.g. [PyCharm Community Edition](https://www.jetbrains.com/de-de/pycharm/)
* Installing Python modules:
  - open administrative cmd and type in the following commands (python must be in your PATH variable): 
    ``` 
    pip install tqdm gnupg validators tk requests bs4
    ```

#### Checkout git repository
There are currently two branches:
* master
* feature_headless

The *master branch* is actually on an older state, but with a GUI to activate specific downloads. Some Crawler modules are outdated, but working properly. Just checkout this branch and try if it fits to your needs.

The *feature_headless* is the actual development Branch, that lets Aid run headless without a GUI. In a later release the control interface will be in a seperate component.

To checkout the *master* branch, go in PyCharm to **File -> Project from version Control...**, select in the left pane **Repository URL**, choose the directory to save the repository in and type in the following URL:  
:
```
https://github.com/berkholz/Aid.git
```

To checkout the *feature_headless* branch, use in PyCharm on the project Aid the **Context menu -> GIT -> Branches...** and choose the following branch: 
```
feature_headless
```
Now you should be ready to go and can RUN the project.

### Linux 
#### Install prequisites
To run Aid on Linux you need some python libraries installed:
| Ubuntu 22.04.5 LTS | Fedora 40 | 
| :--- | :--- |
|* python3-tk<br>* python-tk<br>* python3-tqdm<br>* python3-gnupg<br>* gnupg<br>* python3-validators |* python3-tqdm<br>* python3-gnupg<br>* gnupg<br>* python3-validators |

#### Checkout git repository
There are currently two branches:
* master
* feature_headless

The *master branch* is actually on an older state, but with a GUI to activate specific downloads. Some Crawler modules are outdated, but working properly. Just checkout this branch and try if it fits to your needs.

The *feature_headless* is the actual development Branch, that lets Aid run headless without a GUI. In a later release the control interface will be in a seperate component.

To checkout the *master* branch, use the following command in your favorite folder in terminal:
```
git clone https://github.com/berkholz/Aid.git
```

To checkout the *feature_headless* branch, use the following command in terminal:
```
git clone -b feature_headless https://github.com/berkholz/Aid.git
```


#### Open project in your IDE, e.g. VS Code
After installing the needed packages, start your favorit IDE for python, for example [Visual Studio Code](https://code.visualstudio.com/)]. Here we use VS Code.

In VS Code, open the folder with the git repository.

Open the file main.py.

Then run the python program via the menu *Run -> Run Without Debugging*.

When you run the python pogram all the latest found software packages are activated for download. If you don't want that behaviour, then you have to comment out the following line:
```
activate_download_for_latest_found()
```

For a activation of specific downloads you can use the [DB Browser for SQLite](https://sqlitebrowser.org/), open the aid.db and change the value of column *download* to 1.
