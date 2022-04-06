import glob
import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

import Utils
import pandas

# set file path to retrieve the data
folder_path = '/Users/x-women/Desktop/UCD_ES_Project/ESM_EDIT/ESM_EDIT_Data/ESM_EDIT_Features/'
transition_path = folder_path + 'STM_Transition/'

# NLTK stop words
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['the', 'with', 'and', 'an', 'in', 'into', 'state','community','site','plant', 'phase','result',
                   'use', 'cause','reference','return','condition','also','due','back','also',
                   'transition','species','p'])

# tokenization
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

nlp = spacy.load("en_core_web_sm")

def lemmatization(texts, allowed_postags=['NOUN','ADJ','ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# check whether STM exist
transition_files = glob.glob(transition_path + '*.txt')

trigger_stats = pandas.DataFrame({'MLRA': [],
                             'ES_ID': [],
                             'triggers': []})

data_words = []
for file in transition_files:

    p = open(file, 'r')
    lines = p.readlines()
    MLRA_id = file.split('/')[-1].split('_')[0]

    try:
        # mlra has record
        if len(lines) > 3:
            mlra_data = Utils.txtToDF(lines)
            es_id = mlra_data[mlra_data['MLRA'] == MLRA_id]['"Ecological site ID"'].unique().tolist()

            # iterate through es_id for each mlra
            for id in es_id:
                es_data = mlra_data[mlra_data['"Ecological site ID"'] == id]

                # es_id has data
                if es_data.shape[0] > 0:

                    # covert to list
                    data = es_data.Mechanism.values.tolist()

                    data = list(sent_to_words(data))
                    data_words += data

            es_data = []

    except:
        print(MLRA_id)

# create bigram and trigram
data_words = remove_stopwords(data_words)
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

# faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)


# Form Bigrams
data_words_bigrams = make_bigrams(data_words)

# Do lemmatization keeping only noun, adj, vb, adv
# it has all key words
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN','ADJ','ADV'])

# export the file for future
# pd.DataFrame(data_lemmatized).to_csv("data_lemmatized_noV.csv", index=False, header=False)

# create dictionary and corpus
# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# clean the single words
def cleanLength(data: dict, lenth: int):
    res = {}
    for elm in data.items():
        k = elm[0]
        if len(k.split('_')) == lenth:
            res[k] = elm[1]

    return res

df = cleanLength(bigram.vocab, 2)
df = pd.DataFrame.from_dict(df, orient ='index')
pd.DataFrame(df).to_csv("trigger_bigram_non.csv")

df = cleanLength(trigram.vocab, 3)
df = pd.DataFrame.from_dict(df, orient ='index')
pd.DataFrame(df).to_csv("trigger_trigram_non.csv")