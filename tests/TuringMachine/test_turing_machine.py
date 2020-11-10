""" Turing Machine Tests module """

from src.turing_machine import TuringMachine


def test_turing_machine(suite):
    """
    Checks that the given Turing Machine accepts the given word
    :param suite: Dictionary with test suite
        Dict['path'] - path to the file with the Turing Machine
        Dict['word'] - accepted by the Turing Machine
    :return: None
    """

    turing_machine = TuringMachine.from_txt(suite['path'])
    word = suite['word']

    assert turing_machine.accepts(word) is True
