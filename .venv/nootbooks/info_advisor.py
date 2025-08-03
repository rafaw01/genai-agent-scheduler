import pysqlite3
import sqlite3
sqlite3 = pysqlite3
import os
from dotenv import load_dotenv
import openai

# langchain-community imports to avoid deprecation warnings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

# Ensure pypdf is installed: pip install pypdf

load_dotenv()  # loads OPENAI_API_KEY

class InfoAdvisor:
    """
    Agent for querying PDF documents via a RetrievalQA chain.

    Usage:
        from info_advisor import InfoAdvisor
        advisor = InfoAdvisor(
            pdf_path="MyDoc.pdf", persist_dir="chroma_db", model_name="gpt-4", k=5
        )
        answer = advisor.get_answer("Your question here")
    """
    def __init__(
        self,
        pdf_path: str = "Python Developer Job Description.pdf",
        persist_dir: str = "chroma_db",
        model_name: str = None,
        k: int = 3,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable")
        openai.api_key = api_key

        # Load and split PDF into chunks
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(docs)

        # Build or reuse Chroma vector store
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.vectorstore = Chroma(
            collection_name="pdf_collection",
            embedding_function=embeddings,
            persist_directory=persist_dir
        )
        if not os.path.isdir(persist_dir) or not os.listdir(persist_dir):
            self.vectorstore.add_documents(chunks)
            self.vectorstore.persist()

        # Create retriever and QA chain
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        if model_name is None:
            model_name = os.getenv("INFO_ADVISOR_MODEL", "gpt-3.5-turbo")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                openai_api_key=api_key,
                model_name=model_name,
                temperature=0
            ),
            chain_type="stuff",
            retriever=retriever
        )

    def get_info_answer(self, query: str) -> str:
        """
        Return an answer for the given question using the RetrievalQA chain.
        """
        return self.qa_chain.run(query)





