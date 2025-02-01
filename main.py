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
model = genai.GenerativeModel("gemini-1.5-flash-002")
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
You are an expert in nutrition and dietetics. You are given an image of a meal.
YOUR TASK is to provide the total calories and proteins in the meal along with 
calorie and protein for each item in the below format:
Total Calories: , Total Proteins: \n
Individual Items:\n
Item 1 - Calories:, Proteins: ,\n
Item 2 - Calories:, Proteins: ,\n
----
----
Make sure that each item is in its own line when showing calories and proteins.
Once the counts are provided, you should also mention if the food is healthy or not. Finally you can also mention
percentage split of carbs, sugar and fats etc. and other important things required in the diet.
If you think certain food items have high calories, you can also suggest alternatives at the end.
Keep the response brief and to the point. Don't use adjectives, use numbers for macronutrients where possible

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
                "Google Gemini provides the detailed breakdown you need, just upload an image.")
    st.write("")
    
    # Display image upload widget
    uploaded_file = st.file_uploader("Upload image of a meal", type=["jpg", "jpeg", "png"])
    st.write("")
    # Get response from the model
    if st.button("Get Calories", key="calorie_button", help="Click to get nutritional details"):
        if uploaded_file is not None:
            handle_submit(input_prompt, uploaded_file)
        else:
            st.warning("Please upload an image of a meal.")
    
    # Display the uploaded image
    display_image(uploaded_file)

# Run the app
if __name__ == "__main__":
    main()