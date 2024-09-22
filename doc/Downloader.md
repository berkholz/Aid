The Downloader component is responsible for downloading the software packages.



![sequence diagram of component Downloader](https://www.plantuml.com/plantuml/dpng/dPDFhXen3CRtEOMbhdk1BgfN5LfLUekgvHt09Cx3mfCWsm7HqtSOgZ0WWL2NaD_tPxxCl9YZUXiaX1sgS-GT5eV5-lfdFHIfc4ZXGqBThgNH5V2ZE6aXl_hp6mlPqPo646OE7p_FJk0JS65dH-4_1EaV1ecLebSztYWNwr7nU_cw_Bg2jr-l1hage0XOpNv0fJ0I9wwhHbx9cvRETxR7MGXIwmxOIT49wfucrqaIOEvswnqt5BV06J8B0Tj9feJfsCqftJhqkKRzz-MgavTYMUjm2W_GsNjFrJLSp544dMk17SOjljEeVx2yuVwomOZUdxgfJCjjq3PWRHZX-plVmb3pfMMimwuMAlwusfwKysL3EB1lkk5vdeIEQpHwghZnUq5lIayrx_H_bEpQPrg-_LnyMIqxD8KBcizUdjCX0MT0aNCYn_CTMukHpCW2bVJm4rF2DBVCB7Hzd-5-kRxw7gLDicur6OMNCRuDyXS0)

´´´
@startuml

participant Db
participant Downloader #darkblue
participant Internet
participant Filesystem

Downloader -> Filesystem : inititalize download directory
Downloader -> Db : SELECT URLs for all software
Db -> Downloader : return URLs for software downloads

loop iterate over all URLs
  Downloader -> Downloader : check if file is allready downloaded
  Downloader -> Internet : GET download software from URL
  Internet -> Downloader : return software installation package
  Downloader -> Filesystem : save download
  Downloader -> Db : SELECT url for hash sum
  Db -> Downloader : return url for hash sum of software component
  Downloader -> Filesystem : verify download with hash sum from database
  Downloader -> Db : SELECT url for signature
  Db -> Downloader : return url for signature
  Downloader -> Filesystem : verify download with signature from database
  Downloader -> Db : UPDATE database for last downloaded date if all verification successes
end

Downloader -> Filesystem : read downloaded file for hash sum

Downloader -> Db : UPDATE hash sum value for download file
@enduml
´´´