import reflex as rx
import json
import random
from opus.agent import Agent
from opus.model import Parses
from opus.io import load_preprocessed

PRELOAD_CACHE_FILE = "../opus/results/utterances_00_preprocessed_parsed.jsonl"

def preload_cache(filename):
    ctx = {'input': filename}
    stream = load_preprocessed(ctx)
    cache = {}
    for obj in stream:
        cache.update({hash(obj.utterance.text): obj})
    return cache


async def run_opus(utterance, opus_agent):
    smr = opus_agent.parse(utterance)
    return smr


class State(rx.State):
    current_utterance: str
    current_trade_parse: str
    current_smr: dict
    pretty_smr: str

    # The cache is a dict with the hash(utterance) as its key
    #cache: dict = preload_cache(PRELOAD_CACHE_FILE)
    
    input_display: str
    correct: bool
    loading: bool = False

    def load(self):
        ctx = {"input": PRELOAD_CACHE_FILE} 
        cache = list(load_preprocessed(ctx))
        cache.sort(key=lambda x: len(x.candidate_parses))

        selected = cache[0] # this is a Parses object
        self.current_utterance = selected.utterance.text
        self.current_trade_parse = selected.candidate_parses[0].semantics.trade
        self.current_smr = selected.candidate_parses[0].semantics.smr
        self.pretty_smr = self.to_pretty_smr() 


    def save_to_cache(self):
        self.cache.update(
            {
                hash(self.current_utterance): {
                    "utterance": self.current_utterance,
                    "trade": self.current_trade_parse,
                    "smr": self.pretty_smr,
                }
            }
        )

    def check_cache(self):
        ctx = {"input": PRELOAD_CACHE_FILE} 
        stream = load_preprocessed(ctx)
        cache = {}
        for obj in stream:
            cache.update({
                hash(obj.utterance.text): obj
            })

        if hash(self.current_utterance) in cache:
            return cache
        else:
            return {}

    def to_pretty_smr(self):
        return json.dumps(self.current_smr, indent=2)

    
    async def parse(self):
        cache = self.check_cache()
        if cache:
            self.current_trade_parse = self.cache[hash(self.current_utterance)]["trade"]
            self.current_smr = self.cache[hash(self.current_utterance)]["smr"]
            self.pretty_smr = self.to_pretty_smr()

        else:
            self.loading = True
            yield
            params = {
                "verbose": False,
                "debug": False,
                "model": "gpt-3.5-turbo-16k-0613",
                "source": "openai",
                "speaker": "evan",
                "listener": "self",
            }
            opus_agent = Agent(params)
            self.current_smr = await run_opus(self.current_utterance, opus_agent)
            self.current_trade_parse = opus_agent.trade_semantics(params["speaker"])
            self.pretty_smr = self.to_pretty_smr()
            self.save_to_cache()
        self.loading = False

        # print(f"Cache Length: {len(self.cache)}")
