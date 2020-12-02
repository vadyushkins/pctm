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

# Primes derivation

```
Format:

Sentence : Production : Sentence
```

```bash
python3 pctm.py -ug -w aa

Check by Unrestricted Grammar: True is done in 0:00:00.002747 seconds

A            : 1) A -> R P N R     : R P N R     
R P N R      : 2) P -> P N         : R P N N R   
R P N N R    : 3) P -> G           : R G N N R   
R G N N R    : 4) R G N -> G R N   : G R N N R   
G R N N R    : 5) G R -> C S       : C S N N R   
C S N N R    : 6) S N -> K O       : C K O N R   
C K O N R    : 7) O N -> L I       : C K L I R   
C K L I R    : 37) L I R -> M L R  : C K M L R   
C K M L R    : 38) M L -> M a M    : C K M a M R 
C K M a M R  : 21) M R -> M        : C K M a M   
C K M a M    : 19) a M -> a        : C K M a     
C K M a      : 16) K M -> M a M    : C M a M a   
C M a M a    : 18) M a -> a        : C M a a     
C M a a      : 17) C M -> M        : M a a       
M a a        : 18) M a -> a        : a a         
```

```bash
python3 pctm.py -ug -w aaa

Check by Unrestricted Grammar: True is done in 0:00:00.008455 seconds

A              : 1) A -> R P N R     : R P N R       
R P N R        : 2) P -> P N         : R P N N R     
R P N N R      : 2) P -> P N         : R P N N N R   
R P N N N R    : 3) P -> G           : R G N N N R   
R G N N N R    : 4) R G N -> G R N   : G R N N N R   
G R N N N R    : 5) G R -> C S       : C S N N N R   
C S N N N R    : 6) S N -> K O       : C K O N N R   
C K O N N R    : 7) O N -> L I       : C K L I N R   
C K L I N R    : 8) I N -> D E       : C K L D E R   
C K L D E R    : 9) D E R -> H D R   : C K L H D R   
C K L H D R    : 10) L H D -> H L N  : C K H L N R   
C K H L N R    : 11) K H L -> H K K  : C H K K N R   
C H K K N R    : 12) H K -> K Q      : C K Q K N R   
C K Q K N R    : 13) Q K -> K Q      : C K K Q N R   
C K K Q N R    : 14) Q N -> K J      : C K K K J R   
C K K K J R    : 15) K J R -> M K R  : C K K M K R   
C K K M K R    : 20) M K -> M a M    : C K K M a M R 
C K K M a M R  : 21) M R -> M        : C K K M a M   
C K K M a M    : 19) a M -> a        : C K K M a     
C K K M a      : 16) K M -> M a M    : C K M a M a   
C K M a M a    : 18) M a -> a        : C K M a a     
C K M a a      : 16) K M -> M a M    : C M a M a a   
C M a M a a    : 18) M a -> a        : C M a a a     
C M a a a      : 17) C M -> M        : M a a a       
M a a a        : 18) M a -> a        : a a a         
```

```bash
python3 pctm.py -ug -w aaaaa

Check by Unrestricted Grammar: True is done in 0:00:00.032999 seconds

A                  : 1) A -> R P N R     : R P N R           
R P N R            : 2) P -> P N         : R P N N R         
R P N N R          : 2) P -> P N         : R P N N N R       
R P N N N R        : 2) P -> P N         : R P N N N N R     
R P N N N N R      : 2) P -> P N         : R P N N N N N R   
R P N N N N N R    : 3) P -> G           : R G N N N N N R   
R G N N N N N R    : 4) R G N -> G R N   : G R N N N N N R   
G R N N N N N R    : 5) G R -> C S       : C S N N N N N R   
C S N N N N N R    : 6) S N -> K O       : C K O N N N N R   
C K O N N N N R    : 7) O N -> L I       : C K L I N N N R   
C K L I N N N R    : 8) I N -> D E       : C K L D E N N R   
C K L D E N N R    : 22) D E N -> F D D  : C K L F D D N R   
C K L F D D N R    : 23) L F D -> F L D  : C K F L D D N R   
C K F L D D N R    : 24) K F L -> F K L  : C F K L D D N R   
C F K L D D N R    : 25) F K -> L E      : C L E L D D N R   
C L E L D D N R    : 26) E L -> L E      : C L L E D D N R   
C L L E D D N R    : 27) E D -> D E      : C L L D E D N R   
C L L D E D N R    : 27) E D -> D E      : C L L D D E N R   
C L L D D E N R    : 22) D E N -> F D D  : C L L D F D D R   
C L L D F D D R    : 28) D F D -> F D D  : C L L F D D D R   
C L L F D D D R    : 23) L F D -> F L D  : C L F L D D D R   
C L F L D D D R    : 29) L F L -> F L L  : C F L L D D D R   
C F L L D D D R    : 30) C F L -> F C L  : F C L L D D D R   
F C L L D D D R    : 31) F C -> C T      : C T L L D D D R   
C T L L D D D R    : 32) T L -> K T      : C K T L D D D R   
C K T L D D D R    : 32) T L -> K T      : C K K T D D D R   
C K K T D D D R    : 33) K T D -> F K D  : C K F K D D D R   
C K F K D D D R    : 25) F K -> L E      : C K L E D D D R   
C K L E D D D R    : 27) E D -> D E      : C K L D E D D R   
C K L D E D D R    : 27) E D -> D E      : C K L D D E D R   
C K L D D E D R    : 27) E D -> D E      : C K L D D D E R   
C K L D D D E R    : 9) D E R -> H D R   : C K L D D H D R   
C K L D D H D R    : 34) D H D -> H D N  : C K L D H D N R   
C K L D H D N R    : 34) D H D -> H D N  : C K L H D N N R   
C K L H D N N R    : 10) L H D -> H L N  : C K H L N N N R   
C K H L N N N R    : 11) K H L -> H K K  : C H K K N N N R   
C H K K N N N R    : 12) H K -> K Q      : C K Q K N N N R   
C K Q K N N N R    : 13) Q K -> K Q      : C K K Q N N N R   
C K K Q N N N R    : 14) Q N -> K J      : C K K K J N N R   
C K K K J N N R    : 35) K J N -> F K D  : C K K F K D N R   
C K K F K D N R    : 25) F K -> L E      : C K K L E D N R   
C K K L E D N R    : 27) E D -> D E      : C K K L D E N R   
C K K L D E N R    : 22) D E N -> F D D  : C K K L F D D R   
C K K L F D D R    : 23) L F D -> F L D  : C K K F L D D R   
C K K F L D D R    : 24) K F L -> F K L  : C K F K L D D R   
C K F K L D D R    : 25) F K -> L E      : C K L E L D D R   
C K L E L D D R    : 26) E L -> L E      : C K L L E D D R   
C K L L E D D R    : 27) E D -> D E      : C K L L D E D R   
C K L L D E D R    : 27) E D -> D E      : C K L L D D E R   
C K L L D D E R    : 9) D E R -> H D R   : C K L L D H D R   
C K L L D H D R    : 34) D H D -> H D N  : C K L L H D N R   
C K L L H D N R    : 10) L H D -> H L N  : C K L H L N N R   
C K L H L N N R    : 36) L H L -> H L K  : C K H L K N N R   
C K H L K N N R    : 11) K H L -> H K K  : C H K K K N N R   
C H K K K N N R    : 12) H K -> K Q      : C K Q K K N N R   
C K Q K K N N R    : 13) Q K -> K Q      : C K K Q K N N R   
C K K Q K N N R    : 13) Q K -> K Q      : C K K K Q N N R   
C K K K Q N N R    : 14) Q N -> K J      : C K K K K J N R   
C K K K K J N R    : 35) K J N -> F K D  : C K K K F K D R   
C K K K F K D R    : 25) F K -> L E      : C K K K L E D R   
C K K K L E D R    : 27) E D -> D E      : C K K K L D E R   
C K K K L D E R    : 9) D E R -> H D R   : C K K K L H D R   
C K K K L H D R    : 10) L H D -> H L N  : C K K K H L N R   
C K K K H L N R    : 11) K H L -> H K K  : C K K H K K N R   
C K K H K K N R    : 12) H K -> K Q      : C K K K Q K N R   
C K K K Q K N R    : 13) Q K -> K Q      : C K K K K Q N R   
C K K K K Q N R    : 14) Q N -> K J      : C K K K K K J R   
C K K K K K J R    : 15) K J R -> M K R  : C K K K K M K R   
C K K K K M K R    : 20) M K -> M a M    : C K K K K M a M R 
C K K K K M a M R  : 21) M R -> M        : C K K K K M a M   
C K K K K M a M    : 19) a M -> a        : C K K K K M a     
C K K K K M a      : 16) K M -> M a M    : C K K K M a M a   
C K K K M a M a    : 18) M a -> a        : C K K K M a a     
C K K K M a a      : 16) K M -> M a M    : C K K M a M a a   
C K K M a M a a    : 18) M a -> a        : C K K M a a a     
C K K M a a a      : 16) K M -> M a M    : C K M a M a a a   
C K M a M a a a    : 18) M a -> a        : C K M a a a a     
C K M a a a a      : 16) K M -> M a M    : C M a M a a a a   
C M a M a a a a    : 18) M a -> a        : C M a a a a a     
C M a a a a a      : 17) C M -> M        : M a a a a a       
M a a a a a        : 18) M a -> a        : a a a a a         
```

