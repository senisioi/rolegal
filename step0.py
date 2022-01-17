"""
several approaches:
a) compare each paragraph with existing public procurement articles and do a nearest neighbour
b) train a classifier to identify public procurement articles vs. other articles
c) use the weights and further fine tune the classifier to identify impacting vs contradicting
"""

"""
- classification may fail because contradicting points sometimes refer to previous laws for which we do not have the texts
- classification may fail because the relation between an article / point and existing public procurement laws is not obvious
and so it may overfit
"""

import os
from copy import deepcopy
import pandas as pd
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression


def files_in_folder(mypath):
    return [ os.path.join(mypath,f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]

def get_content(fis):
    with open(fis, 'r', encoding='utf-8') as fin:
        return fin.read()


df = pd.read_csv('impacting_laws.csv', sep='\t')

data = []
labels_impact = []
labels_all = []
for idx, row in df.iterrows():
    impact_artcl_files = files_in_folder(row['impact_dir'])
    for artcl_file in impact_artcl_files:
        data.append(get_content(artcl_file))
        labels_impact.append(1)
        labels_all.append(row['impct_contr'])
    nonrel_artcl_files = files_in_folder(row['nonrel_dir'])
    for artcl_file in nonrel_artcl_files:
        data.append(get_content(artcl_file))
        labels_impact.append(-1)
        labels_all.append(-1)



tfidf = TfidfVectorizer(**{
    'min_df': 1,
    'max_features': None,
    'strip_accents': 'unicode',
    'analyzer': 'word',
    'token_pattern': r'\b[^\d\W]+\b',
    'ngram_range': (1, 2),
    'use_idf': True,
    'smooth_idf': True,
    'sublinear_tf': True,
    'stop_words': 'english'
})

X = tfidf.fit_transform(data)



model = LogisticRegression(**{'penalty': 'l2',
                  'tol': 0.0001,
                  'C': 1,
                  'fit_intercept': True,
                  'intercept_scaling': 1.0,
                  'max_iter': 10000,
                  'solver': 'liblinear',
                  'multi_class': 'ovr',
                  'warm_start': False,
                  'random_state': None,
                  'dual': False,
                  'class_weight': 'balanced'
                  })
default_grid = {"C": [0.001, 0.01, 0.1, 1, 2, 10], "penalty": ["l1", "l2"]}

from sklearn.model_selection import cross_validate
from sklearn.metrics import balanced_accuracy_score, make_scorer
from sklearn.model_selection import LeaveOneOut

scorer = make_scorer(balanced_accuracy_score)
pprint(cross_validate(model, X, labels_impact, scoring=scorer))
pprint(cross_validate(model, X, labels_impact, cv=LeaveOneOut()))



print("done")


