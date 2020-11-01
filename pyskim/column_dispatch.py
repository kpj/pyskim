import warnings

import numpy as np

from .utils import text_histogram


def describe_numeric(column):
    return {
        'name': column.name,
        'na_count': column.isna().sum(),  # / column.shape[0]
        'mean': column.mean(),
        'sd': column.std(),
        'hist': text_histogram(column)
    }


def describe_categorical(column):
    top_counts = ', '.join(
        f'{k}: {v}' for k, v in column.value_counts().head(3).items()
    )

    return {
        'name': column.name,
        'na_count': column.isna().sum(),  # / column.shape[0]
        'n_unique': column.nunique(),
        'top_counts': top_counts
    }


def describe_column(column):
    # functools.singledispatch doesn't work when trying to detect a columns dtype
    DISPATCH_MAP = {
        np.dtype('float64'): describe_numeric,
        np.dtype('int64'): describe_numeric,
        np.dtype('object'): describe_categorical
    }

    dtype = column.dtype
    func = DISPATCH_MAP.get(dtype, None)

    if func is None:
        warnings.warn(f'Unknown dtype {dtype} for column {column.name}, skipping', RuntimeWarning)
        return {}

    return func(column)
