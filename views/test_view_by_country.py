import pytest
import pandas as pd

from view_by_country import CountryContinent

@pytest.fixture(scope="module")
def cc_instance():
    return CountryContinent()

# test to check the mapping function
def test_country_cont_map(cc_instance):
    mapping = cc_instance.country_cont_map()
    assert isinstance(mapping, dict)
    assert "US" in mapping
    assert "ES" in mapping

# test for plotting function
def test_plot_hist_countries(cc_instance):
    sample_data = pd.Series(['US', 'FR', 'US', 'DE'])
    fig = cc_instance.plot_hist(sample_data, "Countries")
    assert fig is not None

# test if there is only one country for plotting
def test_single_data_point(cc_instance):
    single_data = pd.Series(['US'])
    fig = cc_instance.plot_hist(single_data, "Countries")
    assert fig is not None

# test if there is no country for plotting
def test_plot_hist_with_empty_data(cc_instance):
    empty_data = pd.Series([])
    fig = cc_instance.plot_hist(empty_data, "Countries")
    assert fig is not None
