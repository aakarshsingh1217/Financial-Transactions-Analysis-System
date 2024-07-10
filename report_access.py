from abc import abstractmethod, ABCMeta

class IReportAccess(metaclass=ABCMeta):
    @abstractmethod
    def generate_report(self, transactions: list[dict[str, any]]) -> dict[str, float]:
        raise NotImplementedError

class ReportAccess(IReportAccess):
    @staticmethod
    def generate_report(transactions: list[dict[str, any]]) -> dict[str, float]:
        """
        Generate a report summary based on the given transactions.

        Args:
            transactions (List[Dict[str, Any]]): List of transaction dictionaries.

        Returns:
            Dict[str, float]: Summary of transactions with labels and total amount.
        """
        summary = {}  # Initialize an empty dictionary to store the summary
        for transaction in transactions:
            # Ensure every transaction has a label, defaulting to 'Unclassified' if none is present
            label = transaction.get('label', 'Unclassified')
            if label not in summary:
                summary[label] = 0.0  # Initialize label's total amount to zero if not already present
            summary[label] += transaction['amount']  # Add transaction amount to the label's total
        
        total = sum(summary.values())  # total amount by summing all label totals
        summary['Total'] = total  #'Total' key to the summary with the calculated total amount
        return summary  # Return the generated summary
