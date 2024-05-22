import streamlit as st
import yaml
from llm_bot import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, generate_response
import os
import base64

# Load configuration settings
with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Set up the Streamlit app
st.set_page_config(page_title=config["title"], page_icon=config.get("logo", None), layout="wide")

# Load custom CSS
with open(os.path.join("styles", "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helper function to encode images to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the images
user_img_base64 = get_base64_image("images/user.png")
chatbot_img_base64 = get_base64_image("images/chatbot.png")

# Initialize session state if not already initialized
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = config.get("openai_model", "gpt-35-turbo")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0

def reset_chat():
    st.session_state.messages = []
    st.session_state.document_text = ""
    st.session_state.uploaded_file = None
    st.session_state.file_uploader_key += 1  # Change the key to reset the file uploader

# Sidebar with only the "New Chat" button
st.sidebar.title("Chat with Nexa")
if st.sidebar.button("New Chat"):
    reset_chat()
    st.experimental_rerun()  # To re-run the app and reset the file uploader

st.title(config["title"])

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"], key=st.session_state.file_uploader_key)
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document_text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        document_text = extract_text_from_txt(uploaded_file)
    else:
        document_text = "Unsupported file type."
    st.session_state.document_text = document_text
    st.text_area("Document Content", document_text, height=300)
else:
    st.session_state.uploaded_file = None

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message_container user">
            <div class="avatar user_avatar"><img src="data:image/png;base64,{user_img_base64}" /></div>
            <div class="message user_message">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message_container bot">
            <div class="message bot_message">{message["content"]}</div>
            <div class="avatar bot_avatar"><img src="data:image/png;base64,{chatbot_img_base64}" /></div>
        </div>
        """, unsafe_allow_html=True)

# Handle user input
if prompt := st.chat_input("Enter your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
    <div class="message_container user">
        <div class="message user_message">{prompt}</div>
        <div class="avatar user_avatar"><img src="data:image/png;base64,{user_img_base64}" /></div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Nexa is thinking..."):
        context = st.session_state.document_text if st.session_state.document_text else ""
        try:
            if prompt.lower() in ["hi", "hello", "hi!", "hello!", "hey", "hey!", "hi nexa", "hello nexa", "hey nexa"]:
                response_text = "Hello! I'm Nexa, How can I assist you today? 😊"
            elif "thank you" in prompt.lower():
                response_text = "You're welcome! If you have any more questions, feel free to ask. 😃"
            else:
                response_text = generate_response(prompt, context, st.session_state["openai_model"])
            st.markdown(f"""
            <div class="message_container bot">
                <div class="avatar bot_avatar"><img src="data:image/png;base64,{chatbot_img_base64}" /></div>
                <div class="message bot_message">{response_text}</div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Error generating response: {e}")
            st.error(f"Details: {str(e)}")
