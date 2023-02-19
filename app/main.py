import codecs
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


class Word(BaseModel):
    word: str


import json
words_list = []
with codecs.open('vocab.txt', mode='r', encoding='utf-8') as f:
    for item in f:
        words_list.append(item.strip())
        
words_dictionary = dict.fromkeys(words_list, True)
        
def edits_distance_1(word):
    letters = 'ঁংঃঅআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits_distance_2(word):
    edits2_list = []
    for e1 in edits_distance_1(word):
        for e2 in edits_distance_1(e1):
            edits2_list.append(e2)
    return set(edits2_list)


def known_word(words):
    known_list = []
    for item in words:
        if item in words_dictionary:
            known_list.append(item)
    return set(known_list)

def candidates(word):
    return (known_word([word]) or known_word(edits_distance_1(word)) or known_word(edits_distance_2(word)) or [word])

app = FastAPI()

@app.get("/")
def hello():
	return {'Spell Checker': 'Send a POST request to /check with a word in the body to get a list of possible corrections'}

@app.post("/check")
def check_spelling(word: Word)->list:
    return jsonable_encoder(candidates(word.word))