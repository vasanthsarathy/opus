import json
from pathlib import Path
import random
import click
from opus.model import *
from uuid import uuid4


def load_text_utterances(ctx):
    """
    Yields a parse object
    """

    # create speaker and listener objects 
    speaker = Interlocutor(name=ctx['speaker'], 
                           interlocutor_id=str(uuid4()),
                           type_name="human")
    listeners = [Interlocutor(name="self", 
                              interlocutor_id=str(uuid4()),
                              type_name="opus")]

    with open(ctx['input'], "r") as utterance_file:
        for line in utterance_file:
            # unique conversation id per utterance
            # all loc id = 0
            utterance = Utterance(text=line.replace("\n",""), 
                                  utterance_id=str(uuid4()),
                                  speaker=speaker, 
                                  listeners=listeners,
                                  conversation_id=str(uuid4()),
                                  loc_id=0)
            candidate_parses = []
            gold = -1
            obj = Parses(utterance=utterance,
                            candidate_parses=candidate_parses,
                            gold=gold)
            yield obj    # this is a pydantic model object "Parses"


def record_objs(stream, name, ctx):
    """
    Wraps a stream with logic to record each object to a JSON file and yield it
    again for further processing.
    """
    #print(f"// Saving rows to file")
    file_stem = Path(ctx['input']).stem

    output_filepath = f"opus/results/{file_stem}_{name}.jsonl"

    with open(output_filepath, 'wt') as out_file:
        for obj in stream:
            json.dump(obj.dict(), out_file, default=str)
            out_file.write('\n')
            yield obj

def load_preprocessed(ctx):
    data = load_jsonl(ctx['input']) #list of dict data 
    for item in data:
        obj = Parses(**item)
        yield obj

def load_jsonl(input_path) -> list:
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.rstrip('\n|\r')))
    print('Loaded {} records from {}'.format(len(data), input_path))
    return data