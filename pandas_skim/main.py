import pandas as pd

import click
import IPython

from .text_formatter import skim


@click.command(help='Print dataframe summary.')
@click.option('-d', '--delimiter', default=',', help='Delimiter of file.')
@click.option(
    '-i', '--interactive', is_flag=True,
    help='Open prompt with dataframe as `df` after displaying summary.'
)
@click.argument(
    'fname', type=click.Path(exists=True, dir_okay=False),
    metavar='<file>'
)
def main(delimiter: str, interactive: bool, fname: str) -> None:
    df = pd.read_csv(fname, sep=delimiter)
    skim(df)

    if interactive:
        IPython.embed()


if __name__ == '__main__':
    main()
