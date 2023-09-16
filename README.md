# A Spacy Package for Legal Document Processing & Other Resources

[![Build](https://github.com/senisioi/rolegal/actions/workflows/build.yml/badge.svg)](https://github.com/senisioi/rolegal/actions/workflows/build.yml)

This is the source code to build a spacy package with floret embeddings trained on legal documents and with legal NER capabilities.
The directory `ro_legal_fl` contains the full spacy `project.yml` and config that can be used to build `ro_legal_fl` spacy package. 


## Accuracy

| Type | Score |
|:---:|:---:|
| `TOK` | 99.84 |
| `TAG` | 96.27 |
| `POS` | 97.12 |
| `MORPH` | 96.42 |
| `LEMMA` | 95.73 |
| `UAS` | 89.15 |
| `LAS` | 82.46 |
| `SENT_P` | 94.94 |
| `SENT_R` | 95.20 |
| `SENT_F` | 95.07
| `ENTS_F` | 78.35 |
| `ENTS_P` | 79.51 |
| `ENTS_R` | 77.23 |

## NER per type

|             |   P   |   R   |   F   |
|:-----------:|:-----:|:-----:|:-----:|
|    MONEY    | 88.52 | 72.32 | 79.61 |
|   DATETIME  | 85.31 | 84.58 | 84.94 |
|    PERSON   | 76.71 | 72.40 | 74.49 |
|   QUANTITY  | 89.27 | 84.55 | 86.85 |
|   NUMERIC   | 86.53 | 81.72 | 84.06 |
|    LEGAL    | 71.24 | 83.85 | 77.03 |
|     ORG     | 69.24 | 71.96 | 70.58 |
|   ORDINAL   | 89.14 | 89.14 | 89.14 |
|    PERIOD   | 84.39 | 74.11 | 78.92 |
| NAT_REL_POL | 85.09 | 77.46 | 81.10 |
|     GPE     | 81.95 | 82.75 | 82.35 |
| WORK_OF_ART | 39.15 | 28.14 | 32.74 |
|     LOC     | 55.28 | 52.35 | 53.78 |
|    EVENT    | 54.89 | 43.20 | 48.34 |
|   LANGUAGE  | 80.28 | 78.08 | 79.17 |
|   FACILITY  | 60.14 | 47.98 | 53.38 |



The commands belwo assume you are in the `ro_legal_fl` directory:

```bash
cd ro_legal_fl
```



## Install Requirements and Compile floret
```bash
pip install -r requirements.txt


git clone https://github.com/explosion/floret
cd floret
make

```

## Building floret Embedding for Romanian Legal Documents
The training uses continuous bag of words  with subwords ranging between 4 and 5 characters, 2 hashes per entry, and a compact table of 100K entries. The configuration for training embeddings is defined in project.yml. Before proceeding with the training, floret must be compiled and installed on the machine where training will take place.

To train embeddings from scratch, one has to be in the directory of the project, have floret and spacy and then run the following command:
```bash
python -m spacy project run either-train-embeddings
```
Which will run several shell scripts defined in `project.yml` to download the corpus and start floret training. If the user does not want to train embeddings from scratch, but use the ones that we release within a spaCy package, then they may execute the following command instead: `python -m spacy project run either-download-embeddings`.

## Downloading pre-trained floret Embeddigns for Romanian
We provide pre-trained embeddings that can be used with the pipeline. The embeddings are downloaded with the assets:
```bash
python -m spacy project assets
python -m spacy project run either-download-embeddings
```

### Example of using floret nearest-neighbors
An example of using floret vectors to identify similar legal terms can be visible in the following box. 

```bash
./floret/floret nn ./vectors/marcell_clean.dim280.minCount50.n4-5.neg10.modeFloret.hashCount2.bucket100000/vectors.bin 
```

| Query word?                 | Similar Word          | Similarity Score |
|-----------------------------|-----------------------|------------------|
| sectoriale                  |                      |         |
|                            |sectorial/sectoriale | 0.91564|
|                            |sectoriale/intersectoriale | 0.915279|
|                            |transsectoriale | 0.901447|
|                            |subsectoriale | 0.898561|
|                            |naționale/sectoriale | 0.881749|
|                            |multisectoriale | 0.869202|
|                            |publice/sectoriale | 0.863173|
|                            |publică/sectoriale | 0.844522|
|                            |intersectoriale | 0.84431|
|                            |intrasectoriale/intersectoriale | 0.841589|



The results show a robust response where several versions of the word appear highly similar, including terms containing the slash sign after tokenization.


## Building a Complete spaCy Package for Legal Documents

To build the spaCy package, in the same directory run the following two commands:
```bash
# to download the data and depdendencies
python -m spacy project assets
# to train-evaluate a model
python -m spacy project run all
# to package it
python -m spacy project run package
```

The first command will download the necessary assets:

- Romanian universal dependency treebank annotations  to train parsers, part of speech taggers, and lemmatizers; this dataset is essential for training a model that can identify different morphological forms of the same word (e.g., achizitii, achizitie, achizitia etc.) which depend strongly on the part of speech the word has in the particular context; combining this data with the embeddings trained previously on MARCELL corpus will result in a more robust model for legal document processing
- LegalNERo corpus  released by the Research Institute for Artificial Intelligence "Mihai Draganescu" of the Romanian Academy that contains Named Entity annotations for different entity types: Legal, Persons, Locations, Organizations, and Time entities; useful to increase the model’s robustness to legal documents and to be able to identify mentions to legal acts as entities.
- RoNEC corpus  or Romanian named entities; useful to identify Persons, Organizations and several other entities in documents.
 
The second command will run the training pipeline where each action is defined in the project yaml file as shell scripts. The steps of the pipeline are:

1.	initialize the downloaded or trained floret vectors in the new spaCy model
2.	convert treebank dataset to spaCy binary dataset for training 
3.	initialize prediction labels using the configuration defined in configs/ro_legal.cfg
4.	train tok2vec, tagger, morphologizer, parser, lemmatizer, and senter components using the treebank data
5.	evaluate the model on the test set
6.	convert LegalNERo to conllup format
7.	convert RoNEC to conllup format
8.	combine the two named entity recognition corpora into a single file
9.	convert the combined file into spacy binary format
10.	prediction entity labels using the configuration defined in configs/ro_legal.cfg
11.	train named entity recognizer using the data created
12.	evaluate the model on the test set
13.	package everything into a wheel

This will take a lot of time, so please be patient. At the end, in the packages directory a wheel will be created named ro_legal_fl that can be installed using pip as an individual package.



## Repository Resources

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


