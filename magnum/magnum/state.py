import reflex as rx
import json
import random

PRELOAD_CACHE_FILE = "../opus/data/utterances_01-parsed.txt"

def preload_cache(filename):
    """
    Returns a cache dict with a set of parses in a file
    """

    with open(filename, "r") as f:
        utterances_and_parses = json.load(f)
    
    cache = {}
    for item in utterances_and_parses:
        utterance = item['utterance']['text']
        for p in item['parses']:
            if p['parser']['type'] == "opus":
                cache.update({hash(utterance): {
                    "utterance": utterance,
                    "trade": p['parse']['trade'],
                    "smr": p['parse']['smr']
                }})
    
    return cache


class State(rx.State):
    current_utterance: str
    current_trade_parse: str
    current_smr: dict
    pretty_smr: str
    cache: dict = preload_cache(PRELOAD_CACHE_FILE)
    input_display: str

    def save_to_cache(self):
        self.cache.update({hash(self.current_utterance): {"utterance": self.current_utterance, 
                                             "trade": self.current_trade_parse, 
                                             "smr": self.pretty_smr}})
        
    def check_cache(self):
        if hash(self.current_utterance) in self.cache:
            return self.cache
        else:
            return {}
        
    def to_pretty_smr(self):
        return json.dumps(self.current_smr, indent=2)

    def load(self):
        rand_parse = random.choice(list(self.cache.values()))
        self.current_utterance = rand_parse['utterance']
        self.current_trade_parse = rand_parse['trade']
        self.current_smr = rand_parse['smr']
        self.pretty_smr = self.to_pretty_smr()

    def parse(self):
        cache = self.check_cache()
        if cache:
            print("I knew that")
            self.current_trade_parse = self.cache[hash(self.current_utterance)]['trade']
            self.current_smr = self.cache[hash(self.current_utterance)]['smr']
            self.pretty_smr = self.to_pretty_smr()

        else:
            print("Whhaa?")
            self.current_trade_parse = f"parse({self.current_utterance})"
            self.current_smr = {"utterance": self.current_utterance}
            self.pretty_smr = self.to_pretty_smr()
            self.save_to_cache()
            
        
        print(f"Cache Length: {len(self.cache)}")
    



    