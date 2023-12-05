import pytest
import pandas as pd
from view_by_country import CountryContinent

@pytest.fixture
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
    fig = cc_instance.plot_hist(sample_data, "Countries", "green")
    assert fig is not None

# test if there is only one country for plotting
def test_single_data_point(cc_instance):
    single_data = pd.Series(['US'])
    fig = cc_instance.plot_hist(single_data, "Countries", "green")
    assert fig is not None

# test if there is no country for plotting
def test_plot_hist_with_empty_data(cc_instance):
    empty_data = pd.Series([])
    fig = cc_instance.plot_hist(empty_data, "Countries", "green")
    assert fig is not None

# def test_uuid_country_hist(cc_instance):
#     fig_country, fig_continent = cc_instance.uuid_country_cont_hist()
#     assert fig_country is not None
#     assert fig_continent is not None

# def test_uuid_country_hist_with_no_data_uuid(country_continent_instance):
#     no_data_uuid = '140124195414-f5a9acegd5eb6631aa6b39422fba6708'
#     fig_country, fig_continent = country_continent_instance.uuid_country_cont_hist(no_data_uuid)
#     assert fig_country is not None
#     assert fig_continent is not None