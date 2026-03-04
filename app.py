from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

MONGO_URI = "mongodb+srv://alon_admin:DB135@azurecluster.hyeobnc.mongodb.net/ElysianDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client['ElysianDB'] 
users_collection = db['users'] 

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    users_collection.insert_one(data)
    return jsonify({"message": "User registered successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)