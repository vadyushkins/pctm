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

from src.MyProduction import Production


class Grammar:
    """
    Class representing a Grammar abstraction
    """

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

    def accepts(
            self
            , word: Tuple[cfg.Terminal, ...]
            , max_depth: int = -1
    ) -> bool:
        """
        Returns whether the Context Sensitive Grammar generates the given word
        :param word: Tuple from grammar terminals
        :param max_depth: Maximum output tree depth
        :return: Boolean value - did the function succeed in generating the word output tree
        """

        def _accepts(sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...], depth: int) -> bool:
            """
            With the help of all possible suitable productions from the current sentence, it tries to complete the output tree
            :param sentence: Tuple from grammar terminals and nonterminals
            :param depth: Current output tree depth
            :return: Boolean value - did the function succeed in generating the word output tree
            """
            if all(isinstance(x, cfg.Terminal) for x in sentence):
                return sentence == word
            if depth == 0:
                return False
            flag = False
            for production in self.productions:
                for i in range(len(sentence) - len(production.head) + 1):
                    if production.head == sentence[i:i + len(production.head)]:
                        flag |= _accepts(
                            sentence[:i] + production.body + sentence[i + len(production.head):]
                            , depth - 1
                        )
                        if flag:
                            return True
            return flag

        return _accepts((self.start_symbol,), max_depth)

    def copy(self):
        """
        Returns a copy of the Grammar instance
        :return: A copy of the Grammar instance
        """
        g = Grammar()
        g.nonterminals = self.nonterminals.copy()
        g.terminals = self.terminals.copy()
        g.start_symbol = cfg.Variable(self.start_symbol.value)
        g.productions = self.productions.copy()
        return g

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

        with open(path, 'w+') as f:
            f.write(f'start_symbol: {self.start_symbol.value}\n')
            f.write(f'nonterminals: {" ".join(_values(self.nonterminals))}\n')
            f.write(f'terminals: {" ".join(_values(self.terminals))}\n')

            for production in self.productions:
                f.write(f'{" ".join(_values(production.head))} -> {" ".join(_values(production.body))}\n')

    @classmethod
    def from_txt(cls, path: pathlib.Path):
        """
        Loads an instance of a Grammar from a txt file
        :param path: Path to a txt file
        :return: Grammar instance
        """
        g = Grammar()

        with open(path, 'r') as f:
            g.start_symbol = cfg.Variable(f.readline().strip().replace('start_symbol: ', ''))
            g.nonterminals = set([cfg.Variable(x) for x in f.readline().strip().replace('nonterminals: ', '').split()])
            g.terminals = set([cfg.Terminal(x) for x in f.readline().strip().replace('terminals: ', '').split()])

            for p in f:
                head, body = p.strip().split(' -> ')
                g.productions.append(Production(
                    tuple([
                        cfg.Terminal(x) if cfg.Terminal(x) in g.terminals else cfg.Variable(x)
                        for x in head.split()
                    ])
                    , tuple([
                        cfg.Terminal(x) if cfg.Terminal(x) in g.terminals else cfg.Variable(x)
                        for x in body.split()
                    ])
                ))

        return g

    def nonterminals_optimization(self):
        """
        Removes all unused non-terminals in productions
        :return: Grammar instance
        """
        g = self.copy()
        g.nonterminals.clear()

        for production in g.productions:
            for x in production.head:
                if isinstance(x, cfg.Variable):
                    g.nonterminals.add(x)
            for x in production.body:
                if isinstance(x, cfg.Variable):
                    g.nonterminals.add(x)

        return g

    def deep_optimization(self, max_cnt: int = -1):
        """
        Saves only those products that are used to generate some max_cnt words
        :param max_cnt: The maximum number of words generated by the Grammar instance
        :return: Grammar instance
        """

        cnt: int = max_cnt
        words: Set[Tuple[cfg.Terminal, ...]] = set()
        used: Dict[Tuple[Union[cfg.Variable, cfg.Terminal], ...], List[Production]] = dict()
        queue: Deque[Tuple[Union[cfg.Variable, cfg.Terminal], ...]] = deque([(cfg.Variable(self.start_symbol),)])

        while len(queue):
            print(len(queue), words)
            sentence = queue.popleft()

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
                        new_sentence = sentence[:i] + production.body + sentence[i + len(production.head):]
                        if new_sentence not in used:
                            used[new_sentence] = used[sentence].copy() + [production]
                            queue.append(new_sentence)

        productions = list()
        for word in words:
            for x in used[word]:
                if x not in productions:
                    productions.append(x)

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

        def _update_production(
                old_production: Production
                , substitution: Production
        ) -> Production:
            """
            Substitutes substitution into production
            :param old_production: Production in which the substitution is performed
            :param substitution: Substitution production
            :return: Production instance
            """
            old = [old_production.head, old_production.body]
            substitutied_production = [tuple(), tuple()]
            for i in range(len(old)):
                for x in old[i]:
                    if x != substitution.head:
                        substitutied_production[i] += tuple([x])
                    else:
                        substitutied_production[i] += substitution.body
            return Production(*substitutied_production)

        for production in self.productions:
            if len(production.head) == 1 and \
                    sum(1 for x in self.productions if x.head == production.head) == 1 and \
                    production.head[0] != self.start_symbol:
                res = self.copy()
                res.productions.clear()
                for x in self.productions:
                    if x.head != production.head:
                        new_production = _update_production(x, production)
                        res.productions.append(new_production)
                return res.nonterminals_optimization()

        return self.copy().nonterminals_optimization()
