import argparse
import sys
from tabulate import tabulate
import matplotlib.image as mpimg
import subprocess
# from pandasgui import show
# from gui import *
from likes.also_like import AlsoLike
from views.view_by_country import CountryContinent
from views.view_by_browser import BrowserCount
from data_op.data_loader import Reader
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Command line argument parser for cw2")

    parser.add_argument("-u", "--user_uuid", required=True, help="The user UUID")
    parser.add_argument("-d", "--doc_uuid", required=True, help="The document UUID")
    parser.add_argument("-t", "--task_id", required=True, help="The task ID")
    parser.add_argument("-f", "--file_name", required=True, help="The file name")
    args = parser.parse_args()
    reader = Reader(args.file_name)
    # data = reader.load_data()
    pd = reader.concatenate_chunks()
    doc_id = args.doc_uuid
    uid = args.user_uuid
    if not pd['visitor_uuid'].isin([uid]).any():
        uid = None

    if(args.task_id == "2"):
        country_continent = CountryContinent()
        country, cont = country_continent.uuid_country_cont_hist(doc_id,pd)
        plt.figure(country.number)
        plt.show()                     
    elif(args.task_id == "3a"):
        browser_cnt = BrowserCount(pd)
        fig, data_frame_browser = browser_cnt.browser_count_full(doc_id)
        plt.figure(fig)
        plt.show()
    elif(args.task_id == "3b"):
        browser_cnt = BrowserCount(pd)
        fig = browser_cnt.browser_count(doc_id)
        plt.figure(fig)
        plt.show()
    elif(args.task_id == "4"):
        reader = Reader(args.file_name)
        top_reader = reader.top_readers(pd)
        print(tabulate(top_reader, headers = 'keys', tablefmt = 'psql'))

    elif(args.task_id == "5d"):
        also_like_obj = AlsoLike(pd)
        also_liked = also_like_obj.get_also_like(doc_id,None,uid)
        if(also_like.shape == (0,)):
            print("There are no also liked docments.")
        else:
            plt.imshow(also_liked, cmap='gray')
            plt.axis('off')
            plt.show()
    elif(args.task_id == "6"):
        also_like = AlsoLike(pd)
        generate_graph = also_like.generate_graph(doc_id,None,uid)
        img = mpimg.imread(generate_graph+".png")
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    elif(args.task_id == "7"):
        subprocess.run(["streamlit", "run", "gui.py"])
    else:
        print("Please enter a valid task_ID ! \nArigato", file=sys.stderr)


    # print(f"User UUID: {args.user_uuid}")
    # print(f"Document UUID: {args.doc_uuid}")
    # print(f"Task ID: {args.task_id}")
    # print(f"File Name: {args.file_name}")


# 140130130306-000000003c9af9a0f02cd76466e65bbb

if __name__ == "__main__":
    main()