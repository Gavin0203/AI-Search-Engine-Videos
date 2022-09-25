# AI-Search-Engine-Videos
This repository contains the code to build and run an AI powered search engine which uses NLP and Vector databases.

## Pre-requisites

1. Knowledge on Text embeddings using Transfomers.
2. Sentence-Transformer library.
3. Setup Vector Database `Pinecone` and get the API to load the embeddings to the Vector DB.
4. Basic working of streamlit.

## Steps 

The steps followed to build the AI Based Search Engine for GIF's.

1. We first download the training data from ......
2. We then load the data, get the embeddings and update the embeddings and the metadata to the Pinecone vector DB.
3. We build a search engine layout using streamlit.
4. The user search query is then recorded and embedded and we find the most similar by using the Cosine Similarity metric.