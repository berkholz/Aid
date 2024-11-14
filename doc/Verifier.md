The Verifier component is responsible for


The following sequence diagram show the process of Crawlers components:

![UML-Sequence Diagram](https://www.plantuml.com/plantuml/png/XLBBRjim4BppAwRe9J7I7n3W8aNj5aKV3HgxLsCjBMF25AdouS1_NmbqH4i9f9FfqSvZbhptWLo8jHPD-wjArP09-4dA382_x9HKxF2-8dVSwyY3pzzCO6Su3C0lIhC_-y2r49qWFdpiTGfevGEiXBSoF9DZt4IdTtjbxa1DipDKSpgTs7bbM_X0_h0BvuOlHyV-3buz9Qmx9QZJQU9-T-JphH1zyYjt5FXyuF889RCgbCSlQrW8qk4AVhTCC80hhRuo2dnTRx1OT0puM4CgpOk50FBCqFjXky5WUgoTDuS2ZtJYuJY2XRObQSYyujbyxNvCY8ul-I2j6yhE9Exur0lqzFIlrPWjaHKcMgGU4tUMRsRICCrcHojVbys4aT4Vzb6drzaBb9tWH3WbNsZAu_TtbDO4PIA3jMVyY-Iu0nYLVJRQKfLYp7R8iQqSSONejFD2i4nFTLBqYGqx2ZoXExcQzUFsn-RcXNmxzbhjKM3xiFgqMLy7GqqcafwTTkonV6t2fX9YTGdvHYd7LFKbEDKOFF1C7llcFPn8nyGQhkE-TO-r_Wy0)



Diagram source:
```
@startuml
participant Main
participant Verifier #darkblue
participant Internet
participant Filesystem

Main -> Verifier: list of software (url_bin, app_name, app_version, hash_type, hash_res, sig_type, sig_res, url_pub_key)

Verifier -> Verifier : Check if hash_type is None

alt hash_type != None
   Verifier -> Internet : GET **hash sum file**
   Internet -> Verifier : PUT hash sum file
   Verifier -> Filesystem : Save hash sum file to local filesystem

   Verifier -> Internet : GET **signture file** for hash sum file
   Internet -> Verifier : PUT signature file for hash file sum
   Verifier -> Filesystem : Save signature file to local filesystem



   Verifier -> Verifier : Check hash_type
   Verifier -> Filesystem : Check signature of hash sum file
   Filesystem -> Verifier : Result of signature check
   Verifier -> Verifier : if Result is OK continue else quarentine download file
   Verifier -> Filesystem : Check hash sum of download file


else hash_type == None
   Verifier -> Filesystem : generate hash sum of download file
   Filesystem -> Verifier : RESULT(hash sum)
   Verifier -> Db : UPDATE hash_type = manual
   Verifier -> Db : UPDATE hash_res = RESULT(hash sum)
end

Downloader -> Filesystem : read downloaded file for hash sum
Downloader -> Db : UPDATE hash sum value for download file
@enduml
```