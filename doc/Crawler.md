The Crawler component is responsible for crawling the download website extracting the software version, the download url and its architecture.
With these informations a JSON will be generated and added to a complete list of all software products.
The JSON list is something like an API for other componenten of Aid.

The following sequence diagram show the process of Crawlers components:

![UML-Sequence Diagram](https://www.plantuml.com/plantuml/dpng/dLFDRjim3BxhAJxab1ps0ZaC7RfXFsXNOElEXMBHiG2PD2XwRjz-LUt445Bai9j1yllX9_eccrSR--G6hnQRE7WsR1wi8yMjz8CmiMsgxgtwAP4wTv1dO7ClOKoKwvcv-FGvwZjbHnpm2dPLxpiRAPCvjmZWmqUiFDWZDvxHnaGPaT7B6CfdY4gDYRwW5KMMrYQlX20J9_41_UpFhLI5-AInXvADoaWn6wI5Jmd3YtLoac8n7EWOcICVCKNhyEHS4XaGZTGRGVwI5k3YQG5w3cXArJg2ZhpTeIVh93WiUnKZfxMnnzSlZwljYGuv6ZcS9zOyiB-Om_RRu_tTxanT3TEpgMzi3UVLRuvbGvKU1NWLjuhz-NMtOkgyoxRHChmsNJHgR5JA_qjR3COsDjwAoyxdRiapnoFxAzH7ulb9Vln--3a_ba_fxBAIp6_zAuOlRgIGEfphrOWFOHOjYon71vFghawdI1ogAx_utsh9zpYmRKTktk8vadqQXhIabRUxdRiX3cEV_W40)

```
@startuml
participant "Other Component"
participant Crawler #darkblue

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

Crawler -> "Other Component" : return JSON list of all modules (function getApplications())

@enduml
```
