""" Various utilities to support Magnum """
from model import Parse, Utterance, ParsedUtterance
from opus.agent import Agent

def parse(utterance: str, params: dict=None) -> ParsedUtterance:
    """
    Given an utterance, runs OPUS with params 
    """
    
