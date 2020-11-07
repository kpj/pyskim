import pytest
from click.testing import CliRunner

from pyskim import main, skim


@pytest.fixture
def df():
    import numpy as np
    import pandas as pd

    N = 100
    df = pd.DataFrame({
        'boolean_column': np.random.choice([True, False], size=N),
        'int_column': np.r_[
            np.random.randint(-10, 10, size=N // 2),
            np.random.randint(50, 80, size=N // 2)
        ],
        'float_column': np.r_[
            np.random.normal(10, 2, size=N // 2),
            np.random.normal(50, 7, size=N // 2)
        ],
        'category_column': pd.Series(
            np.random.choice(['apple', 'orange'], size=N),
            dtype='category'),
        'string_column': pd.Series(
            np.random.choice(['foo', 'bar', 'baz', 'qux'], size=N),
            dtype='string'),
        'object_column': pd.Series(
            np.random.choice(['obj', 1, False], size=N),
            dtype='object')
    })

    return df


def test_integration(capfd, df):
    skim(df)
    out, err = capfd.readouterr()
    assert 'Data Summary' in out


def test_cli(df):
    runner = CliRunner()
    with runner.isolated_filesystem():
        fname = 'data.csv'
        df.to_csv(fname)

        # run program
        result = runner.invoke(main, [fname])

        # test output
        assert result.exit_code == 0
        assert 'Data Summary' in result.output
