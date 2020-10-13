import time
from collections import deque
from typing import List


class TuringMachine:
    """
    Class representing a possibly non-deterministic Turing Machine
    """
    def __init__(self):
        self.init_state = None
        self.states = set()
        self.accept_states = set()
        self.sigma = set()
        self.gamma = set()
        self.transitions = dict()

    def accepts(self, word: List) -> bool:
        """
        Returns whether the Turing Machine accepts the given word
        Perceives a Turing Machine as non-deterministic
        :param word: List of variables from sigma
        :return: True --- when Turing Machine accepts word; False --- otherwise
        """
        if len(word) == 0:
            word.append('_')

        queue = deque([tuple([word[:], 0, self.init_state[:], word[0][:]])])

        start = time.time()

        while True:
            if time.time() - start >= 9 * 60:
                return False

            cur_word, cur_pos, cur_state, cur_symbol = queue.popleft()

            if cur_state in self.accept_states:
                if (cur_state, cur_symbol) not in self.transitions or \
                        len(self.transitions[(cur_state, cur_symbol)]) == 0:
                    return True

            for next_state, next_symbol, shift in self.transitions[(cur_state, cur_symbol)]:
                new_word = [x if i != cur_pos else next_symbol[:] for i, x in enumerate(cur_word)]
                new_pos = cur_pos

                if (shift == '<') and (new_pos == 0):
                    new_word = ['_'] + new_word
                elif (shift == '>') and (new_pos == len(new_word) - 1):
                    new_word = new_word + ['_']
                    new_pos += 1
                elif shift == '<':
                    new_pos -= 1
                elif shift == '>':
                    new_pos += 1

                new_state = next_state[:]
                new_symbol = new_word[new_pos][:]

                queue.append(tuple([new_word, new_pos, new_state, new_symbol]))

    @classmethod
    def from_txt(cls, path):
        """
        Read Turing Machine from txt file
        Txt file contains:
            at first line --- initial state
            at second line --- accepting states
            at third line --- set of input symbols
            at fourth line --- set of tape symbols
            All other lines contain the transition function of the Turing Machine, one transition per two lines
        :param path: The path to the txt file with a Turing Machine
        :return: Turing Machine instance
        """
        tm = TuringMachine()
        with open(path, 'r') as f:
            tm.init_state = f.readline().replace('init: ', '').strip()
            tm.accept_states = set(f.readline().replace('accept: ', '').strip().split())
            tm.sigma = set(f.readline().replace('sigma: {', '').replace('}', '').strip().split(','))
            tm.gamma = set(f.readline().replace('gamma: {', '').replace('}', '').strip().split(','))

            if not tm.sigma.issubset(tm.gamma):
                tm.gamma |= tm.sigma

            t = list(filter(lambda x: x != '\n', f.readlines()))
            tm.transitions = dict(map(
                lambda p: (tuple(p[0].strip().split(',')), {tuple(p[1].strip().split(','))}),
                zip(t[::2], t[1::2])
            ))

            for cur_state, cur_symbol in tm.transitions:
                tm.states.add(cur_state)
                for next_state, next_symbol, shift in tm.transitions[(cur_state, cur_symbol)]:
                    tm.states.add(next_state)

        return tm
