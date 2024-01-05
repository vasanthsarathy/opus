from opus.model import Parse, Utterance, ParsedUtterance
from opus.agent import Agent
import json
from pydantic import ValidationError
import math
import random


# Given a list of dictionaries, and a key, return the entry in the list that matches
def find_dict_in_list(lst, key, target):
    for item in lst:
        if not key in item:
            #print("Key not in Dict")
            return None
        if item[key] == target:
            return item
    #print("Nothing found")
    return None

def find_all_dicts_in_list(lst, key, target):
    output = []
    for item in lst:
        if not key in item:
            return output
        if item[key] == target:
            output.append(item)
    #print("Nothing found")
    return output



def load_parsed_utterances_from_file(filename: str):
    """
    Returns a list of ParsedUtterances objects that has been loaded from file 

    also validates the schema
    """
    
    with open(filename, "r") as f:
        items = json.load(f)  
        
    parsed_utterances = []
    for i in items:
        #validate data
        try:
            parsed_utterance = ParsedUtterance.validate(i)
        except ValidationError as e:
            print(e)
        parsed_utterances.append(parsed_utterance)
    
    return parsed_utterances


def select_parsed_utterance(parsed_utterances: list[ParsedUtterance]):
    """
    Returns a single ParsedUtterance object 

    This contains the utterance, and all the Parses we have so far. 
    """

    min_num = math.inf
    selected_parsed_utterance = None
    for p in parsed_utterances:
        num = len(p.parses)
        if num < min_num:
            min_num = num
            selected_parsed_utterance = p
    
    if selected_parsed_utterance == None:
        return random.choice(parsed_utterances)
    else:
        return selected_parsed_utterance
