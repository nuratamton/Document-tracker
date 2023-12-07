import numpy as np
import pandas as pd

class SortingDocFunctions:

    def __init__(self, data_frame):
        self.data = data_frame
    # a function that sorts the doc_id list on the basis of a score taken by getting the total views of the document 
    # and multiplying it with the count of the unique countries these visits are from 
    def sort_by_country_diversity_score(self,doc_list):
        get_all_docs = self.data[self.data['env_doc_id'].isin(doc_list)]
        # get the the documents and their corresponding counts
        views_count_with_duplicate = get_all_docs['env_doc_id'].value_counts()
        # group the dataframe by doc_id and get the unique documents with their country and its count
        country_diversity = get_all_docs.groupby('env_doc_id')['visitor_country'].nunique()
        # multiply the two dataframes so that we get the score for each entry
        scores = views_count_with_duplicate * country_diversity
        # sort the dict and return the top 10
        return scores.sort_values(ascending=False).head(10).index.tolist()





    
