import pandas as pd

import click
import IPython

from typing import List

from .text_formatter import skim


@click.command(help="Quickly create summary statistics for a given dataframe.")
@click.option("-d", "--delimiter", default=",", help="Delimiter of file.")
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Open prompt with dataframe as `df` after displaying summary.",
)
@click.option(
    "--no-dtype-conversion",
    is_flag=True,
    default=False,
    help="Skip automatic dtype conversion.",
)
@click.option(
    "--groupby",
    multiple=True,
    help="Group dataframe by this/these variable(s).",
)
@click.argument("fname", type=click.Path(exists=True, dir_okay=False), metavar="<file>")
def main(
    delimiter: str,
    interactive: bool,
    no_dtype_conversion: bool,
    groupby: List[str],
    fname: str,
) -> None:
    # read dataframe
    df = pd.read_csv(fname, sep=delimiter, low_memory=False)

    if not no_dtype_conversion:
        # do type conversion here for availability in interactive mode
        df = df.convert_dtypes()

    # skim dataframe
    obj = df if not groupby else df.groupby(list(groupby))
    skim(obj)

    # interactive mode
    if interactive:
        # reduce loading time when interactive mode is not enabled
        IPython.embed()


if __name__ == "__main__":
    main()
