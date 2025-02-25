import tqdm

all_titles = set()
for line in tqdm.tqdm(open('enwiktionary-latest-all-titles'), desc='Loading titles'):
    all_titles.add(tuple(line.split('\t',1)[1].lower().strip().split("_")))

oneword_titles = {t for t in tqdm.tqdm(all_titles, desc='Loading oneword titles') if len(t)==1}

twoword_titles = {t for t in tqdm.tqdm(all_titles, desc='Loading twoword titles') if len(t)==2}

combo_titles = {(w1,w2) for w1,w2 in tqdm.tqdm(twoword_titles, desc='Loading combo titles') if (w1,) in oneword_titles and (w2,) in oneword_titles}

assert ('dad','bod') in combo_titles
assert ('dad','potato') not in combo_titles

from gensim.models import KeyedVectors
print('Loading model')
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

target = ('dad','bod')
scores = {}
for w1,w2 in tqdm.tqdm(combo_titles, desc='Calculating scores'):
    if w1 not in model or w2 not in model: continue
    if w1==target[0] or w2==target[1]: continue
    sim1 = model.similarity(target[0], w1)
    sim2 = model.similarity(target[1], w2)
    scores[(w1,w2)] = (sim1, sim2)

metric = min
for (w1,w2), sims in sorted(scores.items(), key=lambda x: metric(x[1]), reverse=True)[:100]:
    print(f"{w1+' '+w2:<40} : {metric(sims):.2f} = {sims[0]:.2f}, {sims[1]:.2f}")

import sqlite3
conn = sqlite3.connect('wiktionary.db')

def get_synonyms(w: str):
    return [row[0] for row in conn.execute('select synonym from synonyms where word = ?', [w]).fetchall()]

import itertools
for w1, w2 in combo_titles:
    s1s = get_synonyms(w1)
    s2s = get_synonyms(w2)
    for s1, s2 in itertools.product(s1s, s2s):
        if s1==w1 or s2==w2: continue
        if (s1, s2) in combo_titles:
            print(f"{w1} {w2} = {s1} {s2}")
