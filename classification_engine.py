import re

class ClassificationEngine:
    def __init__(self, rule_access) -> None:
        """
        Initialize the ClassificationEngine with a rule access object.

        Args:
            rule_access (RuleAccess): An object providing access to classification rules.
        """
        self.rule_access = rule_access

    def classify_transaction(self, transaction: dict[str, any]) -> str:
        """
        Classify a single transaction based on classification rules.

        Args:
            transaction (dict): Transaction information.

        Returns:
            str: Label for the classified transaction.
        """
        description = transaction['description'].lower()
        for rule in self.rule_access.get_rules():
            if re.search(rule['pattern'], description):
                return rule['label']
        return 'Unclassified'

    def classify_transactions(self, transactions: list[dict[str, any]]) -> None:
        """
        Classify a list of transactions based on classification rules.

        Args:
            transactions (list): List of transaction dictionaries.

        Modifies:
            Adds 'label' key to each transaction dictionary with the classification result.
        """
        for transaction in transactions:
            transaction['label'] = self.classify_transaction(transaction)
