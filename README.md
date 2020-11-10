[![Build Status](https://travis-ci.com/viabzalov/pctm.svg?branch=dev)](https://travis-ci.com/viabzalov/pctm)
[![Build Status](https://travis-ci.com/viabzalov/pctm.svg?branch=main)](https://travis-ci.com/viabzalov/pctm)

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
usage: pctm.py [-h] [-tm] [-lba] [-csg] [-ug] -w WORD

Primality Check Turing Machine

optional arguments:
  -h, --help            show this help message and exit
  -tm, --turing_machine
                        Check by Turing Machine
  -lba, --linear_bounded_automaton
                        Check by Linear Bounded Automaton
  -csg, --context_sensitive_grammar
                        Check by Context Sensitive Grammar
  -ug, --unrestricted_grammar
                        Check by Unrestricted Grammar
  -w WORD, --word WORD  Word to check

At least one of -tm/--turing_machine, -lba/--linear_bounded_automaton,
-csg/--context_sensitive_grammar, -ug/--unrestricted_grammar required
```

# Examples

```bash
./pctm.py -tm -csg -lba -ug -w a

Check by Turing Machine: False is done in 0:00:00.000017 seconds
Check by Linear Bounded Automaton: False is done in 0:00:00.000009 seconds
Check by Context Sensitive Grammar: False is done in 0:00:00.000167 seconds
Check by Unrestricted Grammar: False is done in 0:00:00.001882 seconds
```

```bash
./pctm.py -lba -tm -w aaa

Check by Turing Machine: True is done in 0:00:00.000032 seconds
Check by Linear Bounded Automaton: True is done in 0:00:00.000022 seconds
```

```bash
./pctm.py -csg -ug -w aaaaaaaaaaaaa

Check by Context Sensitive Grammar: True is done in 0:00:01.174519 seconds
Check by Unrestricted Grammar: True is done in 0:00:17.905302 seconds
```

```bash
./pctm.py --turing_machine --linear_bounded_automaton --context_sensitive_grammar --unrestricted_grammar -w aaaaaa

Check by Turing Machine: False is done in 0:00:00.000086 seconds
Check by Linear Bounded Automaton: False is done in 0:00:00.000075 seconds
Check by Context Sensitive Grammar: False is done in 0:00:00.047003 seconds
Check by Unrestricted Grammar: False is done in 0:00:00.161875 seconds
```
