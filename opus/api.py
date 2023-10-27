# api

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from opus.agent import Agent

class Item(BaseModel):
    utterance: str
    history: list[dict] = []
    model: str = "gpt-3.5-turbo-16k-0613"
    source: str = "openai"
    debug: bool = False
    verbose: bool = False

app = FastAPI()

@app.post("/parse/")
async def parse(item: Item):
    item_dict = dict(item)
    opus_agent = Agent(item_dict)
    parsed = opus_agent.parse(item_dict['utterance'])
    return parsed



def serve():
    uvicorn.run(app, port=8000, host='0.0.0.0')
