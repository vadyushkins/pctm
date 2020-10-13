from itertools import product
from typing import List

from src.TuringMachine import TuringMachine
from collections import deque

import time


class ContextSensitiveGrammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = dict()
        self.start_symbol = 'S'

    def accepts(self, word: List):
        words = set()
        sentences = set()
        queue = deque([self.start_symbol])

        start = time.time()

        while len(queue):
            if time.time() - start >= 9 * 60:
                return False

            cur = queue.popleft()

            if all(t in self.terminals for t in cur):
                words.add(cur)

            print(words)

            if word in words:
                return True

            for head in self.productions:
                sub = ''.join(head)
                if sub in cur:
                    for body in self.productions[head]:
                        tmp = cur.replace(sub, ''.join(body), 1)
                        if tmp not in sentences:
                            queue.append(tmp)
                            sentences.add(tmp)
        return False

    def __add_production(self, head, body):
        self.productions[head] = self.productions.get(head, set()) | {body}

    def copy(self):
        csg = ContextSensitiveGrammar()
        csg.nonterminals = self.nonterminals.copy()
        csg.terminals = self.terminals.copy()
        csg.productions = self.productions.copy()
        csg.start_symbol = self.start_symbol[:]
        return csg

    def to_txt(self, path):
        with open(path, 'w+') as f:
            f.write(f'start_symbol: {self.start_symbol}\n')
            f.write(f'nonterminals: {" ".join(self.nonterminals)}\n')
            f.write(f'terminals: {" ".join(self.terminals)}\n')
            for head in self.productions:
                for body in self.productions[head]:
                    f.write(f'{" ".join(head)} -> {" ".join(body)}\n')

    @classmethod
    def from_txt(cls, path):
        csg = ContextSensitiveGrammar()

        with open(path, 'r') as f:
            csg.start_symbol = f.readline().replace('start_symbol: ', '').strip()
            csg.nonterminals = f.readline().replace('nonterminals: ', '').strip().split()
            csg.terminals = f.readline().replace('terminals: ', '').strip().split()

            for p in f:
                head, body = p.strip().split(' -> ')
                csg.__add_production(tuple(head.split()), tuple(body.split()))

        return csg

    def __add_initial_configs_single(self, lba: TuringMachine, start_symbol) -> None:
        """
        Add production (start_symbol -> [lba.init_state,$,t,t,#]) to Context Sensitive Grammar for all t in lba.sigma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol: The Start symbol of Context Sensitive Grammar
        :return: None
        """
        for t in lba.sigma:
            self.__add_production(tuple([start_symbol]), tuple([f'[{lba.init_state},$,{t},{t},#]']))

    def __add_single_movement_configs(self, lba: TuringMachine) -> None:
        """
        Add productions for movements of Linear Bounded Automaton on a one-character tape $t# from not accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> [$,p,g,t#]) if (p,$,>) in transitions for (q,$) for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> [$,p,g,t,#]) if (p,#,<) in transitions for (q,#) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t,#] -> [p,$,Y,t,#]) if (p,Y,<) in transitions for (q,X) for all t in lba.sigma
        Add production ([$,q,X,t,#] -> [$,Y,t,p,#]) if (p,Y,>) in transitions for (q,X) for all t in lba.sigma
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for g in lba.gamma:
                                self.__add_production(tuple([f'[{cur_state},$,{g},{t},#]']),
                                                      tuple([f'[$,{next_state},{g},{t},#]']))
                        elif cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for g in lba.gamma:
                                self.__add_production(tuple([f'[$,{g},{t},{cur_state},#]']),
                                                      tuple([f'[$,{next_state},{g},{t},#]']))
                        elif shift == '<':
                            self.__add_production(tuple([f'[$,{cur_state},{cur_symbol},{t},#]']),
                                                  tuple([f'[{next_state},$,{next_symbol},{t},#]']))
                        elif shift == '>':
                            self.__add_production(tuple([f'[$,{cur_state},{cur_symbol},{t},#]']),
                                                  tuple([f'[$,{next_symbol},{t},{next_state},#]']))

    def __add_single_movement_restore_configs(self, lba: TuringMachine) -> None:
        """
        Add productions for movements of Linear Bounded Automaton on a one-character tape $t# from accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> t) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,g,t,#] -> t) for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> t) for all t in lba.sigma, g in lba.gamma
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for accept_state in lba.accept_states:
            for t in lba.sigma:
                for g in lba.gamma:
                    self.__add_production(tuple([f'[{accept_state},$,{g},{t},#]']), tuple([f'{t}']))
                    self.__add_production(tuple([f'[$,{accept_state},{g},{t},#]']), tuple([f'{t}']))
                    self.__add_production(tuple([f'[$,{g},{t},{accept_state},#]']), tuple([f'{t}']))

    def __add_initial_configs_general(self, lba: TuringMachine, start_symbol_1: str, start_symbol_2: str) -> None:
        """
        Add productions for modeling Linear Bounded Automaton tape $w# where |w| > 1 to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol_1: Start symbol of Context Sensitive Grammar
        :param start_symbol_2: Symbol for modeling Linear Bounded Automaton tape
        :return:
        """
        for t in lba.sigma:
            self.__add_production(tuple([start_symbol_1]), tuple([f'[{lba.init_state},$,{t},{t}]', start_symbol_2]))
            self.__add_production(tuple([start_symbol_2]), tuple([f'[{t},{t}]', start_symbol_2]))
            self.__add_production(tuple([start_symbol_2]), tuple([f'[{t},{t},#]']))

    def __add_general_movement_configs_left(self, lba: TuringMachine) -> None:
        """
        Add productions for modeling Linear Bounded Automaton movement on left side of tape to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for g in lba.gamma:
                                self.__add_production(tuple([f'[{cur_state},$,{g},{t}]']),
                                                      tuple([f'[$,{next_state},{g},{t}]']))
                        elif shift == '<':
                            self.__add_production(tuple([f'[$,{cur_state},{cur_symbol},{t}]']),
                                                  tuple([f'[{next_state},$,{next_symbol},{t}]']))
                        elif shift == '>':
                            for right_g, right_t in product(lba.gamma, lba.sigma):
                                self.__add_production(
                                    tuple([f'[$,{cur_state},{cur_symbol},{t}]', f'[{right_g},{right_t}]']),
                                    tuple([f'[$,{next_symbol},{t}]', f'[{next_state},{right_g},{right_t}]'])
                                )
                                self.__add_production(
                                    tuple([f'[$,{cur_state},{cur_symbol},{t}]', f'[{right_g},{right_t},#]']),
                                    tuple([f'[$,{next_symbol},{t}]', f'[{next_state},{right_g},{right_t},#]'])
                                )

    def __add_general_movement_configs_center(self, lba: TuringMachine) -> None:
        """
        Add productions for modeling Linear Bounded Automaton movement on center side of tape to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        for right_g, right_t in product(lba.gamma, lba.sigma):
                            if shift == '>':
                                self.__add_production(
                                    tuple([f'[{cur_state},{cur_symbol},{t}]', f'[{right_g},{right_t}]']),
                                    tuple([f'[{next_symbol},{t}]', f'[{next_state},{right_g},{right_t}]'])
                                )
                                self.__add_production(
                                    tuple([f'[{cur_state},{cur_symbol},{t}]', f'[{right_g},{right_t},#]']),
                                    tuple([f'[{next_symbol},{t}]', f'[{next_state},{right_g},{right_t},#]'])
                                )
                            elif shift == '<':
                                self.__add_production(
                                    tuple([f'[{right_g},{right_t}]', f'[{cur_state},{cur_symbol},{t}]']),
                                    tuple([f'[{next_state},{right_g},{right_t}]', f'[{next_symbol},{t}]'])
                                )
                                self.__add_production(
                                    tuple([f'[$,{right_g},{right_t}]', f'[{cur_state},{cur_symbol},{t}]']),
                                    tuple([f'[$,{next_state},{right_g},{right_t}]', f'[{next_symbol},{t}]'])
                                )

    def __add_general_movement_configs_right(self, lba: TuringMachine) -> None:
        """
        Add productions for modeling Linear Bounded Automaton movement on right side of tape to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for g in lba.gamma:
                                self.__add_production(tuple([f'[{g},{t},{cur_state},#]']),
                                                      tuple([f'[{next_state},{g},{t},#]']))
                        elif shift == '>':
                            self.__add_production(tuple([f'[{cur_state},{cur_symbol},{t},#]']),
                                                  tuple([f'[{next_symbol},{t},{next_state},#]']))
                        elif shift == '<':
                            for right_g, right_t in product(lba.gamma, lba.sigma):
                                self.__add_production(
                                    tuple([f'[{right_g},{right_t}]', f'[{cur_state},{cur_symbol},{t},#]']),
                                    tuple([f'[{next_state},{right_g},{right_t}]', f'[{next_symbol},{t},#]'])
                                )
                                self.__add_production(
                                    tuple([f'[$,{right_g},{right_t}]', f'[{cur_state},{cur_symbol},{t},#]']),
                                    tuple([f'[$,{next_state},{right_g},{right_t}]', f'[{next_symbol},{t},#]'])
                                )

    def __add_general_movement_restore_configs(self, lba: TuringMachine) -> None:
        """
        Add productions for movements of Linear Bounded Automaton on tape from accepted states to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for g, t in product(lba.gamma, lba.sigma):
            for accept_state in lba.accept_states:
                self.__add_production(tuple([f'[{accept_state},$,{g},{t}]']), tuple([f'{t}']))
                self.__add_production(tuple([f'[$,{accept_state},{g},{t}]']), tuple([f'{t}']))
                self.__add_production(tuple([f'[{accept_state},{g},{t}]']), tuple([f'{t}']))
                self.__add_production(tuple([f'[{accept_state},{g},{t},#]']), tuple([f'{t}']))
                self.__add_production(tuple([f'[{g},{t},{accept_state},#]']), tuple([f'{t}']))

    def __add_general_movement_restore_word(self, lba: TuringMachine) -> None:
        """
        Add productions to restore word accepted by Linear Bounded Automaton to Context Sensitive Grammar
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for g, t1, t2 in product(lba.gamma, lba.sigma, lba.sigma):
            self.__add_production(tuple([f'{t1}', f'[{g},{t2}]']), tuple([f'{t1}', f'{t2}']))
            self.__add_production(tuple([f'{t1}', f'[{g},{t2},#]']), tuple([f'{t1}', f'{t2}']))
            self.__add_production(tuple([f'[{g},{t1}]', f'{t2}']), tuple([f'{t1}', f'{t2}']))
            self.__add_production(tuple([f'[$,{g},{t1}]', f'{t2}']), tuple([f'{t1}', f'{t2}']))

    def __deep_optimization(self):
        csg = self.copy()
        csg.productions.clear()
        res = csg.copy()

        words = list()
        sentences = set()
        used = dict()
        queue = deque([csg.start_symbol])

        while len(queue) > 0:
            print(len(res.productions), len(queue), words)
            cur = queue.popleft()

            if cur not in used:
                used[cur] = csg.copy()

            if all(t in csg.terminals for t in cur):
                words.append(cur)
                if res.productions != used[cur].productions:
                    for head in used[cur].productions:
                        for body in used[cur].productions[head]:
                            res.__add_production(head, body)
                else:
                    return res

            for head in self.productions:
                sub = ''.join(head)
                if sub in cur:
                    for body in self.productions[head]:
                        tmp = cur.replace(sub, ''.join(body), 1)
                        if tmp not in used:
                            used[tmp] = used[cur].copy()
                        used[tmp].__add_production(head, body)
                        if tmp not in sentences:
                            sentences.add(tmp)
                            queue.append(tmp)

    @classmethod
    def from_lba(cls, lba: TuringMachine):

        csg = ContextSensitiveGrammar()

        start_symbol_1 = 'S1'
        start_symbol_2 = 'S2'

        csg.__add_initial_configs_single(lba, start_symbol_1)
        csg.__add_single_movement_configs(lba)
        csg.__add_single_movement_restore_configs(lba)
        csg.__add_initial_configs_general(lba, start_symbol_1, start_symbol_2)
        csg.__add_general_movement_configs_left(lba)
        csg.__add_general_movement_configs_center(lba)
        csg.__add_general_movement_configs_right(lba)
        csg.__add_general_movement_restore_configs(lba)
        csg.__add_general_movement_restore_word(lba)

        csg.nonterminals = {start_symbol_1, start_symbol_2}
        for head in csg.productions:
            csg.nonterminals |= set(head)
            for body in csg.productions[head]:
                for entry in body:
                    if entry not in csg.terminals:
                        csg.nonterminals.add(entry)

        csg.terminals = lba.sigma.copy()
        csg.start_symbol = start_symbol_1[:]

        csg = csg.__deep_optimization()

        print(f'!! {len(csg.productions)} !!')

        return csg
