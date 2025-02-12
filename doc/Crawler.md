The Crawler component is responsible for crawling the download website extracting the software version, the download url and its architecture.
With these informations a JSON will be generated and added to a complete list of all software products.
The JSON list is something like an API for other componenten of Aid.

The following sequence diagram shows the process of Crawlers components:

![rendered UML-Sequence Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/berkholz/Aid/refs/heads/feature_headless/doc/diagrams/crawler_sequence.puml)

[diagram Source](https://raw.githubusercontent.com/berkholz/Aid/refs/heads/feature_headless/doc/diagrams/crawler_sequence.puml)