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
            end_time = time.perf_counter()
            elapsed_time = round(end_time - start_time, 2)
            print(f"\n{json.dumps(parsed, indent=2)}\n")
            click.secho(f"\n⏲️  {elapsed_time} seconds")

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

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
