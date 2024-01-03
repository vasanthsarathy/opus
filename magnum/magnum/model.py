""" This is the data model """
from pydantic import BaseModel
from typing import List,Dict

class Utterance(BaseModel):
    text: str
    speaker: str
    listener: str

class Parse(BaseModel):
    utterance: Utterance
    parse: Dict["predicate": str, "json": Dict]
    parse_json: str
    parser: str

class ParsedUtterance(Utterance):
    parses: List[Parse]


