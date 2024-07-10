import pytest
import sys
import os
from datetime import datetime
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transactions_access import TransactionsAccess
from reporting_manager import ReportingManager
from report_access import ReportAccess
from rule_access import RuleAccess
from classification_engine import ClassificationEngine

@pytest.fixture
def transactions_access():
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_name = tmp.name
    ta = TransactionsAccess(storage_file=tmp_name)
    yield ta
    os.remove(tmp_name)

@pytest.fixture
def reporting_manager(transactions_access):
    report_access = ReportAccess()
    rule_access = RuleAccess('examples/patterns.csv')
    classification_engine = ClassificationEngine(rule_access)
    return ReportingManager(transactions_access, classification_engine, report_access)

def test_import_transactions(transactions_access):
    transactions_access.import_transactions('examples/transactions.csv')
    assert len(transactions_access.transactions) == 7
    assert transactions_access.transactions[0]['description'] == "Ted's coffee"

def test_get_transactions(transactions_access, reporting_manager):
    transactions_access.import_transactions('examples/transactions.csv')
    transactions_access.save_transactions()

    # Print transactions to debug classification
    for txn in transactions_access.transactions:
        print(f"Before classification: {txn}")

    reporting_manager.classify_transactions('2023-01-01', '2024-01-01')
    
    # Print transactions to debug classification
    for txn in transactions_access.transactions:
        print(f"After classification: {txn}")

    transactions = transactions_access.get_transactions('2023-01-01', '2024-01-01')
    assert len(transactions) == 6
    
    transactions_home = transactions_access.get_transactions('2023-01-01', '2024-01-01', label='Home')
    
    # Print transactions with label 'Home'
    for txn in transactions_home:
        print(f"Home transactions: {txn}")

    assert len(transactions_home) == 2

def test_save_and_load_transactions(transactions_access):
    transactions_access.import_transactions('examples/transactions.csv')
    transactions_access.save_transactions()
    new_access = TransactionsAccess(storage_file=transactions_access.storage_file)
    assert len(new_access.transactions) == 7
    assert new_access.transactions[0]['description'] == "Ted's coffee"
