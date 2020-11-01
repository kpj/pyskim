import pytest
from click.testing import CliRunner

from pyskim import main, skim


@pytest.fixture
def df():
    # import pandas as pd
    #
    # df = pd.DataFrame({
    #
    # })

    import seaborn as sns
    df = sns.load_dataset('iris')

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
