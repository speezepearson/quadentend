Tools to help find [quadruple entendres](https://rickiheicklen.com/unparalleled-misalignments.html).

# Setup

```bash
curl https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing | gunzip > GoogleNews-vectors-negative300.bin

curl https://kaikki.org/dictionary/raw-wiktextract-data.jsonl.gz | gunzip > raw-wiktextract-data.jsonl

curl https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles.gz | gunzip > enwiktionary-latest-all-titles

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 wordnet-extract.py
python3 wiktionary-extract.py
```