```bash
 python3 pctm.py -ug -w aaaaaaa

Check by Unrestricted Grammar: True is done in 0:00:00.159566 seconds

A                      : 1) A -> R P N R     : R P N R               
R P N R                : 2) P -> P N         : R P N N R             
R P N N R              : 2) P -> P N         : R P N N N R           
R P N N N R            : 2) P -> P N         : R P N N N N R         
R P N N N N R          : 2) P -> P N         : R P N N N N N R       
R P N N N N N R        : 2) P -> P N         : R P N N N N N N R     
R P N N N N N N R      : 2) P -> P N         : R P N N N N N N N R   
R P N N N N N N N R    : 3) P -> G           : R G N N N N N N N R   
R G N N N N N N N R    : 4) R G N -> G R N   : G R N N N N N N N R   
G R N N N N N N N R    : 5) G R -> C S       : C S N N N N N N N R   
C S N N N N N N N R    : 6) S N -> K O       : C K O N N N N N N R   
C K O N N N N N N R    : 7) O N -> L I       : C K L I N N N N N R   
C K L I N N N N N R    : 8) I N -> D E       : C K L D E N N N N R   
C K L D E N N N N R    : 22) D E N -> F D D  : C K L F D D N N N R   
C K L F D D N N N R    : 23) L F D -> F L D  : C K F L D D N N N R   
C K F L D D N N N R    : 24) K F L -> F K L  : C F K L D D N N N R   
C F K L D D N N N R    : 25) F K -> L E      : C L E L D D N N N R   
C L E L D D N N N R    : 26) E L -> L E      : C L L E D D N N N R   
C L L E D D N N N R    : 27) E D -> D E      : C L L D E D N N N R   
C L L D E D N N N R    : 27) E D -> D E      : C L L D D E N N N R   
C L L D D E N N N R    : 22) D E N -> F D D  : C L L D F D D N N R   
C L L D F D D N N R    : 28) D F D -> F D D  : C L L F D D D N N R   
C L L F D D D N N R    : 23) L F D -> F L D  : C L F L D D D N N R   
C L F L D D D N N R    : 29) L F L -> F L L  : C F L L D D D N N R   
C F L L D D D N N R    : 30) C F L -> F C L  : F C L L D D D N N R   
F C L L D D D N N R    : 31) F C -> C T      : C T L L D D D N N R   
C T L L D D D N N R    : 32) T L -> K T      : C K T L D D D N N R   
C K T L D D D N N R    : 32) T L -> K T      : C K K T D D D N N R   
C K K T D D D N N R    : 33) K T D -> F K D  : C K F K D D D N N R   
C K F K D D D N N R    : 25) F K -> L E      : C K L E D D D N N R   
C K L E D D D N N R    : 27) E D -> D E      : C K L D E D D N N R   
C K L D E D D N N R    : 27) E D -> D E      : C K L D D E D N N R   
C K L D D E D N N R    : 27) E D -> D E      : C K L D D D E N N R   
C K L D D D E N N R    : 22) D E N -> F D D  : C K L D D F D D N R   
C K L D D F D D N R    : 28) D F D -> F D D  : C K L D F D D D N R   
C K L D F D D D N R    : 28) D F D -> F D D  : C K L F D D D D N R   
C K L F D D D D N R    : 23) L F D -> F L D  : C K F L D D D D N R   
C K F L D D D D N R    : 24) K F L -> F K L  : C F K L D D D D N R   
C F K L D D D D N R    : 25) F K -> L E      : C L E L D D D D N R   
C L E L D D D D N R    : 26) E L -> L E      : C L L E D D D D N R   
C L L E D D D D N R    : 27) E D -> D E      : C L L D E D D D N R   
C L L D E D D D N R    : 27) E D -> D E      : C L L D D E D D N R   
C L L D D E D D N R    : 27) E D -> D E      : C L L D D D E D N R   
C L L D D D E D N R    : 27) E D -> D E      : C L L D D D D E N R   
C L L D D D D E N R    : 22) D E N -> F D D  : C L L D D D F D D R   
C L L D D D F D D R    : 28) D F D -> F D D  : C L L D D F D D D R   
C L L D D F D D D R    : 28) D F D -> F D D  : C L L D F D D D D R   
C L L D F D D D D R    : 28) D F D -> F D D  : C L L F D D D D D R   
C L L F D D D D D R    : 23) L F D -> F L D  : C L F L D D D D D R   
C L F L D D D D D R    : 29) L F L -> F L L  : C F L L D D D D D R   
C F L L D D D D D R    : 30) C F L -> F C L  : F C L L D D D D D R   
F C L L D D D D D R    : 31) F C -> C T      : C T L L D D D D D R   
C T L L D D D D D R    : 32) T L -> K T      : C K T L D D D D D R   
C K T L D D D D D R    : 32) T L -> K T      : C K K T D D D D D R   
C K K T D D D D D R    : 33) K T D -> F K D  : C K F K D D D D D R   
C K F K D D D D D R    : 25) F K -> L E      : C K L E D D D D D R   
C K L E D D D D D R    : 27) E D -> D E      : C K L D E D D D D R   
C K L D E D D D D R    : 27) E D -> D E      : C K L D D E D D D R   
C K L D D E D D D R    : 27) E D -> D E      : C K L D D D E D D R   
C K L D D D E D D R    : 27) E D -> D E      : C K L D D D D E D R   
C K L D D D D E D R    : 27) E D -> D E      : C K L D D D D D E R   
C K L D D D D D E R    : 9) D E R -> H D R   : C K L D D D D H D R   
C K L D D D D H D R    : 34) D H D -> H D N  : C K L D D D H D N R   
C K L D D D H D N R    : 34) D H D -> H D N  : C K L D D H D N N R   
C K L D D H D N N R    : 34) D H D -> H D N  : C K L D H D N N N R   
C K L D H D N N N R    : 34) D H D -> H D N  : C K L H D N N N N R   
C K L H D N N N N R    : 10) L H D -> H L N  : C K H L N N N N N R   
C K H L N N N N N R    : 11) K H L -> H K K  : C H K K N N N N N R   
C H K K N N N N N R    : 12) H K -> K Q      : C K Q K N N N N N R   
C K Q K N N N N N R    : 13) Q K -> K Q      : C K K Q N N N N N R   
C K K Q N N N N N R    : 14) Q N -> K J      : C K K K J N N N N R   
C K K K J N N N N R    : 35) K J N -> F K D  : C K K F K D N N N R   
C K K F K D N N N R    : 25) F K -> L E      : C K K L E D N N N R   
C K K L E D N N N R    : 27) E D -> D E      : C K K L D E N N N R   
C K K L D E N N N R    : 22) D E N -> F D D  : C K K L F D D N N R   
C K K L F D D N N R    : 23) L F D -> F L D  : C K K F L D D N N R   
C K K F L D D N N R    : 24) K F L -> F K L  : C K F K L D D N N R   
C K F K L D D N N R    : 25) F K -> L E      : C K L E L D D N N R   
C K L E L D D N N R    : 26) E L -> L E      : C K L L E D D N N R   
C K L L E D D N N R    : 27) E D -> D E      : C K L L D E D N N R   
C K L L D E D N N R    : 27) E D -> D E      : C K L L D D E N N R   
C K L L D D E N N R    : 22) D E N -> F D D  : C K L L D F D D N R   
C K L L D F D D N R    : 28) D F D -> F D D  : C K L L F D D D N R   
C K L L F D D D N R    : 23) L F D -> F L D  : C K L F L D D D N R   
C K L F L D D D N R    : 29) L F L -> F L L  : C K F L L D D D N R   
C K F L L D D D N R    : 24) K F L -> F K L  : C F K L L D D D N R   
C F K L L D D D N R    : 25) F K -> L E      : C L E L L D D D N R   
C L E L L D D D N R    : 26) E L -> L E      : C L L E L D D D N R   
C L L E L D D D N R    : 26) E L -> L E      : C L L L E D D D N R   
C L L L E D D D N R    : 27) E D -> D E      : C L L L D E D D N R   
C L L L D E D D N R    : 27) E D -> D E      : C L L L D D E D N R   
C L L L D D E D N R    : 27) E D -> D E      : C L L L D D D E N R   
C L L L D D D E N R    : 22) D E N -> F D D  : C L L L D D F D D R   
C L L L D D F D D R    : 28) D F D -> F D D  : C L L L D F D D D R   
C L L L D F D D D R    : 28) D F D -> F D D  : C L L L F D D D D R   
C L L L F D D D D R    : 23) L F D -> F L D  : C L L F L D D D D R   
C L L F L D D D D R    : 29) L F L -> F L L  : C L F L L D D D D R   
C L F L L D D D D R    : 29) L F L -> F L L  : C F L L L D D D D R   
C F L L L D D D D R    : 30) C F L -> F C L  : F C L L L D D D D R   
F C L L L D D D D R    : 31) F C -> C T      : C T L L L D D D D R   
C T L L L D D D D R    : 32) T L -> K T      : C K T L L D D D D R   
C K T L L D D D D R    : 32) T L -> K T      : C K K T L D D D D R   
C K K T L D D D D R    : 32) T L -> K T      : C K K K T D D D D R   
C K K K T D D D D R    : 33) K T D -> F K D  : C K K F K D D D D R   
C K K F K D D D D R    : 25) F K -> L E      : C K K L E D D D D R   
C K K L E D D D D R    : 27) E D -> D E      : C K K L D E D D D R   
C K K L D E D D D R    : 27) E D -> D E      : C K K L D D E D D R   
C K K L D D E D D R    : 27) E D -> D E      : C K K L D D D E D R   
C K K L D D D E D R    : 27) E D -> D E      : C K K L D D D D E R   
C K K L D D D D E R    : 9) D E R -> H D R   : C K K L D D D H D R   
C K K L D D D H D R    : 34) D H D -> H D N  : C K K L D D H D N R   
C K K L D D H D N R    : 34) D H D -> H D N  : C K K L D H D N N R   
C K K L D H D N N R    : 34) D H D -> H D N  : C K K L H D N N N R   
C K K L H D N N N R    : 10) L H D -> H L N  : C K K H L N N N N R   
C K K H L N N N N R    : 11) K H L -> H K K  : C K H K K N N N N R   
C K H K K N N N N R    : 12) H K -> K Q      : C K K Q K N N N N R   
C K K Q K N N N N R    : 13) Q K -> K Q      : C K K K Q N N N N R   
C K K K Q N N N N R    : 14) Q N -> K J      : C K K K K J N N N R   
C K K K K J N N N R    : 35) K J N -> F K D  : C K K K F K D N N R   
C K K K F K D N N R    : 25) F K -> L E      : C K K K L E D N N R   
C K K K L E D N N R    : 27) E D -> D E      : C K K K L D E N N R   
C K K K L D E N N R    : 22) D E N -> F D D  : C K K K L F D D N R   
C K K K L F D D N R    : 23) L F D -> F L D  : C K K K F L D D N R   
C K K K F L D D N R    : 24) K F L -> F K L  : C K K F K L D D N R   
C K K F K L D D N R    : 25) F K -> L E      : C K K L E L D D N R   
C K K L E L D D N R    : 26) E L -> L E      : C K K L L E D D N R   
C K K L L E D D N R    : 27) E D -> D E      : C K K L L D E D N R   
C K K L L D E D N R    : 27) E D -> D E      : C K K L L D D E N R   
C K K L L D D E N R    : 22) D E N -> F D D  : C K K L L D F D D R   
C K K L L D F D D R    : 28) D F D -> F D D  : C K K L L F D D D R   
C K K L L F D D D R    : 23) L F D -> F L D  : C K K L F L D D D R   
C K K L F L D D D R    : 29) L F L -> F L L  : C K K F L L D D D R   
C K K F L L D D D R    : 24) K F L -> F K L  : C K F K L L D D D R   
C K F K L L D D D R    : 25) F K -> L E      : C K L E L L D D D R   
C K L E L L D D D R    : 26) E L -> L E      : C K L L E L D D D R   
C K L L E L D D D R    : 26) E L -> L E      : C K L L L E D D D R   
C K L L L E D D D R    : 27) E D -> D E      : C K L L L D E D D R   
C K L L L D E D D R    : 27) E D -> D E      : C K L L L D D E D R   
C K L L L D D E D R    : 27) E D -> D E      : C K L L L D D D E R   
C K L L L D D D E R    : 9) D E R -> H D R   : C K L L L D D H D R   
C K L L L D D H D R    : 34) D H D -> H D N  : C K L L L D H D N R   
C K L L L D H D N R    : 34) D H D -> H D N  : C K L L L H D N N R   
C K L L L H D N N R    : 10) L H D -> H L N  : C K L L H L N N N R   
C K L L H L N N N R    : 36) L H L -> H L K  : C K L H L K N N N R   
C K L H L K N N N R    : 36) L H L -> H L K  : C K H L K K N N N R   
C K H L K K N N N R    : 11) K H L -> H K K  : C H K K K K N N N R   
C H K K K K N N N R    : 12) H K -> K Q      : C K Q K K K N N N R   
C K Q K K K N N N R    : 13) Q K -> K Q      : C K K Q K K N N N R   
C K K Q K K N N N R    : 13) Q K -> K Q      : C K K K Q K N N N R   
C K K K Q K N N N R    : 13) Q K -> K Q      : C K K K K Q N N N R   
C K K K K Q N N N R    : 14) Q N -> K J      : C K K K K K J N N R   
C K K K K K J N N R    : 35) K J N -> F K D  : C K K K K F K D N R   
C K K K K F K D N R    : 25) F K -> L E      : C K K K K L E D N R   
C K K K K L E D N R    : 27) E D -> D E      : C K K K K L D E N R   
C K K K K L D E N R    : 22) D E N -> F D D  : C K K K K L F D D R   
C K K K K L F D D R    : 23) L F D -> F L D  : C K K K K F L D D R   
C K K K K F L D D R    : 24) K F L -> F K L  : C K K K F K L D D R   
C K K K F K L D D R    : 25) F K -> L E      : C K K K L E L D D R   
C K K K L E L D D R    : 26) E L -> L E      : C K K K L L E D D R   
C K K K L L E D D R    : 27) E D -> D E      : C K K K L L D E D R   
C K K K L L D E D R    : 27) E D -> D E      : C K K K L L D D E R   
C K K K L L D D E R    : 9) D E R -> H D R   : C K K K L L D H D R   
C K K K L L D H D R    : 34) D H D -> H D N  : C K K K L L H D N R   
C K K K L L H D N R    : 10) L H D -> H L N  : C K K K L H L N N R   
C K K K L H L N N R    : 36) L H L -> H L K  : C K K K H L K N N R   
C K K K H L K N N R    : 11) K H L -> H K K  : C K K H K K K N N R   
C K K H K K K N N R    : 12) H K -> K Q      : C K K K Q K K N N R   
C K K K Q K K N N R    : 13) Q K -> K Q      : C K K K K Q K N N R   
C K K K K Q K N N R    : 13) Q K -> K Q      : C K K K K K Q N N R   
C K K K K K Q N N R    : 14) Q N -> K J      : C K K K K K K J N R   
C K K K K K K J N R    : 35) K J N -> F K D  : C K K K K K F K D R   
C K K K K K F K D R    : 25) F K -> L E      : C K K K K K L E D R   
C K K K K K L E D R    : 27) E D -> D E      : C K K K K K L D E R   
C K K K K K L D E R    : 9) D E R -> H D R   : C K K K K K L H D R   
C K K K K K L H D R    : 10) L H D -> H L N  : C K K K K K H L N R   
C K K K K K H L N R    : 11) K H L -> H K K  : C K K K K H K K N R   
C K K K K H K K N R    : 12) H K -> K Q      : C K K K K K Q K N R   
C K K K K K Q K N R    : 13) Q K -> K Q      : C K K K K K K Q N R   
C K K K K K K Q N R    : 14) Q N -> K J      : C K K K K K K K J R   
C K K K K K K K J R    : 15) K J R -> M K R  : C K K K K K K M K R   
C K K K K K K M K R    : 20) M K -> M a M    : C K K K K K K M a M R 
C K K K K K K M a M R  : 21) M R -> M        : C K K K K K K M a M   
C K K K K K K M a M    : 19) a M -> a        : C K K K K K K M a     
C K K K K K K M a      : 16) K M -> M a M    : C K K K K K M a M a   
C K K K K K M a M a    : 18) M a -> a        : C K K K K K M a a     
C K K K K K M a a      : 16) K M -> M a M    : C K K K K M a M a a   
C K K K K M a M a a    : 18) M a -> a        : C K K K K M a a a     
C K K K K M a a a      : 16) K M -> M a M    : C K K K M a M a a a   
C K K K M a M a a a    : 18) M a -> a        : C K K K M a a a a     
C K K K M a a a a      : 16) K M -> M a M    : C K K M a M a a a a   
C K K M a M a a a a    : 18) M a -> a        : C K K M a a a a a     
C K K M a a a a a      : 16) K M -> M a M    : C K M a M a a a a a   
C K M a M a a a a a    : 18) M a -> a        : C K M a a a a a a     
C K M a a a a a a      : 16) K M -> M a M    : C M a M a a a a a a   
C M a M a a a a a a    : 18) M a -> a        : C M a a a a a a a     
C M a a a a a a a      : 17) C M -> M        : M a a a a a a a       
M a a a a a a a        : 18) M a -> a        : a a a a a a a         
```

