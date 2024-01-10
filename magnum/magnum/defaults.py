PRELOAD_CACHE_FILE = "../opus/results/utterances_00_preprocessed_parsed.jsonl"
DATETIMEFORMAT = "%d-%b-%Y (%H:%M:%S.%f)"

ctx = {"input": PRELOAD_CACHE_FILE,
               "speaker": "evan",
               "listeners": ["self"],
               "model": "gpt-3.5-turbo-16k-0613",
               "source": "openai",
               "debug": False,
               "verbose": False}