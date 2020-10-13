from src.TuringMachine import TuringMachine


def test_turing_machine_manual(manual_suite):
    tm = TuringMachine.from_txt(manual_suite['TuringMachine'])
    word = manual_suite['word']

    assert tm.accepts(word) is True


def test_turing_machine_automatic(automatic_suite):
    tm = TuringMachine.from_txt(automatic_suite['TuringMachine'])
    accepted_words = automatic_suite['accepted_words']
    not_accepted_words = automatic_suite['not_accepted_words']

    def check():
        for word in accepted_words:
            if tm.accepts(word) is False:
                return False
        for word in not_accepted_words:
            if tm.accepts(word) is True:
                return False
        return True

    assert check() is True
