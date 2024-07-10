import csv
import re
from abc import abstractmethod, ABCMeta

class IRuleAccess(metaclass=ABCMeta):
    @abstractmethod
    def load_rules(self, rules_file: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_rules(self) -> list[dict[str, any]]:
        raise NotImplementedError

class RuleAccess(IRuleAccess):
    def __init__(self, rules_file: str) -> None:
        """
        Initialize RuleAccess with a path to the rules file.

        Args:
            rules_file (str): Path to the CSV file containing classification rules.
        """
        self.rules: list[dict[str, any]] = []
        self.load_rules(rules_file)

    def load_rules(self, rules_file: str) -> None:
        """
        Load classification rules from a CSV file.

        Args:
            rules_file (str): Path to the CSV file containing classification rules.

        The CSV file should have two columns: 'pattern' and 'label'.
        The 'pattern' column contains regex patterns for matching transaction descriptions.
        The 'label' column contains the label to assign if the pattern matches.
        """
        with open(rules_file, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            for row in reader:
                self.rules.append({'pattern': re.compile(row['pattern']), 'label': row['label']})

    def get_rules(self) -> list[dict[str, any]]:
        """
        Get the loaded classification rules.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing 'pattern' and 'label'.
        """
        return self.rules