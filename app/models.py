from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama



#embed model

embeddings = HuggingFaceEmbeddings(
    #api key
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


#chat model

llm = ChatOllama(
    #api key
    model="llama3.2",
    temperature=0.2,
    num_predict=1024
)



#for testing
    # # Embedding test
    # vector = embeddings.embed_query("What is RAG?")
    # print(len(vector))  # 384

    # # LLM test
response = llm.invoke("Explain RAG in 2 lines")
print(response.content)