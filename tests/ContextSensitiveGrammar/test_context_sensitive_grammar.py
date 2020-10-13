from src.ContextSensitiveGrammar import ContextSensitiveGrammar


def test_csg_manual(suite):
    csg = ContextSensitiveGrammar.from_txt(suite['path'])
    word = suite['word']

    assert csg.accepts(word)
