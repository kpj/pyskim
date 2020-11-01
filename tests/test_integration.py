import pytest

from pyskim import skim


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
