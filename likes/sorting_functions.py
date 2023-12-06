import numpy as np
import pandas as pd

class SortingDocFunctions:

    def __init__(self, data_frame):
        self.data = data_frame
 
    def sort_by_country_diversity_score(self,doc_list):
        get_all_docs = self.data[self.data['subject_doc_id'].isin(doc_list)]
        views_count_with_duplicate = get_all_docs['subject_doc_id'].value_counts()
        country_diversity = get_all_docs.groupby('subject_doc_id')['visitor_country'].nunique()
        scores = views_count_with_duplicate * country_diversity
        return scores.sort_values(ascending=False).head(10).index.tolist()





    
