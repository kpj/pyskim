import pandas as pd

import tabulate

from .utils import group_column_types
from .column_dispatch import describe_column


class TextFormatter():
    def __init__(self, df: pd.DataFrame, width: int = 80):
        self.df = df
        self.width = width
        self.sep_char = '─'

    def _render_header(self, title: str) -> str:
        header = f'{self.sep_char * 2} {title} '
        header += self.sep_char * (self.width - len(header))
        return header

    def _render_divider(self) -> str:
        return self.sep_char * (self.width // 2) + '\n'

    def _render_dataframe_as_table(self, df: pd.DataFrame) -> str:
        # , floatfmt='.3f'
        return tabulate.tabulate(df, headers='keys')

    def render_dataframe_overview(self) -> str:
        txt = ''

        header = self._render_header('Data Summary')
        txt += f'{header}\n'

        txt += self._render_dataframe_as_table(pd.DataFrame({
            'type': ['Number of rows', 'Number of columns'],
            'value': self.df.shape
        }).set_index('type'))
        txt += '\n'

        txt += self._render_divider()

        dtype_freqs = self.df.dtypes.value_counts().to_frame('Count')
        txt += 'Column type frequency:\n'
        txt += self._render_dataframe_as_table(dtype_freqs)
        txt += '\n\n'

        return txt

    def render_variable_summaries(self) -> str:
        txt = ''

        for type_, columns in group_column_types(self.df).items():
            header = self._render_header(f'Variable type: {type_}')
            txt += f'{header}\n'

            df_summary = pd.DataFrame(
                self.df[columns].apply(describe_column).to_list()
            )

            txt += self._render_dataframe_as_table(df_summary)
            txt += '\n\n'

        return txt


def skim(df: pd.DataFrame) -> None:
    fmtr = TextFormatter(df)

    print(fmtr.render_dataframe_overview(), end='')
    print(fmtr.render_variable_summaries(), end='')
