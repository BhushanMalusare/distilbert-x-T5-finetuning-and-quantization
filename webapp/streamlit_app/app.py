import requests
import streamlit as st

# Set page title
st.set_page_config("Intent Recognition x Summarization")

# Streamlit app
st.title("Text Analysis Tool")

# Sidebar with options
option = st.sidebar.radio(
    "Choose an option",
    ("Intent Classification", "Summarization")
)

# Input text
text_input = st.text_area("Enter text:", height=200)

if st.button("Submit"):
    if text_input:
        if option == "Intent Classification":
            # Make API call to Flask backend for intent classification
            response = requests.post(
                "http://127.0.0.1:5000/predict-intent", json={"text": text_input}
            )

            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Class: {result['class']}")
            else:
                st.error("Error: Unable to get the prediction.")
        elif option == "Summarization":
            # Make API call to Flask backend for summarization
            response = requests.post(
                "http://127.0.0.1:5000/summarize", json={"text": text_input}
            )

            if response.status_code == 200:
                result = response.json()
                st.success(f"Summary: {result['summary']}")
            else:
                st.error("Error: Unable to get the summary.")
    else:
        st.warning("Please enter some text.")

# Fetch and display class names for intent classification
if option == "Intent Classification":
    response = requests.get("http://127.0.0.1:5000/classes")
    if response.status_code == 200:
        class_names = response.json().get("classes", {})
        # Convert the class names dictionary to a list of dictionaries
        class_names_list = [
            {"Intents model can predict": value} for _, value in class_names.items()
        ]
        # Display the class names in a table
        st.table(class_names_list)
    else:
        st.error("Error: Unable to fetch class names.")
