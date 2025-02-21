# Import libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import time

# Load environment variables from a .env file 
load_dotenv()

# Configure the API key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load model and get response
# model = genai.GenerativeModel("gemini-1.5-flash-002")
model = genai.GenerativeModel("gemini-2.0-flash-001")
print(model)

def get_response(input_prompt, image):
    """
    Generates a response based on the given input prompt and image.
    """
    response = model.generate_content([input_prompt, image[0]])
    return response.text


# Read the image into bytes 
def read_image(uploaded_file):
    """
    Reads an uploaded image file and returns its content in bytes along with its MIME type.

    Raises:
        FileNotFoundError: If no image file is uploaded.
    """
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image file uploaded.")
    
# Display the uploaded image
def display_image(uploaded_file):
    """
    Uploads an image file and displays it using Streamlit.
    """
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_container_width=True)
    return image

# Handle submission of prompt and image
input_prompt = """
As a registered dietitian, analyze the provided image of a meal.  Provide a nutritional breakdown including:

* Total Calories: [Value], 
* Total Protein (grams): [Value]

Individual Items:
Item 1 - Calories: [Value], Protein (grams): [Value], Carbohydrates (%): [Value], Fat (%): [Value]
Item 2 - Calories: [Value], Protein (grams): [Value], Carbohydrates (%): [Value], Fat (%): [Value]
Item 3 - Calories: [Value], Protein (grams): [Value], Carbohydrates (%): [Value], Fat (%): [Value]
... (Continue for all items)

Assess the overall healthfulness of the meal. Provide a macronutrient breakdown for the *entire meal* as percentages:
Carbohydrates (%): [Value]
Protein (%): [Value]
Fat (%): [Value]

Mention any other relevant nutritional considerations.  If any items are high in calories or have other nutritional concerns, suggest healthier alternatives.  Be concise and use numerical values for macronutrients.
"""
def handle_submit(input_prompt, uploaded_file):
    """
    Handles the submission of a prompt and an uploaded image.
    """
    # Read the image into bytes
    image_data = read_image(uploaded_file)
    # Get response from the model
    response = get_response(input_prompt, image_data)
    # Display the response
    st.write(response)

# Initialize the app

# Initialize query count    
if "query_count" not in st.session_state:
    st.session_state['query_count'] = 0

# Manage query count
def manage_query_count():
    """
    Manage query count and reset after a minute if limit is exceeded.
    """
    if st.session_state['query_count'] > 5:
        st.warning("You have reached the limit of 5 queries. Please try again later.")
        # st.session_state['reset_time'] = time.time()
        return
        # if 'reset_time' in st.session_state and time.time() - st.session_state['reset_time'] > 60:
        #     st.session_state['query_count'] = 0
        #     del st.session_state['reset_time']
    else:
        st.session_state['query_count'] += 1

def main():
    """
    Main function to set up the Streamlit app interface for interacting with an image of a meal.
    1. Sets the page title.
    2. Displays a markdown description of the app.
    3. Provides a file uploader for the user to upload an image of a meal.
    4. Displays a button to get nutritional details of the uploaded image.
    5. Handles the user's action upon button click.
    6. Displays a warning if no image is uploaded.
    7. Displays the uploaded image.
    The app allows users to upload an image of a meal and ask questions to receive detailed responses based on the content of the uploaded image.
    """ 
    # Set header and description
    st.title("Gemini Image Nutrition Analyzer")
    st.write("")
    st.markdown("###### Easily analyze your food's nutrition with AI. "
                "Google Gemini (Gemini 2.0 Flash) provides the detailed breakdown you need, just upload an image.")
    st.write("")
    
    # Display image upload widget
    uploaded_file = st.file_uploader("Upload image of a meal", type=["jpg", "jpeg", "png"])
    st.write("")
    # Get response from the model
    if st.button("Get Calories", key="calorie_button", help="Click to get nutritional details"):
        if uploaded_file is not None:
            handle_submit(input_prompt, uploaded_file)
            manage_query_count()
        else:
            st.warning("Please upload an image of a meal.")
    
    # Display the uploaded image
    display_image(uploaded_file)

# Run the app
if __name__ == "__main__":
    main()