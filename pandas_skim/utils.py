from typing import List, Union, Dict

import numpy as np
import pandas as pd


def group_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Group columns into numeric and categorical ones."""
    # TODO: improve this (e.g. datetime)
    dtype_groups = {
        'numeric': df.select_dtypes(include='number').columns,
        'categorical': df.select_dtypes(exclude='number').columns
    }

    assert {v for vs in dtype_groups.values() for v in vs} == set(df.columns)
    return dtype_groups


def text_barchart(values: List[int], safe: bool = True) -> str:
    # ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    bar_characters = [chr(i) for i in range(9601, 9609)]

    if safe:
        bar_characters = bar_characters[:-1]

    min_ = min(values)
    max_ = max(values)
    if min_ == max_:
        min_ -= 1
        max_ += 1
    bins = np.linspace(min_, max_, len(bar_characters) + 1)

    bar_values = pd.cut(
        values, bins=bins, labels=bar_characters, include_lowest=True
    )

    return ''.join(bar_values)


def text_histogram(
    values: np.ndarray,
    bins: Union[int, List[int]] = 10
) -> str:
    hist, _ = np.histogram(values.dropna(), bins=bins)
    return text_barchart(hist)


if __name__ == '__main__':
    txt = text_histogram(np.r_[
        np.random.normal(10, 2, size=500),
        np.random.normal(50, 7, size=500)
    ])
    print(txt)
