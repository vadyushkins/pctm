from typing import List


class TuringMachine:
    def __init__(self):
        self.init_state = None
        self.accept_states = set()
        self.sigma = set()
        self.gamma = set()
        self.transitions = dict()

    def accepts(self, word: List, verbose=False):
        if len(word) == 0:
            word.append('_')

        cur_state = self.init_state[:]
        cur_symbol = word[0][:]
        cur_word = word[:]
        cur_pos = 0

        if verbose:
            print()

        while (cur_state, cur_symbol) in self.transitions:
            next_state, next_symbol, shift = self.transitions[(cur_state, cur_symbol)]

            if verbose:
                print(f'{"".join(cur_word[:cur_pos])}<{cur_state}>[{cur_word[cur_pos]}]{"".join(cur_word[cur_pos + 1:])} -> ', end='')

            cur_state = next_state[:]
            cur_word[cur_pos] = next_symbol[:]

            if (shift == '<') and (cur_pos == 0):
                cur_word = ['_'] + cur_word
            elif (shift == '>') and (cur_pos == len(cur_word) - 1):
                cur_word = cur_word + ['_']
                cur_pos += 1
            elif shift == '<':
                cur_pos -= 1
            elif shift == '>':
                cur_pos += 1

            cur_symbol = cur_word[cur_pos][:]

            if verbose:
                print(f'{"".join(cur_word[:cur_pos])}<{cur_state}>[{cur_word[cur_pos]}]{"".join(cur_word[cur_pos + 1:])}')

        return cur_state in self.accept_states

    @classmethod
    def from_txt(cls, path):
        tm = TuringMachine()
        with open(path, 'r') as f:
            tm.init_state = f.readline().replace('init: ', '').strip()
            tm.accept_states = set(f.readline().replace('accept: ', '').strip().split())
            tm.sigma = f.readline().replace('sigma: {', '').replace('}', '').strip().split(',')
            tm.gamma = f.readline().replace('gamma: {', '').replace('}', '').strip().split(',')

            t = list(filter(lambda x: x != '\n', f.readlines()))
            tm.transitions = dict(map(
                lambda p: (tuple(p[0].strip().split(',')), tuple(p[1].strip().split(','))),
                zip(t[::2], t[1::2])
            ))

        return tm
