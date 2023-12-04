from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentOperations:
    def __init__(self, file_path):
        self.loader = PyPDFLoader(file_path)
        self.data = self.loader.load()

    def split_documents(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        return text_splitter.split_documents(self.data)
