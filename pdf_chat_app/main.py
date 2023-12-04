from flask import Flask, render_template, request, jsonify
from document_operations import DocumentOperations
from embedding_operations import EmbeddingOperations
from ai_operations import AIOperations
from langchain.llms import OpenAI
from config import openai_keys
import os

os.environ['OPENAI_API_KEY'] = openai_keys.API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    pdf_file = request.files.get('pdfFile')
    user_message = request.form.get('userInput')

    if pdf_file:
        file_path = os.path.join('uploads', pdf_file.filename)
        pdf_file.save(file_path)

        document_ops = DocumentOperations(file_path)
        texts = document_ops.split_documents()

        # Decode only if the object is not a string
        texts = [text.page_content.decode('utf-8') if isinstance(text.page_content, bytes) else text.page_content for text in texts]

        embedding_ops = EmbeddingOperations(texts)
        ai_ops = AIOperations(OpenAI(temperature=0.2))

        # Implement AI logic to get response based on user input
        docs = embedding_ops.docsearch.similarity_search(user_message)
        ai_response = ai_ops.run_chain(docs, user_message)

        return jsonify({"ai_response": ai_response})

    return jsonify({"ai_response": "Invalid request"})


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)



















# from dotenv import load_dotenv
# from config import openai_keys
# from document_operations import DocumentOperations
# from embedding_operations import EmbeddingOperations
# from ai_operations import AIOperations
# from langchain.llms import OpenAI
# import os

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = openai_keys.API_KEY

# file_path = "Data\Ahmed Story.pdf"
# document_ops = DocumentOperations(file_path)
# texts = document_ops.split_documents()

# embedding_ops = EmbeddingOperations(texts)

# ai_ops = AIOperations(OpenAI(temperature=0.2))

# print("\n\n--->Main Start from Here<---\n\n")

# while True:
#     query = input("Enter Prompt: ")
#     docs = embedding_ops.docsearch.similarity_search(query)

#     print(ai_ops.run_chain(docs, query))
#     option = input("Do you wanna continue?(Y/N): ")
#     if option.upper() != 'Y':
#         exit()
