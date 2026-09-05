# RAG-Chatbot-DarshanUniversity Tech Stack & Planning

This document outlines the technology stack and architecture used for the RAG (Retrieval-Augmented Generation) Chatbot project for Darshan University.

## 1. Web Scraping & Data Extraction
- **Scrapy**: Used as the primary web crawling framework to scrape pages from the Darshan University website.
- **readability-lxml & trafilatura**: Used to extract the main content/text from the raw HTML pages while stripping out unnecessary boilerplate.

## 2. Embeddings & Vector Database
- **HuggingFace MiniLM**: The `sentence-transformers/all-MiniLM-L6-v2` model is used to convert the extracted text into structural vector embeddings.
- **ChromaDB**: Used as the local vector store (`data/chroma_db`) to store and retrieve the document embeddings efficiently.

## 3. Large Language Model (LLM) & Framework
- **Ollama**: Acts as the local LLM server to keep requests fast and completely private without relying on external APIs.
- **Phi-3**: The `phi3` model running via Ollama is used for generating grounded answers based strictly on the retrieved context.
- **LangChain**: The LangChain framework (`langchain_community`) is used to orchestrate the integration between the embeddings and the vector store.

## 4. Web Application (UI)
- **Flask**: Used to build the backend server and provide the API (`/api/chat`) for the chat interaction.
- **HTML, CSS, JavaScript (Vanilla)**: The frontend is a dark-themed chat interface that seamlessly communicates with the Flask backend.

## 5. Other Tools & Libraries
- **requests & urllib**: Handing HTTP requests natively (e.g., calling the local Ollama API).
