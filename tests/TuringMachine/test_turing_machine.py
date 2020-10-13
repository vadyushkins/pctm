from src.TuringMachine import TuringMachine


def test_turing_machine(suite):
    tm = TuringMachine.from_txt(suite['path'])
    word = suite['word']

    assert tm.accepts(word) is True
