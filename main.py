import argparse

from src.ContextSensitiveGrammar import ContextSensitiveGrammar
from src.TuringMachine import TuringMachine


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

    csg.to_txt(args.grammar_path)


if __name__ == '__main__':
    main()
