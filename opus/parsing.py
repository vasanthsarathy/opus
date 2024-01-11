from opus.agent import Agent
from datetime import datetime as dt
from opus.model import *
from opus.defaults import DATETIMEFORMAT

def parse_utterances(stream, ctx):
    opus_agent = Agent(ctx)
    for obj in stream:
        smr = opus_agent.parse(obj.utterance.text)
        trade = opus_agent.trade_semantics(obj.utterance.speaker.name)
        candidate_parse = Parse(
            utterance=obj.utterance,
            semantics=Semantics(trade=trade, smr=smr),
            time=Time(
                time=dt.now().strftime(DATETIMEFORMAT), str_format=DATETIMEFORMAT
            ),
            parser=Parser(name=ctx["model"], type_name="opus"),
            comments="",
            is_gold=False
        )
        obj.candidate_parses.append(candidate_parse)
        yield obj
