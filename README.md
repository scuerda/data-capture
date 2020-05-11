# Introduction

Data Capture is a simple shell-based Python programming for entering data, calculating statistics and answering questions about the data.

# Getting Started

## Requirements

Python 3.7+ (should work with lessor versions, but untested)
Python Virtual Environment (for running tests if you want to install dependencies)

## Creating a virtual environment and installing requirements

Create the virtual environment:

`python3 -m venv ./venv`

Activate the virtual environment:

`source venv/bin/activate`

Install the requirements:

`pip install -r requirements`

# Running Tests

`pytests`

# Running the Stats Shell

To launch the interactive shell, run: 

`python data_capture.py`

The shell offers a number of commands for entering data, calculating statistics, and asking questions of the data.

Here is a sample session:

```
$ (capture) python data_capture.py
Welcome to the Stats shell. Type help or ? to list commands. To exit type: quit.

(stats) help

Documented commands (type help <topic>):
========================================
add  btw  calc  exit  greater  gt  help  less  list  lt  quit  reset

(stats) add 3
(stats) add 9
(stats) add 3
(stats) add 4
(stats) add 6
(stats) calc
(stats) less 4
2
(stats) btw 3 6
4
(stats) greater 4
2
(stats) exit
Thank you for using Stats
```