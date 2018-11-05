# Grep utility on Python
Extremely limited version of grep linux utility on Python language.

### Requirements
Python 3.7

### Usage:
```python
usage: grep.py [-h] [-v] text filepath

Grep utility on Python

positional arguments:
  text        Text to find in file. Can be a regex.
  filepath    Path to file

optional arguments:
  -h, --help  show this help message and exit
  -v          Print lines which do not contain a text
```

### Tests
All tests can be found at `tests.py` file.

To call a tests just write
```python
python tests.py
```
