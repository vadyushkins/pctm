from itertools import product

from pyformlang import cfg

from src.Grammar import Grammar
from src.MyProduction import Production
from src.TuringMachine import TuringMachine


class ContextSensitiveGrammar(Grammar):
    """
    Class representing a Context Sensitive Grammar
    Subclass of Grammar
    """

    def __add_initial_configs_single(
            self
            , lba: TuringMachine
            , start_symbol: str
    ):
        """
        Add production (start_symbol -> [lba.init_state,$,t,t,#]) to Context Sensitive Grammar for all t in lba.sigma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol: The Start symbol of Context Sensitive Grammar
        :return: None
        """
        for t in lba.sigma:
            self.productions.append(Production(
                (cfg.Variable(start_symbol),),
                (cfg.Variable(f'[{lba.init_state},$,{t},{t},#]'),)
            ))

    def __add_single_movement_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton on a one-character tape $t# from not accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> [$,p,g,t,#]) if (p,$,>) in transitions for (q,$) for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> [$,p,g,t,#]) if (p,#,<) in transitions for (q,#) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t,#] -> [p,$,Y,t,#]) if (p,Y,<) in transitions for (q,X) for all t in lba.sigma
        Add production ([$,q,X,t,#] -> [$,Y,t,p,#]) if (p,Y,>) in transitions for (q,X) for all t in lba.sigma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for g in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},$,{g},{t},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{g},{t},#]'),)
                                ))

                        elif cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for g in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{g},{t},{cur_state},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{g},{t},#]'),)
                                ))
                        elif shift == '<':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{t},#]'),),
                                (cfg.Variable(f'[{next_state},$,{next_symbol},{t},#]'),)
                            ))
                        elif shift == '>':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{t},#]'),),
                                (cfg.Variable(f'[$,{next_symbol},{t},{next_state},#]'),)
                            ))

    def __add_single_movement_restore_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton on a one-character tape $t# from accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> t) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,g,t,#] -> t) for all t in lba.sigma, g in lba.gamma
        Add production ([$,g,t,q,#] -> t) for all t in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for accept_state in lba.accept_states:
            for t in lba.sigma:
                for g in lba.gamma:
                    self.productions.append(Production(
                        (cfg.Variable(f'[{accept_state},$,{g},{t},#]'),),
                        (cfg.Terminal(f'{t}'),)
                    ))

                    self.productions.append(Production(
                        (cfg.Variable(f'[$,{accept_state},{g},{t},#]'),),
                        (cfg.Terminal(f'{t}'),)
                    ))

                    self.productions.append(Production(
                        (cfg.Variable(f'[$,{g},{t},{accept_state},#]'),),
                        (cfg.Terminal(f'{t}'),)
                    ))

    def __add_initial_configs_general(
            self
            , lba: TuringMachine
            , start_symbol_1: str
            , start_symbol_2: str
    ):
        """
        Add productions for modeling Linear Bounded Automaton tape $w# where |w| > 1 to Context Sensitive Grammar
        Add production (S1 -> [q0,t,t] S2) for all t in lba.sigma
        Add production (S2 -> [t,t] S2) for all t in lba.sigma
        Add production (S2 -> [t,t,#])
        S1 --- start symbol of Context Sensitive Grammar
        S2 --- nonterminal used to build Linear Bounded Automaton tape
        # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :param start_symbol_1: Start symbol of Context Sensitive Grammar
        :param start_symbol_2: Symbol for modeling Linear Bounded Automaton tape
        :return: None
        """
        for t in lba.sigma:
            self.productions.append(Production(
                (cfg.Variable(start_symbol_1),),
                (cfg.Variable(f'[{lba.init_state},$,{t},{t}]'), cfg.Variable(start_symbol_2),)
            ))

            self.productions.append(Production(
                (cfg.Variable(start_symbol_2),),
                (cfg.Variable(f'[{t},{t}]'), cfg.Variable(start_symbol_2),)
            ))

            self.productions.append(Production(
                (cfg.Variable(start_symbol_2),),
                (cfg.Variable(f'[{t},{t},#]'),)
            ))

    def __add_general_movement_configs_left(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement on left side of tape to Context Sensitive Grammar
        Add production ([q,$,g,t,#] -> [$,p,g,t]) if (p,$,>) in transitions for (q,$) for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t] -> [p,$,Y,t]) if (p,Y,<) in transitions for (q,X) for all t in lba.sigma
        Add production ([$,q,X,t] [g,l] -> [$,Y,t] [p,g,l]) if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,q,X,t] [g,l,#] -> [$,Y,t] [p,g,l,#]) if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '$' and next_symbol == '$' and shift == '>':
                            for g in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},$,{g},{t}]'),),
                                    (cfg.Variable(f'[$,{next_state},{g},{t}]'),)
                                ))
                        elif shift == '<':
                            self.productions.append(Production(
                                (cfg.Variable(f'[$,{cur_state},{cur_symbol},{t}]'),),
                                (cfg.Variable(f'[{next_state},$,{next_symbol},{t}]'),)
                            ))
                        elif shift == '>':
                            for right_g, right_t in product(lba.gamma, lba.sigma):
                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{cur_state},{cur_symbol},{t}]'),
                                     cfg.Variable(f'[{right_g},{right_t}]'),),
                                    (cfg.Variable(f'[$,{next_symbol},{t}]'),
                                     cfg.Variable(f'[{next_state},{right_g},{right_t}]'),)
                                ))

                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{cur_state},{cur_symbol},{t}]'),
                                     cfg.Variable(f'[{right_g},{right_t},#]'),),
                                    (cfg.Variable(f'[$,{next_symbol},{t}]'),
                                     cfg.Variable(f'[{next_state},{right_g},{right_t},#]'),)
                                ))

    def __add_general_movement_configs_center(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement on center side of tape to Context Sensitive Grammar
        Add production ([q,X,t] [g,l] -> [Y,t] [p,g,l]) if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([q,X,t] [g,l,#] -> [Y,t] [p,g,l,#]) if (p,Y,>) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([g,l] [q,X,t] -> [p,g,l] [Y,t]) if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] [q,X,t] -> [$,p,g,l] [Y,t]) if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        for right_g, right_t in product(lba.gamma, lba.sigma):
                            if shift == '>':
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},{cur_symbol},{t}]'),
                                     cfg.Variable(f'[{right_g},{right_t}]'),),
                                    (cfg.Variable(f'[{next_symbol},{t}]'),
                                     cfg.Variable(f'[{next_state},{right_g},{right_t}]'),)
                                ))

                                self.productions.append(Production(
                                    (cfg.Variable(f'[{cur_state},{cur_symbol},{t}]'),
                                     cfg.Variable(f'[{right_g},{right_t},#]'),),
                                    (cfg.Variable(f'[{next_symbol},{t}]'),
                                     cfg.Variable(f'[{next_state},{right_g},{right_t},#]'),)
                                ))
                            elif shift == '<':
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{right_g},{right_t}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{t}]'),),
                                    (cfg.Variable(f'[{next_state},{right_g},{right_t}]'),
                                     cfg.Variable(f'[{next_symbol},{t}]'),)
                                ))

                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{right_g},{right_t}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{t}]'),),
                                    (cfg.Variable(f'[$,{next_state},{right_g},{right_t}]'),
                                     cfg.Variable(f'[{next_symbol},{t}]'),)
                                ))

    def __add_general_movement_configs_right(self, lba: TuringMachine):
        """
        Add productions for modeling Linear Bounded Automaton movement on right side of tape to Context Sensitive Grammar
        Add production ([g,t,q,#] -> [p,g,t,#]) if (p,#,<) in transitions for (q,#) for all t in lba.sigma, g in lba.gamma
        Add production ([q,X,t,#] -> [Y,t,p,#]) if (p,Y,>) in transitions for (q,X) for all t in lba.sigma, g in lba.gamma
        Add production ([g,l] [q,X,t,#] -> [p,g,l] [Y,t,#]) if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] [q,X,t,#] -> [$,p,g,l] [Y,t,#]) if (p,Y,<) in transitions for (q,X) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for t in lba.sigma:
            for cur_state, cur_symbol in lba.transitions:
                if cur_state not in lba.accept_states:
                    for next_state, next_symbol, shift in lba.transitions[(cur_state, cur_symbol)]:
                        if cur_symbol == '#' and next_symbol == '#' and shift == '<':
                            for g in lba.gamma:
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{g},{t},{cur_state},#]'),),
                                    (cfg.Variable(f'[{next_state},{g},{t},#]'),)
                                ))
                        elif shift == '>':
                            self.productions.append(Production(
                                (cfg.Variable(f'[{cur_state},{cur_symbol},{t},#]'),),
                                (cfg.Variable(f'[{next_symbol},{t},{next_state},#]'),)
                            ))
                        elif shift == '<':
                            for right_g, right_t in product(lba.gamma, lba.sigma):
                                self.productions.append(Production(
                                    (cfg.Variable(f'[{right_g},{right_t}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{t},#]'),),
                                    (cfg.Variable(f'[{next_state},{right_g},{right_t}]'),
                                     cfg.Variable(f'[{next_symbol},{t},#]'),)
                                ))

                                self.productions.append(Production(
                                    (cfg.Variable(f'[$,{right_g},{right_t}]'),
                                     cfg.Variable(f'[{cur_state},{cur_symbol},{t},#]'),),
                                    (cfg.Variable(f'[$,{next_state},{right_g},{right_t}]'),
                                     cfg.Variable(f'[{next_symbol},{t},#]'),)
                                ))

    def __add_general_movement_restore_configs(self, lba: TuringMachine):
        """
        Add productions for movements of Linear Bounded Automaton on tape from accepted states to Context Sensitive Grammar
        Add production ([q,$,g,t] -> t) if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([$,q,g,t] -> t) if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([q,g,t] -> t) if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([q,g,t,#] -> t) if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        Add production ([g,t,q,#] -> t) if q in accepting states of lba for all t in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for g, t in product(lba.gamma, lba.sigma):
            for accept_state in lba.accept_states:
                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},$,{g},{t}]'),),
                    (cfg.Terminal(f'{t}'),)
                ))

                self.productions.append(Production(
                    (cfg.Variable(f'[$,{accept_state},{g},{t}]'),),
                    (cfg.Terminal(f'{t}'),)
                ))

                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},{g},{t}]'),),
                    (cfg.Terminal(f'{t}'),)
                ))

                self.productions.append(Production(
                    (cfg.Variable(f'[{accept_state},{g},{t},#]'),),
                    (cfg.Terminal(f'{t}'),)
                ))

                self.productions.append(Production(
                    (cfg.Variable(f'[{g},{t},{accept_state},#]'),),
                    (cfg.Terminal(f'{t}'),)
                ))

    def __add_general_movement_restore_word(self, lba: TuringMachine):
        """
        Add productions to restore word accepted by Linear Bounded Automaton to Context Sensitive Grammar
        Add production (l [g,t] -> l t) for all t,l in lba.sigma, g in lba.gamma
        Add production (l [g,t,#] -> l t) for all t,l in lba.sigma, g in lba.gamma
        Add production ([g,l] t -> l t) for all t,l in lba.sigma, g in lba.gamma
        Add production ([$,g,l] t -> l t) for all t,l in lba.sigma, g in lba.gamma
        $ --- left end marker of lba, # --- right end marker of lba
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: None
        """
        for g, t1, t2 in product(lba.gamma, lba.sigma, lba.sigma):
            self.productions.append(Production(
                (cfg.Terminal(f'{t1}'),
                 cfg.Variable(f'[{g},{t2}]'),),
                (cfg.Terminal(f'{t1}'),
                 cfg.Terminal(f'{t2}'),)
            ))

            self.productions.append(Production(
                (cfg.Terminal(f'{t1}'),
                 cfg.Variable(f'[{g},{t2},#]'),),
                (cfg.Terminal(f'{t1}'),
                 cfg.Terminal(f'{t2}'),)
            ))

            self.productions.append(Production(
                (cfg.Variable(f'[{g},{t1}]'),
                 cfg.Terminal(f'{t2}'),),
                (cfg.Terminal(f'{t1}'),
                 cfg.Terminal(f'{t2}'),)
            ))

            self.productions.append(Production(
                (cfg.Variable(f'[$,{g},{t1}]'),
                 cfg.Terminal(f'{t2}'),),
                (cfg.Terminal(f'{t1}'),
                 cfg.Terminal(f'{t2}'),)
            ))

    @classmethod
    def from_lba(cls, lba: TuringMachine):
        """
        Build a Context Sensitive Grammar by a Linear Bounded Automaton
        :param lba: The Linear Bounded Automaton from which the Context Sensitive Grammar is built
        :return: The Context Sensitive Grammar builded by lba
        """
        g = ContextSensitiveGrammar()

        start_symbol_1 = 'S1'
        start_symbol_2 = 'S2'

        g.__add_initial_configs_single(lba, start_symbol_1)
        g.__add_single_movement_configs(lba)
        g.__add_single_movement_restore_configs(lba)
        g.__add_initial_configs_general(lba, start_symbol_1, start_symbol_2)
        g.__add_general_movement_configs_left(lba)
        g.__add_general_movement_configs_center(lba)
        g.__add_general_movement_configs_right(lba)
        g.__add_general_movement_restore_configs(lba)
        g.__add_general_movement_restore_word(lba)

        g.terminals = set([cfg.Terminal(x) for x in lba.sigma.copy()])
        g.start_symbol = cfg.Variable(start_symbol_1)

        g = g.nonterminals_optimization()

        while True:
            prev = len(g.productions)
            print(f'!! PREV {len(g.productions)} !!')
            g = g.deep_optimization(max_cnt=5)
            g = g.substitutions_optimization()
            g = g.nonterminals_optimization()
            print(f'!! NEW {len(g.productions)} !!')
            if prev == len(g.productions):
                break

        return g
