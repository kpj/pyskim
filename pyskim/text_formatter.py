import warnings

from typing import Any

import pandas as pd

import tabulate

from typing import Union

from .column_dispatch import describe_columns


class TextFormatter:
    def __init__(
        self,
        obj: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
        width: int = 100,
    ):
        self.obj = obj
        self.width = width
        self.sep_char = "─"

        # sanity check
        type_ = type(self.obj)
        if type_ not in [pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:
            raise NotImplementedError(f"Skimming not implemented for type {type_}")

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
        df = self.obj if isinstance(self.obj, pd.DataFrame) else self.obj.obj

        # render
        txt = ""

        header = self._render_header("Data Summary")
        txt += f"{header}\n"

        txt += self._render_dataframe_as_table(
            pd.DataFrame(
                {
                    "type": ["Number of rows", "Number of columns"],
                    "value": df.shape,
                }
            ).set_index("type"),
            floatfmt=".0f",
        )
        txt += "\n"

        txt += self._render_divider()

        dtype_freqs = df.dtypes.value_counts().to_frame("Count")
        txt += "Column type frequency:\n"
        txt += self._render_dataframe_as_table(dtype_freqs)
        txt += "\n\n"

        return txt

    def _describe_df(self, df: pd.DataFrame) -> str:
        txt = ""

        # generate descriptions
        described_columns = set()
        for type_, df_summary in describe_columns(df):
            if df_summary is None:
                continue
            described_columns.update(df_summary["name"])

            header = self._render_header(f"Variable type: {type_}")
            txt += f"{header}\n"

            txt += self._render_dataframe_as_table(df_summary, floatfmt=".3g")
            txt += "\n\n"

        # check if all columns were described
        undescribed_columns = set(df.columns) - described_columns
        if len(undescribed_columns) > 0:
            warnings.warn(
                f"The following columns had no matching descriptor: {undescribed_columns}"
            )

        return txt

    def render_variable_summaries(self) -> str:
        if isinstance(self.obj, pd.DataFrame):
            return self._describe_df(self.obj)
        else:
            grouping_keys = self.obj.__dict__["keys"]
            grouping_keys = (
                [grouping_keys] if isinstance(grouping_keys, str) else grouping_keys
            )

            txt = ""
            for group_name, group_df in self.obj:
                group_name = [group_name] if isinstance(group_name, str) else group_name

                txt += (
                    self._render_header(
                        f"Grouping ({group_df.shape[0]} rows): "
                        + ", ".join(
                            f"{gk}={gv}" for gk, gv in zip(grouping_keys, group_name)
                        )
                    )
                    + "\n"
                )

                txt += self._describe_df(group_df)

            return txt


def skim(obj: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]) -> None:
    fmtr = TextFormatter(obj)

    print(fmtr.render_dataframe_overview(), end="")
    print(fmtr.render_variable_summaries(), end="")
