# -*- coding: utf-8 -*-
# ================================================
# Project: sdvu
# Author: Quentin Ducasse
# Email: quentin.ducasse@ensta-bretagne.org
# Repository: https://github.com/QDucasse/pysdvu
# ================================================

import unittest
from unittest.mock import patch, mock_open
from pysdvu.formatter import Formatter

mock_file = """
int c = 1;
int x1 = 0;
int x2 = 0;
state {Q(0), R(1), S(2)} a1.state = 0;
temp bool t_0 = false;
temp int t_1 = 0;
temp bool t_3 = false;
temp byte t_4 = 0;
	process a1
		guardBlock
			t_0 = a1.state == 0,
			t_1 = c < 200,
			t_2 = t_0 and t_1;
		guardCondition t_2;
		effect
			a1.state = 1,
			x1 = c;
	process a1
		guardBlock
            t_3 = a1.state == 1;
		guardCondition t_4;
		effect
            t_4 = 250;
			a1.state = 2,
			x1 = t_4;
"""

expected_global_declarations = [
    "int c = 1;",
    "int x1 = 0;",
    "int x2 = 0;",
    "state {Q(0), R(1), S(2)} a1.state = 0;"
]

expected_temp_declarations = [
    "temp bool t_0 = false;",
    "temp int t_1 = 0;",
    "temp bool t_3 = false;",
    "temp byte t_4 = 0;"
    "t_1 = c < 200,",
    "t_2 = t_0 and t_1;",
    "guardCondition t_2;",
    "effect",
    "a1.state = 1,",
    "x1 = c;",
    "process a1",
    "guardBlock",
    "t_3 = a1.state == 1;",
    "guardCondition t_4;",
    "effect",
    "t_4 = 250;",
    "a1.state = 2,",
    "x1 = t_4;"
]

expected_processes = [
    "process a1",
    "guardBlock",
    "t_0 = a1.state == 0,",
    "t_1 = c < 200,",
    "t_2 = t_0 and t_1;",
    "guardCondition t_2;",
    "effect",
    "a1.state = 1,",
    "x1 = c;",
    "process a1",
    "guardBlock",
    "t_3 = a1.state == 1;",
    "guardCondition t_4;",
    "effect",
    "t_4 = 250;",
    "a1.state = 2,",
    "x1 = t_4;"
]

class FormatterTest(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=mock_file))
    def test_preprocess(self):
        global_declarations, temp_declarations, processes = Formatter.preprocess("path/to/open")
        self.assertCountEqual(expected_global_declarations, global_declarations)
        self.assertCountEqual(expected_temp_declarations, temp_declarations)
        self.assertCountEqual(expected_processes, processes)
