import nltk

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

DANGEROUS_VERBS = {

    stemmer.stem(word)

    for word in [

        "bypass",
        "disable",
        "override",
        "ignore",
        "reveal",
        "leak",
        "hack",
        "build",
        "create",
        "expose",
        "remove",
        "evade",
        "circumvent",
        "exploit",
        "simulate",
        "unlock",
        "simulate",
        "pretend",
        "roleplay",
        "act"
        "free",
        "break"
    ]
}


DANGEROUS_NOUNS = {

    stemmer.stem(word)

    for word in [

        "system",
        "prompt",
        "instruction",
        "safeguard",
        "security",
        "bomb",
        "restriction",
        "ethic",
        "policy",
        "guardrail",
"alignment"
        "malware",
        "explosive",
        "weapon",
        "chemistry",
        "restriction",
        "ethic",
        "policy",
        "guardrail",
        "alignment",
        "compliance",
        "filter",
        "reactor",
        "jailbreak",
        "firewall",
        "protection"
    ]
}


def analyze_intent(prompt):

    raw_tokens = word_tokenize(prompt.lower())

    tokens = [stemmer.stem(word) for word in raw_tokens]

    tagged = pos_tag(raw_tokens)

    verbs = []
    nouns = []
    for word, tag in tagged:
        stemmed_word = stemmer.stem(word.lower())
        if tag.startswith("VB"):

            verbs.append(stemmed_word)

    
        elif tag.startswith("NN"):
            nouns.append(stemmed_word)

    matched_verbs = []
    matched_nouns = []
    for verb in verbs:

        if verb in DANGEROUS_VERBS:
            matched_verbs.append(verb)

   
    for noun in nouns:
        if noun in DANGEROUS_NOUNS:
            matched_nouns.append(noun)

    for token in tokens:
        if token in DANGEROUS_VERBS and token not in matched_verbs:
            matched_verbs.append(token)
        if token in DANGEROUS_NOUNS and token not in matched_nouns:
            matched_nouns.append(token)

    score = len(matched_verbs) + len(matched_nouns)
    risky = False

    if len(matched_verbs) >= 1:
        risky = True
    if score >= 2:
        risky = True
    return {

        "verbs": verbs,
        "nouns": nouns,
        "matched_verbs": matched_verbs,
        "matched_nouns": matched_nouns,
        "intent_score": score,
        "risky": risky
    }