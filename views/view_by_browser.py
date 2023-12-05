import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from user_agents import parse
from views.data_op.data_loader import load_data


def broswer_count(data,doc_id):
    
    #filtering date based on document id given
    filter_document = data[data["env_doc_id"]== doc_id]

    data = filter_document 

    #retrieving browser name removing uneccessary information using parser function from user_agent
    data['visitor_useragent'] = data['visitor_useragent'].apply(lambda x: parse(x).browser.family)

    #removing repeating users using the same browser 
    final_data = data.drop_duplicates(subset=['visitor_useragent', 'visitor_uuid'])  

    # calculating number of users for each browser used
    plot_data = final_data.groupby('visitor_useragent')['visitor_uuid'].nunique().reset_index()
    print(plot_data)

    

    #plotting the graph
    plt.figure(figsize=(5, 3))
    ax = plt.bar(plot_data['visitor_useragent'], plot_data['visitor_uuid'], color='orange')
    ax = plt.gca()  # Get the current Axes instance
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xlabel('Browser')
    plt.ylabel('Number of Users')
    plt.title('Number of Users per Browser')
    plt.xticks(rotation=45)
    
    
    return ax

doc_id = "140224101516-e5c074c3404177518bab9d7a65fb578e"
data = load_data("datasets/dataset.txt")
broswer_count(data,doc_id)
plt.show()
