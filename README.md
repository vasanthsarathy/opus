# opus
Open world parser with unrestricted semantics

### Useful commands

For seeing all available models

```bash
opus models
```

Example of a run command
```
opus run --model gpt-3.5-turbo-16k-0613 --source openai
```

### Troubleshooting

*On server: Failed to unlock the collection* Error when doing `poetry add`

I needed to add this line to my `.bashrc` and `$source \.bashrc` it to get around the error. 
```
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```

### Todo 
- [ ] Get arguments for the CPC. (self, VAR0, etc.) 
- [ ] Figure out how to "constrain" the output of the llama models. Maybe use lmql type constraint guidance.
