from transformers import AutoTokenizer, AutoModel
import torch

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import nltk
from nltk.tag import pos_tag

import numpy as np



nltk.download('punkt_tab')
# WORDS TO ANALYZE
words = [
    "weapon",
    "bomb",
    "explosive",
    "reactor",
    "override",
    "disable",
    "bypass",
    "ignore",
    "extract",
    "reveal",
    "password",
    "prompt",
    "system",
    "malware",
    "attack",
    "harmful"
]


# LOAD MODEL
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")


# GET EMBEDDINGS
embeddings = []

for word in words:

    inputs = tokenizer(word, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    embeddings.append(vector)


embeddings = np.array(embeddings)


# PCA REDUCTION
pca = PCA(n_components=2)

reduced = pca.fit_transform(embeddings)


# K-MEANS
kmeans = KMeans(n_clusters=3, random_state=42)

clusters = kmeans.fit_predict(reduced)


# GROUP WORDS
cluster_map = {}

for word, cluster in zip(words, clusters):

    if cluster not in cluster_map:
        cluster_map[cluster] = []

    cluster_map[cluster].append(word)


# POS ANALYSIS
# POS ANALYSIS
for cluster, cluster_words in cluster_map.items():

    print(f"\nCLUSTER {cluster}")

    verbs = []
    nouns = []

    for word in cluster_words:

        # VERB CONTEXT
        verb_sentence = f"They want to {word}"

        verb_tokens = nltk.word_tokenize(verb_sentence)

        verb_tags = pos_tag(verb_tokens)

        verb_pos = verb_tags[-1][1]


        # NOUN CONTEXT
        noun_sentence = f"The {word} is dangerous"

        noun_tokens = nltk.word_tokenize(noun_sentence)

        noun_tags = pos_tag(noun_tokens)

        noun_pos = noun_tags[1][1]


        # DECISION
        if verb_pos.startswith("VB"):
            verbs.append(word)

        elif noun_pos.startswith("NN"):
            nouns.append(word)


    print("VERBS:", verbs)
    print("NOUNS:", nouns)