import sys
import os
import random

# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC RELATE:NE RELATE:GEONAMES
mapping = {"B-PER": "B-PERSON", "I-PER": "I-PERSON", "B-TIME": "B-DATETIME", "I-TIME": "I-DATETIME", "_": "O"}


def convert(conll_lines):
    new_lines = []
    metadata = []
    for idx, line in enumerate(conll_lines):
        if line.startswith('#'):
            #metadata[idx] = line
            #print(line)
            continue
        elif line.startswith('-') or not line.strip():
            new_lines.append(line)
        else:
            parts = line.split('\t')
            new_lines.append('\t'.join([parts[1], mapping.get(parts[-2], parts[-2])]))
    return new_lines


def split_dir(in_dir, dev_perc=0.075, test_perc=0.075):
    filenames = [fis for fis in os.listdir(in_dir) if '.conllup' in fis]
    #random.shuffle(filenames)
    first_k = int(test_perc*len(filenames))
    test = [os.path.join(in_dir, fis) for fis in filenames[:first_k]]
    train = [os.path.join(in_dir, fis) for fis in filenames[first_k:]]
    dev_first_k = int(dev_perc*len(filenames))
    dev = train[:dev_first_k]
    train = train[dev_first_k:]
    return train, dev, test


doc_separator =  "-DOCSTART-      O"

def cat_lines_from_all_files(infiles):
    lines = []
    for fis in infiles:
        lines.extend(['\n', doc_separator, '\n'])
        with open(fis, 'r', encoding='utf-8') as fin:
            lines.extend(fin.readlines())
    return lines


def dump_lines(lines, out_fis):
    with open(out_fis, 'w', encoding='utf-8') as fout:
        for line in lines:
            fout.write(line.strip() + '\n')


indir = sys.argv[1]
outdir = sys.argv[2]

if not os.path.exists(outdir):
    os.makedirs(outdir)

train, dev, test = split_dir(indir)
dump_lines(convert(cat_lines_from_all_files(train)), os.path.join(outdir, 'train.tsv'))
dump_lines(convert(cat_lines_from_all_files(test)), os.path.join(outdir, 'test.tsv'))
dump_lines(convert(cat_lines_from_all_files(dev)), os.path.join(outdir, 'dev.tsv'))

