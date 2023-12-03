import streamlit as st
from PIL import Image
import pandas as pd
import json as js
import matplotlib.pyplot as plt

# Function to load the data,
# Takes filename as parameter
def load_data(file, is_uploaded_file=False):
    JSON = []
    try:
        if is_uploaded_file:
            lines = file.getvalue().decode("utf-8").splitlines()
        else:
            # Read from a file path
            with open(file, 'r') as f:
                lines = f.readlines()

        # Process each line as JSON
        for line in lines:
            try:
                json_line = js.loads(line.strip())
                JSON.append(json_line)
            except js.JSONDecodeError as e:
                print(json_line)
                print(f"Error parsing JSON on line: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        return pd.DataFrame(JSON)
    except Exception as e:
        print(f"Error reading file: {e}")
        return pd.DataFrame()

# Function for the main page
def main():
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("Upload your file")
    default_file = "dataset.txt"
    data_file = st.file_uploader("Upload your JSON data", type=["json", "txt"], key="unique_file_uploader")

    # Subheader for the displaying of data
    st.subheader("Visualized Data")
    # if a file is already loaded
    if data_file is not None:
        # load the file chosen by the user
        data = load_data(data_file, is_uploaded_file=True)
        # save it
        st.session_state['data'] = data 
    else:
        # if its not specified, load the default file
        data = load_data(default_file, is_uploaded_file=False)
        # save it
        st.session_state['data'] = data 

    # if data contains something
    if not data.empty:
        # write the data
        st.write(data)
    else:
        # if data was empty, show an error message
        st.error('Failed to load data. Please check the file format and contents.')

    # Button to analyse the data
    st.button('Analyse data', on_click=navigate_to_options)

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
        if st.button("View by Country/Continent"):
            st.session_state['task'] = 'View by Country/Continent'
            st.session_state['page'] = 'task_page'
    
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
        st.button("Also Likes", on_click="")

# Funcition to navigate to options page
def navigate_to_options():
    # save the session state
    st.session_state['page'] = 'options'

# Function to navigate to main page
def navigate_to_main():
    st.session_state['page'] = 'main'

# SAMPLE FOR WHERE EACH PAGE LEADS, REMOVE IT
def task_page():
    st.title(f"Task: {st.session_state['task']}")
    st.button('Main menu', on_click=navigate_to_options)

# Initialize state session
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'task' not in st.session_state:
    st.session_state['task'] = None

# Page routing
if st.session_state['page'] == 'main':
    main()
elif st.session_state['page'] == 'options':
    options()
elif st.session_state['page'] == 'task_page':
    task_page()