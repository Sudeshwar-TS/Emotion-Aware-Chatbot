"""
Optional: CORS Configuration for Frontend Integration
Add this to app.py if you need CORS support for React/Vue frontend

Usage in app.py:
    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
"""

from flask_cors import CORS
import os


def setup_cors(app):
    """
    Setup CORS for the Flask app

    Args:
        app: Flask application instance
    """
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    CORS(
        app,
        resources={
            r"/*": {
                "origins": allowed_origins,
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type"],
                "max_age": 3600
            }
        }
    )
