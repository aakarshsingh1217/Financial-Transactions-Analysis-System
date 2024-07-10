import click
from datetime import datetime
from transactions_access import TransactionsAccess
from classification_engine import ClassificationEngine
from report_access import ReportAccess
from reporting_manager import ReportingManager
from rule_access import RuleAccess

DATE_FORMAT='%Y-%m-%d'

arg_start_date = click.argument('start_date', type=click.DateTime(formats=[DATE_FORMAT]), metavar='START_DATE')
arg_end_date = click.argument('end_date', type=click.DateTime(formats=[DATE_FORMAT]), metavar='END_DATE', default=datetime.now().strftime(DATE_FORMAT))

@click.group()
def cli():
    pass

@cli.command(name='import')
@click.argument('transactions_file', type=click.Path(exists=True, dir_okay=False))
def transactions_import_command(transactions_file):
    """Imports the transactions from a file."""
    transactions_access = TransactionsAccess()
    reporting_manager = ReportingManager(transactions_access, None, None)
    reporting_manager.import_transactions(transactions_file)

@cli.command(name='classify')
@click.option('--rules', type=click.Path(exists=True, dir_okay=False), help='CSV file containing the classification rules')
@arg_start_date
@arg_end_date
def classify_command(rules, start_date, end_date):
    """Classifies each transaction in a time period."""
    transactions_access = TransactionsAccess()
    rule_access = RuleAccess(rules)
    classification_engine = ClassificationEngine(rule_access)
    reporting_manager = ReportingManager(transactions_access, classification_engine, None)
    reporting_manager.classify_transactions(start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

@cli.command(name='list')
@click.option('--label', help=("Output transactions corresponding to this label only. If not set, all transactions are shown."))
@arg_start_date
@arg_end_date
def list_command(label, start_date, end_date):
    """Lists transactions corresponding to a given label in a time period."""
    transactions_access = TransactionsAccess()
    reporting_manager = ReportingManager(transactions_access, None, None)
    reporting_manager.list_transactions(start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT), label)

@cli.command(name='report')
@arg_start_date
@arg_end_date
def report_command(start_date, end_date):
    """Summarises expenditure in a period of time."""
    transactions_access = TransactionsAccess()
    report_access = ReportAccess()
    reporting_manager = ReportingManager(transactions_access, None, report_access)
    reporting_manager.generate_report(start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

if __name__ == '__main__':
    cli()
