The Packager is responsible for making a signed package with all software downloads.


![squence diagram of component Packager](https://www.plantuml.com/plantuml/dpng/XLBDJiCm3BxtAInnsGwym0veGeWJ1n1FO5gtjPecbUsiszkJK5O5eNMdHl7tyzLVZcee5aTNLLCwSCqJUeDth0ViIE2XGHc-NAG_urTsf1Sr6gjgXJu-5VTmWBgdUW1kGRdpx3iOwA90PrQh2c2YhH874B8eFdqqEeFGBlXVhTAh97NaIT0eEwr6oTY7qlDcKCKJBS2PhGT7c1mduLC2TQGRVoYKNQTb3WqBrHRaScydOsXYkWJsox6WtjsCOyrxkMfK6mMCuKIWeRKP9Lc4sRk0ZOA5_v4tPEXCTJHQK-_Qw6lZu46Yt-ttMn64i87FZpTE_9TdQDCCsY3Nnd9PFMeF6iVR8hDaUkOk1Trdv1UtmWfcBXNjf-oK-aY-YQFx1W00)

´´´
@startuml

participant Packager #darkblue
participant Filesystem

Packager -> Filesystem : check if signing keys exist
Filesystem -> Packager : return result of exist check
Packager -> Packager : generate siging keys if no keys exist
Packager -> Filesystem : save keys with least privileges
Packager -> Filesystem : create package directory
Packager -> Filesystem : check modules in module directory
Filesystem -> Packager : return list of modules
Packager -> Filesystem : move software downloads to package directory
Packager -> Filesystem : execute modules (function run())
Packager -> Filesystem : read SQLite DB file for generating hash sum
Packager -> Filesystem : write file with hash sum
Packager -> Filesystem : sign hash sum file with private key

@enduml
´´´