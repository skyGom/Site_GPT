import os
import re

from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

import streamlit as st

def _parse_page(soup):
    # header = soup.find("header")
    # footer = soup.find("footer")
    
    # header.decompose() if header else "Header not found"
    # footer.decompose() if footer else "Footer not found"

    return (str(soup.get_text()).replace('\n','').replace('\xa0', '').replace('|','').replace('|','').replace('↗', ' ').replace('@',''))
    
def get_retriever_after_embedding(url, api_key):
    split_docs = _get_split_docs(url)
    cached_embeddings = _get_cached_embeddings(url, api_key)
    st.write(split_docs)
    vector_store = FAISS.from_documents(split_docs, cached_embeddings)
    return vector_store.as_retriever()

def _get_split_docs(url):
    splitter = RecursiveCharacterTextSplitter().from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200
    )
    loader = SitemapLoader(web_path=url,
                           filter_urls=[r"^(.*\/ai-gateway\/).*",
                                        r"^(.*\/vectorize\/).*",
                                        r"^(.*\/workers-ai\/).*",],
                           parsing_function=_parse_page)
    loader.requests_per_second = 2
    loader.requests_kwargs = {"verify": False}
    return loader.load_and_split(text_splitter=splitter)

def _get_cached_embeddings(url, api_key):
    embedding_cache_dir = f'./.cache/embeddings/{_sanitize_url(url)}'
    
    if not os.path.exists(embedding_cache_dir):
        os.makedirs(embedding_cache_dir)
    
    embedding = OpenAIEmbeddings(
        api_key=api_key,
    )
    file_store = LocalFileStore(embedding_cache_dir)
    return CacheBackedEmbeddings(embedding, file_store)
    
def _sanitize_url(url):
    return re.sub(r'[\\/*?:"<>|.-]', '', url)