import  os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter, Depends
from .. import schemas, config, auth2
router = APIRouter( tags=['Cars'])

def process_allpdffiles(pdf_directory):
    all_documents = []
    pdf_dir = Path(pdf_directory)
    
    pdf_files = list(pdf_dir.glob("**/*.pdf"))

    # print(f"Found {len(pdf_files)} PDF files in {pdf_directory}")

    for pdf_file in pdf_files:
        # print(f"processing{pdf_file}")
        try:
            loader = PyMuPDFLoader(str(pdf_file))
            documents = loader.load()
            
            for doc in documents:
                doc.metadata["sorue_file"] = pdf_file.name
                doc.metadata["filetype"] = "pdf"
                doc.metadata["created_at"] = datetime.datetime.now().isoformat()
                doc.metadata["author"] = "murali tharan"

            all_documents.extend(documents)
            # print(f"Loaded {len(documents)} documents from {pdf_file}")
        except Exception as e:
            # print(f"Error processing {pdf_file}: {e}")
            raise

    # print(f"Total documents loaded: {len(all_documents)}")
    return all_documents

all_pdf_docs  = process_allpdffiles("./src/pdffiles/")
all_pdf_docs

def split_documents_into_chunks(documents, chunk_size=1000, chunk_overlap=200):

    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_spliter.split_documents(documents)

    # print(f"Split {len(documents)} documents into {len(split_docs)} chunks")

    # if split_docs:
    #     print(f"First chunk: {split_docs[0].page_content[:100]}...")  # Print first 500 characters of the first chunk
    #     print(f"First chunk metadata: {split_docs[0].metadata}")

    return split_docs

chunked_pdf_docs = split_documents_into_chunks(all_pdf_docs, chunk_size=1000, chunk_overlap=200)
chunked_pdf_docs

contents = [doc.page_content for doc in chunked_pdf_docs]

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Tuple, Any
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingModel():
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        try:
            # print(f"embedding model name : {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            # print(f"Loaded embedding model: {self.model_name}")
            # print(f"Model Loaded Successfully , embedding dimensions : {self.model.get_embedding_dimension()}")
        except Exception as e:
            # print(f"Error loading embedding model {self.model_name}: {e}")
            raise

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model Not Loaded")

        embedding = self.model.encode(texts, show_progress_bar=True)
        # print(f"embdded Length: {len(embedding)}")
        return embedding

embedding_model = EmbeddingModel()
embedding_model

class VectorStore():
    def __init__(self, collection_name: str = "pdfdocuments" , persist_directory: str = "../data/vector_store"):
        self.collection_name=  collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
      
        self._initialize_store()

    def _initialize_store(self):
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client =chromadb.PersistentClient(self.persist_directory)
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name = self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise

    def add_documents(self, documents : List[Any], embeddings:np.ndarray):
        if len(documents) != len(embeddings):
            raise ValueError("Length does not match")

        # print("Number of chunks:", len(documents))


        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i,(document, embedding) in enumerate(zip(documents, embeddings)):

            
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            metadata =dict(document.metadata)
            metadata["doc_index"] = i
            metadata["conttent_length"] = len(document.page_content)
            metadatas.append(metadata)

            documents_text.append(document.page_content)
            embeddings_list.append(embedding.tolist())

        try:
            
            self.collection.add(
                ids = ids,
                embeddings= embeddings_list,
                documents=documents_text,
                metadatas=metadatas
            )
            print("Vector Database loaded")
            # print(f"successfully added {len(documents)} documents to vector store")
            # print(f"toltal documents in collection : {self.collection.count()}")

        except Exception as e:
            # print(f"error during doucments to vector store :: {e}")
            raise

vector_store =VectorStore()
vector_store

texts = [doc.page_content for doc in chunked_pdf_docs]

embeddings  = embedding_model.embed_texts(texts)

vector_store.add_documents(chunked_pdf_docs, embeddings)

class RAGRetrival:
    def __init__(self, vector_store, embedding_manager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(self, querry:str, top_k:int = 3, score_threshold : float = 0.4) -> list[dict[str,any]]:
        print(f"retrieving documents for querry :{querry}")
        print(f"{top_k}, score thershold:{score_threshold}")

        querry_embedding = self.embedding_manager.embed_texts([querry])[0]
        

        try: 
            results = self.vector_store.collection.query(
                query_embeddings = [querry_embedding.tolist()],
                n_results = top_k
            )
            retrived_docs = []
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]

                print(f"distances: {results['distances'][0]}")
                
                for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    similarity_score = 1-distance

                    if similarity_score >= score_threshold:
                        retrived_docs.append({
                            "id" : doc_id,
                            "content" : document,
                            "metadata" : metadata,
                            'similarity_score' : similarity_score,
                            'distance'  : distance,
                            'rank' :  i+1
                        })

                print(f"Retrieved {len(retrived_docs)} documents (after filtering)")
            else :
                print("no documents found")
            return retrived_docs

        except Exception as e:
            print(f"Error during retrieval: {e}")
          

            return []

rag_retrieve = RAGRetrival(vector_store, embedding_model)


#FUNCTION For Making RESPONSE FORM LLM

def RAG_simple(query, retriever, client, top_k=3):
    results = retriever.retrieve(query, top_k)

    context = '\n\n'.join([doc['content'] for doc in results])if results else ""

    if not context:
        print("no relevant answer to the input please retry with different input")


    prompt = f"""Answer using only the context.if you find context as empty reurn this "no relevant answer to the input please retry with different input"

                Context:
                {context}

                Question: {query}
                """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )
    
    return response.output_text


client = OpenAI(
    api_key= config.settings.api_key
)


@router.post("/api/rag/",response_model=schemas.RAGResponse)
def rag_api(question: schemas.RAGRequest, getcurrent_user :dict = Depends(auth2.get_current_user)):

    answer = RAG_simple(
        query=question.query,
        retriever=rag_retrieve,
        client=client
    )

    return {
        "answer": answer
    }