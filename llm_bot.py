import os
import logging
from openai import AzureOpenAI
import pdfplumber
import docx2txt
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Initialize Azure OpenAI API with the API key and endpoint from .env file
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def trim_context(context, max_tokens, buffer_tokens=1000):
    tokens = context.split()
    if len(tokens) + buffer_tokens > max_tokens:
        return " ".join(tokens[-(max_tokens - buffer_tokens):])
    return context

def generate_response(prompt, context="", model="gpt-35-turbo"):
    logging.info(f"Using deployment ID: {model}")
    max_context_length = 8192
    context = trim_context(context, max_context_length)

    messages = [
        {"role": "system", "content": "You are an assistant. Use the context provided to answer questions."},
        {"role": "user", "content": prompt}
    ]

    if context:
        messages.insert(1, {"role": "system", "content": context})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150,
            temperature=0.9
        )
        logging.info(f"Response received: {response}")
        # Check if the response is valid
        if response and response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            logging.error(f"Invalid response structure: {response}")
            return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        raise

# Example usage
if __name__ == "__main__":
    prompt = "Hello, how can I help you?"
    context = "This is an example context."
    model = "gpt-35-turbo"
    response_text = generate_response(prompt, context, model)
    print(response_text)
