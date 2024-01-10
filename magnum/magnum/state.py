from uuid import uuid4
import reflex as rx
import json
import random
from opus.agent import Agent
from opus.model import Parses, Parse, Utterance, Time, Semantics, Interlocutor, Parser
from datetime import datetime as dt
from opus.io import load_preprocessed
import click

#--- GLOBAL DEFAULTS
PRELOAD_CACHE_FILE = "../opus/results/utterances_00_preprocessed_parsed.jsonl"
DATETIMEFORMAT = "%d-%b-%Y (%H:%M:%S.%f)"


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

# TODO: revisit how we do vars, especially with caching
class State(rx.State):
    cache_input_file: str = PRELOAD_CACHE_FILE
    current_utterance: str = ""
    current_trade_parse: str = ""
    current_speaker: str = "evan"
    current_listener: str = "self"
    current_smr: dict = {}
    pretty_smr: str = ""
    username: str = ""
    current_model: str = "gpt-3.5-turbo-16k-0613"

    # input_display: str
    correct_str: str = "yes"
    loading: bool = False

    @rx.cached_var
    def ctx(self):
        click.secho(">> Getting CTX", fg="yellow")
        return dict({"input": self.cache_input_file,
               "speaker": self.current_speaker,
               "listener": self.current_listener,
               "model": self.current_model,
               "source": "openai",
               "verbose": False,
               "debug": False})
    
    @rx.var
    def is_wrong(self):
        if self.correct_str == "yes":
            return False
        else:
            return True
    
    # Cache: dict of "Parses" objects, each key is the hash of the utterance and each value represents an Utterance, and associated list of Parse objects of that utterance
    @rx.cached_var
    def cache(self) -> dict: #just a hashed version of that cache
        click.secho(">> Updating Cache", fg="red")
        list_cache = list(load_preprocessed(self.ctx))
        cache = {}
        for item in list_cache:
            cache.update({hash(item.utterance.text): item.dict()})        
        click.secho("Cache completed", fg="green")
        return cache

    def load(self):
        """
        This loads one utterance + parse combo from the cache
        """
        list_cache = []
        for item in list(self.cache.values()):
            list_cache.append(Parses(**item))
        #list_cache = list(self.cache.values())
        list_cache.sort(key=lambda x: len(x.candidate_parses))
        selected = list_cache[0] # this is a Parses object
        self.current_utterance = selected.utterance.text
        self.current_trade_parse = selected.candidate_parses[0].semantics.trade
        self.current_smr = selected.candidate_parses[0].semantics.smr
        self.pretty_smr = self.to_pretty_smr() 

    def update_cache(self):
        # find the first item corresponding to the current cache and add a parse to it
        if hash(self.current_utterance) in self.cache:
            self.append_to_candidate_parses(self)
        else: # new utterance 
            # Compute new Parse entry for the list of candidate_parses
            speaker = Interlocutor(name="evan", 
                           interlocutor_id=str(uuid4()),
                           type_name="human")
            listeners = [Interlocutor(name="self", 
                                    interlocutor_id=str(uuid4()),
                                    type_name="opus")]
            utterance = Utterance(text=self.current_utterance, 
                                  utterance_id=str(uuid4()),
                                  speaker=speaker, 
                                  listeners=listeners,
                                  conversation_id=str(uuid4()),
                                  loc_id=0)

            computed_smr = self.compute_smr_from_trade()
            semantics=Semantics(trade=self.current_trade_parse,
                                smr=computed_smr)
            new_parse = Parse(utterance=utterance,
                                semantics=semantics,
                                time=Time(
                                    time=dt.now().strftime(DATETIMEFORMAT),
                                    str_format=DATETIMEFORMAT),
                                parser=Parser(name=self.username,
                                                type_name="human"),
                                comments="",
                                is_gold=True)
            self.cache[hash(self.current_utterance)].candidate_parses += new_parse


    def append_to_candidate_parses(self):
        # Pull up the Parses object for that utterance
        parses = self.cache[hash(self.current_utterance)]

        # Compute new Parse entry for the list of candidate_parses
        utterance = parses.utterance
        utterance.loc_id = len(parses.candidate_parses)
        computed_smr = self.compute_smr_from_trade()
        semantics=Semantics(trade=self.current_trade_parse,
                            smr=computed_smr)
        new_parse = Parse(utterance=utterance,
                            semantics=semantics,
                            time=Time(
                                time=dt.now().strftime(DATETIMEFORMAT),
                                str_format=DATETIMEFORMAT),
                            parser=Parser(name=self.username,
                                            type_name="human"),
                            comments="",
                            is_gold=True)

        self.cache[hash(self.current_utterance)].candidate_parses += new_parse

    def compute_smr_from_trade(self):
        # TODO: fix this to actually compute it from trade parse
        return self.current_smr

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
        if hash(self.current_utterance) in self.cache:
            return self.cache
        else:
            return {}

    def to_pretty_smr(self):
        return json.dumps(self.current_smr, indent=2)

    async def parse(self):
        # print(f"\n CTX:\n----\n{json.dumps(self.ctx, indent=2)}")
        cache = self.check_cache()
        if cache:
            # choose the first parse
            parse = self.cache[hash(self.current_utterance)].candidate_parses[0]

            self.current_trade_parse = parse.semantics.trade
            self.current_smr = parse.semantics.smr
            self.pretty_smr = self.to_pretty_smr()

        else:
            self.loading = True
            yield

            opus_agent = Agent(self.ctx)
            self.current_smr = await run_opus(self.current_utterance, opus_agent)
            self.current_trade_parse = opus_agent.trade_semantics(self.ctx["speaker"])
            self.pretty_smr = self.to_pretty_smr()
            self.save_to_cache()
        self.loading = False


