The Automated internet downloader(Aid) consists of some independent components, each has its own aspect of Aid.
These components are:
- [Crawler](Crawler.md)
- [Database](Database.md)
- [Downloader](Downloader.md)
- [Verifier](Verifier.md)
- [Prebuild](PreBuild.md)
- [Packager](Packager.md)
- [Unpackager](Unpacker.md)
- [Manager](Manager.md)


The following diagram shows the states Aid went through. Each involved component is described shortly:

![Activity Diagram](https://www.plantuml.com/plantuml/png/VLDDJzmm4BtxLpnnHli3w0NKNgY0qb9whGPxaepMiIDxmWA_lXebMDaLzEZvc7dlpVDbLIewZz5TV2rqY5o-k9ILKQGVr05h55gavr91CMBCOOvSmI-U9uK3Eh6tpL99FGwY0yx-dkqSSBiM5zQv991LfK0buFl3Zpi4yIevKNc5mz9eAoHrkOnagGfwohD21mPDKnHF5hRPlmTk09Vv5OGeLP6xRR7DRfk4ApJRFDnUNTzXAhalD6AYekSu3E87gw-Q2rShswA190lXuUUDA2EGqXDLtZbE0QQSk_YM3obc2atBo9skQ5lE05Cu7T_8EfWCMmeLadoSW-aRrYbu_7LJLo4IH5kYdghL69iGt4dYq8hHvHYuR2dyuIATd9XXOV2UWjAU_uVVCWFL0PG2glJ9aEVkapjMne4BOwuS3EipsvhNTRvoNqJD8h1fDEl0ISLRR1dPsEm0R9ZS5xudlwUUZuznlPnnAenfoPinbV6QPtXA66dFg7baM-hdgdcKjusMcvKSZgG-jmxUzJi49g_oJ6hKhMCauv8eUKRbyYoU7Op1cDyaHa8dXRlyiZlYi1Buw1fBgbt3F1DoEdo6oXScjRe4dyUfS3MvxVTkt6L374wQM-ToqpgFIzkgliFfZx13MUfqaSKTO8POx5CP5g_Bvr-EOfenzcpNNQrq9KTyTbk17jDwmmz-NCjj7Bji3rje3dYJgI4yPNE-6fAhmm9w0tT-Yk9Nj1zXVRVjdDf2Wy5ju-RhkKjEOHxZFm00)

---

Diagram source:
<details>

```
@startuml
:Crawler;
note right
  Crawler trigers all modules except
  files starting with "_".
  Modules return a standard JSON dictionary
  with all informations about the application.
  The Crawler returns a list of application
  dictionaries to the MAIN program part, which
  stores the information in the SQLite database.
end note
:Downloader;
note left
  The Downloader reads the informations about
  all applications including download URLs.
  Then it downloads the applications to the
  defined download folder.
end note
:Verifier;
note right
  The Verifier takes the informations about
  the hash and signing of the application.
  These were used to verifiy the integrity
  and authenticity of the download.
end note
:PrePackage;
note left
  In the pre package state you can make some
  customizations to the downloaded applications,
  e.g. deactivating the maintenance service
  of mozilla firefox.
end note
:Packager;
note right
  The Packager takes all donwloaded applications,
  creates an compressed file including all
  applications, creates a hash sum file of the
  SQLite database and the compressed file and
  signes these files with the private key of
  the Aid application.
end note
:Unpackager;
note left
  The Unpackager takes the signed compressed
  zip file and SQLite database, verifies
  these with the public key of the Aid application
  and uncompresses the zip file.
end note

@enduml
```

</details>