import shutil
import spacy

with open('__version__', 'w') as fout:
	print(f"Found spacy version {spacy.__version__}")
	fout.write(spacy.__version__)

source = "project.yml" 
destination = "project.yml.bckup"
shutil.copy(source, destination)

with open("project.yml", 'r') as fin:
	text = fin.read()

text = text.replace("version: 0.1.0", f"version: {spacy.__version__}")

with open("project.yml", 'w') as fout:
	fout.write(text)
