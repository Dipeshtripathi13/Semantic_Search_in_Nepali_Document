import os
import chromadb
from gensim.models import FastText
import numpy as np
model_path = r'D:\datasets\alreadyfasttextmodel\processed.fast_text'
fasttext_model = FastText.load(model_path)

def trianing_first(news_directory):
    documents = []
    embedding_list = []  # Rename to avoid confusion with the gensim embeddings variable
    metadatas = []
    ids = []

    # Iterate through news articles
    for idx, filename in enumerate(os.listdir(news_directory), start=1):
        if filename.endswith(".txt"):
            file_path = os.path.join(news_directory, filename)

            # Read the content of the news article
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Tokenization and generate embeddings
            tokens = content.split()  # Replace with your actual tokenization
            embeddings = [fasttext_model.wv[word].tolist() for word in tokens]

            # Flatten the list of embeddings to get a single vector for the document
            document_vector = np.mean(embeddings, axis=0)

            # Store the data in ChromaDB
            documents.append(content)
            embedding_list.append(document_vector.tolist())
            metadatas.append({'file_name': filename})
            ids.append(str(idx))  # Convert ID to string

    # Connect to ChromaDB
    client = chromadb.Client()

    # Create a new collection
    collection = client.create_collection("V2Table")

    # Add data to ChromaDB
    collection.add(
        documents=documents,
        embeddings=embedding_list,  # Corrected variable name
        metadatas=metadatas,
        ids=ids
    )

def get_search_result(query):
    #query = "एमाओवादी रूपान्तरणमा भारतीय चासो एमाओवादीले महाधिवेशनबाट औपचारिक रूपमै आफ्नो नीतिमा परिवर्तन ल्याएपछि त्यो रूपान्तरणलाई भारतभित्र निकै चाखपूर्वक हेरिएको छ  "
    tokens = query.split()  # Replace with your actual tokenization
    input = [fasttext_model.wv[word].tolist() for word in tokens]
    client = chromadb.Client()
    collection = client.get_or_create_collection("V2Table")
            # Flatten the list of embeddings to get a single vector for the document
    input_em = np.mean(input, axis=0).tolist()
    result = collection.query(
        query_embeddings=[input_em],
        n_results=2
    
    )
    res = {
        "summary": result
    }
    return res