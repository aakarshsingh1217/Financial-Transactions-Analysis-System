import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classification_engine import ClassificationEngine
from rule_access import RuleAccess

@pytest.fixture
def classification_engine():
    rule_access = RuleAccess('examples/patterns.csv')
    return ClassificationEngine(rule_access)

def test_classify_transaction(classification_engine):
    transaction = {'description': "Ted's coffee", 'label': 'Unclassified'}
    label = classification_engine.classify_transaction(transaction)
    assert label == 'Food'

def test_classify_transactions(classification_engine):
    transactions = [
        {'description': "Ted's coffee", 'label': 'Unclassified'},
        {'description': "Moe's Shiny Shoes", 'label': 'Unclassified'}
    ]
    classification_engine.classify_transactions(transactions)
    assert transactions[0]['label'] == 'Food'
    assert transactions[1]['label'] == 'Clothing'
