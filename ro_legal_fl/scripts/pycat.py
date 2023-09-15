# to do cat on windows
import shutil
import sys

with open(sys.argv[3], 'wb') as outfis:
    with open(sys.argv[1], 'rb') as fin1, open(sys.argv[2], 'rb') as fin2:
        shutil.copyfileobj(fin1, outfis)
        outfis.write(b'\n')
        shutil.copyfileobj(fin2, outfis)