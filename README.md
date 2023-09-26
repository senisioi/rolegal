# A Spacy Package for Romanian Legal Document Processing & Other Resources

[![Build](https://github.com/senisioi/rolegal/actions/workflows/build.yml/badge.svg)](https://github.com/senisioi/rolegal/actions/workflows/build.yml) [![PyPI version](https://badge.fury.io/py/ro-legal-fl.svg)](https://badge.fury.io/py/ro-legal-fl)



### Contents
- [Usage](#usage)
- [Training Data](#data)
- [Model Evaluation](#eval)
- [Building a Package from Scratch](#build)
- [Other Resources](#resources)


<img align="left" width="250" height="250" src="https://github.com/senisioi/rolegal/blob/main/img/paper.jpeg?raw=true">

This is a spacy language model for **noisy Romanian legal documents** with floret n-gram embeddings and `LEGAL` entity recognition.
The embeddings are trained using [MARCELL Romanian legislative corpus](https://marcell-project.eu/deliverables.html) consisting in 160K documents available at https://legislatie.just.ro and released by the Research Institute for Artificial Intelligence of the Romanian Academy. We preprocessed the corpus, removed short sentences, standardized diacritics, tokenized words using an empty spaCy model for Romanian, and dumped every document into a single large file publicly available for download [available here]( https://github.com/scrapperorg/nlp-resources/releases/download/legal_corpus_v1/MARCELL_Corpus_cln_tok.tar.gz).


<br>
<br>
<br>

<a name="usage"></a> 
## Usage

To use the spacy language model right away, install the released version:
```bash
pip install ro-legal-fl
```

Example:
```python
import spacy
nlp = spacy.load("ro_legal_fl")

doc = nlp("Titlul III din LEGEA nr. 255 din 19 iulie 2013, publicată în MONITORUL OFICIAL")

# legal entity identification
for entity in doc.ents:
    print('entity: ', entity, '; entity type: ', entity.label_)
# entity:  III ; entity type:  NUMERIC
# entity:  LEGEA nr. 255 din 19 iulie 2013 ; entity type:  LEGAL
# entity:  MONITORUL OFICIAL ; entity type:  ORG

# floret n-gram embeddings robust to typos
print(nlp('achizit1e public@').similarity(nlp('achiziții publice')))
# 0.7393895566928835
print(nlp('achizitii publice').similarity(nlp('achiziții publice')))
# 0.8996480808279399
```



<a name="data"></a> 
## Training Data

The following data is used for training:
1. [Romanian universal dependency treebank annotations](https://github.com/UniversalDependencies) to train parsers, part of speech taggers, and lemmatizers; this dataset is essential for training a model that can identify different morphological forms of the same word (e.g., achizitii, achizitie, achizitia etc.) which depend strongly on the part of speech the word has in the particular context; combining this data with the embeddings trained previously on MARCELL corpus will result in a more robust model for legal document processing
2. [LegalNERo corpus](https://zenodo.org/record/7025333/) released by the Research Institute for Artificial Intelligence "Mihai Draganescu" of the Romanian Academy that contains Named Entity annotations for different entity types: Legal, Persons, Locations, Organizations, and Time entities; useful to increase the model’s robustness to legal documents and to be able to identify mentions to legal acts as entities.
3. [RoNEC corpus]( https://github.com/dumitrescustefan/ronec) or Romanian Named Entity corpus; useful to identify Persons, Organizations and several other entities in documents. Currently, at version 2.0, holds 12330 sentences with over 0.5M tokens, annotated with 15 classes, to a total of 80.283 distinctly annotated entities.


| Feature | Description |
| --- | --- |
| **Name** | `ro_legal_fl` |
| **Version** | `3.6.1` - fixed with spacy version|
| **spaCy** | `>=3.6.1,<3.7.0` |
| **Default Pipeline** | `tok2vec`, `tagger`, `morphologizer`, `parser`, `lemmatizer`, `attribute_ruler`, `ner` |
| **Components** | `tok2vec`, `tagger`, `morphologizer`, `parser`, `lemmatizer`, `attribute_ruler`, `ner` |
| **Vectors** | -1 keys, 100000 unique vectors (280 dimensions) |
| **Sources** | MARCELL legislative corpus, LegalNeRo, RoNEC |
| **License** | CC4R https://constantvzw.org/wefts/cc4r.en.html |
| **Author** | [Sergiu Nisioi](sergiu.nisioi@unibuc.ro) |



<a name="eval"></a> 
## Model Evaluation
The evaluation of the legal spacy model is not directly comparable with other models for Romanian because we used a different training set, a different domain, and a completely different test set. We copy in the table below the values of the language model released by spaCy on generic Romanian language called ro_core_news_lg1 only to present a rough comparison with the evaluation scores of our model on the legal domain:

|           Metric          |           Description                                                   |             ro-core-news-lg         |              ro-legal-fl          |
|-------------|--------------------------------------------------------|----------------|-----------|
|           TOKEN_ACC        |              Tokenization            accuracy                                        |           1.00                 |              1.00            |
|           TAG_ACC            |            Part-of-speech          tags (fine grained tags, Token.tag)            |            0.97                 |              0.96            |
|           SENTS_P            |            Sentence            segmentation (precision)                            |           0.97                 |              0.95            |
|           SENTS_R            |            Sentence            segmentation (recall)                              |            0.97                 |              0.96            |
|           SENTS_F            |            Sentence            segmentation (F-score)                            |             0.97                 |              0.96            |
|           DEP_UAS            |            Unlabeled           dependencies                                       |            0.89                 |              0.89            |
|           DEP_LAS            |            Labeled             dependencies                                         |              0.84                 |              0.83            |
|           LEMMA_ACC        |              Lemmatization                                               |           0.96                 |              0.96            |
|           POS_ACC            |            Part-of-speech          tags (coarse grained tags, Token.pos)        |              0.94                 |              0.97            |
|           MORPH_ACC        |              Morphological           analysis                                       |            0.95                 |              0.96            |


NER scores are reported in the following table:

|               Metric           |                  Description                                   |                 Ro-Core-News             |                      RoLegal              |
|----------|------------------------------------|----------------|---------------|
|               ENTS_P           |                        Named                 entities (precision)             |                  0.75                     |                  0.79                    |
|               ENTS_R           |                   Named              entities (recall)                    |                  0.77                     |                  0.76                    |
|               ENTS_F           |                      Named               entities (F-score)               |                  0.76                     |                  0.77                    |


### NER per type

Below are the evaluation metrics per entity type. The results are consistent with [exiting published data on legal entity detection](https://aclanthology.org/2021.nllp-1.2.pdf)

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





<a name="build"></a> 
## Building a spacy Package from Scratch

The commands below assume you are in the `ro_legal_fl` directory:

```bash
cd ro_legal_fl
```


### Install Requirements and Compile floret
```bash
pip install -r requirements.txt


git clone https://github.com/explosion/floret
cd floret
make

```

### Building floret Embedding for Romanian Legal Documents
The training uses continuous bag of words  with subwords ranging between 4 and 5 characters, 2 hashes per entry, and a compact table of 100K entries. The configuration for training embeddings is defined in project.yml. Before proceeding with the training, floret must be compiled and installed on the machine where training will take place.

To train embeddings from scratch, one has to be in the directory of the project, have floret and spacy and then run the following command:
```bash
python -m spacy project run either-train-embeddings
```
Which will run several shell scripts defined in `project.yml` to download the corpus and start floret training. If the user does not want to train embeddings from scratch, but use the ones that we release within a spaCy package, then they may execute the following command instead: `python -m spacy project run either-download-embeddings`.

### Downloading pre-trained floret Embeddigns for Romanian
We provide pre-trained embeddings that can be used with the pipeline. The embeddings are downloaded with the assets:
```bash
python -m spacy project assets
python -m spacy project run either-download-embeddings
```

#### Example of using floret nearest-neighbors
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


### Building a Complete spaCy Package for Legal Documents

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



<a name="resources"></a> 
## Repository Resources

This repository contains two datasets:

#### 1. Historical Public Procurement Legislation (PPL)

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


