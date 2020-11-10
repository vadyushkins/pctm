""" Turing Machine module """

import time
from collections import deque
from typing import Dict, Deque
from typing import List
from typing import Set
from typing import Tuple


class TuringMachine:
    """ Class representing a possibly non-deterministic Turing Machine """

    def __init__(self):
        self.init_state: str = ''
        self.states: Set[str] = set()
        self.accept_states: Set[str] = set()
        self.sigma: Set[str] = set()
        self.gamma: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], Set[Tuple[str, str, str]]] = dict()

    def accepts(self, word: List[str]) -> bool:
        """
        Returns whether the Turing Machine accepts the given word
        Perceives a Turing Machine as non-deterministic
        :param word: List of variables from sigma
        :return: Boolean value - if Turing Machine accepts word then True, else False
        """

        if len(word) == 0:
            word.append('_')

        queue: Deque[Tuple[List[str], int, str, str]] = \
            deque([(word[:], 0, self.init_state[:], word[0][:])])

        start: float = time.time()

        while len(queue) != 0:
            if time.time() - start >= 9 * 60:
                return False

            cur_word, cur_pos, cur_state, cur_symbol = queue.popleft()

            if cur_state in self.accept_states:
                if (cur_state, cur_symbol) not in self.transitions or \
                        len(self.transitions[(cur_state, cur_symbol)]) == 0:
                    return True

            if (cur_state, cur_symbol) not in self.transitions:
                continue

            for next_state, next_symbol, shift in self.transitions[(cur_state, cur_symbol)]:
                new_word: List[str] = \
                    [x if i != cur_pos else next_symbol[:] for i, x in enumerate(cur_word)]
                new_pos: int = cur_pos

                if (shift == '<') and (new_pos == 0):
                    new_word = ['_'] + new_word
                elif (shift == '>') and (new_pos == len(new_word) - 1):
                    new_word = new_word + ['_']
                    new_pos += 1
                elif shift == '<':
                    new_pos -= 1
                elif shift == '>':
                    new_pos += 1

                new_state: str = next_state[:]
                new_symbol: str = new_word[new_pos][:]

                queue.append((new_word, new_pos, new_state, new_symbol))

        return False

    @classmethod
    def from_txt(cls, path):
        """
        Read Turing Machine from txt file
        Txt file contains:
            at first line --- initial state
            at second line --- accepting states
            at third line --- set of input symbols
            at fourth line --- set of tape symbols
            Other lines contain the transition function of the Turing Machine
            , one transition per two lines
        :param path: The path to the txt file with a Turing Machine
        :return: Turing Machine instance
        """

        turing_machine = TuringMachine()

        with open(path, 'r') as input_file:
            turing_machine.init_state = \
                input_file \
                    .readline() \
                    .replace('init: ', '') \
                    .strip()

            turing_machine.accept_states = set(
                input_file
                    .readline()
                    .replace('accept: ', '')
                    .strip()
                    .split()
            )

            turing_machine.sigma = set(
                input_file
                    .readline()
                    .replace('sigma: {', '')
                    .replace('}', '')
                    .strip()
                    .split(',')
            )

            turing_machine.gamma = set(
                input_file
                    .readline()
                    .replace('gamma: {', '')
                    .replace('}', '')
                    .strip()
                    .split(',')
            )

            if not turing_machine.sigma.issubset(turing_machine.gamma):
                turing_machine.gamma |= turing_machine.sigma

            transitions = list(filter(lambda x: x != '\n', input_file.readlines()))
            turing_machine.transitions = dict(map(
                lambda p: (tuple(p[0].strip().split(',')), {tuple(p[1].strip().split(','))}),
                zip(transitions[::2], transitions[1::2])
            ))

            for cur_state, cur_symbol in turing_machine.transitions:
                turing_machine.states.add(cur_state)
                for next_state, _, _ in turing_machine.transitions[(cur_state, cur_symbol)]:
                    turing_machine.states.add(next_state)

        return turing_machine