```bash
python3 pctm.py -ug -w aaaaaaaaaaa

Check by Unrestricted Grammar: True is done in 0:00:00.860178 seconds

A                              : 1) A -> R P N R     : R P N R                       
R P N R                        : 2) P -> P N         : R P N N R                     
R P N N R                      : 2) P -> P N         : R P N N N R                   
R P N N N R                    : 2) P -> P N         : R P N N N N R                 
R P N N N N R                  : 2) P -> P N         : R P N N N N N R               
R P N N N N N R                : 2) P -> P N         : R P N N N N N N R             
R P N N N N N N R              : 2) P -> P N         : R P N N N N N N N R           
R P N N N N N N N R            : 2) P -> P N         : R P N N N N N N N N R         
R P N N N N N N N N R          : 2) P -> P N         : R P N N N N N N N N N R       
R P N N N N N N N N N R        : 2) P -> P N         : R P N N N N N N N N N N R     
R P N N N N N N N N N N R      : 2) P -> P N         : R P N N N N N N N N N N N R   
R P N N N N N N N N N N N R    : 3) P -> G           : R G N N N N N N N N N N N R   
R G N N N N N N N N N N N R    : 4) R G N -> G R N   : G R N N N N N N N N N N N R   
G R N N N N N N N N N N N R    : 5) G R -> C S       : C S N N N N N N N N N N N R   
C S N N N N N N N N N N N R    : 6) S N -> K O       : C K O N N N N N N N N N N R   
C K O N N N N N N N N N N R    : 7) O N -> L I       : C K L I N N N N N N N N N R   
C K L I N N N N N N N N N R    : 8) I N -> D E       : C K L D E N N N N N N N N R   
C K L D E N N N N N N N N R    : 22) D E N -> F D D  : C K L F D D N N N N N N N R   
C K L F D D N N N N N N N R    : 23) L F D -> F L D  : C K F L D D N N N N N N N R   
C K F L D D N N N N N N N R    : 24) K F L -> F K L  : C F K L D D N N N N N N N R   
C F K L D D N N N N N N N R    : 25) F K -> L E      : C L E L D D N N N N N N N R   
C L E L D D N N N N N N N R    : 26) E L -> L E      : C L L E D D N N N N N N N R   
C L L E D D N N N N N N N R    : 27) E D -> D E      : C L L D E D N N N N N N N R   
C L L D E D N N N N N N N R    : 27) E D -> D E      : C L L D D E N N N N N N N R   
C L L D D E N N N N N N N R    : 22) D E N -> F D D  : C L L D F D D N N N N N N R   
C L L D F D D N N N N N N R    : 28) D F D -> F D D  : C L L F D D D N N N N N N R   
C L L F D D D N N N N N N R    : 23) L F D -> F L D  : C L F L D D D N N N N N N R   
C L F L D D D N N N N N N R    : 29) L F L -> F L L  : C F L L D D D N N N N N N R   
C F L L D D D N N N N N N R    : 30) C F L -> F C L  : F C L L D D D N N N N N N R   
F C L L D D D N N N N N N R    : 31) F C -> C T      : C T L L D D D N N N N N N R   
C T L L D D D N N N N N N R    : 32) T L -> K T      : C K T L D D D N N N N N N R   
C K T L D D D N N N N N N R    : 32) T L -> K T      : C K K T D D D N N N N N N R   
C K K T D D D N N N N N N R    : 33) K T D -> F K D  : C K F K D D D N N N N N N R   
C K F K D D D N N N N N N R    : 25) F K -> L E      : C K L E D D D N N N N N N R   
C K L E D D D N N N N N N R    : 27) E D -> D E      : C K L D E D D N N N N N N R   
C K L D E D D N N N N N N R    : 27) E D -> D E      : C K L D D E D N N N N N N R   
C K L D D E D N N N N N N R    : 27) E D -> D E      : C K L D D D E N N N N N N R   
C K L D D D E N N N N N N R    : 22) D E N -> F D D  : C K L D D F D D N N N N N R   
C K L D D F D D N N N N N R    : 28) D F D -> F D D  : C K L D F D D D N N N N N R   
C K L D F D D D N N N N N R    : 28) D F D -> F D D  : C K L F D D D D N N N N N R   
C K L F D D D D N N N N N R    : 23) L F D -> F L D  : C K F L D D D D N N N N N R   
C K F L D D D D N N N N N R    : 24) K F L -> F K L  : C F K L D D D D N N N N N R   
C F K L D D D D N N N N N R    : 25) F K -> L E      : C L E L D D D D N N N N N R   
C L E L D D D D N N N N N R    : 26) E L -> L E      : C L L E D D D D N N N N N R   
C L L E D D D D N N N N N R    : 27) E D -> D E      : C L L D E D D D N N N N N R   
C L L D E D D D N N N N N R    : 27) E D -> D E      : C L L D D E D D N N N N N R   
C L L D D E D D N N N N N R    : 27) E D -> D E      : C L L D D D E D N N N N N R   
C L L D D D E D N N N N N R    : 27) E D -> D E      : C L L D D D D E N N N N N R   
C L L D D D D E N N N N N R    : 22) D E N -> F D D  : C L L D D D F D D N N N N R   
C L L D D D F D D N N N N R    : 28) D F D -> F D D  : C L L D D F D D D N N N N R   
C L L D D F D D D N N N N R    : 28) D F D -> F D D  : C L L D F D D D D N N N N R   
C L L D F D D D D N N N N R    : 28) D F D -> F D D  : C L L F D D D D D N N N N R   
C L L F D D D D D N N N N R    : 23) L F D -> F L D  : C L F L D D D D D N N N N R   
C L F L D D D D D N N N N R    : 29) L F L -> F L L  : C F L L D D D D D N N N N R   
C F L L D D D D D N N N N R    : 30) C F L -> F C L  : F C L L D D D D D N N N N R   
F C L L D D D D D N N N N R    : 31) F C -> C T      : C T L L D D D D D N N N N R   
C T L L D D D D D N N N N R    : 32) T L -> K T      : C K T L D D D D D N N N N R   
C K T L D D D D D N N N N R    : 32) T L -> K T      : C K K T D D D D D N N N N R   
C K K T D D D D D N N N N R    : 33) K T D -> F K D  : C K F K D D D D D N N N N R   
C K F K D D D D D N N N N R    : 25) F K -> L E      : C K L E D D D D D N N N N R   
C K L E D D D D D N N N N R    : 27) E D -> D E      : C K L D E D D D D N N N N R   
C K L D E D D D D N N N N R    : 27) E D -> D E      : C K L D D E D D D N N N N R   
C K L D D E D D D N N N N R    : 27) E D -> D E      : C K L D D D E D D N N N N R   
C K L D D D E D D N N N N R    : 27) E D -> D E      : C K L D D D D E D N N N N R   
C K L D D D D E D N N N N R    : 27) E D -> D E      : C K L D D D D D E N N N N R   
C K L D D D D D E N N N N R    : 22) D E N -> F D D  : C K L D D D D F D D N N N R   
C K L D D D D F D D N N N R    : 28) D F D -> F D D  : C K L D D D F D D D N N N R   
C K L D D D F D D D N N N R    : 28) D F D -> F D D  : C K L D D F D D D D N N N R   
C K L D D F D D D D N N N R    : 28) D F D -> F D D  : C K L D F D D D D D N N N R   
C K L D F D D D D D N N N R    : 28) D F D -> F D D  : C K L F D D D D D D N N N R   
C K L F D D D D D D N N N R    : 23) L F D -> F L D  : C K F L D D D D D D N N N R   
C K F L D D D D D D N N N R    : 24) K F L -> F K L  : C F K L D D D D D D N N N R   
C F K L D D D D D D N N N R    : 25) F K -> L E      : C L E L D D D D D D N N N R   
C L E L D D D D D D N N N R    : 26) E L -> L E      : C L L E D D D D D D N N N R   
C L L E D D D D D D N N N R    : 27) E D -> D E      : C L L D E D D D D D N N N R   
C L L D E D D D D D N N N R    : 27) E D -> D E      : C L L D D E D D D D N N N R   
C L L D D E D D D D N N N R    : 27) E D -> D E      : C L L D D D E D D D N N N R   
C L L D D D E D D D N N N R    : 27) E D -> D E      : C L L D D D D E D D N N N R   
C L L D D D D E D D N N N R    : 27) E D -> D E      : C L L D D D D D E D N N N R   
C L L D D D D D E D N N N R    : 27) E D -> D E      : C L L D D D D D D E N N N R   
C L L D D D D D D E N N N R    : 22) D E N -> F D D  : C L L D D D D D F D D N N R   
C L L D D D D D F D D N N R    : 28) D F D -> F D D  : C L L D D D D F D D D N N R   
C L L D D D D F D D D N N R    : 28) D F D -> F D D  : C L L D D D F D D D D N N R   
C L L D D D F D D D D N N R    : 28) D F D -> F D D  : C L L D D F D D D D D N N R   
C L L D D F D D D D D N N R    : 28) D F D -> F D D  : C L L D F D D D D D D N N R   
C L L D F D D D D D D N N R    : 28) D F D -> F D D  : C L L F D D D D D D D N N R   
C L L F D D D D D D D N N R    : 23) L F D -> F L D  : C L F L D D D D D D D N N R   
C L F L D D D D D D D N N R    : 29) L F L -> F L L  : C F L L D D D D D D D N N R   
C F L L D D D D D D D N N R    : 30) C F L -> F C L  : F C L L D D D D D D D N N R   
F C L L D D D D D D D N N R    : 31) F C -> C T      : C T L L D D D D D D D N N R   
C T L L D D D D D D D N N R    : 32) T L -> K T      : C K T L D D D D D D D N N R   
C K T L D D D D D D D N N R    : 32) T L -> K T      : C K K T D D D D D D D N N R   
C K K T D D D D D D D N N R    : 33) K T D -> F K D  : C K F K D D D D D D D N N R   
C K F K D D D D D D D N N R    : 25) F K -> L E      : C K L E D D D D D D D N N R   
C K L E D D D D D D D N N R    : 27) E D -> D E      : C K L D E D D D D D D N N R   
C K L D E D D D D D D N N R    : 27) E D -> D E      : C K L D D E D D D D D N N R   
C K L D D E D D D D D N N R    : 27) E D -> D E      : C K L D D D E D D D D N N R   
C K L D D D E D D D D N N R    : 27) E D -> D E      : C K L D D D D E D D D N N R   
C K L D D D D E D D D N N R    : 27) E D -> D E      : C K L D D D D D E D D N N R   
C K L D D D D D E D D N N R    : 27) E D -> D E      : C K L D D D D D D E D N N R   
C K L D D D D D D E D N N R    : 27) E D -> D E      : C K L D D D D D D D E N N R   
C K L D D D D D D D E N N R    : 22) D E N -> F D D  : C K L D D D D D D F D D N R   
C K L D D D D D D F D D N R    : 28) D F D -> F D D  : C K L D D D D D F D D D N R   
C K L D D D D D F D D D N R    : 28) D F D -> F D D  : C K L D D D D F D D D D N R   
C K L D D D D F D D D D N R    : 28) D F D -> F D D  : C K L D D D F D D D D D N R   
C K L D D D F D D D D D N R    : 28) D F D -> F D D  : C K L D D F D D D D D D N R   
C K L D D F D D D D D D N R    : 28) D F D -> F D D  : C K L D F D D D D D D D N R   
C K L D F D D D D D D D N R    : 28) D F D -> F D D  : C K L F D D D D D D D D N R   
C K L F D D D D D D D D N R    : 23) L F D -> F L D  : C K F L D D D D D D D D N R   
C K F L D D D D D D D D N R    : 24) K F L -> F K L  : C F K L D D D D D D D D N R   
C F K L D D D D D D D D N R    : 25) F K -> L E      : C L E L D D D D D D D D N R   
C L E L D D D D D D D D N R    : 26) E L -> L E      : C L L E D D D D D D D D N R   
C L L E D D D D D D D D N R    : 27) E D -> D E      : C L L D E D D D D D D D N R   
C L L D E D D D D D D D N R    : 27) E D -> D E      : C L L D D E D D D D D D N R   
C L L D D E D D D D D D N R    : 27) E D -> D E      : C L L D D D E D D D D D N R   
C L L D D D E D D D D D N R    : 27) E D -> D E      : C L L D D D D E D D D D N R   
C L L D D D D E D D D D N R    : 27) E D -> D E      : C L L D D D D D E D D D N R   
C L L D D D D D E D D D N R    : 27) E D -> D E      : C L L D D D D D D E D D N R   
C L L D D D D D D E D D N R    : 27) E D -> D E      : C L L D D D D D D D E D N R   
C L L D D D D D D D E D N R    : 27) E D -> D E      : C L L D D D D D D D D E N R   
C L L D D D D D D D D E N R    : 22) D E N -> F D D  : C L L D D D D D D D F D D R   
C L L D D D D D D D F D D R    : 28) D F D -> F D D  : C L L D D D D D D F D D D R   
C L L D D D D D D F D D D R    : 28) D F D -> F D D  : C L L D D D D D F D D D D R   
C L L D D D D D F D D D D R    : 28) D F D -> F D D  : C L L D D D D F D D D D D R   
C L L D D D D F D D D D D R    : 28) D F D -> F D D  : C L L D D D F D D D D D D R   
C L L D D D F D D D D D D R    : 28) D F D -> F D D  : C L L D D F D D D D D D D R   
C L L D D F D D D D D D D R    : 28) D F D -> F D D  : C L L D F D D D D D D D D R   
C L L D F D D D D D D D D R    : 28) D F D -> F D D  : C L L F D D D D D D D D D R   
C L L F D D D D D D D D D R    : 23) L F D -> F L D  : C L F L D D D D D D D D D R   
C L F L D D D D D D D D D R    : 29) L F L -> F L L  : C F L L D D D D D D D D D R   
C F L L D D D D D D D D D R    : 30) C F L -> F C L  : F C L L D D D D D D D D D R   
F C L L D D D D D D D D D R    : 31) F C -> C T      : C T L L D D D D D D D D D R   
C T L L D D D D D D D D D R    : 32) T L -> K T      : C K T L D D D D D D D D D R   
C K T L D D D D D D D D D R    : 32) T L -> K T      : C K K T D D D D D D D D D R   
C K K T D D D D D D D D D R    : 33) K T D -> F K D  : C K F K D D D D D D D D D R   
C K F K D D D D D D D D D R    : 25) F K -> L E      : C K L E D D D D D D D D D R   
C K L E D D D D D D D D D R    : 27) E D -> D E      : C K L D E D D D D D D D D R   
C K L D E D D D D D D D D R    : 27) E D -> D E      : C K L D D E D D D D D D D R   
C K L D D E D D D D D D D R    : 27) E D -> D E      : C K L D D D E D D D D D D R   
C K L D D D E D D D D D D R    : 27) E D -> D E      : C K L D D D D E D D D D D R   
C K L D D D D E D D D D D R    : 27) E D -> D E      : C K L D D D D D E D D D D R   
C K L D D D D D E D D D D R    : 27) E D -> D E      : C K L D D D D D D E D D D R   
C K L D D D D D D E D D D R    : 27) E D -> D E      : C K L D D D D D D D E D D R   
C K L D D D D D D D E D D R    : 27) E D -> D E      : C K L D D D D D D D D E D R   
C K L D D D D D D D D E D R    : 27) E D -> D E      : C K L D D D D D D D D D E R   
C K L D D D D D D D D D E R    : 9) D E R -> H D R   : C K L D D D D D D D D H D R   
C K L D D D D D D D D H D R    : 34) D H D -> H D N  : C K L D D D D D D D H D N R   
C K L D D D D D D D H D N R    : 34) D H D -> H D N  : C K L D D D D D D H D N N R   
C K L D D D D D D H D N N R    : 34) D H D -> H D N  : C K L D D D D D H D N N N R   
C K L D D D D D H D N N N R    : 34) D H D -> H D N  : C K L D D D D H D N N N N R   
C K L D D D D H D N N N N R    : 34) D H D -> H D N  : C K L D D D H D N N N N N R   
C K L D D D H D N N N N N R    : 34) D H D -> H D N  : C K L D D H D N N N N N N R   
C K L D D H D N N N N N N R    : 34) D H D -> H D N  : C K L D H D N N N N N N N R   
C K L D H D N N N N N N N R    : 34) D H D -> H D N  : C K L H D N N N N N N N N R   
C K L H D N N N N N N N N R    : 10) L H D -> H L N  : C K H L N N N N N N N N N R   
C K H L N N N N N N N N N R    : 11) K H L -> H K K  : C H K K N N N N N N N N N R   
C H K K N N N N N N N N N R    : 12) H K -> K Q      : C K Q K N N N N N N N N N R   
C K Q K N N N N N N N N N R    : 13) Q K -> K Q      : C K K Q N N N N N N N N N R   
C K K Q N N N N N N N N N R    : 14) Q N -> K J      : C K K K J N N N N N N N N R   
C K K K J N N N N N N N N R    : 35) K J N -> F K D  : C K K F K D N N N N N N N R   
C K K F K D N N N N N N N R    : 25) F K -> L E      : C K K L E D N N N N N N N R   
C K K L E D N N N N N N N R    : 27) E D -> D E      : C K K L D E N N N N N N N R   
C K K L D E N N N N N N N R    : 22) D E N -> F D D  : C K K L F D D N N N N N N R   
C K K L F D D N N N N N N R    : 23) L F D -> F L D  : C K K F L D D N N N N N N R   
C K K F L D D N N N N N N R    : 24) K F L -> F K L  : C K F K L D D N N N N N N R   
C K F K L D D N N N N N N R    : 25) F K -> L E      : C K L E L D D N N N N N N R   
C K L E L D D N N N N N N R    : 26) E L -> L E      : C K L L E D D N N N N N N R   
C K L L E D D N N N N N N R    : 27) E D -> D E      : C K L L D E D N N N N N N R   
C K L L D E D N N N N N N R    : 27) E D -> D E      : C K L L D D E N N N N N N R   
C K L L D D E N N N N N N R    : 22) D E N -> F D D  : C K L L D F D D N N N N N R   
C K L L D F D D N N N N N R    : 28) D F D -> F D D  : C K L L F D D D N N N N N R   
C K L L F D D D N N N N N R    : 23) L F D -> F L D  : C K L F L D D D N N N N N R   
C K L F L D D D N N N N N R    : 29) L F L -> F L L  : C K F L L D D D N N N N N R   
C K F L L D D D N N N N N R    : 24) K F L -> F K L  : C F K L L D D D N N N N N R   
C F K L L D D D N N N N N R    : 25) F K -> L E      : C L E L L D D D N N N N N R   
C L E L L D D D N N N N N R    : 26) E L -> L E      : C L L E L D D D N N N N N R   
C L L E L D D D N N N N N R    : 26) E L -> L E      : C L L L E D D D N N N N N R   
C L L L E D D D N N N N N R    : 27) E D -> D E      : C L L L D E D D N N N N N R   
C L L L D E D D N N N N N R    : 27) E D -> D E      : C L L L D D E D N N N N N R   
C L L L D D E D N N N N N R    : 27) E D -> D E      : C L L L D D D E N N N N N R   
C L L L D D D E N N N N N R    : 22) D E N -> F D D  : C L L L D D F D D N N N N R   
C L L L D D F D D N N N N R    : 28) D F D -> F D D  : C L L L D F D D D N N N N R   
C L L L D F D D D N N N N R    : 28) D F D -> F D D  : C L L L F D D D D N N N N R   
C L L L F D D D D N N N N R    : 23) L F D -> F L D  : C L L F L D D D D N N N N R   
C L L F L D D D D N N N N R    : 29) L F L -> F L L  : C L F L L D D D D N N N N R   
C L F L L D D D D N N N N R    : 29) L F L -> F L L  : C F L L L D D D D N N N N R   
C F L L L D D D D N N N N R    : 30) C F L -> F C L  : F C L L L D D D D N N N N R   
F C L L L D D D D N N N N R    : 31) F C -> C T      : C T L L L D D D D N N N N R   
C T L L L D D D D N N N N R    : 32) T L -> K T      : C K T L L D D D D N N N N R   
C K T L L D D D D N N N N R    : 32) T L -> K T      : C K K T L D D D D N N N N R   
C K K T L D D D D N N N N R    : 32) T L -> K T      : C K K K T D D D D N N N N R   
C K K K T D D D D N N N N R    : 33) K T D -> F K D  : C K K F K D D D D N N N N R   
C K K F K D D D D N N N N R    : 25) F K -> L E      : C K K L E D D D D N N N N R   
C K K L E D D D D N N N N R    : 27) E D -> D E      : C K K L D E D D D N N N N R   
C K K L D E D D D N N N N R    : 27) E D -> D E      : C K K L D D E D D N N N N R   
C K K L D D E D D N N N N R    : 27) E D -> D E      : C K K L D D D E D N N N N R   
C K K L D D D E D N N N N R    : 27) E D -> D E      : C K K L D D D D E N N N N R   
C K K L D D D D E N N N N R    : 22) D E N -> F D D  : C K K L D D D F D D N N N R   
C K K L D D D F D D N N N R    : 28) D F D -> F D D  : C K K L D D F D D D N N N R   
C K K L D D F D D D N N N R    : 28) D F D -> F D D  : C K K L D F D D D D N N N R   
C K K L D F D D D D N N N R    : 28) D F D -> F D D  : C K K L F D D D D D N N N R   
C K K L F D D D D D N N N R    : 23) L F D -> F L D  : C K K F L D D D D D N N N R   
C K K F L D D D D D N N N R    : 24) K F L -> F K L  : C K F K L D D D D D N N N R   
C K F K L D D D D D N N N R    : 25) F K -> L E      : C K L E L D D D D D N N N R   
C K L E L D D D D D N N N R    : 26) E L -> L E      : C K L L E D D D D D N N N R   
C K L L E D D D D D N N N R    : 27) E D -> D E      : C K L L D E D D D D N N N R   
C K L L D E D D D D N N N R    : 27) E D -> D E      : C K L L D D E D D D N N N R   
C K L L D D E D D D N N N R    : 27) E D -> D E      : C K L L D D D E D D N N N R   
C K L L D D D E D D N N N R    : 27) E D -> D E      : C K L L D D D D E D N N N R   
C K L L D D D D E D N N N R    : 27) E D -> D E      : C K L L D D D D D E N N N R   
C K L L D D D D D E N N N R    : 22) D E N -> F D D  : C K L L D D D D F D D N N R   
C K L L D D D D F D D N N R    : 28) D F D -> F D D  : C K L L D D D F D D D N N R   
C K L L D D D F D D D N N R    : 28) D F D -> F D D  : C K L L D D F D D D D N N R   
C K L L D D F D D D D N N R    : 28) D F D -> F D D  : C K L L D F D D D D D N N R   
C K L L D F D D D D D N N R    : 28) D F D -> F D D  : C K L L F D D D D D D N N R   
C K L L F D D D D D D N N R    : 23) L F D -> F L D  : C K L F L D D D D D D N N R   
C K L F L D D D D D D N N R    : 29) L F L -> F L L  : C K F L L D D D D D D N N R   
C K F L L D D D D D D N N R    : 24) K F L -> F K L  : C F K L L D D D D D D N N R   
C F K L L D D D D D D N N R    : 25) F K -> L E      : C L E L L D D D D D D N N R   
C L E L L D D D D D D N N R    : 26) E L -> L E      : C L L E L D D D D D D N N R   
C L L E L D D D D D D N N R    : 26) E L -> L E      : C L L L E D D D D D D N N R   
C L L L E D D D D D D N N R    : 27) E D -> D E      : C L L L D E D D D D D N N R   
C L L L D E D D D D D N N R    : 27) E D -> D E      : C L L L D D E D D D D N N R   
C L L L D D E D D D D N N R    : 27) E D -> D E      : C L L L D D D E D D D N N R   
C L L L D D D E D D D N N R    : 27) E D -> D E      : C L L L D D D D E D D N N R   
C L L L D D D D E D D N N R    : 27) E D -> D E      : C L L L D D D D D E D N N R   
C L L L D D D D D E D N N R    : 27) E D -> D E      : C L L L D D D D D D E N N R   
C L L L D D D D D D E N N R    : 22) D E N -> F D D  : C L L L D D D D D F D D N R   
C L L L D D D D D F D D N R    : 28) D F D -> F D D  : C L L L D D D D F D D D N R   
C L L L D D D D F D D D N R    : 28) D F D -> F D D  : C L L L D D D F D D D D N R   
C L L L D D D F D D D D N R    : 28) D F D -> F D D  : C L L L D D F D D D D D N R   
C L L L D D F D D D D D N R    : 28) D F D -> F D D  : C L L L D F D D D D D D N R   
C L L L D F D D D D D D N R    : 28) D F D -> F D D  : C L L L F D D D D D D D N R   
C L L L F D D D D D D D N R    : 23) L F D -> F L D  : C L L F L D D D D D D D N R   
C L L F L D D D D D D D N R    : 29) L F L -> F L L  : C L F L L D D D D D D D N R   
C L F L L D D D D D D D N R    : 29) L F L -> F L L  : C F L L L D D D D D D D N R   
C F L L L D D D D D D D N R    : 30) C F L -> F C L  : F C L L L D D D D D D D N R   
F C L L L D D D D D D D N R    : 31) F C -> C T      : C T L L L D D D D D D D N R   
C T L L L D D D D D D D N R    : 32) T L -> K T      : C K T L L D D D D D D D N R   
C K T L L D D D D D D D N R    : 32) T L -> K T      : C K K T L D D D D D D D N R   
C K K T L D D D D D D D N R    : 32) T L -> K T      : C K K K T D D D D D D D N R   
C K K K T D D D D D D D N R    : 33) K T D -> F K D  : C K K F K D D D D D D D N R   
C K K F K D D D D D D D N R    : 25) F K -> L E      : C K K L E D D D D D D D N R   
C K K L E D D D D D D D N R    : 27) E D -> D E      : C K K L D E D D D D D D N R   
C K K L D E D D D D D D N R    : 27) E D -> D E      : C K K L D D E D D D D D N R   
C K K L D D E D D D D D N R    : 27) E D -> D E      : C K K L D D D E D D D D N R   
C K K L D D D E D D D D N R    : 27) E D -> D E      : C K K L D D D D E D D D N R   
C K K L D D D D E D D D N R    : 27) E D -> D E      : C K K L D D D D D E D D N R   
C K K L D D D D D E D D N R    : 27) E D -> D E      : C K K L D D D D D D E D N R   
C K K L D D D D D D E D N R    : 27) E D -> D E      : C K K L D D D D D D D E N R   
C K K L D D D D D D D E N R    : 22) D E N -> F D D  : C K K L D D D D D D F D D R   
C K K L D D D D D D F D D R    : 28) D F D -> F D D  : C K K L D D D D D F D D D R   
C K K L D D D D D F D D D R    : 28) D F D -> F D D  : C K K L D D D D F D D D D R   
C K K L D D D D F D D D D R    : 28) D F D -> F D D  : C K K L D D D F D D D D D R   
C K K L D D D F D D D D D R    : 28) D F D -> F D D  : C K K L D D F D D D D D D R   
C K K L D D F D D D D D D R    : 28) D F D -> F D D  : C K K L D F D D D D D D D R   
C K K L D F D D D D D D D R    : 28) D F D -> F D D  : C K K L F D D D D D D D D R   
C K K L F D D D D D D D D R    : 23) L F D -> F L D  : C K K F L D D D D D D D D R   
C K K F L D D D D D D D D R    : 24) K F L -> F K L  : C K F K L D D D D D D D D R   
C K F K L D D D D D D D D R    : 25) F K -> L E      : C K L E L D D D D D D D D R   
C K L E L D D D D D D D D R    : 26) E L -> L E      : C K L L E D D D D D D D D R   
C K L L E D D D D D D D D R    : 27) E D -> D E      : C K L L D E D D D D D D D R   
C K L L D E D D D D D D D R    : 27) E D -> D E      : C K L L D D E D D D D D D R   
C K L L D D E D D D D D D R    : 27) E D -> D E      : C K L L D D D E D D D D D R   
C K L L D D D E D D D D D R    : 27) E D -> D E      : C K L L D D D D E D D D D R   
C K L L D D D D E D D D D R    : 27) E D -> D E      : C K L L D D D D D E D D D R   
C K L L D D D D D E D D D R    : 27) E D -> D E      : C K L L D D D D D D E D D R   
C K L L D D D D D D E D D R    : 27) E D -> D E      : C K L L D D D D D D D E D R   
C K L L D D D D D D D E D R    : 27) E D -> D E      : C K L L D D D D D D D D E R   
C K L L D D D D D D D D E R    : 9) D E R -> H D R   : C K L L D D D D D D D H D R   
C K L L D D D D D D D H D R    : 34) D H D -> H D N  : C K L L D D D D D D H D N R   
C K L L D D D D D D H D N R    : 34) D H D -> H D N  : C K L L D D D D D H D N N R   
C K L L D D D D D H D N N R    : 34) D H D -> H D N  : C K L L D D D D H D N N N R   
C K L L D D D D H D N N N R    : 34) D H D -> H D N  : C K L L D D D H D N N N N R   
C K L L D D D H D N N N N R    : 34) D H D -> H D N  : C K L L D D H D N N N N N R   
C K L L D D H D N N N N N R    : 34) D H D -> H D N  : C K L L D H D N N N N N N R   
C K L L D H D N N N N N N R    : 34) D H D -> H D N  : C K L L H D N N N N N N N R   
C K L L H D N N N N N N N R    : 10) L H D -> H L N  : C K L H L N N N N N N N N R   
C K L H L N N N N N N N N R    : 36) L H L -> H L K  : C K H L K N N N N N N N N R   
C K H L K N N N N N N N N R    : 11) K H L -> H K K  : C H K K K N N N N N N N N R   
C H K K K N N N N N N N N R    : 12) H K -> K Q      : C K Q K K N N N N N N N N R   
C K Q K K N N N N N N N N R    : 13) Q K -> K Q      : C K K Q K N N N N N N N N R   
C K K Q K N N N N N N N N R    : 13) Q K -> K Q      : C K K K Q N N N N N N N N R   
C K K K Q N N N N N N N N R    : 14) Q N -> K J      : C K K K K J N N N N N N N R   
C K K K K J N N N N N N N R    : 35) K J N -> F K D  : C K K K F K D N N N N N N R   
C K K K F K D N N N N N N R    : 25) F K -> L E      : C K K K L E D N N N N N N R   
C K K K L E D N N N N N N R    : 27) E D -> D E      : C K K K L D E N N N N N N R   
C K K K L D E N N N N N N R    : 22) D E N -> F D D  : C K K K L F D D N N N N N R   
C K K K L F D D N N N N N R    : 23) L F D -> F L D  : C K K K F L D D N N N N N R   
C K K K F L D D N N N N N R    : 24) K F L -> F K L  : C K K F K L D D N N N N N R   
C K K F K L D D N N N N N R    : 25) F K -> L E      : C K K L E L D D N N N N N R   
C K K L E L D D N N N N N R    : 26) E L -> L E      : C K K L L E D D N N N N N R   
C K K L L E D D N N N N N R    : 27) E D -> D E      : C K K L L D E D N N N N N R   
C K K L L D E D N N N N N R    : 27) E D -> D E      : C K K L L D D E N N N N N R   
C K K L L D D E N N N N N R    : 22) D E N -> F D D  : C K K L L D F D D N N N N R   
C K K L L D F D D N N N N R    : 28) D F D -> F D D  : C K K L L F D D D N N N N R   
C K K L L F D D D N N N N R    : 23) L F D -> F L D  : C K K L F L D D D N N N N R   
C K K L F L D D D N N N N R    : 29) L F L -> F L L  : C K K F L L D D D N N N N R   
C K K F L L D D D N N N N R    : 24) K F L -> F K L  : C K F K L L D D D N N N N R   
C K F K L L D D D N N N N R    : 25) F K -> L E      : C K L E L L D D D N N N N R   
C K L E L L D D D N N N N R    : 26) E L -> L E      : C K L L E L D D D N N N N R   
C K L L E L D D D N N N N R    : 26) E L -> L E      : C K L L L E D D D N N N N R   
C K L L L E D D D N N N N R    : 27) E D -> D E      : C K L L L D E D D N N N N R   
C K L L L D E D D N N N N R    : 27) E D -> D E      : C K L L L D D E D N N N N R   
C K L L L D D E D N N N N R    : 27) E D -> D E      : C K L L L D D D E N N N N R   
C K L L L D D D E N N N N R    : 22) D E N -> F D D  : C K L L L D D F D D N N N R   
C K L L L D D F D D N N N R    : 28) D F D -> F D D  : C K L L L D F D D D N N N R   
C K L L L D F D D D N N N R    : 28) D F D -> F D D  : C K L L L F D D D D N N N R   
C K L L L F D D D D N N N R    : 23) L F D -> F L D  : C K L L F L D D D D N N N R   
C K L L F L D D D D N N N R    : 29) L F L -> F L L  : C K L F L L D D D D N N N R   
C K L F L L D D D D N N N R    : 29) L F L -> F L L  : C K F L L L D D D D N N N R   
C K F L L L D D D D N N N R    : 24) K F L -> F K L  : C F K L L L D D D D N N N R   
C F K L L L D D D D N N N R    : 25) F K -> L E      : C L E L L L D D D D N N N R   
C L E L L L D D D D N N N R    : 26) E L -> L E      : C L L E L L D D D D N N N R   
C L L E L L D D D D N N N R    : 26) E L -> L E      : C L L L E L D D D D N N N R   
C L L L E L D D D D N N N R    : 26) E L -> L E      : C L L L L E D D D D N N N R   
C L L L L E D D D D N N N R    : 27) E D -> D E      : C L L L L D E D D D N N N R   
C L L L L D E D D D N N N R    : 27) E D -> D E      : C L L L L D D E D D N N N R   
C L L L L D D E D D N N N R    : 27) E D -> D E      : C L L L L D D D E D N N N R   
C L L L L D D D E D N N N R    : 27) E D -> D E      : C L L L L D D D D E N N N R   
C L L L L D D D D E N N N R    : 22) D E N -> F D D  : C L L L L D D D F D D N N R   
C L L L L D D D F D D N N R    : 28) D F D -> F D D  : C L L L L D D F D D D N N R   
C L L L L D D F D D D N N R    : 28) D F D -> F D D  : C L L L L D F D D D D N N R   
C L L L L D F D D D D N N R    : 28) D F D -> F D D  : C L L L L F D D D D D N N R   
C L L L L F D D D D D N N R    : 23) L F D -> F L D  : C L L L F L D D D D D N N R   
C L L L F L D D D D D N N R    : 29) L F L -> F L L  : C L L F L L D D D D D N N R   
C L L F L L D D D D D N N R    : 29) L F L -> F L L  : C L F L L L D D D D D N N R   
C L F L L L D D D D D N N R    : 29) L F L -> F L L  : C F L L L L D D D D D N N R   
C F L L L L D D D D D N N R    : 30) C F L -> F C L  : F C L L L L D D D D D N N R   
F C L L L L D D D D D N N R    : 31) F C -> C T      : C T L L L L D D D D D N N R   
C T L L L L D D D D D N N R    : 32) T L -> K T      : C K T L L L D D D D D N N R   
C K T L L L D D D D D N N R    : 32) T L -> K T      : C K K T L L D D D D D N N R   
C K K T L L D D D D D N N R    : 32) T L -> K T      : C K K K T L D D D D D N N R   
C K K K T L D D D D D N N R    : 32) T L -> K T      : C K K K K T D D D D D N N R   
C K K K K T D D D D D N N R    : 33) K T D -> F K D  : C K K K F K D D D D D N N R   
C K K K F K D D D D D N N R    : 25) F K -> L E      : C K K K L E D D D D D N N R   
C K K K L E D D D D D N N R    : 27) E D -> D E      : C K K K L D E D D D D N N R   
C K K K L D E D D D D N N R    : 27) E D -> D E      : C K K K L D D E D D D N N R   
C K K K L D D E D D D N N R    : 27) E D -> D E      : C K K K L D D D E D D N N R   
C K K K L D D D E D D N N R    : 27) E D -> D E      : C K K K L D D D D E D N N R   
C K K K L D D D D E D N N R    : 27) E D -> D E      : C K K K L D D D D D E N N R   
C K K K L D D D D D E N N R    : 22) D E N -> F D D  : C K K K L D D D D F D D N R   
C K K K L D D D D F D D N R    : 28) D F D -> F D D  : C K K K L D D D F D D D N R   
C K K K L D D D F D D D N R    : 28) D F D -> F D D  : C K K K L D D F D D D D N R   
C K K K L D D F D D D D N R    : 28) D F D -> F D D  : C K K K L D F D D D D D N R   
C K K K L D F D D D D D N R    : 28) D F D -> F D D  : C K K K L F D D D D D D N R   
C K K K L F D D D D D D N R    : 23) L F D -> F L D  : C K K K F L D D D D D D N R   
C K K K F L D D D D D D N R    : 24) K F L -> F K L  : C K K F K L D D D D D D N R   
C K K F K L D D D D D D N R    : 25) F K -> L E      : C K K L E L D D D D D D N R   
C K K L E L D D D D D D N R    : 26) E L -> L E      : C K K L L E D D D D D D N R   
C K K L L E D D D D D D N R    : 27) E D -> D E      : C K K L L D E D D D D D N R   
C K K L L D E D D D D D N R    : 27) E D -> D E      : C K K L L D D E D D D D N R   
C K K L L D D E D D D D N R    : 27) E D -> D E      : C K K L L D D D E D D D N R   
C K K L L D D D E D D D N R    : 27) E D -> D E      : C K K L L D D D D E D D N R   
C K K L L D D D D E D D N R    : 27) E D -> D E      : C K K L L D D D D D E D N R   
C K K L L D D D D D E D N R    : 27) E D -> D E      : C K K L L D D D D D D E N R   
C K K L L D D D D D D E N R    : 22) D E N -> F D D  : C K K L L D D D D D F D D R   
C K K L L D D D D D F D D R    : 28) D F D -> F D D  : C K K L L D D D D F D D D R   
C K K L L D D D D F D D D R    : 28) D F D -> F D D  : C K K L L D D D F D D D D R   
C K K L L D D D F D D D D R    : 28) D F D -> F D D  : C K K L L D D F D D D D D R   
C K K L L D D F D D D D D R    : 28) D F D -> F D D  : C K K L L D F D D D D D D R   
C K K L L D F D D D D D D R    : 28) D F D -> F D D  : C K K L L F D D D D D D D R   
C K K L L F D D D D D D D R    : 23) L F D -> F L D  : C K K L F L D D D D D D D R   
C K K L F L D D D D D D D R    : 29) L F L -> F L L  : C K K F L L D D D D D D D R   
C K K F L L D D D D D D D R    : 24) K F L -> F K L  : C K F K L L D D D D D D D R   
C K F K L L D D D D D D D R    : 25) F K -> L E      : C K L E L L D D D D D D D R   
C K L E L L D D D D D D D R    : 26) E L -> L E      : C K L L E L D D D D D D D R   
C K L L E L D D D D D D D R    : 26) E L -> L E      : C K L L L E D D D D D D D R   
C K L L L E D D D D D D D R    : 27) E D -> D E      : C K L L L D E D D D D D D R   
C K L L L D E D D D D D D R    : 27) E D -> D E      : C K L L L D D E D D D D D R   
C K L L L D D E D D D D D R    : 27) E D -> D E      : C K L L L D D D E D D D D R   
C K L L L D D D E D D D D R    : 27) E D -> D E      : C K L L L D D D D E D D D R   
C K L L L D D D D E D D D R    : 27) E D -> D E      : C K L L L D D D D D E D D R   
C K L L L D D D D D E D D R    : 27) E D -> D E      : C K L L L D D D D D D E D R   
C K L L L D D D D D D E D R    : 27) E D -> D E      : C K L L L D D D D D D D E R   
C K L L L D D D D D D D E R    : 9) D E R -> H D R   : C K L L L D D D D D D H D R   
C K L L L D D D D D D H D R    : 34) D H D -> H D N  : C K L L L D D D D D H D N R   
C K L L L D D D D D H D N R    : 34) D H D -> H D N  : C K L L L D D D D H D N N R   
C K L L L D D D D H D N N R    : 34) D H D -> H D N  : C K L L L D D D H D N N N R   
C K L L L D D D H D N N N R    : 34) D H D -> H D N  : C K L L L D D H D N N N N R   
C K L L L D D H D N N N N R    : 34) D H D -> H D N  : C K L L L D H D N N N N N R   
C K L L L D H D N N N N N R    : 34) D H D -> H D N  : C K L L L H D N N N N N N R   
C K L L L H D N N N N N N R    : 10) L H D -> H L N  : C K L L H L N N N N N N N R   
C K L L H L N N N N N N N R    : 36) L H L -> H L K  : C K L H L K N N N N N N N R   
C K L H L K N N N N N N N R    : 36) L H L -> H L K  : C K H L K K N N N N N N N R   
C K H L K K N N N N N N N R    : 11) K H L -> H K K  : C H K K K K N N N N N N N R   
C H K K K K N N N N N N N R    : 12) H K -> K Q      : C K Q K K K N N N N N N N R   
C K Q K K K N N N N N N N R    : 13) Q K -> K Q      : C K K Q K K N N N N N N N R   
C K K Q K K N N N N N N N R    : 13) Q K -> K Q      : C K K K Q K N N N N N N N R   
C K K K Q K N N N N N N N R    : 13) Q K -> K Q      : C K K K K Q N N N N N N N R   
C K K K K Q N N N N N N N R    : 14) Q N -> K J      : C K K K K K J N N N N N N R   
C K K K K K J N N N N N N R    : 35) K J N -> F K D  : C K K K K F K D N N N N N R   
C K K K K F K D N N N N N R    : 25) F K -> L E      : C K K K K L E D N N N N N R   
C K K K K L E D N N N N N R    : 27) E D -> D E      : C K K K K L D E N N N N N R   
C K K K K L D E N N N N N R    : 22) D E N -> F D D  : C K K K K L F D D N N N N R   
C K K K K L F D D N N N N R    : 23) L F D -> F L D  : C K K K K F L D D N N N N R   
C K K K K F L D D N N N N R    : 24) K F L -> F K L  : C K K K F K L D D N N N N R   
C K K K F K L D D N N N N R    : 25) F K -> L E      : C K K K L E L D D N N N N R   
C K K K L E L D D N N N N R    : 26) E L -> L E      : C K K K L L E D D N N N N R   
C K K K L L E D D N N N N R    : 27) E D -> D E      : C K K K L L D E D N N N N R   
C K K K L L D E D N N N N R    : 27) E D -> D E      : C K K K L L D D E N N N N R   
C K K K L L D D E N N N N R    : 22) D E N -> F D D  : C K K K L L D F D D N N N R   
C K K K L L D F D D N N N R    : 28) D F D -> F D D  : C K K K L L F D D D N N N R   
C K K K L L F D D D N N N R    : 23) L F D -> F L D  : C K K K L F L D D D N N N R   
C K K K L F L D D D N N N R    : 29) L F L -> F L L  : C K K K F L L D D D N N N R   
C K K K F L L D D D N N N R    : 24) K F L -> F K L  : C K K F K L L D D D N N N R   
C K K F K L L D D D N N N R    : 25) F K -> L E      : C K K L E L L D D D N N N R   
C K K L E L L D D D N N N R    : 26) E L -> L E      : C K K L L E L D D D N N N R   
C K K L L E L D D D N N N R    : 26) E L -> L E      : C K K L L L E D D D N N N R   
C K K L L L E D D D N N N R    : 27) E D -> D E      : C K K L L L D E D D N N N R   
C K K L L L D E D D N N N R    : 27) E D -> D E      : C K K L L L D D E D N N N R   
C K K L L L D D E D N N N R    : 27) E D -> D E      : C K K L L L D D D E N N N R   
C K K L L L D D D E N N N R    : 22) D E N -> F D D  : C K K L L L D D F D D N N R   
C K K L L L D D F D D N N R    : 28) D F D -> F D D  : C K K L L L D F D D D N N R   
C K K L L L D F D D D N N R    : 28) D F D -> F D D  : C K K L L L F D D D D N N R   
C K K L L L F D D D D N N R    : 23) L F D -> F L D  : C K K L L F L D D D D N N R   
C K K L L F L D D D D N N R    : 29) L F L -> F L L  : C K K L F L L D D D D N N R   
C K K L F L L D D D D N N R    : 29) L F L -> F L L  : C K K F L L L D D D D N N R   
C K K F L L L D D D D N N R    : 24) K F L -> F K L  : C K F K L L L D D D D N N R   
C K F K L L L D D D D N N R    : 25) F K -> L E      : C K L E L L L D D D D N N R   
C K L E L L L D D D D N N R    : 26) E L -> L E      : C K L L E L L D D D D N N R   
C K L L E L L D D D D N N R    : 26) E L -> L E      : C K L L L E L D D D D N N R   
C K L L L E L D D D D N N R    : 26) E L -> L E      : C K L L L L E D D D D N N R   
C K L L L L E D D D D N N R    : 27) E D -> D E      : C K L L L L D E D D D N N R   
C K L L L L D E D D D N N R    : 27) E D -> D E      : C K L L L L D D E D D N N R   
C K L L L L D D E D D N N R    : 27) E D -> D E      : C K L L L L D D D E D N N R   
C K L L L L D D D E D N N R    : 27) E D -> D E      : C K L L L L D D D D E N N R   
C K L L L L D D D D E N N R    : 22) D E N -> F D D  : C K L L L L D D D F D D N R   
C K L L L L D D D F D D N R    : 28) D F D -> F D D  : C K L L L L D D F D D D N R   
C K L L L L D D F D D D N R    : 28) D F D -> F D D  : C K L L L L D F D D D D N R   
C K L L L L D F D D D D N R    : 28) D F D -> F D D  : C K L L L L F D D D D D N R   
C K L L L L F D D D D D N R    : 23) L F D -> F L D  : C K L L L F L D D D D D N R   
C K L L L F L D D D D D N R    : 29) L F L -> F L L  : C K L L F L L D D D D D N R   
C K L L F L L D D D D D N R    : 29) L F L -> F L L  : C K L F L L L D D D D D N R   
C K L F L L L D D D D D N R    : 29) L F L -> F L L  : C K F L L L L D D D D D N R   
C K F L L L L D D D D D N R    : 24) K F L -> F K L  : C F K L L L L D D D D D N R   
C F K L L L L D D D D D N R    : 25) F K -> L E      : C L E L L L L D D D D D N R   
C L E L L L L D D D D D N R    : 26) E L -> L E      : C L L E L L L D D D D D N R   
C L L E L L L D D D D D N R    : 26) E L -> L E      : C L L L E L L D D D D D N R   
C L L L E L L D D D D D N R    : 26) E L -> L E      : C L L L L E L D D D D D N R   
C L L L L E L D D D D D N R    : 26) E L -> L E      : C L L L L L E D D D D D N R   
C L L L L L E D D D D D N R    : 27) E D -> D E      : C L L L L L D E D D D D N R   
C L L L L L D E D D D D N R    : 27) E D -> D E      : C L L L L L D D E D D D N R   
C L L L L L D D E D D D N R    : 27) E D -> D E      : C L L L L L D D D E D D N R   
C L L L L L D D D E D D N R    : 27) E D -> D E      : C L L L L L D D D D E D N R   
C L L L L L D D D D E D N R    : 27) E D -> D E      : C L L L L L D D D D D E N R   
C L L L L L D D D D D E N R    : 22) D E N -> F D D  : C L L L L L D D D D F D D R   
C L L L L L D D D D F D D R    : 28) D F D -> F D D  : C L L L L L D D D F D D D R   
C L L L L L D D D F D D D R    : 28) D F D -> F D D  : C L L L L L D D F D D D D R   
C L L L L L D D F D D D D R    : 28) D F D -> F D D  : C L L L L L D F D D D D D R   
C L L L L L D F D D D D D R    : 28) D F D -> F D D  : C L L L L L F D D D D D D R   
C L L L L L F D D D D D D R    : 23) L F D -> F L D  : C L L L L F L D D D D D D R   
C L L L L F L D D D D D D R    : 29) L F L -> F L L  : C L L L F L L D D D D D D R   
C L L L F L L D D D D D D R    : 29) L F L -> F L L  : C L L F L L L D D D D D D R   
C L L F L L L D D D D D D R    : 29) L F L -> F L L  : C L F L L L L D D D D D D R   
C L F L L L L D D D D D D R    : 29) L F L -> F L L  : C F L L L L L D D D D D D R   
C F L L L L L D D D D D D R    : 30) C F L -> F C L  : F C L L L L L D D D D D D R   
F C L L L L L D D D D D D R    : 31) F C -> C T      : C T L L L L L D D D D D D R   
C T L L L L L D D D D D D R    : 32) T L -> K T      : C K T L L L L D D D D D D R   
C K T L L L L D D D D D D R    : 32) T L -> K T      : C K K T L L L D D D D D D R   
C K K T L L L D D D D D D R    : 32) T L -> K T      : C K K K T L L D D D D D D R   
C K K K T L L D D D D D D R    : 32) T L -> K T      : C K K K K T L D D D D D D R   
C K K K K T L D D D D D D R    : 32) T L -> K T      : C K K K K K T D D D D D D R   
C K K K K K T D D D D D D R    : 33) K T D -> F K D  : C K K K K F K D D D D D D R   
C K K K K F K D D D D D D R    : 25) F K -> L E      : C K K K K L E D D D D D D R   
C K K K K L E D D D D D D R    : 27) E D -> D E      : C K K K K L D E D D D D D R   
C K K K K L D E D D D D D R    : 27) E D -> D E      : C K K K K L D D E D D D D R   
C K K K K L D D E D D D D R    : 27) E D -> D E      : C K K K K L D D D E D D D R   
C K K K K L D D D E D D D R    : 27) E D -> D E      : C K K K K L D D D D E D D R   
C K K K K L D D D D E D D R    : 27) E D -> D E      : C K K K K L D D D D D E D R   
C K K K K L D D D D D E D R    : 27) E D -> D E      : C K K K K L D D D D D D E R   
C K K K K L D D D D D D E R    : 9) D E R -> H D R   : C K K K K L D D D D D H D R   
C K K K K L D D D D D H D R    : 34) D H D -> H D N  : C K K K K L D D D D H D N R   
C K K K K L D D D D H D N R    : 34) D H D -> H D N  : C K K K K L D D D H D N N R   
C K K K K L D D D H D N N R    : 34) D H D -> H D N  : C K K K K L D D H D N N N R   
C K K K K L D D H D N N N R    : 34) D H D -> H D N  : C K K K K L D H D N N N N R   
C K K K K L D H D N N N N R    : 34) D H D -> H D N  : C K K K K L H D N N N N N R   
C K K K K L H D N N N N N R    : 10) L H D -> H L N  : C K K K K H L N N N N N N R   
C K K K K H L N N N N N N R    : 11) K H L -> H K K  : C K K K H K K N N N N N N R   
C K K K H K K N N N N N N R    : 12) H K -> K Q      : C K K K K Q K N N N N N N R   
C K K K K Q K N N N N N N R    : 13) Q K -> K Q      : C K K K K K Q N N N N N N R   
C K K K K K Q N N N N N N R    : 14) Q N -> K J      : C K K K K K K J N N N N N R   
C K K K K K K J N N N N N R    : 35) K J N -> F K D  : C K K K K K F K D N N N N R   
C K K K K K F K D N N N N R    : 25) F K -> L E      : C K K K K K L E D N N N N R   
C K K K K K L E D N N N N R    : 27) E D -> D E      : C K K K K K L D E N N N N R   
C K K K K K L D E N N N N R    : 22) D E N -> F D D  : C K K K K K L F D D N N N R   
C K K K K K L F D D N N N R    : 23) L F D -> F L D  : C K K K K K F L D D N N N R   
C K K K K K F L D D N N N R    : 24) K F L -> F K L  : C K K K K F K L D D N N N R   
C K K K K F K L D D N N N R    : 25) F K -> L E      : C K K K K L E L D D N N N R   
C K K K K L E L D D N N N R    : 26) E L -> L E      : C K K K K L L E D D N N N R   
C K K K K L L E D D N N N R    : 27) E D -> D E      : C K K K K L L D E D N N N R   
C K K K K L L D E D N N N R    : 27) E D -> D E      : C K K K K L L D D E N N N R   
C K K K K L L D D E N N N R    : 22) D E N -> F D D  : C K K K K L L D F D D N N R   
C K K K K L L D F D D N N R    : 28) D F D -> F D D  : C K K K K L L F D D D N N R   
C K K K K L L F D D D N N R    : 23) L F D -> F L D  : C K K K K L F L D D D N N R   
C K K K K L F L D D D N N R    : 29) L F L -> F L L  : C K K K K F L L D D D N N R   
C K K K K F L L D D D N N R    : 24) K F L -> F K L  : C K K K F K L L D D D N N R   
C K K K F K L L D D D N N R    : 25) F K -> L E      : C K K K L E L L D D D N N R   
C K K K L E L L D D D N N R    : 26) E L -> L E      : C K K K L L E L D D D N N R   
C K K K L L E L D D D N N R    : 26) E L -> L E      : C K K K L L L E D D D N N R   
C K K K L L L E D D D N N R    : 27) E D -> D E      : C K K K L L L D E D D N N R   
C K K K L L L D E D D N N R    : 27) E D -> D E      : C K K K L L L D D E D N N R   
C K K K L L L D D E D N N R    : 27) E D -> D E      : C K K K L L L D D D E N N R   
C K K K L L L D D D E N N R    : 22) D E N -> F D D  : C K K K L L L D D F D D N R   
C K K K L L L D D F D D N R    : 28) D F D -> F D D  : C K K K L L L D F D D D N R   
C K K K L L L D F D D D N R    : 28) D F D -> F D D  : C K K K L L L F D D D D N R   
C K K K L L L F D D D D N R    : 23) L F D -> F L D  : C K K K L L F L D D D D N R   
C K K K L L F L D D D D N R    : 29) L F L -> F L L  : C K K K L F L L D D D D N R   
C K K K L F L L D D D D N R    : 29) L F L -> F L L  : C K K K F L L L D D D D N R   
C K K K F L L L D D D D N R    : 24) K F L -> F K L  : C K K F K L L L D D D D N R   
C K K F K L L L D D D D N R    : 25) F K -> L E      : C K K L E L L L D D D D N R   
C K K L E L L L D D D D N R    : 26) E L -> L E      : C K K L L E L L D D D D N R   
C K K L L E L L D D D D N R    : 26) E L -> L E      : C K K L L L E L D D D D N R   
C K K L L L E L D D D D N R    : 26) E L -> L E      : C K K L L L L E D D D D N R   
C K K L L L L E D D D D N R    : 27) E D -> D E      : C K K L L L L D E D D D N R   
C K K L L L L D E D D D N R    : 27) E D -> D E      : C K K L L L L D D E D D N R   
C K K L L L L D D E D D N R    : 27) E D -> D E      : C K K L L L L D D D E D N R   
C K K L L L L D D D E D N R    : 27) E D -> D E      : C K K L L L L D D D D E N R   
C K K L L L L D D D D E N R    : 22) D E N -> F D D  : C K K L L L L D D D F D D R   
C K K L L L L D D D F D D R    : 28) D F D -> F D D  : C K K L L L L D D F D D D R   
C K K L L L L D D F D D D R    : 28) D F D -> F D D  : C K K L L L L D F D D D D R   
C K K L L L L D F D D D D R    : 28) D F D -> F D D  : C K K L L L L F D D D D D R   
C K K L L L L F D D D D D R    : 23) L F D -> F L D  : C K K L L L F L D D D D D R   
C K K L L L F L D D D D D R    : 29) L F L -> F L L  : C K K L L F L L D D D D D R   
C K K L L F L L D D D D D R    : 29) L F L -> F L L  : C K K L F L L L D D D D D R   
C K K L F L L L D D D D D R    : 29) L F L -> F L L  : C K K F L L L L D D D D D R   
C K K F L L L L D D D D D R    : 24) K F L -> F K L  : C K F K L L L L D D D D D R   
C K F K L L L L D D D D D R    : 25) F K -> L E      : C K L E L L L L D D D D D R   
C K L E L L L L D D D D D R    : 26) E L -> L E      : C K L L E L L L D D D D D R   
C K L L E L L L D D D D D R    : 26) E L -> L E      : C K L L L E L L D D D D D R   
C K L L L E L L D D D D D R    : 26) E L -> L E      : C K L L L L E L D D D D D R   
C K L L L L E L D D D D D R    : 26) E L -> L E      : C K L L L L L E D D D D D R   
C K L L L L L E D D D D D R    : 27) E D -> D E      : C K L L L L L D E D D D D R   
C K L L L L L D E D D D D R    : 27) E D -> D E      : C K L L L L L D D E D D D R   
C K L L L L L D D E D D D R    : 27) E D -> D E      : C K L L L L L D D D E D D R   
C K L L L L L D D D E D D R    : 27) E D -> D E      : C K L L L L L D D D D E D R   
C K L L L L L D D D D E D R    : 27) E D -> D E      : C K L L L L L D D D D D E R   
C K L L L L L D D D D D E R    : 9) D E R -> H D R   : C K L L L L L D D D D H D R   
C K L L L L L D D D D H D R    : 34) D H D -> H D N  : C K L L L L L D D D H D N R   
C K L L L L L D D D H D N R    : 34) D H D -> H D N  : C K L L L L L D D H D N N R   
C K L L L L L D D H D N N R    : 34) D H D -> H D N  : C K L L L L L D H D N N N R   
C K L L L L L D H D N N N R    : 34) D H D -> H D N  : C K L L L L L H D N N N N R   
C K L L L L L H D N N N N R    : 10) L H D -> H L N  : C K L L L L H L N N N N N R   
C K L L L L H L N N N N N R    : 36) L H L -> H L K  : C K L L L H L K N N N N N R   
C K L L L H L K N N N N N R    : 36) L H L -> H L K  : C K L L H L K K N N N N N R   
C K L L H L K K N N N N N R    : 36) L H L -> H L K  : C K L H L K K K N N N N N R   
C K L H L K K K N N N N N R    : 36) L H L -> H L K  : C K H L K K K K N N N N N R   
C K H L K K K K N N N N N R    : 11) K H L -> H K K  : C H K K K K K K N N N N N R   
C H K K K K K K N N N N N R    : 12) H K -> K Q      : C K Q K K K K K N N N N N R   
C K Q K K K K K N N N N N R    : 13) Q K -> K Q      : C K K Q K K K K N N N N N R   
C K K Q K K K K N N N N N R    : 13) Q K -> K Q      : C K K K Q K K K N N N N N R   
C K K K Q K K K N N N N N R    : 13) Q K -> K Q      : C K K K K Q K K N N N N N R   
C K K K K Q K K N N N N N R    : 13) Q K -> K Q      : C K K K K K Q K N N N N N R   
C K K K K K Q K N N N N N R    : 13) Q K -> K Q      : C K K K K K K Q N N N N N R   
C K K K K K K Q N N N N N R    : 14) Q N -> K J      : C K K K K K K K J N N N N R   
C K K K K K K K J N N N N R    : 35) K J N -> F K D  : C K K K K K K F K D N N N R   
C K K K K K K F K D N N N R    : 25) F K -> L E      : C K K K K K K L E D N N N R   
C K K K K K K L E D N N N R    : 27) E D -> D E      : C K K K K K K L D E N N N R   
C K K K K K K L D E N N N R    : 22) D E N -> F D D  : C K K K K K K L F D D N N R   
C K K K K K K L F D D N N R    : 23) L F D -> F L D  : C K K K K K K F L D D N N R   
C K K K K K K F L D D N N R    : 24) K F L -> F K L  : C K K K K K F K L D D N N R   
C K K K K K F K L D D N N R    : 25) F K -> L E      : C K K K K K L E L D D N N R   
C K K K K K L E L D D N N R    : 26) E L -> L E      : C K K K K K L L E D D N N R   
C K K K K K L L E D D N N R    : 27) E D -> D E      : C K K K K K L L D E D N N R   
C K K K K K L L D E D N N R    : 27) E D -> D E      : C K K K K K L L D D E N N R   
C K K K K K L L D D E N N R    : 22) D E N -> F D D  : C K K K K K L L D F D D N R   
C K K K K K L L D F D D N R    : 28) D F D -> F D D  : C K K K K K L L F D D D N R   
C K K K K K L L F D D D N R    : 23) L F D -> F L D  : C K K K K K L F L D D D N R   
C K K K K K L F L D D D N R    : 29) L F L -> F L L  : C K K K K K F L L D D D N R   
C K K K K K F L L D D D N R    : 24) K F L -> F K L  : C K K K K F K L L D D D N R   
C K K K K F K L L D D D N R    : 25) F K -> L E      : C K K K K L E L L D D D N R   
C K K K K L E L L D D D N R    : 26) E L -> L E      : C K K K K L L E L D D D N R   
C K K K K L L E L D D D N R    : 26) E L -> L E      : C K K K K L L L E D D D N R   
C K K K K L L L E D D D N R    : 27) E D -> D E      : C K K K K L L L D E D D N R   
C K K K K L L L D E D D N R    : 27) E D -> D E      : C K K K K L L L D D E D N R   
C K K K K L L L D D E D N R    : 27) E D -> D E      : C K K K K L L L D D D E N R   
C K K K K L L L D D D E N R    : 22) D E N -> F D D  : C K K K K L L L D D F D D R   
C K K K K L L L D D F D D R    : 28) D F D -> F D D  : C K K K K L L L D F D D D R   
C K K K K L L L D F D D D R    : 28) D F D -> F D D  : C K K K K L L L F D D D D R   
C K K K K L L L F D D D D R    : 23) L F D -> F L D  : C K K K K L L F L D D D D R   
C K K K K L L F L D D D D R    : 29) L F L -> F L L  : C K K K K L F L L D D D D R   
C K K K K L F L L D D D D R    : 29) L F L -> F L L  : C K K K K F L L L D D D D R   
C K K K K F L L L D D D D R    : 24) K F L -> F K L  : C K K K F K L L L D D D D R   
C K K K F K L L L D D D D R    : 25) F K -> L E      : C K K K L E L L L D D D D R   
C K K K L E L L L D D D D R    : 26) E L -> L E      : C K K K L L E L L D D D D R   
C K K K L L E L L D D D D R    : 26) E L -> L E      : C K K K L L L E L D D D D R   
C K K K L L L E L D D D D R    : 26) E L -> L E      : C K K K L L L L E D D D D R   
C K K K L L L L E D D D D R    : 27) E D -> D E      : C K K K L L L L D E D D D R   
C K K K L L L L D E D D D R    : 27) E D -> D E      : C K K K L L L L D D E D D R   
C K K K L L L L D D E D D R    : 27) E D -> D E      : C K K K L L L L D D D E D R   
C K K K L L L L D D D E D R    : 27) E D -> D E      : C K K K L L L L D D D D E R   
C K K K L L L L D D D D E R    : 9) D E R -> H D R   : C K K K L L L L D D D H D R   
C K K K L L L L D D D H D R    : 34) D H D -> H D N  : C K K K L L L L D D H D N R   
C K K K L L L L D D H D N R    : 34) D H D -> H D N  : C K K K L L L L D H D N N R   
C K K K L L L L D H D N N R    : 34) D H D -> H D N  : C K K K L L L L H D N N N R   
C K K K L L L L H D N N N R    : 10) L H D -> H L N  : C K K K L L L H L N N N N R   
C K K K L L L H L N N N N R    : 36) L H L -> H L K  : C K K K L L H L K N N N N R   
C K K K L L H L K N N N N R    : 36) L H L -> H L K  : C K K K L H L K K N N N N R   
C K K K L H L K K N N N N R    : 36) L H L -> H L K  : C K K K H L K K K N N N N R   
C K K K H L K K K N N N N R    : 11) K H L -> H K K  : C K K H K K K K K N N N N R   
C K K H K K K K K N N N N R    : 12) H K -> K Q      : C K K K Q K K K K N N N N R   
C K K K Q K K K K N N N N R    : 13) Q K -> K Q      : C K K K K Q K K K N N N N R   
C K K K K Q K K K N N N N R    : 13) Q K -> K Q      : C K K K K K Q K K N N N N R   
C K K K K K Q K K N N N N R    : 13) Q K -> K Q      : C K K K K K K Q K N N N N R   
C K K K K K K Q K N N N N R    : 13) Q K -> K Q      : C K K K K K K K Q N N N N R   
C K K K K K K K Q N N N N R    : 14) Q N -> K J      : C K K K K K K K K J N N N R   
C K K K K K K K K J N N N R    : 35) K J N -> F K D  : C K K K K K K K F K D N N R   
C K K K K K K K F K D N N R    : 25) F K -> L E      : C K K K K K K K L E D N N R   
C K K K K K K K L E D N N R    : 27) E D -> D E      : C K K K K K K K L D E N N R   
C K K K K K K K L D E N N R    : 22) D E N -> F D D  : C K K K K K K K L F D D N R   
C K K K K K K K L F D D N R    : 23) L F D -> F L D  : C K K K K K K K F L D D N R   
C K K K K K K K F L D D N R    : 24) K F L -> F K L  : C K K K K K K F K L D D N R   
C K K K K K K F K L D D N R    : 25) F K -> L E      : C K K K K K K L E L D D N R   
C K K K K K K L E L D D N R    : 26) E L -> L E      : C K K K K K K L L E D D N R   
C K K K K K K L L E D D N R    : 27) E D -> D E      : C K K K K K K L L D E D N R   
C K K K K K K L L D E D N R    : 27) E D -> D E      : C K K K K K K L L D D E N R   
C K K K K K K L L D D E N R    : 22) D E N -> F D D  : C K K K K K K L L D F D D R   
C K K K K K K L L D F D D R    : 28) D F D -> F D D  : C K K K K K K L L F D D D R   
C K K K K K K L L F D D D R    : 23) L F D -> F L D  : C K K K K K K L F L D D D R   
C K K K K K K L F L D D D R    : 29) L F L -> F L L  : C K K K K K K F L L D D D R   
C K K K K K K F L L D D D R    : 24) K F L -> F K L  : C K K K K K F K L L D D D R   
C K K K K K F K L L D D D R    : 25) F K -> L E      : C K K K K K L E L L D D D R   
C K K K K K L E L L D D D R    : 26) E L -> L E      : C K K K K K L L E L D D D R   
C K K K K K L L E L D D D R    : 26) E L -> L E      : C K K K K K L L L E D D D R   
C K K K K K L L L E D D D R    : 27) E D -> D E      : C K K K K K L L L D E D D R   
C K K K K K L L L D E D D R    : 27) E D -> D E      : C K K K K K L L L D D E D R   
C K K K K K L L L D D E D R    : 27) E D -> D E      : C K K K K K L L L D D D E R   
C K K K K K L L L D D D E R    : 9) D E R -> H D R   : C K K K K K L L L D D H D R   
C K K K K K L L L D D H D R    : 34) D H D -> H D N  : C K K K K K L L L D H D N R   
C K K K K K L L L D H D N R    : 34) D H D -> H D N  : C K K K K K L L L H D N N R   
C K K K K K L L L H D N N R    : 10) L H D -> H L N  : C K K K K K L L H L N N N R   
C K K K K K L L H L N N N R    : 36) L H L -> H L K  : C K K K K K L H L K N N N R   
C K K K K K L H L K N N N R    : 36) L H L -> H L K  : C K K K K K H L K K N N N R   
C K K K K K H L K K N N N R    : 11) K H L -> H K K  : C K K K K H K K K K N N N R   
C K K K K H K K K K N N N R    : 12) H K -> K Q      : C K K K K K Q K K K N N N R   
C K K K K K Q K K K N N N R    : 13) Q K -> K Q      : C K K K K K K Q K K N N N R   
C K K K K K K Q K K N N N R    : 13) Q K -> K Q      : C K K K K K K K Q K N N N R   
C K K K K K K K Q K N N N R    : 13) Q K -> K Q      : C K K K K K K K K Q N N N R   
C K K K K K K K K Q N N N R    : 14) Q N -> K J      : C K K K K K K K K K J N N R   
C K K K K K K K K K J N N R    : 35) K J N -> F K D  : C K K K K K K K K F K D N R   
C K K K K K K K K F K D N R    : 25) F K -> L E      : C K K K K K K K K L E D N R   
C K K K K K K K K L E D N R    : 27) E D -> D E      : C K K K K K K K K L D E N R   
C K K K K K K K K L D E N R    : 22) D E N -> F D D  : C K K K K K K K K L F D D R   
C K K K K K K K K L F D D R    : 23) L F D -> F L D  : C K K K K K K K K F L D D R   
C K K K K K K K K F L D D R    : 24) K F L -> F K L  : C K K K K K K K F K L D D R   
C K K K K K K K F K L D D R    : 25) F K -> L E      : C K K K K K K K L E L D D R   
C K K K K K K K L E L D D R    : 26) E L -> L E      : C K K K K K K K L L E D D R   
C K K K K K K K L L E D D R    : 27) E D -> D E      : C K K K K K K K L L D E D R   
C K K K K K K K L L D E D R    : 27) E D -> D E      : C K K K K K K K L L D D E R   
C K K K K K K K L L D D E R    : 9) D E R -> H D R   : C K K K K K K K L L D H D R   
C K K K K K K K L L D H D R    : 34) D H D -> H D N  : C K K K K K K K L L H D N R   
C K K K K K K K L L H D N R    : 10) L H D -> H L N  : C K K K K K K K L H L N N R   
C K K K K K K K L H L N N R    : 36) L H L -> H L K  : C K K K K K K K H L K N N R   
C K K K K K K K H L K N N R    : 11) K H L -> H K K  : C K K K K K K H K K K N N R   
C K K K K K K H K K K N N R    : 12) H K -> K Q      : C K K K K K K K Q K K N N R   
C K K K K K K K Q K K N N R    : 13) Q K -> K Q      : C K K K K K K K K Q K N N R   
C K K K K K K K K Q K N N R    : 13) Q K -> K Q      : C K K K K K K K K K Q N N R   
C K K K K K K K K K Q N N R    : 14) Q N -> K J      : C K K K K K K K K K K J N R   
C K K K K K K K K K K J N R    : 35) K J N -> F K D  : C K K K K K K K K K F K D R   
C K K K K K K K K K F K D R    : 25) F K -> L E      : C K K K K K K K K K L E D R   
C K K K K K K K K K L E D R    : 27) E D -> D E      : C K K K K K K K K K L D E R   
C K K K K K K K K K L D E R    : 9) D E R -> H D R   : C K K K K K K K K K L H D R   
C K K K K K K K K K L H D R    : 10) L H D -> H L N  : C K K K K K K K K K H L N R   
C K K K K K K K K K H L N R    : 11) K H L -> H K K  : C K K K K K K K K H K K N R   
C K K K K K K K K H K K N R    : 12) H K -> K Q      : C K K K K K K K K K Q K N R   
C K K K K K K K K K Q K N R    : 13) Q K -> K Q      : C K K K K K K K K K K Q N R   
C K K K K K K K K K K Q N R    : 14) Q N -> K J      : C K K K K K K K K K K K J R   
C K K K K K K K K K K K J R    : 15) K J R -> M K R  : C K K K K K K K K K K M K R   
C K K K K K K K K K K M K R    : 20) M K -> M a M    : C K K K K K K K K K K M a M R 
C K K K K K K K K K K M a M R  : 21) M R -> M        : C K K K K K K K K K K M a M   
C K K K K K K K K K K M a M    : 19) a M -> a        : C K K K K K K K K K K M a     
C K K K K K K K K K K M a      : 16) K M -> M a M    : C K K K K K K K K K M a M a   
C K K K K K K K K K M a M a    : 18) M a -> a        : C K K K K K K K K K M a a     
C K K K K K K K K K M a a      : 16) K M -> M a M    : C K K K K K K K K M a M a a   
C K K K K K K K K M a M a a    : 18) M a -> a        : C K K K K K K K K M a a a     
C K K K K K K K K M a a a      : 16) K M -> M a M    : C K K K K K K K M a M a a a   
C K K K K K K K M a M a a a    : 18) M a -> a        : C K K K K K K K M a a a a     
C K K K K K K K M a a a a      : 16) K M -> M a M    : C K K K K K K M a M a a a a   
C K K K K K K M a M a a a a    : 18) M a -> a        : C K K K K K K M a a a a a     
C K K K K K K M a a a a a      : 16) K M -> M a M    : C K K K K K M a M a a a a a   
C K K K K K M a M a a a a a    : 18) M a -> a        : C K K K K K M a a a a a a     
C K K K K K M a a a a a a      : 16) K M -> M a M    : C K K K K M a M a a a a a a   
C K K K K M a M a a a a a a    : 18) M a -> a        : C K K K K M a a a a a a a     
C K K K K M a a a a a a a      : 16) K M -> M a M    : C K K K M a M a a a a a a a   
C K K K M a M a a a a a a a    : 18) M a -> a        : C K K K M a a a a a a a a     
C K K K M a a a a a a a a      : 16) K M -> M a M    : C K K M a M a a a a a a a a   
C K K M a M a a a a a a a a    : 18) M a -> a        : C K K M a a a a a a a a a     
C K K M a a a a a a a a a      : 16) K M -> M a M    : C K M a M a a a a a a a a a   
C K M a M a a a a a a a a a    : 18) M a -> a        : C K M a a a a a a a a a a     
C K M a a a a a a a a a a      : 16) K M -> M a M    : C M a M a a a a a a a a a a   
C M a M a a a a a a a a a a    : 18) M a -> a        : C M a a a a a a a a a a a     
C M a a a a a a a a a a a      : 17) C M -> M        : M a a a a a a a a a a a       
M a a a a a a a a a a a        : 18) M a -> a        : a a a a a a a a a a a         
```
