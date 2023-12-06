import argparse
import sys
from pandasgui import show
from gui import *
from likes.also_like import AlsoLike
from views.view_by_country import CountryContinent
from views.view_by_browser import BrowserCount
from data_op.data_loader import Reader

def main():
    parser = argparse.ArgumentParser(description="Command line argument parser for cw2")

    parser.add_argument("-u", "--user_uuid", required=True, help="The user UUID")
    parser.add_argument("-d", "--doc_uuid", required=True, help="The document UUID")
    parser.add_argument("-t", "--task_id", required=True, help="The task ID")
    parser.add_argument("-f", "--file_name", required=True, help="The file name")
    args = parser.parse_args()

    if(args.task_id == "2a"):
        country_continent = CountryContinent()
        country_continent.uuid_country_cont_hist()
        show()
    elif(args.task_id == "2b"):
        pass                        
    elif(args.task_id == "3a"):
        pass
    elif(args.task_id == "3b"):
        pass
    elif(args.task_id == "4"):
        pass
    elif(args.task_id == "5d"):
        pass
    elif(args.task_id == "6"):
        pass
    elif(args.task_id == "7"):
        pass
    else:
        print("Please enter a valid task_ID ! \nArigato", file=sys.stderr)


    # print(f"User UUID: {args.user_uuid}")
    # print(f"Document UUID: {args.doc_uuid}")
    # print(f"Task ID: {args.task_id}")
    # print(f"File Name: {args.file_name}")


# 140130130306-000000003c9af9a0f02cd76466e65bbb

if __name__ == "__main__":
    main()

























# from data_op.data_loader import Reader
# file = "datasets/sample_3m_lines.json"
# reader = Reader(file)
# doc_id = 1393631983
# data= reader.concatenate_chunks()

# print(data)
# doc_data = []
# for i in data:
#     if i["ts"] == doc_id:
#         doc_data.append(i)