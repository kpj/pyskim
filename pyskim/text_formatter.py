import warnings

from typing import Any

import pandas as pd

import tabulate

from .column_dispatch import describe_columns


class TextFormatter:
    def __init__(self, df: pd.DataFrame, width: int = 100):
        self.df = df
        self.width = width
        self.sep_char = "─"

    def _render_header(self, title: str) -> str:
        header = f"{self.sep_char * 2} {title} "
        header += self.sep_char * (self.width - len(header))
        return header

    def _render_divider(self) -> str:
        return self.sep_char * (self.width // 2) + "\n"

    def _render_dataframe_as_table(self, df: pd.DataFrame, **kwargs: Any) -> str:
        # , floatfmt='.3f'
        return tabulate.tabulate(df, headers="keys", **kwargs)

    def render_dataframe_overview(self) -> str:
        txt = ""

        header = self._render_header("Data Summary")
        txt += f"{header}\n"

        txt += self._render_dataframe_as_table(
            pd.DataFrame(
                {
                    "type": ["Number of rows", "Number of columns"],
                    "value": self.df.shape,
                }
            ).set_index("type"),
            floatfmt=".0f",
        )
        txt += "\n"

        txt += self._render_divider()

        dtype_freqs = self.df.dtypes.value_counts().to_frame("Count")
        txt += "Column type frequency:\n"
        txt += self._render_dataframe_as_table(dtype_freqs)
        txt += "\n\n"

        return txt

    def render_variable_summaries(self) -> str:
        txt = ""

        # generate descriptions
        described_columns = set()
        for type_, df_summary in describe_columns(self.df):
            if df_summary is None:
                continue
            described_columns.update(df_summary["name"])

            header = self._render_header(f"Variable type: {type_}")
            txt += f"{header}\n"

            txt += self._render_dataframe_as_table(df_summary, floatfmt=".3g")
            txt += "\n\n"

        # check if all columns were described
        undescribed_columns = set(self.df.columns) - described_columns
        if len(undescribed_columns) > 0:
            warnings.warn(
                f"The following columns had no matching descriptor: {undescribed_columns}"
            )

        return txt


def skim(df: pd.DataFrame, convert_dtypes=False) -> None:
    if convert_dtypes:
        df = df.convert_dtypes()

    fmtr = TextFormatter(df)

    print(fmtr.render_dataframe_overview(), end="")
    print(fmtr.render_variable_summaries(), end="")
