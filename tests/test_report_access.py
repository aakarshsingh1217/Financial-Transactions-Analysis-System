import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from report_access import ReportAccess

def test_generate_report():
    transactions = [
        {'amount': 6.50, 'label': 'Food'},
        {'amount': 249.99, 'label': 'Clothing'},
        {'amount': 24.99, 'label': 'Unclassified'},
        {'amount': 950.00, 'label': 'Home'},
        {'amount': 472.50, 'label': 'Utilities'},
        {'amount': 950.00, 'label': 'Home'}
    ]
    report_access = ReportAccess()
    report = report_access.generate_report(transactions)
    assert report['Food'] == 6.50
    assert report['Clothing'] == 249.99
    assert report['Unclassified'] == 24.99
    assert report['Home'] == 1900.00
    assert report['Utilities'] == 472.50
    assert report['Total'] == 2653.98