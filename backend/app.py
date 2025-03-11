from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
