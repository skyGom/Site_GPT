import os

from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

from utility.url import extract_site_name

def _parse_page(soup):
    # header = soup.find("header")
    # footer = soup.find("footer")
    
    # header.decompose() if header else "Header not found"
    # footer.decompose() if footer else "Footer not found"

    return (str(soup.get_text()).replace('\n','').replace('\xa0', '').replace('|','').replace('↗', ' ').replace('@',''))
    
def get_retriever_after_embedding(url, api_key):
    split_docs = _get_split_docs(url)
    # cached_embeddings = _get_cached_embeddings(url, api_key)
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vector_store = FAISS.from_documents(split_docs, embeddings)
    return vector_store.as_retriever()

def _get_split_docs(url):
    splitter = RecursiveCharacterTextSplitter().from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200
    )
    loader = SitemapLoader(web_path=url,
                           filter_urls=[
                                r"^https:\/\/developers\.cloudflare\.com\/ai-gateway\/.*",
                                r"^https:\/\/developers\.cloudflare\.com\/vectorize\/.*",
                                r"^https:\/\/developers\.cloudflare\.com\/workers-ai\/.*"
                            ],
                           parsing_function=_parse_page)
    loader.requests_per_second = 20
    return loader.load_and_split(text_splitter=splitter)

# def _get_cached_embeddings(url, api_key):
#     embedding_cache_dir = f'./.cache/embeddings/{extract_site_name(url)}'
    
#     os.makedirs(embedding_cache_dir, exist_ok=True)
    
#     embedding = OpenAIEmbeddings(
#         api_key=api_key,
#     )
#     file_store = LocalFileStore(embedding_cache_dir)
#     return CacheBackedEmbeddings(embedding, file_store)