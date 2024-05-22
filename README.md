# Nexa-Ai

![Streamlit](https://img.shields.io/badge/Streamlit-1.12.0-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-0.11.0-brightgreen)
![Azure](https://img.shields.io/badge/Azure-2024--05--01--preview-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## Nexa-Ai: AI Chatbot with PDF Reading

Nexa-Ai is an AI chatbot powered by Azure OpenAI services, capable of reading PDFs. This project leverages Streamlit for the frontend interface and integrates functionalities via Azure OpenAI's API.

## Features

- **Chat with PDF**: Upload a PDF and ask questions based on its content.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API key and endpoint
- Git

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/nexa-ai.git
   cd nexa-ai

   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv myenv
   source myenv/bin/activate # On Windows: myenv\Scripts\activate

   ```

3. **Install Dependencies**

```bash
   pip install -r requirements.txt
```

4. **Set Up Environment Variables**

```bash
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your_openai_resource_name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-05-01-preview
```

5. **Run the Streamlit App**

```bash
streamlit run main.py
```
