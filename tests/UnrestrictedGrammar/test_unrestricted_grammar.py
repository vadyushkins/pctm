""" Unrestricted Grammar Tests module """

from src.unrestricted_grammar import UnrestrictedGrammar


def test_csg_manual(suite):
    """
    Checks that the given Unrestricted Gramamr generates the given word
    :param suite: Dictionary with test suite
        Dict['path'] - path to the file with the grammar
        Dict['word'] - word generated by the grammar
    :return: None
    """

    grammar = UnrestrictedGrammar.from_txt(suite['path'])
    word = suite['word']

    assert grammar.accepts(word)