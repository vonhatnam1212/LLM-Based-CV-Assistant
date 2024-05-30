import sys

sys.path.append("../api")
from config import (
    FILE_PATH,
)


# llama index
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import StorageContext
from feature_pipeline.get_documents import get_extract_documents
from model import (
    llamaindex_cohere_rerank,
    llamaindex_embed_model,
    pinecone_index,
)

Settings.chunk_size = 512


def save_index_vectordb():
    origin_documents = get_extract_documents(FILE_PATH)
    from llama_index.core import Document

    documents = []
    for document in origin_documents:
        documents.append(
            Document(
                text=document["overview_CV"],
                metadata=document["metadata"],
            )
        )
    # Không chạy cell này mà chạy cell dưới (cái này dùng để tạo vector db)
    # Create an index over the documnts
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
        embed_model=llamaindex_embed_model,
    )
    return index


def load_index_vectordb():
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        show_progress=True,
        embed_model=llamaindex_embed_model,
    )

    return index


def get_query_engine():
    try:

        index = load_index_vectordb()
        # configure retriever
        retriever = VectorIndexRetriever(
            index,
            verbose=True,
            similarity_top_k=5,
        )

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[llamaindex_cohere_rerank],
        )
        print("query engine successful")
    except:
        print("error query engine")
    return query_engine
