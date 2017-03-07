# -*- coding: utf8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from syntaxnet_wrapper import tagger, parser


class TestParser(TestCase):
    def test_tagger_en(self):
        raw = tagger['en'].query('this is a good day', returnRaw=True)
        self.assertEqual(
            raw,
            '1\tthis\t_\tDET\tDT\t_\t0\t_\t_\t_\n'
            '2\tis\t_\tVERB\tVBZ\t_\t0\t_\t_\t_\n'
            '3\ta\t_\tDET\tDT\t_\t0\t_\t_\t_\n'
            '4\tgood\t_\tADJ\tJJ\t_\t0\t_\t_\t_\n'
            '5\tday\t_\tNOUN\tNN\t_\t0\t_\t_\t_\n')

    def test_parser_en(self):
        raw = parser['en'].query('Alice drove down the street in her car', returnRaw=True)
        self.assertEqual(
            raw,
            '1\tAlice\t_\tNOUN\tNNP\t_\t2\tnsubj\t_\t_\n'
            '2\tdrove\t_\tVERB\tVBD\t_\t0\tROOT\t_\t_\n'
            '3\tdown\t_\tADP\tIN\t_\t2\tprep\t_\t_\n'
            '4\tthe\t_\tDET\tDT\t_\t5\tdet\t_\t_\n'
            '5\tstreet\t_\tNOUN\tNN\t_\t3\tpobj\t_\t_\n'
            '6\tin\t_\tADP\tIN\t_\t2\tprep\t_\t_\n'
            '7\ther\t_\tPRON\tPRP$\t_\t8\tposs\t_\t_\n'
            '8\tcar\t_\tNOUN\tNN\t_\t6\tpobj\t_\t_\n')

    def test_tagger_zh(self):
        raw = tagger['zh'].query(u'今天 天氣 很 好', returnRaw=True)
        self.assertEqual(
            raw,
            '1\t\u4eca\u5929\t_\tNOUN\tNN\tfPOS=NOUN++NN\t0\t_\t_\t_\n'
            '2\t\u5929\u6c23\t_\tNOUN\tNN\tfPOS=NOUN++NN\t0\t_\t_\t_\n'
            '3\t\u5f88\t_\tADV\tRB\tfPOS=ADV++RB\t0\t_\t_\t_\n'
            '4\t\u597d\t_\tADJ\tJJ\tfPOS=ADJ++JJ\t0\t_\t_\t_\n')

    def test_parser_zh(self):
        raw = parser['zh'].query(u'今天 天氣 很 好', returnRaw=True)
        self.assertEqual(
            raw,
            '1\t\u4eca\u5929\t_\tNOUN\tNN\tfPOS=NOUN++NN\t4\tnmod:tmod\t_\t_\n'
            '2\t\u5929\u6c23\t_\tNOUN\tNN\tfPOS=NOUN++NN\t4\tnsubj\t_\t_\n'
            '3\t\u5f88\t_\tADV\tRB\tfPOS=ADV++RB\t4\tadvmod\t_\t_\n'
            '4\t\u597d\t_\tADJ\tJJ\tfPOS=ADJ++JJ\t0\tROOT\t_\t_\n')
