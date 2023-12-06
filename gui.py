import streamlit as st
from PIL import Image
import pandas as pd
import json as js
import matplotlib.pyplot as plt
import graphviz
import time

from views.view_by_country import CountryContinent
from likes.also_like import AlsoLike
from data_op.data_loader import Reader

# Initialize state session
if "page" not in st.session_state:
    st.session_state["page"] = "main"
if "data" not in st.session_state:
    st.session_state["data"] = None
if "task" not in st.session_state:
    st.session_state['task'] = None

def show_progress(duration=1):
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(duration / 100)
        progress_bar.progress(percent_complete + 1)

# Function for the main page
def main():
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("Upload your file")
    default_file = "datasets/dataset.txt"
    data_file = st.file_uploader("Upload your JSON data", type=["json", "txt"], key="unique_file_uploader")

    # Subheader for the displaying of data
    st.subheader("Visualized Data")
    # if a file is already loaded
    if data_file is not None:
        reader = Reader(data_file)
        # # load the file chosen by the user
        # data = reader.concatenate_chunks()
    else:
        reader = Reader(default_file)
        # if its not specified, load the default file
        # data = reader.load_data()

    data = reader.concatenate_chunks()
    st.session_state['data'] = data
    st.success("Data loaded successfully.")

    if 'data' in st.session_state and not st.session_state['data'].empty:
        st.write("Showing first 100 rows of the data:")
        st.write(st.session_state['data'].head(100)) 
    else:
        # if data was empty, show an error message
        st.error('Failed to load data. Please check the file format and contents.')

    # Button to analyse the data
    st.button('Analyse data', on_click=navigate_to_options)

# Function to navigate to main page
def navigate_to_main():
    show_progress()
    st.session_state["page"] = "main"

# Function for options page
def options():
    # Back button to go back to the main page
    st.button('⬅ Back', on_click=navigate_to_main)
    # Adds a title
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # Adds a subtitle
    st.subheader("Choose an option:")

    # Creates 2 columns on top and two in the button for spacing
    col1, col2 = st.columns(2, gap="large")
    col3, col4 = st.columns(2, gap="large")
    
    # in the first column
    with col1:
        # to load the image
        image = Image.open("images/continent.png")
        # displaying the image maintaing the column width
        st.image(image,use_column_width=True)
        # A button to view by country/continent
        st.button("View by Country/Continent", on_click=navigate_to_opt1)
    
    # in the second column
    with col2:
        # to load image
        image = Image.open("images/browser.png")
        # display the image while maintaining the column width
        st.image(image,use_column_width=True)
        # if button to view by browser is clicked
        if st.button("View by Browser"):
            # update session state
            st.session_state['task'] = 'View by Browser'
            print("Done")
            st.session_state['page'] = 'task_page'

    st.write("")
    st.write("")

    # in the third column
    with col3:
        # to load image
        image = Image.open("images/profile.png")
        st.image(image,use_column_width=True)
        st.button("Reader profiles", on_click=navigate_to_opt3)

    # in the fourth column
    with col4:
        # to load image
        image = Image.open("images/likes.png")
        # to display the image
        st.image(image,use_column_width=True)
        # the button to Also Likes
        st.button("Also Likes", on_click=navigate_to_opt4)

# Funcition to navigate to options page
def navigate_to_options():
    show_progress()
    # save the session state
    st.session_state['page'] = 'options'

def view_by_countries():
    country_cont = CountryContinent()
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
        # Perform operations with data
    else:
        st.write("Data not loaded yet")

    # back button
    st.button('⬅ Back', on_click=navigate_to_options)
    # added the title for the page
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # spacing for better visibility
    st.write("")
    # added the subheader for the page
    st.subheader("View by countries and continents")
    st.write("")
    # gets user input (the doc id)
    document_uuid = st.text_input('Enter Document UUID:')
    st.write("")
    # if document id is given
    if document_uuid:
        # get the graphs from the defined function
        fig_country, fig_continent = country_cont.uuid_country_cont_hist(document_uuid, data)
        # added subheader for the countries graph
        st.subheader("View by Countries")
        # display the graph
        st.pyplot(fig_country)
        st.write("")
        st.write("")
        # added subheader for the continents graph
        st.subheader("View by Continents")
        # display the graph
        st.pyplot(fig_continent)

def navigate_to_opt1():
    show_progress()
    st.session_state['task'] = 'View by Country/Continent'
    st.session_state['page'] = 'opt1'

def display_top_readers():
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
    else:
        st.write("Data not loaded yet")

    st.button('⬅ Back', on_click=navigate_to_options)
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("View top readers")

    # reader class instance
    reader = Reader(data)
    # getting the top readers
    top_readers = reader.top_readers(data)
    # converting the series to dataframe for display

    if not top_readers.empty:
        # add a column with the rank of the readers
        top_readers['Rank'] = range(1, len(top_readers) + 1)
        # reorder columns to display rank first
        top_readers_df = top_readers[['Rank', 'visitor_uuid']]
        st.table(top_readers_df)
    else:
        st.write("No top readers data available.")

def navigate_to_opt3():
    show_progress()
    st.session_state['task'] = "Reader profiles"
    st.session_state['page'] = "opt3"

def display_also_like():
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
        # Perform operations with data
    else:
        st.write("Data not loaded yet")

    also_like = AlsoLike(data)

    st.button('⬅ Back', on_click=navigate_to_options)
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("View 'Also Liked'")
    document_uuid = st.text_input('Enter Document UUID:')

    also_likes_list = also_like.get_also_like(document_uuid)
    if also_likes_list.size > 0:
        # Convert list to DataFrame for display
        df = pd.DataFrame({'Recommended Documents': also_likes_list}, index=range(1, len(also_likes_list) + 1))
        st.subheader("Other readers of this document also like:")
        st.table(df)
    else:
        st.write("No recommendations available for this document.")

    also_likes_graph = also_like.generate_graph(document_uuid)
        # to display the image
    st.image(also_likes_graph+".png")

def navigate_to_opt4():
    show_progress()
    st.session_state['task'] = "Also Likes"
    st.session_state['page'] = "opt4"

# SAMPLE FOR WHERE EACH PAGE LEADS, REMOVE IT
def task_page():
    st.title(f"Task: {st.session_state['task']}")
    st.button('Main menu', on_click=navigate_to_options)

# Page routing
if st.session_state["page"] == "main":
    main()
elif st.session_state["page"] == 'options':
    options()
elif st.session_state["page"] == "opt1":
    view_by_countries()
elif st.session_state["page"]=="opt3":
    display_top_readers()
elif st.session_state["page"] == "opt4":
    display_also_like()