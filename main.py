# import sys
# print(sys.argv)

from gui import *

file = "datasets/sample_600k_lines.json"
doc_id = 1393631983
data= load_data(file)
print(data)
# doc_data = []
# for i in data:
#     if i["ts"] == doc_id:
#         doc_data.append(i)