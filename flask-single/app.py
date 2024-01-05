from flask import Flask, request, jsonify
from gensim.models import FastText
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

fasttext_model_path = r'D:\datasets\alreadyfasttextmodel\processed.fast_text'
fasttext_model = FastText.load(fasttext_model_path)

@app.route('/get_similarity', methods=['POST'])
def get_similarity():
    data = request.get_json()

    query = data['query']
    document = data['document']

    # Tokenize and embed the query
    query_embedding = fasttext_model.wv[query]

    # Tokenize the document into sentences
    document_sentences = [sentence.strip() for sentence in document.split('।') if sentence.strip()]

    # Set the window size
    window_size = 3

    # Calculate similarity for each window
    results = []
    for i in range(len(document_sentences) - window_size + 1):
        window = document_sentences[i:i + window_size]
        window_text = ' । '.join(window)  # Concatenate the sentences in the window
        window_embedding = fasttext_model.wv[window_text]  # Embed the concatenated window
        window_similarity = cosine_similarity([query_embedding], [window_embedding]).ravel()

        # Append the results as a dictionary
        results.append({
            "window_text": window_text,
            "score": float(window_similarity[0])  # Convert float32 to native Python float
        })

    # Return the results as JSON
    return jsonify(results[0].window_text)
    #return jsonify(document[:100])

if __name__ == '__main__':
    app.run(debug=True)
