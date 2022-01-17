# rolegal
Romanian Legal Data Processing

This repository contains two datasets:

### 1. Historical Public Procurement Legislation (PPL)

This dataset consist in an archive that containes raw scraped documents covering PPL. And a .csv file containing the metadata for each file in the archive: published year, month, header, source URL, type (if primary or secondary).

Files:

- historical_procurement_legislation.zip
- historical_procurement_legislation.csv


### 2. A subset of annotated legislative bills 

This dataset is extracted from the public pages of the Parliament (Senate and Chamber of Deputies). The files have been downloaded in PDF format the tesseract-ocr has been applied to convert them into Romanian. The archive contains a list of directories named after the PLX id of each legislative proposal from the Chamber of Deputies. Each directory contains a list of txt files encompassing the entire folder of a bill (written advices from different comissions, various forms that were passed. etc.)
For each proposal each directory, there are two more directories called "impact" or "nonrelevant". The "impact" directory contains the articles, paragraphs and fragments that have been annotated as impacting public procurement legislation. The "nonrelevant" contains the remaining content of the bill.


Files:

- cdep_senat_txt_annotated.zip
- impacting_laws.csv


