import streamlit as st
from PIL import Image
import google.generativeai as genai
import pyttsx3
from deep_translator import GoogleTranslator
import os

# Streamlit app
st.title("AI Image Description & Translation")
st.write("Upload an image and enter a prompt. The model will generate a description based on your prompt.")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
user_prompt = st.text_input("Enter your prompt:", value="")

from gtts import gTTS

def generate_audio():
    if 'description' not in st.session_state:
        return
    tts = gTTS(text=st.session_state.description, lang='en')
    tts.save("1.mp3")


def change_language(language):
    if 'description' not in st.session_state:
        return "No description available to translate."
    translator = GoogleTranslator(source='auto', target=language)
    translated_text = translator.translate(st.session_state.description)
    return translated_text

if uploaded_file and user_prompt:
    try:
        if 'description' not in st.session_state:
            api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyCxD89Z76-pKgVVEOqRqNnQtBozIg_aDQk')

            if not api_key or api_key in ['AIzaSyCS95kvEAWTJeHPwhPU0j_iduZnzIBwAgE', 'AIzaSyCO5vAm-bR1NEEysv7Sqj88t7DaSxqGb1I']:
                st.error("⚠ Please set a valid Google API key. The current key is invalid.")
                st.info("""
                *How to get a Google API key:*
                1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. Sign in with your Google account
                3. Click "Create API Key"
                4. Copy the API key

                *How to set the API key:*
                - Set environment variable: export GOOGLE_API_KEY=your_api_key_here
                - Or replace the hardcoded key in the code
                """)
                st.stop()

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.session_state.img = Image.open(uploaded_file)
            response = model.generate_content([user_prompt, st.session_state.img])
            st.session_state.description = response.text
        st.image(st.session_state.img, caption='Uploaded Image', use_column_width=True)
        st.write(st.session_state.description)
    except Exception as e:
        st.error(f"Error processing the image: {e}")
else:
    if not uploaded_file:
        st.write("No image file selected.")
    if not user_prompt:
        st.write("Please enter a prompt.")

voice_choice = st.selectbox("Enable voice output?", ["No", "Yes"])
if voice_choice == "Yes" and 'description' in st.session_state:
    generate_audio()
    st.audio("1.mp3", format='audio/mp3')
elif voice_choice != "None" and 'description' not in st.session_state:
    st.warning("Please upload an image and generate a description first before using voice features.")

lang_choice = st.selectbox("Choose a Language to Translate:", ["None", "English", "Hindi", "Odia", "Telugu", "Tamil", "Punjabi", "Malayalam", "Marathi"])
if lang_choice != "None" and 'description' in st.session_state:
    lang_code = {'English': 'en', 'Hindi': 'hi', 'Odia': 'or', 'Telugu': 'te', 'Tamil': 'ta', 'Punjabi': 'pa', 'Malayalam': 'ml', 'Marathi': 'mr'}[lang_choice]
    translated_text = change_language(lang_code)
    st.write("*Translated Text:*")
    st.write(translated_text)
elif lang_choice != "None" and 'description' not in st.session_state:
    st.warning("Please upload an image and generate a description first before using translation features.")
