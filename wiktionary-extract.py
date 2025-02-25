"""Pull data out of a Wiktionary dump into sqlite for faster querying."""

import json, tqdm, sqlite3

lines = (json.loads(line) for line in open('raw-wiktextract-data.jsonl'))

with sqlite3.connect('wiktionary.db') as conn:
  c = conn.cursor()
  
  c.execute('''CREATE TABLE IF NOT EXISTS glosses (
    word TEXT, gloss TEXT
  )''')
  c.execute('''CREATE INDEX IF NOT EXISTS word_idx ON glosses (word)''')

  c.execute('''CREATE TABLE IF NOT EXISTS synonyms (
    word TEXT, synonym TEXT
  )''')
  c.execute('''CREATE INDEX IF NOT EXISTS word_idx ON synonyms (word)''')

  c.execute('''CREATE TABLE IF NOT EXISTS hyponyms (
    word TEXT, hyponym TEXT
  )''')
  c.execute('''CREATE INDEX IF NOT EXISTS word_idx ON hyponyms (word)''')

  c.execute('''CREATE TABLE IF NOT EXISTS hypernyms (
    word TEXT, hypernym TEXT
  )''')
  c.execute('''CREATE INDEX IF NOT EXISTS word_idx ON hypernyms (word)''')


  try:
    for line in tqdm.tqdm(lines, desc='Processing lines'):
      if line.get('lang') != 'English': continue
      
      glosses = sum([sense.get('glosses',[]) for sense in line.get('senses',[])], [])
      for gloss in glosses:
        c.execute('INSERT INTO glosses (word, gloss) VALUES (?, ?)', (line['word'], gloss))
      
      synonyms = sum([line.get('synonyms',[]), *[sense.get('synonyms',[]) for sense in line.get('senses',[])]], [])
      for synonym in synonyms:
        c.execute('INSERT INTO synonyms (word, synonym) VALUES (?, ?)', (line['word'], synonym['word']))
      
      hyponyms = sum([line.get('hyponyms',[]), *[sense.get('hyponyms',[]) for sense in line.get('senses',[])]], [])
      for hyponym in hyponyms:
        c.execute('INSERT INTO hyponyms (word, hyponym) VALUES (?, ?)', (line['word'], hyponym['word']))
      
      hypernyms = sum([line.get('hypernyms',[]), *[sense.get('hypernyms',[]) for sense in line.get('senses',[])]], [])
      for hypernym in hypernyms:
        c.execute('INSERT INTO hypernyms (word, hypernym) VALUES (?, ?)', (line['word'], hypernym['word']))
  except KeyboardInterrupt:
    pass
