# pctm
Turing Machine for Primality Check in Unary Alphabet

# Using docker
```bash
# build docker image
docker build -t pctm .

# run docker container
docker run -it --rm -v "$PWD":/pctm pctm python3 main.py
```

# How to use
```bash
usage: 
    Primality Check Turing Machine 
        [-h] -t TURING_MACHINE_PATH
        [-cs CONTEXT_SENSITIVE_GRAMMAR_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -t TURING_MACHINE_PATH, --turing_machine_path TURING_MACHINE_PATH
                        Path to Turing Machine file
  -cs CONTEXT_SENSITIVE_GRAMMAR_PATH, --context_sensitive_grammar_path CONTEXT_SENSITIVE_GRAMMAR_PATH
                        Path where to save generated grammar
```
