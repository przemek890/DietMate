from src.GPT.tools import stream_response, generate_jwt, require_valid_token
from tools import is_docker
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from typing import Dict, Any, Union
from pymongo import MongoClient, collection
import os
import groq
import uuid
import datetime
import redis
############################################################################################################
# Flask app initialization and CORS setup
app = Flask(__name__)
cors_origins = os.getenv("REACT_APP_DOMAIN", "http://localhost")
if cors_origins.startswith('https'):
    CORS(app, origins=[cors_origins], supports_credentials=True)
else:
    CORS(app, supports_credentials=True)

# MongoDB connection configuration
connection: str = os.getenv("MONGO_CONNECTION_STRING", "").strip()
if not connection:
    raise ValueError("MONGO_CONNECTION_STRING environment variable must be set")

client: MongoClient = MongoClient(connection)
db = client.dietmate
collection1: collection.Collection = db['GPT']

# Redis connection configuration
r = None
try:
    redis_cloud_host = os.getenv("REDIS_CLOUD_HOST", None)
    redis_cloud_password = os.getenv("REDIS_CLOUD_PASSWORD", None)
    if redis_cloud_host and redis_cloud_password:
        print("✅ Using Redis Cloud configuration (Free tier - 30MB).")
        r = redis.Redis(
            host=redis_cloud_host,
            port=15355,
            decode_responses=True,
            username="default",
            password=redis_cloud_password,
        )
    else:
        if is_docker():
            host = "redis" 
            print("✅ Detected Docker environment.")
        else:
            host = "localhost"
            print("✅ Detected Host environment.")
        r = redis.Redis(host=host, port=6379)
    
    if r.ping():
        print("✅ Redis connection successful.")
    else:
        print("⚠️ Redis server is not responding.")
        r = None     
except Exception as e:
    print("⚠️ Warning: Redis connection failed:", e)
    r = None

############################################################################################################

@app.route('/api/session', methods=['GET'])
def manage_session():
    """
    Create a new session and generate JWT token.

    This endpoint creates a new session with a unique UUID and generates a corresponding JWT token.

    Returns:
        tuple: A tuple containing:
            - dict: JSON response with:
                - message (str): Success message
                - token (str): Generated JWT token
            - int: HTTP 200 status code
    """
    new_session_id = str(uuid.uuid4())
    token = generate_jwt(new_session_id)
    return jsonify({
        "message": "New session created",
        "token": token
    }), 200

@app.route('/api/askGPT', methods=['POST'])
@require_valid_token
def ask_gpt_endpoint(session_id: str) -> Response:
    """
    Protected endpoint to interact with GPT-like models for streaming responses.
    Session verification is handled by the require_valid_token decorator.

    Args:
        session_id: Automatically injected by the decorator after token verification
    """
    try:
        data: Dict[str, Any] = request.json or {}
        message: str = data.get('message', '')
        file_name: str = data.get('fileName', '')
        file_content: str = data.get('fileContent', '')

        response_content = []
        client: groq.Groq = groq.Groq()

        def generate_stream():
            for chunk in stream_response(message, file_name, file_content, client, session_id, collection1):
                response_content.append(chunk)
                yield chunk

        response = Response(generate_stream(), content_type='text/event-stream')

        @response.call_on_close
        def save_to_database():
            bot_message = ''.join(response_content)
            try:
                document = {
                    "session_id": session_id,
                    "user_message": message,
                    "bot_message": bot_message,
                    "file_name": file_name,
                    "file_content": file_content,
                    "date_added": datetime.datetime.now(),
                    "model": os.getenv("GROQ_GPT_MODEL", "")
                }
                collection1.insert_one(document)

            except Exception as db_error:
                print(f"Error saving interaction to the database: {db_error}")

        return response

    except Exception as e:
        return Response(f"***ERROR***: {e}", status=500)

DIETS = [
    {"id": 1, "name": "Keto", "description": "Ketogenic diet", "price": 150},
    {"id": 2, "name": "Vegan", "description": "Vegan diet", "price": 130},
    {"id": 3, "name": "Low-carb", "description": "Low-carbohydrate diet", "price": 100}
]

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API for Next.js - DietMate!"})

@app.route("/api/diets", methods=["GET"])
def get_all_diets():
    return jsonify({"diets": DIETS})

@app.route("/api/diets/<int:diet_id>", methods=["GET"])
def get_diet_by_id(diet_id):
    diet = next((d for d in DIETS if d["id"] == diet_id), None)
    if diet is None:
        return jsonify({"error": "Diet not found"}), 404
    return jsonify(diet)

@app.route("/api/purchase", methods=["POST"])
def purchase_diet():
    data = request.json
    diet_id = data.get("dietId")
    user_data = data.get("userData", {})
    user_name = user_data.get("name", "Anonymous")
    return jsonify({"message": f"User {user_name} has purchased diet ID {diet_id}!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
