from opus.io import load_text_utterances, record_objs, load_preprocessed, load_jsonl
from opus.parsing import parse_utterances

def parse_from_raw_file(ctx):
    stream = load_text_utterances(ctx)
    stream = record_objs(stream, "preprocessed", ctx)
    stream = parse_utterances(stream, ctx)
    stream = record_objs(stream, "parsed", ctx)
    for obj in stream:
        pass


def batch_parse_from_preprocessed_file(ctx):
    stream = load_preprocessed(ctx)
    stream = parse_utterances(stream, ctx)
    stream = record_objs(stream, "parsed", ctx)
    for obj in stream:
        pass


def select_from_file(ctx):
    """
    Randomly select an Parses from a parsed file. 
    """

    stream = load_preprocessed(ctx)
    for obj in stream:
        gold_exists = False
        for parse in obj.parses:
            if not parse.is_gold:
                gold_exists = True
                break
        
        if not gold_exists:
            
        











def parse_one(utterance, ctx):
    opus_agent = Agent(ctx)
    DATETIMEFORMAT = "%d-%b-%Y (%H:%M:%S.%f)"
    smr = opus_agent.parse(utterance)
    trade = opus_agent.trade_semantics(ctx['speaker'])
    candidate_parse = Parse(
        utterance=utterance,
        semantics=Semantics(trade=trade, smr=smr),
        time=Time(
            time=dt.now().strftime(DATETIMEFORMAT), str_format=DATETIMEFORMAT
        ),
        parser=Parser(name=ctx["model"], type_name="opus"),
        comments=ctx['comments'],
        is_gold=ctx['is_gold']
    )
        obj.candidate_parses.append(candidate_parse)
        yield obj