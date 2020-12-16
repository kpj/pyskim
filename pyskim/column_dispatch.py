import warnings
from typing import Any, Dict, Callable, Iterator, Tuple

import numpy as np
import pandas as pd

from .utils import text_histogram, top_counts


def describe_numeric(column: pd.Series) -> Dict[str, Any]:
    return {
        'mean': column.mean(),
        'sd': column.std(),
        **{f'p{q*100:.0f}': column.quantile(q=q)
           for q in [0, .25, .5, .75, 1]},
        'hist': text_histogram(column)
    }


def describe_categorical(column: pd.Series) -> Dict[str, Any]:
    return {
        'n_unique': column.nunique(),
        'top_counts': top_counts(column)
    }


def describe_boolean(column: pd.Series) -> Dict[str, Any]:
    return {
        'mean': column.mean(),
        'top_counts': top_counts(column)
    }


def describe_datetime(column: pd.Series) -> Dict[str, Any]:
    return {
        'n_unique': column.nunique(),
        'mean': column.mean(),
        'min': column.min(),
        'max': column.max()
    }


def describe_column(
    column: pd.Series,
    func: Callable[[pd.Series], Dict[str, Any]]
) -> Dict[str, Any]:
    """Provide statistics useful for all dtypes and call descriptor."""
    # clean column
    if np.inf in column.dropna().values or -np.inf in column.dropna().values:
        msg = f'Column "{column.name}" contains +-Inf, replacing with NA.'
        warnings.warn(RuntimeWarning(msg))

        column = column.replace([np.inf, -np.inf], pd.NA)

    # compute statistics
    return {
        'name': column.name,
        'na_count': column.isna().sum(),  # / column.shape[0]
        **func(column)
    }


def describe_columns(df: pd.DataFrame) -> Iterator[Tuple[str, pd.DataFrame]]:
    DISPATCH_MAP = {
        'boolean': describe_boolean,
        'number': describe_numeric,
        'category': describe_categorical,
        'string': describe_categorical,
        'datetime': describe_datetime,
        'object': describe_categorical
    }

    for type_, func in DISPATCH_MAP.items():
        df_sub = df.select_dtypes(include=type_)
        if df_sub.empty:
            yield type_, None
            continue

        df_summary = pd.DataFrame(
            df_sub.apply(lambda x: describe_column(x, func)).to_list())
        yield type_, df_summary
