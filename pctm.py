#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Command-Line interface for interacting with Turing Machines and Grammars for primality check """

import argparse
from datetime import timedelta
from timeit import default_timer as timer
from typing import Tuple, List, Union

from pyformlang import cfg

from src.context_sensitive_grammar import ContextSensitiveGrammar
from src.my_production import Production
from src.turing_machine import TuringMachine
from src.unrestricted_grammar import UnrestrictedGrammar


def print_trace(
        res: Tuple[List[Production], List[Tuple[Union[cfg.Variable, cfg.Terminal], ...]]]
        , grammar: Union[ContextSensitiveGrammar, UnrestrictedGrammar]
):
    """ Print word output trace """

    productions, sentences = res
    for i in range(len(productions)):
        sentence_from = list(map(lambda x: x.value, sentences[i]))
        if sentence_from == [grammar.start_symbol]:
            sentence_from = [grammar.start_symbol.value]
        production_head = list(map(lambda x: x.value, productions[i].head))
        production_body = list(map(lambda x: x.value, productions[i].body))
        sentence_to = list(map(lambda x: x.value, sentences[i + 1]))
        print(
            f'{" ".join(sentence_from)} : {" ".join(production_head)} -> {" ".join(production_body)} : {" ".join(sentence_to)}')


def main():
    """ Command-Line tool for interacting with Turing Machines and Grammars for primality check """

    parser = argparse.ArgumentParser(
        description='Primality Check Turing Machine'
        , epilog="At least one of -tm/--turing_machine, "
                 + "-lba/--linear_bounded_automaton, "
                 + "-csg/--context_sensitive_grammar, "
                 + "-ug/--unrestricted_grammar required"
    )
    parser.add_argument(
        '-tm'
        , '--turing_machine'
        , help='Check by Turing Machine'
        , action='store_true'
    )
    parser.add_argument(
        '-lba'
        , '--linear_bounded_automaton'
        , help='Check by Linear Bounded Automaton'
        , action='store_true'
    )
    parser.add_argument(
        '-csg'
        , '--context_sensitive_grammar'
        , help='Check by Context Sensitive Grammar'
        , action='store_true'
    )
    parser.add_argument(
        '-ug'
        , '--unrestricted_grammar'
        , help='Check by Unrestricted Grammar'
        , action='store_true'
    )
    parser.add_argument(
        '-w'
        , '--word'
        , help='Word to check'
        , type=str
        , required=True
    )

    args = parser.parse_args()

    if args.turing_machine is False and \
            args.linear_bounded_automaton is False and \
            args.context_sensitive_grammar is False and \
            args.unrestricted_grammar is False:
        parser.error("At least one of -tm/--turing_machine, "
                     + "-lba/--linear_bounded_automaton, "
                     + "-csg/--context_sensitive_grammar, "
                     + "-ug/--unrestricted_grammar required"
                     )

    turing_machine = None
    if args.turing_machine is True:
        turing_machine = TuringMachine.from_txt('resources/primality_check_tm.txt')

    linear_bounded_automaton = None
    if args.linear_bounded_automaton is True:
        linear_bounded_automaton = TuringMachine.from_txt('resources/primality_check_lba.txt')

    context_sensitive_grammar = None
    if args.context_sensitive_grammar is True:
        context_sensitive_grammar = ContextSensitiveGrammar.from_txt('resources/primality_check_csg.txt')

    unrestricted_grammar = None
    if args.unrestricted_grammar is True:
        unrestricted_grammar = UnrestrictedGrammar.from_txt('resources/primality_check_ug.txt')

    if turing_machine is not None:
        start = timer()
        res = turing_machine.accepts(args.word)
        end = timer()
        result = res != tuple
        result_time = timedelta(seconds=end - start)
        print(f'Check by Turing Machine: {result} is done in {result_time} seconds')

    if linear_bounded_automaton is not None:
        start = timer()
        res = linear_bounded_automaton.accepts("$" + args.word + "#")
        end = timer()
        result = res != tuple
        result_time = timedelta(seconds=end - start)
        print(f'Check by Linear Bounded Automaton: {result} is done in {result_time} seconds')

    if context_sensitive_grammar is not None:
        start = timer()
        res = context_sensitive_grammar.accepts(args.word)
        end = timer()
        result = res != tuple
        result_time = timedelta(seconds=end - start)
        print(f'Check by Context Sensitive Grammar: {result} is done in {result_time} seconds')
        if result:
            print_trace(res, context_sensitive_grammar)

    if unrestricted_grammar is not None:
        start = timer()
        res = unrestricted_grammar.accepts(args.word)
        end = timer()
        result = res != tuple
        result_time = timedelta(seconds=end - start)
        print(f'Check by Unrestricted Grammar: {result} is done in {result_time} seconds')
        if result:
            print_trace(res, unrestricted_grammar)


if __name__ == '__main__':
    main()
