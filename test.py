#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.

from syntaxnet_wrapper import tagger, parser

tag = tagger['en'].query('this is a good day', returnRaw=True)
assert tag
print tag
p = parser['en'].query('Alice drove down the street in her car', returnRaw=True)
assert p
print p
