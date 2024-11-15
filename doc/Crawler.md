> [!NOTE]
> This module is implemented and working.

The Crawler component is responsible for crawling the download website extracting the software version, the download url and its architecture.
With these informations a JSON will be generated and added to a complete list of all software products.
The JSON list is something like an API for other componenten of Aid.

The following sequence diagram shows the process of Crawlers components:

![UML-Sequence Diagram](https://www.plantuml.com/plantuml/png/dLFFRjOm3B_dAQoTjWCli0CQ6WY6jY71E4zPudwrbDgLuz3jxMdKV0hz1ZjmQXN__lmSErVPl5gPaflNBmMQFHkStNsukOThcMPXP3lR5Q_LBmdLkITvXXKgiIJCUyns-FYHz2_73Zd2IdQxsWqRAgCvrmpWtVkket09ENY6WLOp88P9Igo_aHI3YRx080fP1bky8aHPE8cFC6tvN9Ugmfj7LLMqeWo9ie4Cu5E2-SL6ELgn63pXWPY93x2GZV3eN1APWGpL6uByGgt4bgaHFKS8zTH612ryVW4JsYZH0RngyHBm6KEnbLmu60at2d7hm463LjBnijRydpyzz6ONVCfa5Nj4T8iLUug3yoyFTxSNNRg3Qo1J7wnVwTfbhi46bGagyKrUD_lv_RPpzbEgTqIMmMiOoJ1OKSp_Ari3qa31Mqqv-ZosAMGwi7z3-e2y3VBhZs_tsuXzIZtbdvPvg_yxyAlDggBxaNU8Zt4phOsqGOF9RXkF2umSTs_Zz95sHx_ZL_rMoQUQLyYnJEat)


---
Diagram source:
<details>

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
  Crawler -> Module: execute function run() in module
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

</details>