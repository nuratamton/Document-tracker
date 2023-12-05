import pandas as pd
import matplotlib.pyplot as plt

class CountryContinent:
    def __init__(self):
        # loads country continent mapping on initialization
        self.country_cont_dict = self.country_cont_map()

    # function to retrieve a dictionary from the dataframe
    def country_cont_map(self):
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
    
    # function to plot a histogram
    def plot_hist(self, data, label, color):
        if (len(data) < 2):
            num_bins = 1
        else:
            num_bins = len(data.unique())
        # creates figure and subplot
        fig, ax  = plt.subplots(figsize=(10, 5))
        # creates a histogram with the same number of bins as unique values in data
        ax.hist(data, bins=num_bins, edgecolor="black", color=color)
        # the title for countries against number of viewers graph is set
        ax.set_title(f"View by {label}")
         # the label for x axis is set
        ax.set_xlabel(label)
         # the label for y axis is set
        ax.set_ylabel("Views")
        # set positions of the ticks
        ax.set_xticks(range(len(data.unique())))
        # creates a label for each unique element of data
        ax.set_xticklabels(data.unique(), rotation = 90)
        return fig

    # function to return the plotted histogram
    def uuid_country_cont_hist(self, uuid, data):
        # filters the data and gets only the selected UUID
        selected_uuid = data[data['subject_doc_id'] == uuid]
        # selects the country column after filtering data
        countries = selected_uuid['visitor_country']
        # to plot the histogram for viewers against country
        fig_country = self.plot_hist(countries, "Countries", "green")
        # continent names using the mapping dictionary
        continents = countries.map(self.country_cont_dict)
        # to plot the histogram for viewers against continent
        fig_cont = self.plot_hist(continents, "Continents", "brown")
        return fig_country, fig_cont