import sys

from pyformlang import cfg

from src.ContextSensitiveGrammar import ContextSensitiveGrammar

sys.setrecursionlimit(10000)


def test_csg_manual(suite):
    g = ContextSensitiveGrammar.from_txt(suite['path'])
    word = tuple([cfg.Terminal(x) for x in suite['word']])

    assert g.accepts(word, max_depth=500)
