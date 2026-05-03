"""
Emotion-Aware Chatbot - Main Entry Point
Run this file to start the Flask backend server
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the server
from server import app

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print("\n" + "="*60)
    print("   🎭  EMOTION-AWARE CHATBOT - BACKEND SERVER")
    print("="*60)
    print(f"✅ Starting on http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📁 Source: src/")
    print("   Frontend: http://localhost:3000")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
