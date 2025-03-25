from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()
loader = DirectoryLoader("./FAQ",
                         glob="**/*.txt",
                         loader_cls=TextLoader,
                         show_progress=True
                        )
documents = loader.load()
logger.info(f"Loaded {len(documents)} documents")
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
logger.info(f"Split {len(docs)} documents")
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@127.0.0.1:5433/vectordb"
COLLECTION_NAME = "vectordb"
db = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)
logger.info(f"Inserted {len(docs)} documents")


