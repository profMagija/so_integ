# StackOverflow Integration for Python

A simple exception hook to print a helpful StackOverflow search link. Also an experiment into site customization. Saves you a copy-paste.

## Installation

Download / clone this repo, and run the script with `install` argument:

```sh
python so_integ.py install
```

## Usage

The script is added to your user site customization path. This means that it is active for all interactive and non-interactive sessions. Here are few examples:

```python
>>> [0,1,2][3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range

Search on stack overflow?
    https://stackoverflow.com/search?q=IndexError%3A%20list%20index%20out%20of%20range

>>> 1 / 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero

Search on stack overflow?
    https://stackoverflow.com/search?q=ZeroDivisionError%3A%20division%20by%20zero

```

## Uninstalling

Just run with `uninstall` argument:

```sh
python so_integ.py uninstall
```

Alternatively, remove the initialization code from your `usercustomize.py` file. The file is located in user site directory, which can be found using
```sh
python -m site --user-site
```