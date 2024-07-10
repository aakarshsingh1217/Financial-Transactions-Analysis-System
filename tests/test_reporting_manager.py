import pytest
import sys
import os
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transactions_access import TransactionsAccess
from classification_engine import ClassificationEngine
from report_access import ReportAccess
from rule_access import RuleAccess
from reporting_manager import ReportingManager

@pytest.fixture
def reporting_manager():
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_name = tmp.name
    transactions_access = TransactionsAccess(storage_file=tmp_name)
    rule_access = RuleAccess('examples/patterns.csv')
    classification_engine = ClassificationEngine(rule_access)
    report_access = ReportAccess()
    yield ReportingManager(transactions_access, classification_engine, report_access)
    os.remove(tmp_name)

def test_import_transactions(reporting_manager):
    reporting_manager.import_transactions('examples/transactions.csv')
    assert len(reporting_manager.transactions_access.transactions) == 7

def test_classify_transactions(reporting_manager):
    transactions_access = reporting_manager.transactions_access
    reporting_manager.import_transactions('examples/transactions.csv')
    reporting_manager.classify_transactions('2023-01-01', '2024-01-01')
    transactions = transactions_access.get_transactions('2023-01-01', '2024-01-01', label='Food')
    assert len(transactions) == 1

def test_list_transactions(reporting_manager):
    reporting_manager.import_transactions('examples/transactions.csv')
    transactions = reporting_manager.transactions_access.get_transactions('2023-01-01', '2024-01-01')
    assert len(transactions) == 6

def test_generate_report(reporting_manager):
    reporting_manager.import_transactions('examples/transactions.csv')
    reporting_manager.classify_transactions('2023-01-01', '2024-01-01')
    report = reporting_manager.generate_report('2023-01-01', '2024-01-01')
    assert 'Food' in report
    assert 'Total' in report
    assert report['Food'] == 6.5
    assert report['Total'] == 2653.98  # Ensure the total matches expected value
