import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import streamlit as st
import google.auth
import os
import time

generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.9,
    "top_p": 1,
}


safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

def app():

    key_path = st.secrets["google_key_path"]

    # Set the environment variable to point to the key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    # Authenticate using the key file
    credentials, project_id = google.auth.default()


    vertexai.init(project="learn-vertex-ai-417510", location="asia-southeast1")

    model = GenerativeModel(
        #"gemini-1.0-pro-001",
        "gemini-1.5-pro-preview-0409",
    )

    chat = model.start_chat()

    # Initialize chat history
    chat_history = []

    # Create two columns
    col1, col2 = st.columns([1, 4])

    # Display the image in the left column
    with col1:
        st.image("wvsu-logo.jpg")

    # Display the title in the right column
    with col2:
        st.title("A Teaching Co-pilot Powered by Google Gemini on Vertex AI")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University"""

    with st.expander("Click to display developer information."):
        st.text(text)
    st.subheader("Empower Your Teaching with AI: The Gemini Teacher Copilot")
    text = """Unleash creativity and personalize learning in your classroom with 
    the Gemini Teacher Copilot, a revolutionary data app powered by Google's 
    cutting-edge large language model, Gemini 1.5 on Vertex AI. This AI co-pilot 
    equips educators with a treasure trove of ideas and resources to spark 
    student engagement, tackle challenging concepts, differentiate instruction, 
    design formative assessments, and seamlessly integrate technology into 
    lessons, all while saving educators time and boosting their teaching potential."""
    st.write(text)

    context = """You are a teaching co-pilot designed to assist educators in various classroom tasks. 
    When responding to prompts, prioritize providing resources and strategies that directly benefit teachers.
    Remember, your primary function is to empower teachers and enhance their effectiveness in the classroom."""

    options = ['K1', 'K2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 
    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
  
    yearlevel = st.selectbox(
    label="Select year level:",
    options=options,
    index=7  # Optionally set a default selected index
    )

    topic = st.text_input("Please input the topic: ")

    options = ['Generate engaging learning activities', 
    'Suggest alternative explanations for a concept students find challenging', 
    'Provide differentiation strategies to cater to learners with varying needs',
    'Create formative assessment ideas to gauge student understanding',
    'Offer resources for incorporating technology into the classroom']
    
    # Create the combobox (selectbox) with a descriptive label
    selected_option = st.selectbox(
    label="Choose a task for the teaching co-pilot:",
    options=options,
    index=0  # Optionally set a default selected index
    )

    question = selected_option + " for year level " + yearlevel + " on topic " + topic

    # Create a checkbox and store its value
    checkbox_value = st.checkbox("Check this box to input a custom prompt.")

    # Display whether the checkbox is checked or not
    if checkbox_value:
        # Ask the user to input text
        question = st.text_input("Please input a prompt (indicate year level and topic): ")

    # Button to generate response
    if st.button("Generate Response"):
        progress_bar = st.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
        if question:

            # Add user message to chat history
            chat_history.append({"speaker": "User", "message": context + " " + question})

            # Generate response from Gemma
            bot_response = chat.send_message(question,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            # Access the content of the response text
            bot_response = bot_response.text

            # Add bot response to chat history
            chat_history.append({"speaker": "Gemini", "message": bot_response})

            # Display chat history
            for message in chat_history:
                st.write(f"{message['speaker']}: {message['message']}")

        else:
            st.error("Please enter a prompt.")

        # update the progress bar
        for i in range(100):
            # Update progress bar value
            progress_bar.progress(i + 1)
            # Simulate some time-consuming task (e.g., sleep)
            time.sleep(0.01)
        # Progress bar reaches 100% after the loop completes
        st.success("AI teacher co-pilot task completed!") 


#run the app
if __name__ == "__main__":
  app()
