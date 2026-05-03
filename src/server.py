"""
Emotion-Aware Chatbot API
Flask backend for emotion detection and adaptive response generation
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from emotion_analyzer import EmotionAnalyzer
from openrouter_client import ClaudeResponseGenerator  # Renamed from claude_client

# Load environment variables from root .env
load_dotenv(Path(__file__).parent.parent / ".env")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# ✅ ENABLE CORS (VERY IMPORTANT)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize components
emotion_analyzer = EmotionAnalyzer()

try:
    response_generator = ClaudeResponseGenerator()
except ValueError as e:
    print(f"Warning: {e}")
    response_generator = None


# ==================== ROUTES ====================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "service": "Emotion-Aware Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Send user input and receive emotion-aware response",
            "GET /health": "Health check",
            "POST /reset": "Reset emotion history"
        }
    })


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "api_available": response_generator is not None
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "user_input" not in data:
            return jsonify({"error": "Missing required field: user_input"}), 400

        user_input = data.get("user_input", "").strip()

        if not user_input:
            return jsonify({"error": "user_input cannot be empty"}), 400

        if len(user_input) > 10000:
            return jsonify({"error": "user_input too long"}), 400

        # Emotion analysis
        analysis = emotion_analyzer.analyze(user_input)

        # Generate responses
        if response_generator is None:
            normal_response = "API not available. Please check your API key."
            emotion_response = normal_response
        else:
            normal_response = response_generator.generate_normal_response(user_input)
            emotion_response = response_generator.generate_emotion_based_response(
                user_input,
                analysis["emotion"],
                analysis["intensity"]
            )

        # UI + speed
        response_speed = emotion_analyzer.get_response_speed(analysis["emotion"])
        ui_color = emotion_analyzer.get_ui_color(analysis["emotion"])

        return jsonify({
            "emotion": analysis["emotion"],
            "intensity": analysis["intensity"],
            "confidence": analysis["confidence"],
            "response_speed": response_speed,
            "ui_color": ui_color,
            "emotion_history": analysis["emotion_history"],
            "normal_response": normal_response,
            "emotion_based_response": emotion_response
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route("/reset", methods=["POST"])
def reset_history():
    try:
        emotion_analyzer.reset_history()
        return jsonify({
            "status": "success",
            "message": "Emotion history reset"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to reset history",
            "details": str(e)
        }), 500


# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    print(f"Starting Emotion-Aware Chatbot API on port {port}...")
    print(f"Debug mode: {debug}")

    app.run(host="0.0.0.0", port=port, debug=debug)