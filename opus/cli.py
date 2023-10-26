import os
import click
import json
import random
from opus.pipelines import parse

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
@click.pass_context
def run(ctx, **kwargs):
    ctx.obj.update(kwargs)
    done = False
    click.secho("\nType in your utterance and OPUS will parse it. Type '\\bye' to quit. \n")
    while not done:
        utterance = input("\nUtterance: ")
        if utterance == "\\bye":
            done = True
        else:
            parsed = parse(utterance)
            click.secho(f"\nParse:\n{parsed}")


cli.add_command(run)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
