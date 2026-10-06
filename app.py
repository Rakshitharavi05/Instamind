from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_profile

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "InstaMind AI backend is working!"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "error": "Instagram URL is required"
        }), 400

    instagram_url = data["url"]

    # Send the URL to our analysis engine
    result = analyze_profile(instagram_url)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)