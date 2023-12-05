import pandas as pd
import matplotlib.pyplot as plt

# function to retrieve a dictionary from the dataframe
def country_cont_map():
    # load the full dataset into dataset
    dataset = pd.read_csv("datasets/country_continent.csv", encoding="ISO-8859-1")
    # selects only country and continent fields and stores it
    mapping = dataset[["code_2", "continent"]]
    # country column is set as index
    # continent column has country as index
    # to_dict() is used to convert it into a dictionary
    country_cont = mapping.set_index('code_2')['continent'].to_dict()
    # return the contry_continent mapping
    return country_cont

# function to return the plotted histogram
def uuid_country_hist(uuid, data, country_cont_dict):

    # filters the data and gets only the selected UUID
    selected_uuid = data[data['subject_doc_id'] == uuid]
    # selects the country column after filtering data
    countries = selected_uuid['visitor_country']
    print(countries)

    # to plot the histogram for viewers against country
    fig_country, ax_country = plt.subplots(figsize=(10, 5))
    ax_country.hist(countries, bins = len(countries.unique()), edgecolor="black", color = "green")
    # the title for countries against number of viewers graph is set
    ax_country.set_title('Views by Country')
    # the label for x axis is set
    ax_country.set_xlabel('Country')
    # the label for y axis is set
    ax_country.set_ylabel('Views')
    ax_country.set_xticks(range(len(countries.unique())))
    ax_country.set_xticklabels(countries.unique(), rotation = 90)

    # continent names using the mapping dictionary
    continents = countries.map(country_cont_dict)

    # to plot the histogram for viewers against continent
    fig_cont, ax_cont = plt.subplots(figsize=(10, 5))
    # 
    ax_cont.hist(continents, bins=len(continents.unique()), edgecolor="black", color="brown")
    # the title for continent against number of viewers graph
    ax_cont.set_title('Views by Continent')
    # the label for x axis
    ax_cont.set_xlabel('Continent')
    # the label for y axis
    ax_cont.set_ylabel('Views')
    ax_cont.set_xticks(range(len(continents.unique())))
    ax_cont.set_xticklabels(continents.unique(), rotation = 90)

    return fig_country, fig_cont