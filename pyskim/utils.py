from typing import List, Union

import numpy as np
import pandas as pd


def text_barchart(values: List[int], safe: bool = True) -> str:
    """Render given values as bars in signle line."""
    # ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    bar_characters = [chr(i) for i in range(9601, 9609)]

    if safe:
        bar_characters = bar_characters[:-1]

    min_ = min(values)
    max_ = max(values)
    if min_ == max_:
        if min_ == 0:
            # bars should be empty
            max_ = 1
        else:
            # bars should be something non-empty
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
    """Render histogram of given `values` in single line."""
    hist, _ = np.histogram(values.dropna(), bins=bins)
    return text_barchart(hist)


def shorten_str(text: str, width: int = 30, suffix: str = '[...]') -> str:
    """Custom string shortening (`textwrap.shorten` collapses whitespace)."""
    if len(text) <= width:
        return text
    else:
        return text[:width-len(suffix)] + suffix


def top_counts(column: pd.Series, num: int = 3) -> str:
    """Render values of column with highest counts to string."""
    return ', '.join(
        f'{shorten_str(str(k))}: {v}'
        for k, v in column.value_counts().head(num).items()
    )


if __name__ == '__main__':
    txt = text_histogram(pd.Series(np.r_[
        np.random.normal(10, 2, size=500),
        np.random.normal(50, 7, size=500)
    ]))
    print(txt)
