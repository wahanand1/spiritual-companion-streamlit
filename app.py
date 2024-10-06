import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import time

# Function to load Lottie file
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the brain animation
lottie_brain = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_SkhtL8.json")

# Function to call the API
def call_api(query):
    # Replace with your actual API endpoint
    api_url = "https://h4fpomvaqf.execute-api.us-east-1.amazonaws.com/Development/spiritual-companion-api"
    
    try:
        response = requests.post(api_url, json={"user_query": query})
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()  # This should now work correctly
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {str(e)}")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="Spiritual Companion by Brahma Kumaris", page_icon=":cherry_blossom:", layout="wide")

    st.title(":cherry_blossom: Spiritual Companion by Brahma Kumaris")

    # User input
    user_question = st.text_input("Ask your question:")

    if st.button("Get Answer"):
        if user_question:
            # Display spinning brain while processing
            with st.spinner("Thinking..."):
                brain_placeholder = st.empty()
                with brain_placeholder:
                    st_lottie(lottie_brain, height=200, key="brain")
                
                # Call API
                result = call_api(user_question)
                
                # Remove spinning brain
                brain_placeholder.empty()

            if result:
                # Display the response in a nice format
                st.subheader("Response:")
                st.write(result.get('generated_response', 'No response body available'))

                # Display additional information
                with st.expander("See details"):
                    st.json({
                        "Query": result.get('query', 'N/A'),
                        "Status Code": result.get('statusCode', 'N/A'),
                        "Source": result.get('s3_location', 'N/A')
                    })
            else:
                st.error("Failed to get a valid response from the API.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()