import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Medicine Symptoms Checker",
    page_icon="💊",
    layout="centered",
)

# Load API key safely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY. Check your .env file or environment variables.")
    st.stop()

# Configure Google Gemini API
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error configuring API: {str(e)}")
    st.stop()

# Verify available models and choose the correct one
try:
    available_models = [model.name for model in gen_ai.list_models()]
    
    # Choose the best available model
    model_name = "models/gemini-1.5-pro-latest" if "models/gemini-1.5-pro-latest" in available_models else "models/gemini-1.5-pro"
    
    if model_name not in available_models:
        st.error(f"Suitable Gemini model not found! Available models: {available_models}")
        st.stop()
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.stop()

# Use the correct model name
model = gen_ai.GenerativeModel(model_name)

# Function to translate roles
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("💊 Medicine Symptoms Checker")

# Show chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Handle user input
user_prompt = st.chat_input("Describe your symptoms...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    # Try generating response based on the symptoms entered
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Extract response safely
        if hasattr(gemini_response, "text") and gemini_response.text:
            response_text = gemini_response.text
        else:
            response_text = "No response received."

        # Suggest possible diseases and consulting a doctor
        disease_suggestion = (
            "Based on the symptoms you've provided, it seems you may have a condition related to the mentioned symptoms. "
            "However, this is not a diagnosis."
        )
        doctor_suggestion = "We strongly recommend that you consult a healthcare professional for a proper diagnosis and treatment plan."

        # Combine chatbot response with medical advice
        response_text = f"{response_text}\n\n{disease_suggestion}\n{doctor_suggestion}"

    except Exception as e:
        response_text = f"Error: {str(e)}"

    # Display response
    with st.chat_message("assistant"):
        st.markdown(response_text)
