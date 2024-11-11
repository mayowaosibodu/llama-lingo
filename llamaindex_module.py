from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
import logging
import sys



logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


api_key = "72f89b36b6b3444a81cefa0d20716e43"
azure_endpoint = "https://aditu-openai-resource-2.openai.azure.com/"
api_version = "2023-07-01-preview"



llm = AzureOpenAI(
    model= "gpt-4-32k",
    deployment_name="GPT4-32k",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
 )



embed_model = AzureOpenAIEmbedding(
    model="text-embedding-3-large",
    deployment_name="text-embedding-3-large",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)


Settings.llm = llm
Settings.embed_model = embed_model

print('\n_________________________\nPreparing Data Index...')

from llama_index.core import StorageContext, load_index_from_storage

# # rebuild storage context
# storage_context = StorageContext.from_defaults(persist_dir="index")

# # load index
# index = load_index_from_storage(storage_context)


documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

index.storage_context.persist(persist_dir="index")

query_engine = index.as_query_engine()

# print('\n_________________________\nDone.')

# while True:
#     text = input('Enter query: ')
#     response = query_engine.query(text)
#     print(response)


