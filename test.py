#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.

from syntaxnet_wrapper import tagger, parser

assert tagger['en'].query('this is a good day', returnRaw=True)
assert parser['en'].query('Alice drove down the street in her car', returnRaw=True)

assert tagger['zh'].query(u'今天 天氣 很 好', returnRaw=True)
assert parser['zh'].query(u'今天 天氣 很 好', returnRaw=True)

