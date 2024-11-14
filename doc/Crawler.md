The Crawler component is responsible for crawling the download website extracting the software version, the download url and its architecture.
With these informations a JSON will be generated and added to a complete list of all software products.
The JSON list is something like an API for other componenten of Aid.

The following sequence diagram show the process of Crawlers components:

![UML-Sequence Diagram](https://www.plantuml.com/plantuml/png/dLFDRjH03BxFKtpggJtm0ZsWeeAWg2qIb7Crct4s8qtioEEGzkt9ACb6iq0Ft2Bx-_diSMwoURMnJsxmQh69WsV3nSE7kqVSIZy84zj5rRnLFoLIvmxoWXagOKoKQynIVFuOzIzbHnmmartLksCZPJBdLWEyUuzT1zV8ZMUqSJP3PFGoXl8Peb9ZegzeHP6bjSah8SZ4INn0l-HpkrGHtZokeMIZCbBC1cdXKyBmQfriLYo60nqZS-GZfcWTdfrB8WEYaNeZo2_IGbmphKJF0KsfMaVGaI-lqDCi71pMkKgGRMnSu_EdfptsH8SSZHnEY7qVC_OSXyilJm_tLoVf2amlfhwnVJbptXpBX2ez2l5Dtcxsy_lzpgdtNQQDbk6rwQ9HOwDI_b_P4Z2siV5MKdO-T-i-SpooVqFwIBmyoTSVtnwNn_8fdL9Mbddf_plm7pTIH1ssUWtn8Q3qbq7wHSIakglj58b3TUNdlzlkw2j-qLyx-LppPXOT-_GR)



Diagram source:
```
@startuml
participant "MAIN Component"
participant Crawler

box  "Modules"
participant Module_Dir
participant Module
end box

participant Internet

Crawler -> Module_Dir : scan files in moudles directory for software download modules
Module_Dir -> Crawler : return list of all python files not beginning with _

loop iterate over all moudle files and call the run() method
  Module -> Internet : GET download website
  Internet -> Module : download website (HTML)
  Module -> Module : extract software version from HTML
  Module -> Module : extract download URL from HTML for software and its architectures
  Module -> Module : extract download URL from HTML for verification hashes and signatures
  Module -> Module : generate JSON with all software download URLs with architectures
  Module -> Crawler : return JSON
  Crawler -> Crawler : add JSON from module to list of all modules
end

Crawler -> "MAIN Component" : return a list of all JSON returns of all modules
@enduml
```