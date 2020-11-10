""" Context Sensitive Grammar module """

import itertools

from pyformlang import cfg

from src.grammar import Grammar
from src.my_production import Production
from src.turing_machine import TuringMachine


class ContextSensitiveGrammar(Grammar):
    """ Class representing a Context Sensitive Grammar
        Subclass of Grammar Class """

    def __add_initial_configs_single(
            self
            , lba: TuringMachine
            , start_symbol: str
    ):
        """
        Add production (start_symbol -> [lba.init_state,$,t,t,#])
            to Context Sensitive Grammar for all t in lba.sigma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol: The Start symbol of Context Sensitive Grammar
        :return: None
        """

        for sigma_symbol in lba.sigma:
            self.productions.append(Production(
                (cfg.Variable(start_symbol),),
                (cfg.Variable(f'[{lba.init_state},$,{sigma_symbol},{sigma_symbol},#]'),)
            ))

    def __add_single_movement_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton
            on a one-character tape $t#
            from not accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> [$,p,g,t,#])
            if (p,$,>) in transitions for (q,$) for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> [$,p,g,t,#])
            if (p,#,<) in transitions for (q,#) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t,#] -> [p,$,Y,t,#])
            if (p,Y,<) in transitions for (q,X) for all t in lba.sigma
        Add production ([$,q,X,t,#] -> [$,Y,t,p,#])
            if (p,Y,>) in transitions for (q,X) for all t in lba.sigma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for sigma_symbol in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for gamma_symbol in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},$,{gamma_symbol},{sigma_symbol},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{gamma_symbol},{sigma_symbol},#]'),)
                                ))
                        elif cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for gamma_symbol in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{gamma_symbol},{sigma_symbol},{cur_state},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{gamma_symbol},{sigma_symbol},#]'),)
                                ))
                        elif shift == '<':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{sigma_symbol},#]'),),
                                (cfg.Variable(f'[{next_state},$,{next_symbol},{sigma_symbol},#]'),)
                            ))
                        elif shift == '>':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{sigma_symbol},#]'),),
                                (cfg.Variable(f'[$,{next_symbol},{sigma_symbol},{next_state},#]'),)
                            ))

    def __add_single_movement_restore_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton
            on a one-character tape $t#
            from accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> t)
            for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,g,t,#] -> t)
            for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> t)
            for all t in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for accept_state in lba.accept_states:
            for sigma_symbol in lba.sigma:
                for gamma_symbol in lba.gamma:
                    self.productions.append(Production(
                        (cfg.Variable(f'[{accept_state},$,{gamma_symbol},{sigma_symbol},#]'),),
                        (cfg.Terminal(f'{sigma_symbol}'),)
                    ))
                    self.productions.append(Production(
                        (cfg.Variable(f'[$,{accept_state},{gamma_symbol},{sigma_symbol},#]'),),
                        (cfg.Terminal(f'{sigma_symbol}'),)
                    ))
                    self.productions.append(Production(
                        (cfg.Variable(f'[$,{gamma_symbol},{sigma_symbol},{accept_state},#]'),),
                        (cfg.Terminal(f'{sigma_symbol}'),)
                    ))

    def __add_initial_configs_general(
            self
            , lba: TuringMachine
            , start_symbol_1: str
            , start_symbol_2: str
    ):
        """
        Add productions for modeling Linear Bounded Automaton tape $w#
            where |w| > 1
            to Context Sensitive Grammar
        Add production (S1 -> [q0,t,t] S2)
            for all t in lba.sigma
        Add production (S2 -> [t,t] S2)
            for all t in lba.sigma
        Add production (S2 -> [t,t,#])
            for all t in lba.sigma
        S1 --- start symbol of Context Sensitive Grammar
        S2 --- nonterminal used to build Linear Bounded Automaton tape
        # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol_1: Start symbol of Context Sensitive Grammar
        :param start_symbol_2: Symbol for modeling Linear Bounded Automaton tape
        :return: None
        """

        for sigma_symbol in lba.sigma:
            self.productions.append(Production(
                (cfg.Variable(start_symbol_1),),
                (cfg.Variable(
                    f'[{lba.init_state},$,{sigma_symbol},{sigma_symbol}]'
                ), cfg.Variable(
                    start_symbol_2
                ),)
            ))
            self.productions.append(Production(
                (cfg.Variable(start_symbol_2),),
                (cfg.Variable(f'[{sigma_symbol},{sigma_symbol}]'), cfg.Variable(start_symbol_2),)
            ))
            self.productions.append(Production(
                (cfg.Variable(start_symbol_2),),
                (cfg.Variable(f'[{sigma_symbol},{sigma_symbol},#]'),)
            ))

    def __add_general_movement_configs_left(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement
            on left side of tape
            to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> [$,p,g,t])
            if (p,$,>) in transitions for (q,$) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t] -> [p,$,Y,t])
            if (p,Y,<) in transitions for (q,X) for all t in lba.sigma
        Add production ([$,q,X,t] [g,l] -> [$,Y,t] [p,g,l])
            if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t] [g,l,#] -> [$,Y,t] [p,g,l,#])
            if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for sigma_symbol in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for gamma_symbol in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},$,{gamma_symbol},{sigma_symbol}]'),),
                                    (cfg.Variable(f'[$,{next_state},{gamma_symbol},{sigma_symbol}]'),)
                                ))
                        elif shift == '<':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{sigma_symbol}]'),),
                                (cfg.Variable(f'[{next_state},$,{next_symbol},{sigma_symbol}]'),)
                            ))
                        elif shift == '>':
                            for gamma_symbol_right, sigma_symbol_right in itertools.product(lba.gamma, lba.sigma):
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{cur_state},{cur_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right}]'),),
                                    (cfg.Variable(f'[$,{next_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),)
                                ))
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{cur_state},{cur_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right},#]'),),
                                    (cfg.Variable(f'[$,{next_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right},#]'),)
                                ))

    def __add_general_movement_configs_center(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement
            on center side of tape
            to Context Sensitive Grammar
        Add production ([q,X,t] [g,l] -> [Y,t] [p,g,l])
            if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([q,X,t] [g,l,#] -> [Y,t] [p,g,l,#])
            if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([g,l] [q,X,t] -> [p,g,l] [Y,t])
            if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] [q,X,t] -> [$,p,g,l] [Y,t])
            if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for sigma_symbol in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        for gamma_symbol_right, sigma_symbol_right in itertools.product(lba.gamma, lba.sigma):
                            if shift == '>':
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right}]'),),
                                    (cfg.Variable(f'[{next_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),)
                                ))
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right},#]'),),
                                    (cfg.Variable(f'[{next_symbol},{sigma_symbol}]'),
                                     cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right},#]'),)
                                ))
                            elif shift == '<':
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol}]'),),
                                    (cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{next_symbol},{sigma_symbol}]'),)
                                ))
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol}]'),),
                                    (cfg.Variable(f'[$,{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{next_symbol},{sigma_symbol}]'),)
                                ))

    def __add_general_movement_configs_right(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement
            on right side of tape
            to Context Sensitive Grammar
        Add production ([g,t,q,#] -> [p,g,t,#])
            if (p,#,<) in transitions for (q,#) for all t in lba.sigma, g in lba.gamma
        Add production ([q,X,t,#] -> [Y,t,p,#])
            if (p,Y,>) in transitions for (q,X) for all t in lba.sigma, g in lba.gamma
        Add production ([g,l] [q,X,t,#] -> [p,g,l] [Y,t,#])
            if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] [q,X,t,#] -> [$,p,g,l] [Y,t,#])
            if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for sigma_symbol in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for gamma_symbol in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{gamma_symbol},{sigma_symbol},{cur_state},#]'),),
                                    (cfg.Variable(f'[{next_state},{gamma_symbol},{sigma_symbol},#]'),)
                                ))
                        elif shift == '>':
                            self.productions.append(Production(
                                (cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol},#]'),),
                                (cfg.Variable(f'[{next_symbol},{sigma_symbol},{next_state},#]'),)
                            ))
                        elif shift == '<':
                            for gamma_symbol_right, sigma_symbol_right in itertools.product(lba.gamma, lba.sigma):
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol},#]'),),
                                    (cfg.Variable(f'[{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{next_symbol},{sigma_symbol},#]'),)
                                ))
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{sigma_symbol},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{gamma_symbol_right},{sigma_symbol_right}]'),
                                     cfg.Variable(f'[{next_symbol},{sigma_symbol},#]'),)
                                ))

    def __add_general_movement_restore_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton on tape
            from accepted states
            to Context Sensitive Grammar
        Add production ([q,$,g,t] -> t)
            if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,g,t] -> t)
            if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([q,g,t] -> t)
            if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([q,g,t,#] -> t)
            if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([g,t,q,#] -> t)
            if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for gamma_symbol, sigma_symbol in itertools.product(lba.gamma, lba.sigma):
            for accept_state in lba.accept_states:
                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},$,{gamma_symbol},{sigma_symbol}]'),),
                    (cfg.Terminal(f'{sigma_symbol}'),)
                ))
                self.productions.append(Production(
                    (cfg.Variable(f'[$,{accept_state},{gamma_symbol},{sigma_symbol}]'),),
                    (cfg.Terminal(f'{sigma_symbol}'),)
                ))
                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},{gamma_symbol},{sigma_symbol}]'),),
                    (cfg.Terminal(f'{sigma_symbol}'),)
                ))
                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},{gamma_symbol},{sigma_symbol},#]'),),
                    (cfg.Terminal(f'{sigma_symbol}'),)
                ))
                self.productions.append(Production(
                    (cfg.Variable(f'[{gamma_symbol},{sigma_symbol},{accept_state},#]'),),
                    (cfg.Terminal(f'{sigma_symbol}'),)
                ))

    def __add_general_movement_restore_word(self, lba: TuringMachine):
        """
        Add productions to restore word accepted by Linear Bounded Automaton
            to Context Sensitive Grammar
        Add production (l [g,t] -> l t)
            for all t,l in lba.sigma, g in lba.gamma
        Add production (l [g,t,#] -> l t)
            for all t,l in lba.sigma, g in lba.gamma
        Add production ([g,l] t -> l t)
            for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] t -> l t)
            for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """

        for gamma_symbol, sigma_symbol_1, sigma_symbol_2 in itertools.product(lba.gamma, lba.sigma, lba.sigma):
            self.productions.append(Production(
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Variable(f'[{gamma_symbol},{sigma_symbol_2}]'),),
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Terminal(f'{sigma_symbol_2}'),)
            ))
            self.productions.append(Production(
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Variable(f'[{gamma_symbol},{sigma_symbol_2},#]'),),
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Terminal(f'{sigma_symbol_2}'),)
            ))
            self.productions.append(Production(
                (cfg.Variable(f'[{gamma_symbol},{sigma_symbol_1}]'),
                 cfg.Terminal(f'{sigma_symbol_2}'),),
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Terminal(f'{sigma_symbol_2}'),)
            ))
            self.productions.append(Production(
                (cfg.Variable(f'[$,{gamma_symbol},{sigma_symbol_1}]'),
                 cfg.Terminal(f'{sigma_symbol_2}'),),
                (cfg.Terminal(f'{sigma_symbol_1}'),
                 cfg.Terminal(f'{sigma_symbol_2}'),)
            ))

    @classmethod
    def from_lba(cls, lba: TuringMachine):
        """
        Build a Context Sensitive Grammar by a Linear Bounded Automaton
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: The Context Sensitive Grammar builded by lba
        """

        grammar = ContextSensitiveGrammar()
        grammar.terminals = {cfg.Terminal(x) for x in lba.sigma}
        grammar.start_symbol = cfg.Variable('S1')
        grammar.__add_initial_configs_single(lba, 'S1')
        grammar.__add_single_movement_configs(lba)
        grammar.__add_single_movement_restore_configs(lba)
        grammar.__add_initial_configs_general(lba, 'S1', 'S2')
        grammar.__add_general_movement_configs_left(lba)
        grammar.__add_general_movement_configs_center(lba)
        grammar.__add_general_movement_configs_right(lba)
        grammar.__add_general_movement_restore_configs(lba)
        grammar.__add_general_movement_restore_word(lba)
        grammar = grammar.nonterminals_optimization()

        while True:
            prev = len(grammar.productions)
            grammar = grammar.deep_optimization(max_cnt=5)
            grammar = grammar.substitutions_optimization()
            if prev == len(grammar.productions):
                break

        return grammar
