import pathlib
from collections import defaultdict
from typing import DefaultDict
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
        self.productions: DefaultDict[Production.head, Set[Production.body]] = defaultdict(set)

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
            for head in self.productions:
                for i in range(len(sentence) - len(head) + 1):
                    if head == sentence[i:i + len(head)]:
                        flag = False
                        for body in self.productions[head]:
                            if flag is False:
                                flag |= _accepts(
                                    sentence[:i] + body + sentence[i + len(head):]
                                    , depth - 1
                                )
                            else:
                                break
                        return flag
            return False

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
            Iterable[cfg.variable]
            , Iterable[cfg.Terminal]
            , Iterable[Production.head]
            , Iterable[Production.body]
        ]) -> List[str]:
            return list(map(lambda x: x.value, values))

        with open(path, 'w+') as f:
            f.write(f'start_symbol: {self.start_symbol.value}\n')
            f.write(f'nonterminals: {" ".join(_values(self.nonterminals))}\n')
            f.write(f'terminals: {" ".join(_values(self.terminals))}\n')

            for head in self.productions:
                for body in self.productions[head]:
                    f.write(f'{" ".join(_values(head))} -> {" ".join(_values(body))}\n')

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
                production = Production(
                    tuple([
                        cfg.Terminal(x) if cfg.Terminal(x) in g.terminals else cfg.Variable(x)
                        for x in head.split()
                    ])
                    , tuple([
                        cfg.Terminal(x) if cfg.Terminal(x) in g.terminals else cfg.Variable(x)
                        for x in body.split()
                    ])
                )
                g.productions[production.head].add(production.body)

        return g

    def nonterminals_optimization(self):
        """
        Removes all unused non-terminals in productions
        :return: Grammar instance
        """
        g = self.copy()
        g.nonterminals.clear()

        for head in g.productions:
            for x in head:
                if isinstance(x, cfg.Variable):
                    g.nonterminals.add(x)
            for body in g.productions[head]:
                for x in body:
                    if isinstance(x, cfg.Variable):
                        g.nonterminals.add(x)

        return g

    def deep_optimization(self, max_depth: int = -1, max_cnt: int = -1):
        """
        Saves only those products that are used to generate max_cnt words whose output trees are no more than max_depth deep
        :param max_depth: Maximum output tree depth
        :param max_cnt: The maximum number of words generated by the Grammar instance
        :return: Grammar instance
        """

        def _optimize(
                sentence: Tuple[Union[cfg.Variable, cfg.Terminal], ...]
                , depth: int
                , cnt: int
                , used: List[Production]
        ) -> List[Production]:
            """
            With the help of all possible suitable productions from the current sentence, it tries to complete the output tree
            :param sentence: Tuple from grammar terminals and nonterminals
            :param depth: Current output tree depth
            :param cnt: Number of words not yet generated by the Grammar instance
            :param used: List of used productions
            :return: List of used productions
            """
            if depth == 0:
                return []
            if all(map(lambda x: isinstance(x, cfg.Terminal), sentence)):
                if cnt == 0:
                    return used
                else:
                    cnt -= 1
            for head in self.productions:
                for i in range(len(sentence) - len(head) + 1):
                    if head == sentence[i:i + len(head)]:
                        for body in self.productions[head]:
                            new_production = Production(head, body)
                            optimize_res = _optimize(
                                sentence[:i] + body + sentence[i + len(head):]
                                , depth - 1
                                , cnt
                                , used + ([new_production] if new_production not in used else [])
                            )
                            return used + [x for x in optimize_res if x not in used]

        productions = _optimize(
            (self.start_symbol,)
            , max_depth
            , max_cnt
            , list()
        )

        if len(productions) == 0:
            return self.copy().nonterminals_optimization()

        res = self.copy()
        res.productions.clear()

        for production in productions:
            res.productions[production.head].add(production.body)

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

        for head in self.productions:
            if len(head) == 1 and len(self.productions[head]) == 1:
                body = list(self.productions[head])[0]
                res = self.copy()
                res.productions.clear()
                for h in self.productions:
                    for b in self.productions[h]:
                        new_production = _update_production(Production(h, b), Production(head, body))
                        res.productions[new_production.head].add(new_production.body)
                return res.nonterminals_optimization().substitutions_optimization()

        return self.copy().nonterminals_optimization()
