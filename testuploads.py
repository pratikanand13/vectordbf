from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
from sentence_transformers import SentenceTransformer
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        try:
            df = pd.read_csv(file)
            organization_name = request.form.get('organization_name')
            intent_name = request.form.get('intent_name')
            
            if not organization_name:
                return jsonify({"error": "No organization name provided"})
            
            if not intent_name:
                return jsonify({"error": "No intent name provided"})
            
            # Process the DataFrame
            df['combined_info'] = df.fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            model = SentenceTransformer('all-mpnet-base-v2', cache_folder='models')
            df['embeddings'] = df['combined_info'].apply(lambda x: model.encode(x).tolist())
            
            # Save to MongoDB
            mongo_uri = ""
            client = MongoClient(mongo_uri)
            db = client[organization_name]
            collection = db[intent_name]
            
            data_list = df.to_dict(orient='records')
            collection.insert_many(data_list)
            
            return jsonify({"message": "Embeddings have been saved to MongoDB"})
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
