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
── Data Summary ────────────────────────────────────────────────────────────────
type                 value
-----------------  -------
Number of rows         150
Number of columns        5
────────────────────────────────────────
Column type frequency:
           Count
-------  -------
float64        4
object         1

── Variable type: numeric ──────────────────────────────────────────────────────
    name            na_count     mean        sd  hist
--  ------------  ----------  -------  --------  ----------
 0  sepal_length           0  5.84333  0.828066  ▂▆▃▇▄▇▅▁▁▁
 1  sepal_width            0  3.05733  0.435866  ▁▁▄▅▇▆▂▂▁▁
 2  petal_length           0  3.758    1.7653    ▇▃▁▁▂▅▆▄▃▁
 3  petal_width            0  1.19933  0.762238  ▇▂▁▂▂▆▁▄▂▃

── Variable type: categorical ──────────────────────────────────────────────────
    name       na_count    n_unique  top_counts
--  -------  ----------  ----------  -----------------------------------------
 0  species           0           3  setosa: 50, versicolor: 50, virginica: 50
```

Full overview:

```bash
$ pyskim --help
Usage: pyskim [OPTIONS] <file>

  Print dataframe summary.

Options:
  -d, --delimiter TEXT  Delimiter of file.
  -i, --interactive     Open prompt with dataframe as `df` after displaying
                        summary.

  --help                Show this message and exit.
```

### Python API

Alternatively, it is possible to use it in code:

```python
>>> from pyskim import skim
>>> from seaborn import load_dataset

>>> iris = load_dataset('iris')
>>> skim(iris)
# ── Data Summary ────────────────────────────────────────────────────────────────
# type                 value
# -----------------  -------
# Number of rows         150
# Number of columns        5
# ────────────────────────────────────────
# Column type frequency:
#            Count
# -------  -------
# float64        4
# object         1
#
# ── Variable type: numeric ──────────────────────────────────────────────────────
#     name            na_count     mean        sd  hist
# --  ------------  ----------  -------  --------  ----------
#  0  sepal_length           0  5.84333  0.828066  ▂▆▃▇▄▇▅▁▁▁
#  1  sepal_width            0  3.05733  0.435866  ▁▁▄▅▇▆▂▂▁▁
#  2  petal_length           0  3.758    1.7653    ▇▃▁▁▂▅▆▄▃▁
#  3  petal_width            0  1.19933  0.762238  ▇▂▁▂▂▆▁▄▂▃
#
# ── Variable type: categorical ──────────────────────────────────────────────────
#     name       na_count    n_unique  top_counts
# --  -------  ----------  ----------  -----------------------------------------
#  0  species           0           3  setosa: 50, versicolor: 50, virginica: 50
```
