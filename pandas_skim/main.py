import pandas as pd

import click

from .text_formatter import skim


@click.command(help='Print dataframe summary.')
@click.argument(
    'fname', type=click.Path(exists=True, dir_okay=False),
    metavar='<file>'
)
def main(fname: str) -> None:
    df = pd.read_csv(fname)
    skim(df)


if __name__ == '__main__':
    main()
