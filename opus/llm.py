# All code relating to our core LLM infrastructure
from yaspin import yaspin
from langchain.llms import Ollama

@yaspin(text="Loading LLM...", color="green")
def initialize_llm(ctx):
    from langchain.prompts import PromptTemplate
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI,ChatAnthropic
    from langchain.chains import LLMChain

    # TODO: add ability to specify LLM and params as input


    if ctx['local']:
        if 'model' in ctx:
            llm = Ollama(model=ctx['model'])
        else:
            llm = Ollama("llama2")
    else:
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)
    return llm
