import numpy as np
from graphviz import Digraph,Source
import pandas as pd
from data_op.data_loader import Reader

# class to handle the also liked feature
class AlsoLike:
    # class init; take dataframe and use that as an attribute
    def __init__(self, data_frame):
        self.data_frame = data_frame

    # this function takes a doc_id and returns a set of visitor ids
    def get_visitor_uuid(self, doc_id):
        visitor_collection = set()
        # from the data frame, get a list of the entries that have the field 'env_doc_id' as doc_id
        filtered_data = self.data_frame[self.data_frame['env_doc_id'] == doc_id]
        # create a set of visitor_uuids and return it
        for _,item in filtered_data.iterrows():
            visitor_collection.add(item['visitor_uuid'])
        return visitor_collection
    
    # this function takes a visitor uuid and returns a set of doc ids
    def get_document_uuid(self, visitor_uuid):

        document_collection = set()
        # from the data frame, get a list of the entries that have the field 'visitor_uuid' visitor_uuid
        filtered_data = self.data_frame[self.data_frame['visitor_uuid'] == visitor_uuid]
        # create a set of document_uuids and return it
        for _,item in filtered_data.iterrows():
            document_collection.add(item['env_doc_id'])
        return document_collection
    
    # private helper method to sort a list of documents on default by the order of number of views
    # the best 10 are returned
    def _sort_documents(self,documents,sorting_function):
        # if a sorting function is provided, it uses that 
        if sorting_function is not None:
            return sorting_function(documents)[:10]
        # otherwise, it sorts them based on the number of times they were viewed (default behavior)
        else:
            unique_docs, count = np.unique(documents, return_counts=True)
            index = np.argsort(-count)
            return unique_docs[index][:10]

    # function to get the also like list
    def get_also_like(self, doc_id, sorting_function = None ,visitor_uuid = None):
        # using the 'get_visitor_uuid' function get a list of the reader of the given doc id
        visitors = self.get_visitor_uuid(doc_id)
        # if a visitor_uuid was provided and its in the visitors list, we check all the documents read only by that visitor
        if visitor_uuid in visitors:
            visitors = [visitor_uuid]
        # get a numpy array of all the documents that every document that the readers of the provided document have read
        document_collection = np.array([doc for v in visitors for doc in self.get_document_uuid(v) if doc != doc_id])
        # return the best 10 sorted documents
        return self._sort_documents(document_collection, sorting_function)
    
    # function to generate the also-like graph
    def generate_graph(self, doc_id, sorting_function = None ,visitor_uuid = None ):
        graph = Digraph(comment="graph")
        if not self.data_frame[self.data_frame['env_doc_id'] == doc_id].empty:
            graph.node(doc_id[-4:],style = 'filled',fillcolor="darkslategrey",shape='box')

        input_doc_visitors = self.get_visitor_uuid(doc_id)
        if visitor_uuid and visitor_uuid in input_doc_visitors:
            graph.node(visitor_uuid[-4:],style = 'filled',fillcolor='darkslategrey')
            graph.edge(visitor_uuid[-4:], doc_id[-4:])
            input_doc_visitors = {visitor_uuid}
        
        for v in input_doc_visitors:
            if v != visitor_uuid:
                graph.node(v[-4:], style ='filled', fillcolor="magenta")
            graph.edge(v[-4:], doc_id[-4:])
            
        for doc in self.get_also_like(doc_id,sorting_function,visitor_uuid):
            graph.node(doc[-4:], shape="box")
            visitor = self.get_visitor_uuid(doc)
            for v in visitor:
                if v != visitor_uuid:
                    graph.node(v[-4:])
                    graph.edge(v[-4:], doc[-4:])
        output_path = 'graph'
        output_path2 = 'graph_image'
        graph.render(output_path, format='pdf', cleanup=True)
        graph.render(output_path2, format='png', cleanup=True)
        return output_path2