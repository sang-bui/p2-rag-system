# About the own corpus

This corpus is 345 research papers on drought indices (the Palmer Drought Severity Index and its self-calibrating version, the Standardized Precipitation Index, and the Standardized Precipitation Evapotranspiration Index). Each document is one paper's title and abstract, with a header that gives its authors, journal, year, DOI and license.

## Where it came from

The candidates came from OpenAlex (https://openalex.org) searches of titles and abstracts, and `scripts/fetch_drought_corpus.py` is the exact procedure. A paper was kept only if Crossref, the publisher's own metadata record, lists a Creative Commons Attribution license (CC BY, or CC BY-SA) for it, with no NonCommercial or NoDerivatives terms. OpenAlex's own license label was not trusted by itself, because in a sample it was wrong for 2 of 8 papers.

## Licenses and attribution

- 299 papers are under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/) and 46 under CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/). `manifest.tsv` gives each paper's license, its DOI as the source, and the license URL Crossref lists.
- Each paper's authors, title, journal, year, DOI and license are at the top of its own file, which is the attribution the licenses ask for.
- Copyright in each abstract stays with its authors or publisher. These documents are shared here under the paper's own license, and using them in this project does not mean the authors or publishers endorse it.

## Changes made

The abstract text was rebuilt from OpenAlex's word index of the abstract, so the original formatting (paragraphs, italics, sub- and superscripts) is gone, and a citation header was added to each file. Nothing else was edited.

## Papers that were left out

Three IEEE papers were removed after the license tool flagged the publisher name in their header, and one Springer paper was removed because Crossref lists its CC BY license only for text and data mining and the publisher's page could not be read to confirm the license.
