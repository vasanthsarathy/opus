# All code relating to our core LLM infrastructure
from yaspin import yaspin

@yaspin(text="Loading LLM...", color="green")
def initialize_llm(ctx):
    from langchain.chat_models import ChatOpenAI,ChatAnthropic
    from langchain.llms import Ollama

    # TODO: add ability to specify LLM and params as input

    if 'model' in ctx:
        if 'source' in ctx:
            if "open" in ctx['source'].lower(): 
                llm = ChatOpenAI(model_name=ctx['model'], temperature=0.0)
            elif "anthro" in ctx['source'].lower(): 
                llm = ChatAnthropic(model=ctx['model'], temperature = 0.0)
            elif "ollama" in ctx['source'].lower() or "local" in ctx['source'].lower():
                llm = Ollama(model=ctx['model'],temperature=0.1)
            else:
                raise ValueError("Source you provided does not work with OPUS")
        else:
            raise ValueError("Need to provide a source using --source. For example, you can say 'openai'")

    return llm
