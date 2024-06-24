# File Manager

## Description
A simple file manager that lists, sorts, and filters files and directories with detailed information.

## Features
- List all files and directories
- Filter by file or directory
- Sort by modification time and size, in ascending or descending order.
- Display detailed information from file. (First column corresponds to permissions, 2nd column corresponds to
size, 3rd to 5th is date and time, and the last is file or directory name)
- Display detailed information from file in reverse. Command: python -m pyls -l -r
- Print a helpful message. Include description and usage. Command: ls --help


## Installation
To install the required dependencies, run on bash:
pip install -r requirements.txt


## Running test cases
pytest test_pyls.py
