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


def main():
    st.title(''' :rainbow[Document Tracker] :bar_chart:''')
    st.subheader("Upload your file")
    default_file = "dataset.txt"
    data_file = st.file_uploader("Upload your JSON data", type=["json", "txt"], key="unique_file_uploader")

    st.subheader("Visualized Data")
    if data_file is not None:
        data = load_data(data_file, is_uploaded_file=True)
        st.session_state['data'] = data 
    else:
        data = load_data(default_file, is_uploaded_file=False)
        st.session_state['data'] = data 

    if not data.empty:
        st.write(data)
    else:
        st.error('Failed to load data. Please check the file format and contents.')

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
    

    with col1:
        # to load the image
        image = Image.open("images/continent.jpg")
        # displaying the image maintaing the column width
        st.image(image,use_column_width=True)
        if st.button("View by Country/Continent"):
            st.session_state['task'] = 'View by Country/Continent'
            st.session_state['page'] = 'task_page'
        
    with col2:
        image = Image.open("images/browser.png")
        st.image(image,use_column_width=True)
        if st.button("View by Browser"):
            # update session state
            st.session_state['task'] = 'View by Browser'
            print("Done")
            st.session_state['page'] = 'task_page'
    st.write("")
    with col3:
        image = Image.open("images/profile.jpg")
        st.image(image,use_column_width=True)
        st.button("Reader profiles")
    with col4:
        image = Image.open("images/likes.png")
        st.image(image,use_column_width=True)
        st.button("Also Likes", on_click="")

# Funcition to navigate to options page
def navigate_to_options():
    st.session_state['page'] = 'options'
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