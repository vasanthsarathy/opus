# opus
Open world parser with unrestricted semantics


### Troubleshooting

*Failed to unlock the collection* Error when doing `poetry add`

I needed to add this line to my `.bashrc` and `$source \.bashrc` it to get around the error. 
```
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```

### Todo 
- [ ] Get arguments for the CPC. (self, VAR0, etc.) 
- [ ] Figure out how to "constrain" the output of the llama models. Maybe use lmql type constraint guidance.
