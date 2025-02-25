import nltk
from nltk.corpus import wordnet as wn

def download_wordnet():
    """Download WordNet if not already downloaded."""
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading WordNet...")
        nltk.download('wordnet')
        print("WordNet downloaded successfully!")

def get_synonyms(word):
    """
    Get all synonyms for a given word from WordNet.
    
    Args:
        word (str): The input word to find synonyms for
    
    Returns:
        list: A list of synonyms for the input word
    """
    synonyms = []
    
    # Get all synsets for the word
    for synset in wn.synsets(word):
        # Get all lemmas for each synset
        for lemma in synset.lemmas():
            # Get the name of each lemma (synonyms)
            synonym = lemma.name().replace('_', ' ')
            # Add to list if not already there and not the original word
            if synonym != word and synonym not in synonyms:
                synonyms.append(synonym)
    
    return synonyms

def create_synonym_dictionary(word_list=None):
    """
    Create a dictionary mapping words to their synonyms.
    
    Args:
        word_list (list, optional): List of words to map. 
                                   If None, uses all words in WordNet.
    
    Returns:
        dict: A dictionary with words as keys and lists of synonyms as values
    """
    synonym_dict = {}
    
    if word_list is None:
        # If no word list is provided, use all words in WordNet
        # This is computationally intensive and will take time!
        all_lemmas = set()
        for synset in tqdm.tqdm(wn.all_synsets()):
            for lemma in synset.lemmas():
                all_lemmas.add(lemma.name())
        
        word_list = [lemma.replace('_', ' ') for lemma in all_lemmas]
    
    # Process each word
    for word in tqdm.tqdm(word_list):
        synonym_dict[word] = get_synonyms(word)
    
    return synonym_dict

def main():
    # Ensure WordNet is downloaded
    download_wordnet()
    
    # Example usage with a small set of words
    sample_words = ['happy', 'sad', 'good', 'bad', 'big', 'small']
    
    print("Creating synonym dictionary for sample words...")
    synonym_dict = create_synonym_dictionary(sample_words)
    
    # Print results
    for word, synonyms in synonym_dict.items():
        print(f"\n{word}: {', '.join(synonyms)}")
    
    # Uncomment to create a dictionary for all WordNet words
    # Warning: This will take a long time and use a lot of memory!
    # print("\nCreating synonym dictionary for all WordNet words...")
    # all_synonym_dict = create_synonym_dictionary()
    
    # Save to file example
    # import json
    # with open('wordnet_synonyms.json', 'w') as f:
    #     json.dump(synonym_dict, f, indent=2)

import tqdm

all_titles = set()
for line in tqdm.tqdm(open('enwiktionary-latest-all-titles'), desc='Loading titles'):
    all_titles.add(tuple(line.split('\t',1)[1].lower().strip().split("_")))

oneword_titles = {t for t in tqdm.tqdm(all_titles, desc='Loading oneword titles') if len(t)==1}

import sqlite3
# dump synonyms into sqlite
with sqlite3.connect('wiktionary.db') as conn:

  for word, in tqdm.tqdm(oneword_titles, desc='Dumping synonyms'):
      synonyms = get_synonyms(word)
      if synonyms: print(word, synonyms)
      # for synonym in synonyms:
      #     conn.execute('insert into synonyms (word, synonym) values (?, ?)', (word, synonym))
