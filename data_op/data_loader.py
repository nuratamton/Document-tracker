import numpy as np
import json as js
import pandas as pd

class Reader:
    def __init__(self, file, batch_size = 10000):
        self.file = file
        self.batch_size = batch_size

    def load_data(self):
        try:
            reader = pd.read_json(self.file, lines=True, chunksize=self.batch_size)
            return reader
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def concatenate_chunks(self):
        chunks = []
        try:
            for chunk in self.load_data():
                chunks.append(chunk)
            return pd.concat(chunks, ignore_index=True)
        except Exception as e:
            print(f"Error in concatenate_chunks: {e}")

    def top_readers(self, data):
        #checking event type to check if the sample has reading time of a user
        reading_events = data[(data['event_type'] == 'pagereadtime') & (data['subject_type'] == 'doc')]

        #calculating the total time a user spent on readin documents
        total_reading_time = reading_events.groupby('visitor_uuid')['event_readtime'].sum().reset_index()

        #sorting the data in descending order
        total_reading_time = total_reading_time.sort_values(by='event_readtime', ascending=False)

        #returning the top 10 reader based on reading time
        return total_reading_time.head(10)[['visitor_uuid']]