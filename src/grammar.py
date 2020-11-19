""" Generic Grammar definition module """

import pathlib
from collections import deque
from typing import Deque
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

from pyformlang import cfg

from src.my_production import Production


class Grammar:
    """ Class representing a Grammar abstraction """

    def __init__(self):
        """
        Constructor of Grammar instance
        nonterminals - set of nonterminal variables
        terminals - set of terminal varibles
        start symbol - start symbol of Grammar instance
        productions - dictionary matching the head of production to set of bodies
        """

        self.nonterminals: Set[cfg.Variable] = set()
        self.terminals: Set[cfg.Terminal] = set()
        self.start_symbol: cfg.Variable = cfg.Variable('S')
        self.productions: List[Production] = list()

    def accepts(self, word: str) -> Tuple[
        List[Production],
        List[Tuple[Union[cfg.Variable, cfg.Terminal], ...]]
    ]:
        """
        Returns whether the Context Sensitive Grammar generates the given word
        :param word: Tuple from grammar terminals
        :return: Tuple(used productions, sentences)
        if Context Sensitive Grammar generates the given word
        else empty tuple
        """

        word = tuple(cfg.Terminal(x) for x in word)

        used: Dict[
            Tuple[Union[cfg.Variable, cfg.Terminal], ...],
            List[Production]
        ] = dict()

        parent: Dict[
            Tuple[Union[cfg.Variable, cfg.Terminal], ...],
            Tuple[Union[cfg.Variable, cfg.Terminal], ...]
        ] = dict()

        queue: Deque[Tuple[Union[cfg.Variable, cfg.Terminal], ...]] = \
            deque([(cfg.Variable(self.start_symbol),)])

        while len(queue) != 0:
            sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...] = queue.popleft()

            if sentence not in used:
                used[sentence] = list()

            if all(isinstance(x, cfg.Terminal) for x in sentence):
                if sentence == word:
                    trace = list()
                    prev = word
                    while prev in parent:
                        trace.append(prev)
                        prev = parent[prev]
                    trace.append(prev)
                    trace.reverse()
                    return used[word], trace
                if len(sentence) > len(word):
                    return tuple()

            for production in self.productions:
                for i in range(len(sentence) - len(production.head) + 1):
                    if production.head == sentence[i:i + len(production.head)]:
                        new_sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...] = \
                            sentence[:i] + production.body + sentence[i + len(production.head):]
                        if new_sentence not in used:
                            used[new_sentence] = used[sentence].copy() + [production]
                            parent[new_sentence] = sentence
                            if any(isinstance(x, cfg.Terminal) for x in new_sentence):
                                queue.appendleft(new_sentence)
                            else:
                                queue.append(new_sentence)

            queue = deque(sorted(
                queue
                , key=lambda y: sum(1 for x in y if isinstance(x, cfg.Variable))
            ))

        return tuple()

    def copy(self):
        """
        Returns a copy of the Grammar instance
        :return: A copy of the Grammar instance
        """

        grammar = Grammar()
        grammar.nonterminals = self.nonterminals.copy()
        grammar.terminals = self.terminals.copy()
        grammar.start_symbol = cfg.Variable(self.start_symbol.value)
        grammar.productions = self.productions.copy()
        return grammar

    def to_txt(self, path: pathlib.Path):
        """
        Saves an instance of the Grammar to a txt file
        :param path: Path to a txt file
        :return: None
        """

        def _values(values: Union[
            Iterable[cfg.Variable]
            , Iterable[cfg.Terminal]
            , Iterable[Tuple[Union[cfg.Variable, cfg.Terminal], ...]]
            , Iterable[Tuple[Union[cfg.Variable, cfg.Terminal], ...]]
        ]) -> List[str]:
            return list(map(lambda x: x.value, values))

        with open(path, 'w+') as output_file:
            output_file.write(f'start_symbol: {self.start_symbol.value}\n')
            output_file.write(f'nonterminals: {" ".join(_values(self.nonterminals))}\n')
            output_file.write(f'terminals: {" ".join(_values(self.terminals))}\n')

            for production in self.productions:
                output_file.write(
                    f'{" ".join(_values(production.head))}'
                    + ' -> '
                    + f'{" ".join(_values(production.body))}\n'
                )

    @classmethod
    def from_txt(cls, path: pathlib.Path):
        """
        Loads an instance of a Grammar from a txt file
        :param path: Path to a txt file
        :return: Grammar instance
        """

        grammar = Grammar()

        with open(path, 'r') as input_file:
            grammar.start_symbol = cfg.Variable(
                input_file.readline().strip().replace('start_symbol: ', '')
            )

            grammar.nonterminals = {
                cfg.Variable(x)
                for x in input_file.readline().strip().replace('nonterminals: ', '').split()
            }

            grammar.terminals = {
                cfg.Terminal(x)
                for x in input_file.readline().strip().replace('terminals: ', '').split()
            }

            for production in input_file:
                head, body = production.split(' -> ')
                grammar.productions.append(Production(
                    tuple(
                        cfg.Terminal(x) if cfg.Terminal(x) in grammar.terminals else cfg.Variable(x)
                        for x in head.split()
                    )
                    , tuple(
                        cfg.Terminal(x) if cfg.Terminal(x) in grammar.terminals else cfg.Variable(x)
                        for x in body.split()
                    )
                ))

        return grammar

    def nonterminals_optimization(self):
        """
        Removes all unused non-terminals in productions
        :return: Grammar instance
        """

        grammar = self.copy()
        grammar.nonterminals.clear()

        for production in grammar.productions:
            for unit in production.head:
                if isinstance(unit, cfg.Variable):
                    grammar.nonterminals.add(unit)
            for unit in production.body:
                if isinstance(unit, cfg.Variable):
                    grammar.nonterminals.add(unit)

        return grammar

    def names_optimization(self):
        """
        Renames all nonterminals with nice names
        :return: Grammar instance
        """

        rename: Dict[cfg.Variable, cfg.Variable] = {
            self.start_symbol: cfg.Variable('S')
        }

        grammar = self.copy()
        grammar.start_symbol = rename[self.start_symbol]
        grammar.nonterminals.clear()
        grammar.productions.clear()

        for nonterminal in self.nonterminals:
            if nonterminal not in rename:
                rename[nonterminal] = \
                    cfg.Variable(rename[self.start_symbol].value + f'{len(rename)}')
            grammar.nonterminals.add(rename[nonterminal])

        for production in self.productions:
            new_production = Production(tuple(), tuple())

            for unit in production.head:
                if unit in self.nonterminals:
                    new_production.head += (rename[unit],)
                else:
                    new_production.head += (unit,)

            for unit in production.body:
                if unit in self.nonterminals:
                    new_production.body += (rename[unit],)
                else:
                    new_production.body += (unit,)

            grammar.productions.append(new_production)

        return grammar.nonterminals_optimization()

    def deep_optimization(self, max_cnt: int = -1):
        """
        Saves only those products that are used to generate some max_cnt words
        :param max_cnt: The maximum number of words generated by the Grammar instance
        :return: Grammar instance
        """

        cnt: int = max_cnt

        words: Set[Tuple[cfg.Terminal, ...]] = set()

        used: Dict[
            Tuple[Union[cfg.Variable, cfg.Terminal], ...], List[Production]
        ] = dict()

        queue: Deque[Tuple[Union[cfg.Variable, cfg.Terminal], ...]] = \
            deque([(cfg.Variable(self.start_symbol),)])

        while len(queue) != 0:
            sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...] = queue.popleft()
            print(len(queue), words)

            if sentence not in used:
                used[sentence] = list()

            if all(isinstance(x, cfg.Terminal) for x in sentence):
                cnt -= 1
                words.add(sentence)
                if cnt == 0:
                    break

            for production in self.productions:
                for i in range(len(sentence) - len(production.head) + 1):
                    if production.head == sentence[i:i + len(production.head)]:
                        new_sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...] = \
                            sentence[:i] + production.body + sentence[i + len(production.head):]
                        if new_sentence not in used:
                            used[new_sentence] = used[sentence].copy() + [production]
                            if any(isinstance(x, cfg.Terminal) for x in new_sentence):
                                queue.appendleft(new_sentence)
                            else:
                                queue.append(new_sentence)

            queue = deque(sorted(
                queue
                , key=lambda y: sum(1 for x in y if isinstance(x, cfg.Variable))
            ))

        productions: List[Production] = list()
        for word in words:
            for production in used[word]:
                if production not in productions:
                    productions.append(production)

        if len(productions) == 0:
            return self.copy().nonterminals_optimization()

        res = self.copy()
        res.productions.clear()

        for production in productions:
            res.productions.append(production)

        return res.nonterminals_optimization()

    def substitutions_optimization(self):
        """
        Removes all simple substitutions from productions
        :return: Grammar instance
        """

        def _update_production(old_production: Production, substitution: Production) -> Production:
            """
            Substitutes substitution into production
            :param old_production: Production in which the substitution is performed
            :param substitution: Substitution production
            :return: Production instance
            """

            old: Tuple[
                Tuple[Union[cfg.Variable, cfg.Terminal], ...],
                Tuple[Union[cfg.Variable, cfg.Terminal], ...]
            ] = (old_production.head, old_production.body)

            substitutied_production = [tuple(), tuple()]

            for i in [0, 1]:
                for unit in old[i]:
                    if unit != substitution.head[0]:
                        substitutied_production[i] += tuple([unit])
                    else:
                        substitutied_production[i] += substitution.body

            new = Production(*substitutied_production)

            return new

        res = self.copy()

        while True:
            prev: int = len(res.productions)
            for production in res.productions:
                if len(production.head) == 1 and \
                        len(production.body) == 1 and \
                        sum(1 for x in res.productions if x.head == production.head) == 1:
                    new_productions: List[Production] = list()
                    for res_production in res.productions:
                        if res_production.head != production.head:
                            new_production = _update_production(res_production, production)
                            new_productions.append(new_production)
                    res.productions = new_productions.copy()
                    break
            if prev == len(res.productions):
                break

        return res.nonterminals_optimization()
