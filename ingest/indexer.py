"""Vector Index Builder for SuperStream RAG System."""

from pathlib import Path
from typing import List, Optional, Any

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

import faiss

from config import EMBEDDING_MODEL, EMBEDDING_MODEL_TYPE, OPENAI_API_KEY, OPENAI_API_BASE


def create_embedding_model(
    model_name: str,
    model_type: str = EMBEDDING_MODEL_TYPE,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None
) -> Any:
    """
    Create embedding model based on type.

    Args:
        model_name: Name of the embedding model.
        model_type: Type of model - "openai" or "huggingface".
        api_key: OpenAI API key (required for OpenAI models).
        api_base: OpenAI API base URL (optional for OpenAI models).

    Returns:
        Embedding model instance.
    """
    if model_type == "openai":
        return OpenAIEmbedding(
            model=model_name,
            api_key=api_key or OPENAI_API_KEY,
            api_base=api_base or OPENAI_API_BASE
        )
    elif model_type == "huggingface":
        # HuggingFace embedding models (like E5-Large-V2)
        return HuggingFaceEmbedding(model_name=model_name)
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")


class IndexBuilder:
    """
    Builds and manages FAISS vector indexes for RAG system.

    Uses embeddings (OpenAI or HuggingFace) to vectorize documents and stores them
    in FAISS for efficient similarity search.

    Attributes:
        embedding_model: Embedding model name.
    """

    def __init__(
        self,
        embedding_model: str = EMBEDDING_MODEL,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None
    ):
        """
        Initialize index builder.

        Args:
            embedding_model: Embedding model name.
            api_key: OpenAI API key. Defaults to OPENAI_API_KEY from config.
            api_base: OpenAI API base URL. Defaults to OPENAI_API_BASE from config.
        """
        self.embedding_model = embedding_model
        self.api_key = api_key or OPENAI_API_KEY
        self.api_base = api_base or OPENAI_API_BASE

        # Initialize embedding model
        self.embedding = create_embedding_model(
            model_name=embedding_model,
            model_type=EMBEDDING_MODEL_TYPE,
            api_key=self.api_key,
            api_base=self.api_base
        )

    def build_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Build a FAISS vector index from documents.

        Creates a new FAISS index, embeds all documents, and returns
        a VectorStoreIndex ready for querying.

        Args:
            documents: List of Document objects to index.

        Returns:
            VectorStoreIndex object for querying.

        Raises:
            ValueError: If documents list is empty.
        """
        if not documents:
            raise ValueError("Documents list is empty")

        try:
            # Create FAISS index
            # E5-Large-V2 uses 1024 dimensions, OpenAI embeddings use 1536
            dimension = 1024 if EMBEDDING_MODEL_TYPE == "huggingface" else 1536
            faiss_index = faiss.IndexFlatL2(dimension)

            # Create vector store
            vector_store = FaissVectorStore(faiss_index=faiss_index)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store
            )

            # Build index from documents
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                embed_model=self.embedding,
                show_progress=True
            )

            print(f"Index built successfully with {len(documents)} documents")
            return index

        except Exception as e:
            print(f"Error building index: {e}")
            raise

