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