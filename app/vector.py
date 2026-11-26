
import logging
import time
from functools import lru_cache

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from app.config import settings
from app.models import embeddings

log = logging.getLogger(__name__)


# 1. Initialize and validate Pinecone index
@lru_cache(maxsize=1)
def get_index():

    s = settings()

    if not s.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY missing")

    if not s.pinecone_index_name:
        raise RuntimeError("PINECONE_INDEX_NAME missing")

    pc = Pinecone(api_key=s.pinecone_api_key)
    name = s.pinecone_index_name

    try:
        info = pc.describe_index(name)

    except Exception as exc:

        if getattr(exc, "status", None) != 404:
            raise

        log.info("Creating Pinecone index: %s", name)

        try:
            pc.create_index(
                name=name,
                dimension=s.embed_dim,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=s.pinecone_cloud,
                    region=s.pinecone_region
                )
            )

        except Exception as create_exc:

            if getattr(create_exc, "status", None) != 409:
                raise

        info = pc.describe_index(name)

    # Dimension validation
    if int(info.dimension) != s.embed_dim:
        raise ValueError("Embedding dimension mismatch")

    # Metric validation
    if str(info.metric).lower() != "cosine":
        raise ValueError("Pinecone metric must be cosine")

    # Wait until index is ready
    deadline = time.monotonic() + s.pinecone_ready_timeout

    while not pc.describe_index(name).status["ready"]:

        if time.monotonic() >= deadline:
            raise TimeoutError("Pinecone index not ready")

        time.sleep(3)

    log.info("Pinecone index ready: %s", name)

    return pc.Index(name)


# 2. Get LangChain VectorStore
def get_vectorstore(tenant):

    index = get_index()

    return PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=f"tenant-{tenant}"
    )


# 3. Upsert documents
def upsert(tenant, documents):

    vectorstore = get_vectorstore(tenant)

    return vectorstore.add_documents(documents)


# 4. Similarity search with ACL
def search(tenant, query, groups, owner, limit=5):

    vectorstore = get_vectorstore(tenant)

    acl = {
        "$or": [
            {"allowed_groups": {"$in": list(groups)}},
            {"owner_sub": {"$eq": owner}}
        ]
    }

    return vectorstore.similarity_search(
        query=query,
        k=limit,
        filter=acl
    )


# 5. Delete document chunks
def delete_document(tenant, ids):

    if not ids:
        return

    vectorstore = get_vectorstore(tenant)

    return vectorstore.delete(ids=ids)
