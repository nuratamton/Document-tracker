import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from user_agents import parse
from data_op.data_loader import Reader


class BrowserCount:

    def broswer_count(data,doc_id):
        
        #filtering date based on document id given
        filter_document = data[data["env_doc_id"]== doc_id]
    
        data = filter_document 
    
        #retrieving browser name removing uneccessary information using parser function from user_agent
        data["visitor_useragent"] = data["visitor_useragent"].apply(lambda x: parse(x).browser.family)
    
        #removing repeating users using the same browser 
        final_data = data.drop_duplicates(subset=["visitor_useragent", "visitor_uuid"])  
    
        # calculating number of users for each browser used
        plot_data = final_data.groupby("visitor_useragent")["visitor_uuid"].nunique().reset_index()
    
        #Storing browser name
        browser_name= plot_data["visitor_useragent"].unique() 
        # Storing number of users per browser 
        user_count = plot_data["visitor_uuid"]  
    
        # storing data for plotting the histogram
        hist_data = np.repeat(browser_name, user_count)
    
        
        plt.figure(figsize=(5, 3))
    
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
        return ax
        
    def broswer_count_full(data,doc_id):
        #filtering data by doc id
        filter_document = data[data["subject_doc_id"]== doc_id]
        data = filter_document 
    
        final_data = data.drop_duplicates(subset=["visitor_useragent", "visitor_uuid"])   
        
        plot_data = final_data.groupby("visitor_useragent")["visitor_uuid"].nunique().reset_index()
        print(plot_data)
        #Storing browser name
        browser_name= plot_data["visitor_useragent"].unique() 
        # Storing number of users per browser 
        user_count = plot_data["visitor_uuid"]  
    
        # storing data for plotting the histogram
        hist_data = np.repeat(browser_name, user_count)
    
        
        plt.figure(figsize=(5, 3))
    
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
        return ax,index_table
    


