
import numpy as np
from graphviz import Digraph,Source
# class to handle the also liked feature
class also_like:
    # class init; take dataframe and use that as an attribute
    def __init__(self, data_frame):
        self.data_frame = data_frame

    # this function takes a doc_id and returns a set of visitor ids
    def get_visitor_uuid(self, doc_id):

        visitor_collection = set()
        # from the data frame, get a list of the entries that have the field 'subject_doc_id' as doc_id
        filtered_data = self.data_frame[self.data_frame['subject_doc_id'] == doc_id]
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
            document_collection.add(item['subject_doc_id'])
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
            return np.argsort(-count)[:10]

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
        return self._sort_documents(document_collection,sorting_function)
    
    # function to generate the also-like graph
    def generate_graph(self, doc_id, sorting_function = None ,visitor_uuid = None ):
        graph = Digraph(comment="graph")

        graph.node(doc_id[-4:],style = 'filled',fillcolor="purple")

        if visitor_uuid:
            graph.node(visitor_uuid[-4:],style = 'filled',fillcolor='purple')
            graph.edge(visitor_uuid[-4:], doc_id[-4:])
        
        for doc in self.get_also_like(doc_id,sorting_function,visitor_uuid):
            graph.node(doc[-4:], shape="box")
            visitor = self.get_visitor_uuid(doc)
            for v in visitor:
                if not visitor_uuid or (visitor_uuid and v == visitor_uuid):
                    graph.edge(v[-4:], doc[-4:])
        output_path = 'graph.pdf'
        graph.render(output_path, format='pdf', cleanup=True)
        return output_path
