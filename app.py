from flask import Flask, request
import prompt
import db

# llm
from langchain_community.llms import Ollama

# pdf -> vectorstore
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# rag
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

app = Flask(__name__)

folder_path = 'db'
model = 'llama3.1'

cached_llm = Ollama(model=model)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, length_function=len, is_separator_regex=False
)

embedding = HuggingFaceEmbeddings()


@app.route('/ai', methods=['POST'])
def aiPost():
    print('POST /ai called')
    json_content = request.json
    query = json_content.get('query')

    response = cached_llm.invoke(query)
    print(response)

    response_answer = {'answer': response}
    return response_answer


@app.route('/airbot', methods=['POST'])
def askAI_RAG():
    print('POST /airbot called')
    json_content = request.json

    query = json_content.get('query')
    user_id = json_content.get('user_id')
    chat_id = json_content.get('chat_id')

    connection = db.Connection()
    cursor = db.Cursor(connection)
    db.send_message(query, user_id, chat_id, True, cursor, connection)

    print('loading the vector store')
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print('creating a retriever')
    retriever = vector_store.as_retriever(
        search_type='similarity_score_threshold',
        search_kwargs={
            'k': 4,
            'score_threshold': 0.1,
        },
    )
    raw_template = prompt.generate_prompt(user_id, chat_id, cursor)
    raw_prompt = PromptTemplate.from_template(raw_template)
    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({'input': query, })
    answer = result['answer']

    db.send_message(answer, user_id, chat_id, False, cursor, connection)
    db.delete_older_rows(user_id, chat_id, cursor, connection)
    db.Disconnect(cursor, connection)

    response_answer = {'answer': answer}
    return response_answer


@app.route('/pdf', methods=['POST'])
def pdfPost():
    file = request.files['file']
    file_name = file.filename
    save_file = 'pdf/' + file_name
    file.save(save_file)
    print(f'filename: {file_name}')

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f'docs len={len(docs)}')

    chunks = text_splitter.split_documents(docs)
    print(f'chunks len={len(chunks)}')

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    response = {
        'status': 'Successfully Uploaded',
        'filename': file_name,
        'docs': len(docs),
        'chunks': len(chunks),
    }
    return response


def start_app():
    app.run(host='0.0.0.0',
            port=8080,
            debug=True
            )


if __name__ == "__main__":
    start_app()
