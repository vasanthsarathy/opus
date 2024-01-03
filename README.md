# OPUS
Open world parser with unrestricted semantics.


### Useful commands

For seeing all available models

```bash
opus models
```

Example of a run command
```
opus run --model gpt-3.5-turbo-16k-0613 --source openai
```

### API

A rest api can be started up with 
```bash
opus serve
```

After that requests can be sent with a json containing ONE required string field called "utterance".

Example: 

```json
{
  "utterance": "pass the salt",
  "history": [],
  "model": "gpt-3.5-turbo-16k-0613",
  "source": "openai",
  "debug": false,
  "verbose": false
}
```


Output (parsed) 
```json
{
  "referents": [
    {
      "text": "salt",
      "type": "physobj",
      "role": "central",
      "variable_name": "VAR0",
      "cognitive_status": "DEFINITE"
    }
  ],
  "intention": {
    "intent": "instruct",
    "proposition": {
      "text": "pass",
      "type": "action",
      "arguments": [
        "VAR0"
      ]
    }
  },
  "descriptors": [
    {
      "text": "salt",
      "arguments": [
        "VAR0"
      ]
    }
  ]
}
```
### Magnum Opus
This is the data annotation tool. The source code for this tool is found in the `magnum` folder. It is built on a `reflex.dev` pure-python web framework.

Run by going in the magnum folder: `$ cd magnum` and then type `reflex run` to start the app server. Click on the link provided and you are good to go.

Please read the "instructions" first on the sidebar menu before annotating anything. 


### Troubleshooting

*On server: Failed to unlock the collection* Error when doing `poetry add`

I needed to add this line to my `.bashrc` and `$ source \.bashrc` it to get around the error. 
```
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```

### Todo 
- [ ] Get arguments for the CPC. (self, VAR0, etc.) 
- [ ] Figure out how to "constrain" the output of the llama models. Maybe use lmql type constraint guidance.
