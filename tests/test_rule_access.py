import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rule_access import RuleAccess

def test_load_rules():
    rule_access = RuleAccess('examples/patterns.csv')
    rules = rule_access.get_rules()
    assert len(rules) == 6
    assert rules[0]['label'] == 'Food'
    assert rules[1]['pattern'].pattern == 'shoe'
