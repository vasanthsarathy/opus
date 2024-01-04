import os
import pdb
import click
import json
import random
from opus.agent import Agent
import time
from magnum.magnum.model import Parse, ParsedUtterance, Utterance


# Shared click options
shared_options = [
    click.option('--verbose/--no-verbose', '-v', default=False, help="If set, console output is verbose"),
]

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
@click.option('--verbose/--no-verbose', '-v', default=False, help="If set, console output is verbose")
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)
    ctx.obj = kwargs
    click.clear()
    click.secho('🐧 OPUS', bold=True, fg='blue')
    click.secho(f"Open World Parser with Unrestricted Semantics", fg='yellow')
    print(f'-----------------')


@click.command()
@add_options(shared_options)
@click.option('--debug/--no-debug', '-d', default=False, help="If set, then debugging printing happens")
@click.option('--model', '-m', default="gpt-3.5-turbo-16k-0613", help="specify a model. Run 'opus models' to see available models and their sources.")
@click.option('--source', '-s', default="openai", help="specify a source for your model")
@click.pass_context
def run(ctx, **kwargs):
    ctx.obj.update(kwargs)
    done = False
    click.secho("\nType in your utterance and OPUS will parse it. Type '\\bye' to quit. \n")
    opus_agent = Agent(ctx.obj)
    while not done:
        utterance = input("\n>> ")
        if utterance == "\\bye":
            done = True
        else:
            start_time = time.perf_counter()
            parsed = opus_agent.parse(utterance)
            trade_parse = opus_agent.trade_semantics("brad")
            end_time = time.perf_counter()
            elapsed_time = round(end_time - start_time, 2)
            print(f"\n{json.dumps(parsed, indent=2)}\n")
            print(trade_parse)
            click.secho(f"\n⏲️  {elapsed_time} seconds")

@click.command()
@add_options(shared_options)
@click.option('--debug/--no-debug', '-d', default=False, 
              help="If set, then debugging printing happens")
@click.option('--input', '-i', default="", help="Input file path")
@click.option('--speaker', '-s', default="evan", help="Speaker name")
@click.option('--listener', '-l', default="self", help="Listener name")
@click.option('--model', '-m', default="gpt-3.5-turbo-16k-0613",
              help="specify a model. Run 'opus models' to see available models and their sources.")
@click.option('--source', '-s', default="openai", help="specify a source for your model")
@click.pass_context
def batch(ctx, **kwargs):
    ctx.obj.update(kwargs)
    
    opus_agent = Agent(ctx.obj)
    #Pull file
    utterances = [] 
    with open(ctx.obj["input"], "r") as utterance_file:
        for line in utterance_file:
            utterances.append(Utterance(text=line.replace("\n",""), 
                                        speaker=ctx.obj["speaker"], 
                                        listener=ctx.obj["listener"],
                                        dialog=[line.replace("\n","")],
                                        loc=0))
            #TODO will need to address the situation this is a dialog file. 
    
    # Parse Utterances
    parses = []
    parsed_utterances = [] # this is a list of ParsedUtterances, 
    for u in utterances:
        smr = opus_agent.parse(u.text)
        trade = opus_agent.trade_semantics(u.speaker)
        parse = Parse(utterance=u,
                      parse={"trade": trade,
                              "smr": smr},
                              parser=ctx.obj["model"])
        parses.append(parse)

        different_parses = [] # this is the list of different ways of parsing an utterance
        different_parses.append(parse) #we only append the one parse for now, but in the future we can add
        
        parsed_utterance = ParsedUtterance(utterance=u, parses=different_parses)
        parsed_utterances.append(parsed_utterance)
        click.secho(u.text, fg="green")
        click.secho(trade, fg="blue")

    # dump to file 
    output_filename = ctx.obj["input"].replace(".", "-parsed.")    

    dicts = [p.dict() for p in parsed_utterances]
    with open(output_filename, "w") as output_file:
        json.dump(dicts, output_file, indent=2)    


@click.command()
@add_options(shared_options)
@click.pass_context
def serve(ctx, **kwargs):
    ctx.obj.update(kwargs)
    from opus.api import serve
    serve()



@click.command()
@add_options(shared_options)
@click.pass_context
def models(ctx, **kwargs):
    ctx.obj.update(kwargs)
    click.secho("\nAvailable Models (use --model option in 'opus run'\n", bold=True)
    openai = ["gpt-4-0613", "gpt-4-0314", "gpt-4","gpt-3.5-turbo-16k","gpt-3.5-turbo-16k-0613"]
    anthropic = ["claude-instant-1", "claude-2"]
    ollama = ["llama-2", "llama-2-uncensored", "opus"]

    click.secho("Source: Openai\n")
    for m in openai:
        print(f"\t{m}")

    click.secho("\n Source: Anthropic\n")
    for m in anthropic:
        print(f"\t{m}")

    click.secho("\n Source: Ollama (LOCAL)\n")
    for m in ollama:
        print(f"\t{m}")



cli.add_command(run)
cli.add_command(models)
cli.add_command(serve)
cli.add_command(batch)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
