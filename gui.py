import streamlit as st
from PIL import Image
import pandas as pd
import json as js
import matplotlib.pyplot as plt
import graphviz
import time

from likes.sorting_functions import SortingDocFunctions
from views.view_by_country import CountryContinent
from views.view_by_browser import BrowserCount
from likes.also_like import AlsoLike
from data_op.data_loader import Reader

# Initialize state session
if "page" not in st.session_state:
    st.session_state["page"] = "main"
if "data" not in st.session_state:
    st.session_state["data"] = None
if "task" not in st.session_state:
    st.session_state['task'] = None

# Function to show progress bar
def show_progress(duration=1):
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(duration / 100)
        progress_bar.progress(percent_complete + 1)

# Function for the main page
def main():
    #  sets the title for the page
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # set the sub title asking the user to upload
    st.subheader("Upload your file")
    # the default dataset to load if none uploaded
    default_file = "datasets/dataset.txt"
    # file uploader to get the file from the user
    data_file = st.file_uploader("Upload your JSON data", type=["json", "txt"], key="unique_file_uploader")

    # Subheader for the displaying of data
    st.subheader("Visualized Data")
    # if a file is already loaded
    if data_file is not None:
        reader = Reader(data_file)
    else:
        reader = Reader(default_file)

    # method to read the data
    data = reader.concatenate_chunks()
    # storing the data in session
    st.session_state['data'] = data
    # printing success messsage
    st.success("Data loaded successfully.")

    # displays first 100 rows
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
    # to show prgress bar
    show_progress()
    # update the page state
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
        st.button("View by Browser", on_click=navigate_to_opt2)

    # for spacing
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
    # showing the progress
    show_progress()
    # update the session state
    st.session_state['page'] = 'options'

# function to access when first button is clicked
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
        st.write("")
        st.write("")
        # get the graphs from the defined function
        fig_country_pie, fig_cont_pie = country_cont.country_cont_pie(document_uuid, data)
        # added subheader for the pie chart of countries
        st.subheader("View by Countries - Pie")
        # display the graph
        st.pyplot(fig_country_pie)
        st.write("")
        st.write("")
        # added subheader for the pie chart of continents
        st.subheader("View by Continents - Pie")
        # display the graph
        st.pyplot(fig_cont_pie)
        

# function to run on button click
def navigate_to_opt1():
    show_progress()
    st.session_state['task'] = 'View by Country/Continent'
    st.session_state['page'] = 'opt1'

# function to access when second button is clicked
def view_by_browser():
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
        # Perform operations with data
    else:
        st.write("Data not loaded yet")
    browser_count = BrowserCount(data)
    # back button
    st.button('⬅ Back', on_click=navigate_to_options)
    # added the title for the page
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # spacing for better visibility
    st.write("")
    # added the subheader for the page
    st.subheader("View by Browser")
    st.write("")
    # gets user input (the doc id)
    document_uuid = st.text_input('Enter Document UUID:')
    st.write("")
    # if document id is given
    if document_uuid:
        # get the graphs from the defined function
        fig_browser_full, index_table = browser_count.browser_count_full(document_uuid)
        # added subheader for the countries graph
        st.subheader("View by  Identifiers")
        st.write(index_table)
        # display the graph
        st.pyplot(fig_browser_full)
        st.write("")
        st.write("")
        fig_browser_main = browser_count.browser_count(document_uuid)
        # added subheader for the continents graph
        st.subheader("View by Main Browser")
        # display the graph
        st.pyplot(fig_browser_main)

# function to run when second button is clicked
def navigate_to_opt2():
    show_progress()
    st.session_state['task'] = 'View by Browser'
    st.session_state['page'] = 'opt2'

# function to display the top readers
def display_top_readers():
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
    else:
        st.write("Data not loaded yet")
    
    # back button to go to previous page
    st.button('⬅ Back', on_click=navigate_to_options)
    # added the title for the page
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # spacing for better visibility
    st.write("")
    # added the subheader for the page
    st.subheader("View top readers")
    st.write("")

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
        # display the table
        st.table(top_readers_df)
    else:
        st.write("No top readers data available.")
    # spacing
    st.write("")
    # displays the subheader
    st.subheader("View devices used")
    st.write("")
    # instatiates BrowserCount
    browser_count = BrowserCount(data)
    # gets the pie chart for device used
    fig_device = browser_count.device_used()
    # displays the pie chart
    st.pyplot(fig_device)

# function to run when third button is clicked
def navigate_to_opt3():
    show_progress()
    st.session_state['task'] = "Reader profiles"
    st.session_state['page'] = "opt3"

# function to display also like
def display_also_like():
    if "data" in st.session_state:
        # Access the data
        data = st.session_state["data"]
        # Perform operations with data
    else:
        st.write("Data not loaded yet")

    # instantiates also likes
    also_like = AlsoLike(data)
    # instantiates sorting class
    sort = SortingDocFunctions(data)
    # back button
    st.button('⬅ Back', on_click=navigate_to_options)
    # title for the page
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    # for spacing
    st.write("")
    # subtitle for the page
    st.subheader("View 'Also Liked'")
    st.write("")
    # gets doc id from user
    document_uuid = st.text_input('Enter Document UUID:')
    st.write("")
    # gets visitor id from user
    visitor_uuid = st.text_input('Enter Visitor UUID:')
    st.write("")
    # asks user to select a sorting method
    sorting = st.selectbox("Select Sorting Method:", ("Default", "Country Diversity Score"))

    # If Country Diversity Score is selected
    if(sorting == "Country Diversity Score"):
        # sorting is assigned to country diversity score
        sorting = sort.sort_by_country_diversity_score
    else:
        # else it is kept as none
        sorting = None

    # if document uuid is entered
    if document_uuid:
        # gets the also likes list
        also_likes_list = also_like.get_also_like(doc_id=document_uuid, sorting_function=sorting, visitor_uuid=visitor_uuid)
        # if the list is not empty
        if len(also_likes_list)>0:
            # Convert list to DataFrame for display
            df = pd.DataFrame({'Recommended Documents': also_likes_list}, index=range(1, len(also_likes_list) + 1))
            # add a sub header
            st.subheader("Other readers of this document also like:")
            st.write("")
            # display the dataframe in a table
            st.table(df)
            st.write("")
            # subheader for the graph
            st.subheader("Graph")
            st.write("")
            # get the graph
            also_likes_graph = also_like.generate_graph(doc_id=document_uuid, visitor_uuid=visitor_uuid, sorting_function=sorting)
            # to display the graph
            st.image(also_likes_graph+".png")
        else:
            # else write No recommendations available
            st.write("No recommendations available for this document.")
        

# function to navigate to fourth option
def navigate_to_opt4():
    show_progress()
    # update task and page session states
    st.session_state['task'] = "Also Likes"
    st.session_state['page'] = "opt4"

# Page routing
# if session state of page is main
if st.session_state["page"] == "main":
    # call the main function
    main()
# else if the session state of page is options
elif st.session_state["page"] == 'options':
    # call the options function
    options()
# else if the session state of page is opt1
elif st.session_state["page"] == "opt1":
    # call the view by countries function
    view_by_countries()
# else if the session state of page is opt2
elif st.session_state["page"] == "opt2":
    # call the view by browser function
    view_by_browser()
# else if the session state of page is opt3
elif st.session_state["page"]=="opt3":
    # call the display top readers function
    display_top_readers()
# else if the session state of page is opt4
elif st.session_state["page"] == "opt4":
    # call the display also like function
    display_also_like()