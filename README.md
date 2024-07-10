# Code description

The code given in this folder provides a skeleton and some functions that you can use to develop your solution.

## Installation

Several packages are required for this code to work. They are listed in file `requirements.txt`.

It is recommended that you create a dedicated Python environment for this assignment. That is, do not install the necessary packages in your system-wide Python environment.

To create a Python environment, you can use [conda](https://www.anaconda.com/download) or venv/pip.

Using `conda` (run from a terminal/command line):

```shell
conda create --channel conda-forge --name whateverYouChoose --file requirements.txt

conda activate whateverYouChoose
```

Instructions for `venv` and `pip` are at <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/>

use [Visual Studio Code](https://code.visualstudio.com/), you will need to select this environment as the Python interpreter.

## Execution

You can run the code from a terminal/command line using the example commands below:

```shell
python financial_report.py import examples/transactions.csv

python financial_report.py classify rules=examples/rules.csv 2023-01-01 2024-01-01 

python python financial_report.py list label=Home 2023-01-01 2024-02-01

python financial_report.py list label=Unclassified 2023-01-01 2024-02-01

python financial_report.py list 2023-01-01 2024-02-01

python financial_report.py report 2023-01-01 2024-01-01
```