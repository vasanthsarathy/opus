""" This is the data model """
from pydantic import BaseModel

class Utterance(BaseModel):
    text: str
    speaker: str
    listener: str
    dialog: list[str] #dialog history
    loc: int # index of current utterance in dialog 

class Parse(BaseModel):
    utterance: Utterance
    parse: dict
    parser: dict

class ParsedUtterance(BaseModel):
    utterance: Utterance
    parses: list[Parse]
