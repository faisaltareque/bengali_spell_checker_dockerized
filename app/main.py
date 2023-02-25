from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from spell_check import SpellChecker
spell_checker = SpellChecker()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


class Word(BaseModel):
    word: str
    
class Word_rank(BaseModel):
    word: str
    top: int

@app.get("/")
def hello():
	return {'Spell Checker': 'Send a POST request to /check with a word in the body to get a list of possible corrections'}

@app.post("/candidates")
def check_spelling(word: Word)->list:
    return jsonable_encoder(spell_checker.candidates(word.word))

@app.post("/top_candidates")
def check_spelling(word: Word_rank)->list:
    return jsonable_encoder(spell_checker.top_K_candidates(word.word, word.top))