# pyskim

[![PyPI](https://img.shields.io/pypi/v/pyskim.svg?style=flat)](https://pypi.python.org/pypi/pyskim)

Quickly create summary statistics for a given dataframe.

This package aspires to be as awesome as [skimr](https://github.com/ropensci/skimr).


## Installation

```bash
$ pip install pyskim
```

## Usage

### Commandline tool


`pyskim` can be used from the commandline:

```bash
$ pyskim iris.csv
── Data Summary ────────────────────────────────────────────────────────────────────────────────────
type                 value
-----------------  -------
Number of rows         150
Number of columns        5
──────────────────────────────────────────────────
Column type frequency:
           Count
-------  -------
float64        4
string         1

── Variable type: number ───────────────────────────────────────────────────────────────────────────
    name            na_count    mean     sd    p0    p25    p50    p75    p100  hist
--  ------------  ----------  ------  -----  ----  -----  -----  -----  ------  ----------
 0  sepal_length           0    5.84  0.828   4.3    5.1   5.8     6.4     7.9  ▂▆▃▇▄▇▅▁▁▁
 1  sepal_width            0    3.06  0.436   2      2.8   3       3.3     4.4  ▁▁▄▅▇▆▂▂▁▁
 2  petal_length           0    3.76  1.77    1      1.6   4.35    5.1     6.9  ▇▃▁▁▂▅▆▄▃▁
 3  petal_width            0    1.2   0.762   0.1    0.3   1.3     1.8     2.5  ▇▂▁▂▂▆▁▄▂▃

── Variable type: string ───────────────────────────────────────────────────────────────────────────
    name               na_count    n_unique  top_counts
--  ---------------  ----------  ----------  -----------------------------------------
 0          species           0           3  versicolor: 50, setosa: 50, virginica: 50
```

Full overview:

```bash
$ pyskim --help
Usage: pyskim [OPTIONS] <file>

  Quickly create summary statistics for a given dataframe.

Options:
  -d, --delimiter TEXT   Delimiter of file.
  -i, --interactive      Open prompt with dataframe as `df` after displaying
                         summary.

  --no-dtype-conversion  Skip automatic dtype conversion.
  --help                 Show this message and exit.
```

### Python API

Alternatively, it is possible to use it in code:

```python
>>> from pyskim import skim
>>> from seaborn import load_dataset

>>> iris = load_dataset('iris')
>>> skim(iris)
# ── Data Summary ────────────────────────────────────────────────────────────────────────────────────
# type                 value
# -----------------  -------
# Number of rows         150
# Number of columns        5
# ──────────────────────────────────────────────────
# Column type frequency:
#            Count
# -------  -------
# float64        4
# string         1
#
# ── Variable type: number ───────────────────────────────────────────────────────────────────────────
#     name            na_count    mean     sd    p0    p25    p50    p75    p100  hist
# --  ------------  ----------  ------  -----  ----  -----  -----  -----  ------  ----------
#  0  sepal_length           0    5.84  0.828   4.3    5.1   5.8     6.4     7.9  ▂▆▃▇▄▇▅▁▁▁
#  1  sepal_width            0    3.06  0.436   2      2.8   3       3.3     4.4  ▁▁▄▅▇▆▂▂▁▁
#  2  petal_length           0    3.76  1.77    1      1.6   4.35    5.1     6.9  ▇▃▁▁▂▅▆▄▃▁
#  3  petal_width            0    1.2   0.762   0.1    0.3   1.3     1.8     2.5  ▇▂▁▂▂▆▁▄▂▃
#
# ── Variable type: string ───────────────────────────────────────────────────────────────────────────
#     name               na_count    n_unique  top_counts
# --  ---------------  ----------  ----------  -----------------------------------------
#  0          species           0           3  versicolor: 50, setosa: 50, virginica: 50
```
