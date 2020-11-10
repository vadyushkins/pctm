#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Command-Line interface for interacting with Turing Machines or Grammars """

import argparse
from datetime import timedelta
from timeit import default_timer as timer

from src.context_sensitive_grammar import ContextSensitiveGrammar
from src.turing_machine import TuringMachine
from src.unrestricted_grammar import UnrestrictedGrammar


def main():
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
        print(f'Check by Turing Machine: {res} is done in {timedelta(seconds=end - start)} seconds')

    if linear_bounded_automaton is not None:
        start = timer()
        res = linear_bounded_automaton.accepts("$" + args.word + "#")
        end = timer()
        print(f'Check by Linear Bounded Automaton: {res} is done in {timedelta(seconds=end - start)} seconds')

    if context_sensitive_grammar is not None:
        start = timer()
        res = context_sensitive_grammar.accepts(args.word)
        end = timer()
        print(f'Check by Context Sensitive Grammar: {res} is done in {timedelta(seconds=end - start)} seconds')

    if unrestricted_grammar is not None:
        start = timer()
        res = unrestricted_grammar.accepts(args.word)
        end = timer()
        print(f'Check by Unrestricted Grammar: {res} is done in {timedelta(seconds=end - start)} seconds')


if __name__ == '__main__':
    main()
