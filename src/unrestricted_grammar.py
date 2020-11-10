""" Unrestricted Grammar module """

import itertools

from pyformlang import cfg

from src.grammar import Grammar
from src.my_production import Production
from src.turing_machine import TuringMachine


class UnrestrictedGrammar(Grammar):
    """ Class representing a Unrestricted Grammar
        Subclass of Grammar Class """

    def __add_initial_configs(
            self
            , turing_machine: TuringMachine
            , start_symbol: str
            , initialization_symbol: str
    ):
        """
        Add production (start_symbol -> [,_] tm.init_state initialization_symbol [,_])
            to Unrestricted Grammar
            for initialize tape initial state
        Add production ([,_] -> [,_] [,_])
            to Unrestricted Grammar
            for initialize as many blanks as need
        Add production (initialization_symbol -> [t,t] initialization_symbol)
            for all t in turing_machine.sigma
            to Unrestricted Grammar
            for initialize input word on tape
        Add production (initialization_symbol -> )
            to Unrestricted Grammar
            for nishing initialization input word on tape
        :param turing_machine: The Turing Machine from which the Unrestricted Grammar is built
        :param start_symbol: The Start symbol of Unrestricted Grammar
        :param initialization_symbol: The input word initialization symbol of Unrestricted Gramamr
        :return:
        """

        self.productions.append(Production(
            (cfg.Variable(start_symbol),),
            (cfg.Variable('[,_]'), cfg.Variable(turing_machine.init_state),
             cfg.Variable(initialization_symbol), cfg.Variable('[,_]'))
        ))

        self.productions.append(Production(
            (cfg.Variable('[,_]'),),
            (cfg.Variable('[,_]'), cfg.Variable('[,_]'))
        ))

        for sigma_symbol in turing_machine.sigma:
            self.productions.append(Production(
                (cfg.Variable(initialization_symbol),),
                (cfg.Variable(f'[{sigma_symbol},{sigma_symbol}]'),
                 cfg.Variable(initialization_symbol))
            ))

        self.productions.append(Production(
            (cfg.Variable(initialization_symbol),),
            tuple()
        ))

    def __add_movement_configs(self, turing_machine: TuringMachine):
        """
        Add productions for movements of Turing Machine on tape to Unrestricted Grammar
        Add production (q [t,X] -> [t,Y] p)
            if (p,Y,>) in transitions for (q,X)
            for all t in turing_machine.sigma
        Add production ([g, l] q [t,X] -> p [g, l] [t,Y])
            if (p,Y,<) in transitions for (q,X)
            for all t in turing_machine.sigma
        :param turing_machine: The Turing Machine from which the Unrestricted Grammar is built
        :return: None
        """

        for sigma_symbol in turing_machine.sigma | {''}:
            for cur_state, cur_symbol in turing_machine.transitions:
                for next_state, next_symbol, shift in turing_machine.transitions[(cur_state, cur_symbol)]:
                    if shift == '>':
                        self.productions.append(Production(
                            (cfg.Variable(cur_state),
                             cfg.Variable(f'[{sigma_symbol},{cur_symbol}]')),
                            (cfg.Variable(f'[{sigma_symbol},{next_symbol}]'),
                             cfg.Variable(next_state))
                        ))
                    elif shift == '<':
                        for sigma_symbol_left, gamma_symbol_left in itertools.product(turing_machine.sigma | {''}, turing_machine.gamma):
                            self.productions.append(Production(
                                (cfg.Variable(f'[{sigma_symbol_left},{gamma_symbol_left}]'), cfg.Variable(cur_state),
                                 cfg.Variable(f'[{sigma_symbol},{cur_symbol}]')),
                                (cfg.Variable(next_state), cfg.Variable(f'[{sigma_symbol_left},{gamma_symbol_left}]'),
                                 cfg.Variable(f'[{sigma_symbol},{next_symbol}]'))
                            ))

    def __add_restore_configs(self, turing_machine: TuringMachine):
        """
        Add productions to restore word accepted by Turing Machine
            to Unrestricted Grammar
        Add production ([g,l] q -> q g q)
            for all q in turing_machine.accepted_states
            for all g in turing_machine.sigma + epsilon
            for all l in turing_machine.gamma
        Add production (q [g,l] -> q g q)
            for all q in turing_machine.accepted_states
            for all g in turing_machine.sigma + epsilon
            for all l in turing_machine.gamma
        Add production ([_,l] q -> q g q)
            for all q in turing_machine.accepted_states
            for all l in turing_machine.gamma
        Add production (q [_,l] -> q g q)
            for all q in turing_machine.accepted_states
            for all l in turing_machine.gamma
        Add production (q g -> g)
            for all q in turing_machine.accepted_states
            for all g in turing_machine.sigma
        Add production (g q -> g)
            for all q in turing_machine.accepted_states
            for all g in turing_machine.sigma
        :param turing_machine: The Turing Machine from which the Unrestricted Grammar is built
        :return: None
        """

        for accept_state in turing_machine.accept_states:
            for sigma_symbol, gamma_symbol in itertools.product(turing_machine.sigma | {''}, turing_machine.gamma):
                self.productions.append(Production(
                    (cfg.Variable(f'[{sigma_symbol},{gamma_symbol}]'), cfg.Variable(accept_state)),
                    (cfg.Variable(accept_state), cfg.Terminal(sigma_symbol), cfg.Variable(accept_state))
                ))

                self.productions.append(Production(
                    (cfg.Variable(accept_state), cfg.Variable(f'[{sigma_symbol},{gamma_symbol}]')),
                    (cfg.Variable(accept_state), cfg.Terminal(sigma_symbol), cfg.Variable(accept_state))
                ))

            for gamma_symbol in turing_machine.gamma:
                self.productions.append(Production(
                    (cfg.Variable(f'[,{gamma_symbol}]'), cfg.Variable(accept_state)),
                    (cfg.Variable(accept_state),)
                ))

                self.productions.append(Production(
                    (cfg.Variable(accept_state), cfg.Variable(f'[,{gamma_symbol}]')),
                    (cfg.Variable(accept_state),)
                ))

            for sigma_symbol in turing_machine.sigma:
                self.productions.append(Production(
                    (cfg.Variable(accept_state), cfg.Terminal(sigma_symbol)),
                    (cfg.Terminal(sigma_symbol),)
                ))

                self.productions.append(Production(
                    (cfg.Terminal(sigma_symbol), cfg.Variable(accept_state)),
                    (cfg.Terminal(sigma_symbol),)
                ))

    @classmethod
    def from_turing_machine(cls, turing_machine: TuringMachine):
        """
        Build a Unrestricted Grammar by a Turing Machine
        :param turing_machine: The Turing Machine from which the Unrestricted Grammar is built
        :return: The Unrestricted Grammar builded by lba
        """

        grammar = UnrestrictedGrammar()

        grammar.__add_initial_configs(turing_machine, 'S1', 'S2')
        grammar.__add_movement_configs(turing_machine)
        grammar.__add_restore_configs(turing_machine)

        grammar.terminals = {cfg.Terminal(x) for x in turing_machine.sigma}
        grammar.start_symbol = cfg.Variable('S1')

        grammar = grammar.nonterminals_optimization()

        while True:
            prev = len(grammar.productions)
            grammar = grammar.deep_optimization(max_cnt=4)
            grammar = grammar.substitutions_optimization()
            if prev == len(grammar.productions):
                break

        return grammar
