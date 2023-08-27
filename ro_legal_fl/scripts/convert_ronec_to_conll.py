import json
import sys

def convert(inp, outp):
    with open(inp, encoding='utf-8') as fin:
        data = json.load(fin)
    #sent_separator =  "\n-DOCSTART-      O\n"
    sent_separator =  "\n"
    with open(outp, 'w', encoding='utf-8') as fout:
        for item in data:
            fout.write(sent_separator)
            for tok, tag in zip(item['tokens'], item['ner_tags']):
                fout.write(tok + '\t' + tag + '\n')


convert(sys.argv[1], sys.argv[2])