import argparse

from src.context_sensitive_grammar import ContextSensitiveGrammar
from src.turing_machine import TuringMachine


def main():
    parser = argparse.ArgumentParser("Primality Check Turing Machine")
    parser.add_argument(
        '-t'
        , '--turing_machine_path'
        , help='Path to Turing Machine file'
        , type=str
        , required=True
    )
    parser.add_argument(
        '-cs'
        , '--context_sensitive_grammar_path'
        , help='Path where to save generated grammar'
        , type=str
        , required=False
        , default='resources/grammars/default_csg.txt'
    )

    args = parser.parse_args()

    tm = TuringMachine.from_txt(args.turing_machine_path)

    csg = ContextSensitiveGrammar.from_lba(tm)

    csg.to_txt(args.context_sensitive_grammar_path)


if __name__ == '__main__':
    main()
