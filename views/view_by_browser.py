import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from user_agents import parse
import pandas as pd
import numpy as np
from data_op.data_loader import Reader

class BrowserCount:
    def __init__(self, data):
        self.data = data

    def browser_count(self,doc_id):
        #filtering date based on document id given
        filter_document = self.data[self.data["env_doc_id"]== doc_id]
        #retrieving browser name removing uneccessary information using parser function from user_agent
        filter_document["visitor_useragent"] = filter_document["visitor_useragent"].apply(lambda x: parse(x).browser.family)
        #removing repeating users using the same browser 
        final_data = filter_document.drop_duplicates(subset=["visitor_useragent", "visitor_uuid"])  
        # calculating number of users for each browser used
        plot_data = final_data.groupby("visitor_useragent")["visitor_uuid"].nunique().reset_index()
        #Storing browser name
        browser_name= plot_data["visitor_useragent"].unique() 
        # Storing number of users per browser 
        user_count = plot_data["visitor_uuid"]  
        # storing data for plotting the histogram
        hist_data = np.repeat(browser_name, user_count)
        fig = plt.figure(figsize=(5, 3))
        # mapping the values for graph
        browser_to_number = {browser: i for i, browser in enumerate(browser_name)}
        numerical_data = [browser_to_number[browser] for browser in hist_data]

        ax = plt.hist(numerical_data, bins=np.arange(len(browser_name)+1)-0.7, color="green",edgecolor="black")
        # Alligning labels
        plt.gca().set_xticks(np.arange(len(browser_name)))
        # Setting the x-axis labels 
        plt.gca().set_xticklabels(browser_name, ha="center")
        # Setting the y-axis values 
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        # Labeling the graph
        plt.xlabel("Browser")
        plt.ylabel("Number of Users")
        plt.title("Number of Users per Browser")   
        plt.tight_layout()     
        return fig
        
    def browser_count_full(self,doc_id):
        #filtering data by doc id
        filter_document = self.data[self.data["subject_doc_id"]== doc_id]
        final_data = filter_document.drop_duplicates(subset=["visitor_useragent", "visitor_uuid"])   
        plot_data = final_data.groupby("visitor_useragent")["visitor_uuid"].nunique().reset_index()
        print(plot_data)
        #Storing browser name
        browser_name= plot_data["visitor_useragent"].unique() 
        # Storing number of users per browser 
        user_count = plot_data["visitor_uuid"]  
        # storing data for plotting the histogram
        hist_data = np.repeat(browser_name, user_count)

        fig = plt.figure(figsize=(5, 3))
    
        # mapping the values for graph
        browser_to_number = {browser: i for i, browser in enumerate(browser_name)}
        numerical_data = [browser_to_number[browser] for browser in hist_data]
        ax = plt.hist(numerical_data, bins=np.arange(len(browser_name)+1)-0.7, color="green",edgecolor="black")
    
        # Alligning labels
        plt.gca().set_xticks(np.arange(len(browser_name)))
        # Setting the x-axis labels 
        plt.gca().set_xticklabels(np.arange(len(browser_name)), ha="center")
        # Setting the y-axis values 
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        #mapping the ind
        index_table = pd.DataFrame({"Index_Number": np.arange(len(browser_name)), "Browser_Name": browser_name })
    
        # Labeling the graph
        plt.xlabel("Browser")
        plt.ylabel("Number of Users")
        plt.title("Number of Users per Browser")
        plt.tight_layout()     
        return fig ,index_table
    
    def device_used(data):
        data['device_used'] = [
                                "Mobile" if parse(device).is_mobile else 
                                "PC" if parse(device).is_pc else
                                "Tablet" if parse(device).is_tablet else
                                "Other"
                                for device in data["visitor_useragent"]
                                ]
        device_count = data['device_used'].value_counts()
        fig, ax = plt.figure(figsize=(8, 6))
        colors = ["#483D8B", "#6A5ACD", "#9370DB", "#7B68EE"]
        ax = plt.pie(device_count, labels=device_count.index, autopct="%1.1f%%", startangle=180,colors=colors)
        ax.set_title('Percentage of Each Device Used')
        return fig

    


