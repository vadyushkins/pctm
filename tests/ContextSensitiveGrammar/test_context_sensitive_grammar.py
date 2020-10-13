from src.ContextSensitiveGrammar import ContextSensitiveGrammar


def test_csg_manual(manual_suite):
    csg = ContextSensitiveGrammar.from_txt(manual_suite['ContextSensitiveGrammar'])
    word = manual_suite['word']

    assert csg.accepts(word)