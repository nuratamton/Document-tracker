import streamlit as st
from PIL import Image
import pandas as pd
import json as js
import matplotlib.pyplot as plt
import graphviz

from views.view_by_country import CountryContinent
from also_like import AlsoLike
from data_op.data_loader import Reader

# Initialize state session
if "page" not in st.session_state:
    st.session_state["page"] = "main"
if "data" not in st.session_state:
    st.session_state["data"] = None
if "task" not in st.session_state:
    st.session_state['task'] = None

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
        st.write(st.session_state['data'].head(100))  # Display first 100 rows as an example


    # if data contains something
    # if not data.empty:
    #     # write the data
    #     st.write(data)
    # else:
    #     # if data was empty, show an error message
    #     st.error('Failed to load data. Please check the file format and contents.')

    # Button to analyse the data
    st.button('Analyse data', on_click=navigate_to_options)

# Function to navigate to main page
def navigate_to_main():
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

    # in the third column
    with col3:
        # to load image
        image = Image.open("images/profile.png")
        st.image(image,use_column_width=True)
        st.button("Reader profiles")

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

    st.button('⬅ Back', on_click=navigate_to_options)
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("View by countries and continents")
    document_uuid = st.text_input('Enter Document UUID:')
    if document_uuid:
        fig_country, fig_continent = country_cont.uuid_country_cont_hist(document_uuid, data)
        st.pyplot(fig_country)
        st.pyplot(fig_continent)

def navigate_to_opt1():
    st.session_state['task'] = 'View by Country/Continent'
    st.session_state['page'] = 'opt1'

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
    st.subheader("View 'Also Likes'")
    document_uuid = st.text_input('Enter Document UUID:')

    also_likes_list = also_like.get_also_like(document_uuid)
    print(also_likes_list)

    st.subheader("Also Likes List")
    st.write(also_likes_list)

    also_likes_graph = also_like.generate_graph(document_uuid)

    st.subheader("Also Likes Graph")

    with open(also_likes_graph) as f:
        dot_graph = f.read()
    st.graphviz_chart(dot_graph)

def navigate_to_opt4():
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
elif st.session_state["page"] == "opt4":
    display_also_like()