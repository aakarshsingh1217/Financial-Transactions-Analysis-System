import csv
import os
from datetime import datetime, timedelta
from abc import abstractmethod, ABCMeta
from typing import Optional

class ITransactionsAccess(metaclass=ABCMeta):
    @abstractmethod
    def load_transactions(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def save_transactions(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def import_transactions(self, transactions_file: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_transactions(self, start_date: datetime, end_date: datetime, label: Optional[str]) -> list[dict[str, any]]:
        raise NotImplementedError

class TransactionsAccess:
    def __init__(self, storage_file: str = 'transactions_storage.csv') -> None:
        """
        Initialize TransactionsAccess with a storage file.
        
        Args:
            storage_file (str): Path to the storage file. Defaults to 'transactions_storage.csv'.
        """
        self.storage_file = storage_file
        self.transactions = []
        if os.path.exists(self.storage_file):
            self.load_transactions()

    def load_transactions(self) -> None:
        """
        Load transactions from the storage file.
        """
        with open(self.storage_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # First, try the expected day/month/year format
                    row['date'] = datetime.strptime(row['date'], '%d/%m/%Y')
                except ValueError:
                    # If the first format fails, try the year-month-day format
                    row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
                row['amount'] = float(row['amount'])
                self.transactions.append(row)

    def save_transactions(self) -> None:
        """
        Save transactions to the storage file.
        """
        with open(self.storage_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'description', 'amount', 'label'])
            writer.writeheader()
            for transaction in self.transactions:
                # Create a copy of the transaction dict for CSV writing
                transaction_copy = transaction.copy()
                # Convert datetime to string in the copy only
                transaction_copy['date'] = transaction_copy['date'].strftime('%Y-%m-%d')
                writer.writerow(transaction_copy)

    def import_transactions(self, transactions_file: str) -> None:
        """
        Import transactions from a CSV file and save them to storage.
        
        Args:
            transactions_file (str): Path to the CSV file containing transactions.
        """
        with open(transactions_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle multiple date formats, prioritize day/month/year as per your data
                try:
                    row['date'] = datetime.strptime(row['date'], '%d/%m/%Y')
                except ValueError:
                    raise ValueError(f"Date {row['date']} does not match any known formats")
                
                row['amount'] = float(row['amount'])
                row['label'] = 'Unclassified'  # Initial label for all imported transactions
                self.transactions.append(row)
        self.save_transactions()

    def get_transactions(self, start_date: datetime, end_date: datetime, label: Optional[str] = None) -> list[dict[str, any]]:
        """
        Get transactions within a specified date range and optionally filtered by label.

        Args:
            start_date (datetime): Start date.
            end_date (datetime): End date.
            label (str, optional): Filter transactions by label. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of filtered transactions.
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Adjust end_date to include the entire day
        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        # Filter transactions
        if label:
            filtered_transactions = [txn for txn in self.transactions if start_date <= txn['date'] < end_date and txn['label'] == label]
        else:
            filtered_transactions = [txn for txn in self.transactions if start_date <= txn['date'] < end_date]

        return filtered_transactions
