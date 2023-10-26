import click

def parse(ctx):
    
    utt = ctx['utterance']

    # get LLM
    llm = initialize_llm(ctx)
    print(llm)
    # Extract intent

    
