# Airline Customer Support Bot


## Overview
This repository contains the code for an Airline Customer Support Bot designed to assist with customer queries efficiently and effectively.

## Tools Used
- **Langchain**
- **ChromaDB** (vector store)
- **Ollama** (Llama 3.1 AI model)
- **MySQL** (chat history)
- **Flask**

## Setup Instructions

Ensure you have Ollama running:
```
ollama serve
```

Set up a virtual environment:
```
python -m venv venv
```

Install the necessary libraries:
```
pip install -r requirements.txt
```


Modify the \`.env\` file with your specific information.


Create the \`messages\` table using **create_messages_table.sql**:


Execute the \`app.py\` file to start the application:
```
python app.py
```

## API Endpoints

### /ai
- **Description**: Ask LLM
- **Chat History**: None
- **Context from PDFs**: None

### /airbot
- **Description**: Ask LLM
- **Chat History**: Includes a maximum of 6 past messages
- **Context from PDFs**: Yes

### /pdf
- **Description**: Upload PDFs to the vector store

## Contribution
Feel free to open issues or submit pull requests if you have suggestions or improvements.
