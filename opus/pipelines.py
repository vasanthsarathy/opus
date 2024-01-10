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
    candidates = []
    for obj in stream:
        candidates.append(obj.candidate_parses)

    candidates.sort(key=lambda x:len(x.candidate_parses))

    return candidates[0] # returns a "Parses" object that contains all the parses for a particular utterance. 
