""" This is the data model """
from pydantic import BaseModel

"""
dataset contains a list of parsesOfUtterances
Each parsesOfUtterance contains an Utterance and list of Parses
Each Parse contains an utterance, semantics and info about parser, time

"""

class Interlocutor(BaseModel):
    """
    Agents that are involved in the conversation as speaker/listener
    """
    name: str # e.g., evan | opusv0.1
    interlocutor_id: str #random id assigned at inception 
    type_name: str # e.g. human | ai 

class Parser(BaseModel):
    """
    Agent that performs the parsing
    """
    name: str 
    type_name: str

class Time(BaseModel):
    """
    Time model compatible with datetime library

    can use strftime and strptime 
    """
    time: str
    str_format: str

class Semantics(BaseModel):
    """
    All the different semantics structures
    """
    trade: str 
    smr: dict 

class Utterance(BaseModel):
    text: str
    utterance_id: str
    speaker: Interlocutor
    listeners: list[Interlocutor]
    conversation_id: str # associated conversation.conversation_id
    loc_id: int # index of current utterance in conversation.history 

class Context(BaseModel):
    context_id: str
    type_name: str # task 
    info: dict # various information about the context

class Conversation(BaseModel):
    conversation_id: str
    history: list[Utterance]
    contexts: list[Context]

class Parse(BaseModel):
    utterance: Utterance
    semantics: Semantics #{ trade: str, smr: dict }
    time: Time #{time:str, format:str} when parse was performed
    parser: Parser
    comments: str # comments 
    is_gold: bool # whether or not this is a gold parse of an utterance

"""
Currently
semantics={"trade": str,
"smr": str}

time = dt.now().strftime(DATETIMEFORMAT)

parser={"type": "opus" | "human","name": str model name}
"""

class Parses(BaseModel):
    """
    For a particular utterance, contains a list of parses

    E.g., an utterance could receive different parses from
    an AI or different humans or "gold". 
    """
    utterance: Utterance
    candidate_parses: list[Parse]
    gold: int # location of gold parse, if none, then -1 

class Corpus(BaseModel):
    """
    Contains a dataset of parses of utterances
    """
    parsed_utterances: list[Parses]
