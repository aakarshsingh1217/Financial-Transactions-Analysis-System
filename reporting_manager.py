from transactions_access import TransactionsAccess
from classification_engine import ClassificationEngine
from report_access import ReportAccess
from rule_access import RuleAccess
from typing import Optional

class ReportingManager:
    def __init__(self, transactions_access: TransactionsAccess, classification_engine: Optional[ClassificationEngine], report_access: Optional[ReportAccess]) -> None:
        """
        Initialize the ReportingManager with access to transaction, classification, and report functionality.

        Args:
            transactions_access (TransactionsAccess): Object providing access to transaction data.
            classification_engine (ClassificationEngine, optional): Object providing classification functionality.
            report_access (ReportAccess, optional): Object providing access to report generation.
        """
        self.transactions_access = transactions_access
        self.classification_engine = classification_engine
        self.report_access = report_access

    def import_transactions(self, transactions_file: str) -> None:
        """
        Import transactions from a file and save them to storage.

        Args:
            transactions_file (str): Path to the CSV file containing transactions.
        """
        self.transactions_access.import_transactions(transactions_file)
        print(f"Imported {len(self.transactions_access.transactions)} transactions.")

    def classify_transactions(self, start_date: str, end_date: str) -> None:
        """
        Classify transactions within a date range using classification rules.

        Args:
            start_date (str): Start date for the transaction classification.
            end_date (str): End date for the transaction classification.
        """
        transactions = self.transactions_access.get_transactions(start_date, end_date)
        self.classification_engine.classify_transactions(transactions)
        self.transactions_access.save_transactions()

        # Print classification output for each transaction
        for txn in transactions:
            if txn['label'] == 'Unclassified':
                print(f"{txn['date'].strftime('%Y-%m-%d')} {txn['description']}: {txn['amount']} unable to classify")
            else:
                print(f"{txn['date'].strftime('%Y-%m-%d')} {txn['description']}: {txn['amount']} classified as {txn['label']}")
        print(f"{len(transactions)} transactions processed")

    def list_transactions(self, start_date: str, end_date: str, label: Optional[str] = None) -> None:
        """
        List transactions within a date range and optional label filter.

        Args:
            start_date (str): Start date for listing transactions.
            end_date (str): End date for listing transactions.
            label (str, optional): Filter transactions by label. Defaults to None.
        """
        transactions = self.transactions_access.get_transactions(start_date, end_date, label)
        for txn in transactions:
            label_display = f"[{txn['label']}]" if txn['label'] else "[]"
            print(f"{txn['date'].strftime('%Y-%m-%d')} {txn['description']}: {txn['amount']} {label_display}")
        print(f"{len(transactions)} transactions listed")

    def generate_report(self, start_date: str, end_date: str) -> dict[str, float]:
        """
        Generate a report for transactions within a date range.

        Args:
            start_date (str): Start date for the report.
            end_date (str): End date for the report.

        Returns:
            Dict[str, float]: Summary report with labels and total amounts.
        """
        transactions = self.transactions_access.get_transactions(start_date, end_date)
        report = self.report_access.generate_report(transactions)
        for label, amount in report.items():
            print(f"{label}: {amount:.2f}")
        return report
