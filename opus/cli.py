import os
import click
import json
import random
from opus.agent import Agent
import time

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
@click.option('--local/--no-local', '-v', default=False, help="If set, then model is loaded from a local Ollama server")
@click.option('--debug/--no-debug', '-d', default=False, help="If set, then debugging printing happens")
@click.option('--model', '-m', default="llama2", help="choose an Ollama model")
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
            end_time = time.perf_counter()
            elapsed_time = round(end_time - start_time, 2)
            print(f"\n{json.dumps(parsed, indent=2)}\n")
            click.secho(f"\n⏲️  {elapsed_time} seconds")

cli.add_command(run)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
