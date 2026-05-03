"""
QUICK START GUIDE
Emotion-Aware Chatbot Backend

This guide will get you up and running in 5 minutes.
"""


print("""
╔════════════════════════════════════════════════════════════════╗
║                      QUICK START GUIDE                         ║
║                 Emotion-Aware Chatbot Backend                  ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Setup Python Environment
────────────────────────────────────────────────────────────────
Windows:
  python -m venv venv
  venv\\Scripts\\activate

macOS/Linux:
  python3 -m venv venv
  source venv/bin/activate


STEP 2: Install Dependencies
────────────────────────────────────────────────────────────────
pip install -r requirements.txt


STEP 3: Add Your Anthropic API Key
────────────────────────────────────────────────────────────────
1. Open file: .env
2. Replace with your API key from console.anthropic.com:
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
3. Save file


STEP 4: Test Emotion Detection (Optional)
────────────────────────────────────────────────────────────────
python test_emotion_analyzer.py

This tests emotion detection WITHOUT needing the API key.


STEP 5: Run the Backend
────────────────────────────────────────────────────────────────
python app.py

You should see:
  Starting Emotion-Aware Chatbot API on port 5000...
  Available endpoints: GET /, GET /health, POST /chat, POST /reset


STEP 6: Test the API (in another terminal)
────────────────────────────────────────────────────────────────
Using Python:
  python test_api.py

Using cURL:
  curl -X POST http://localhost:5000/chat \\
    -H "Content-Type: application/json" \\
    -d '{"user_input": "I am so happy!"}'


STEP 7: Connect Your Frontend
────────────────────────────────────────────────────────────────
Update your React/Vue frontend to call:
  POST http://localhost:5000/chat
  Body: {"user_input": "user message"}

See README.md for React example code.


COMMON QUESTIONS
════════════════════════════════════════════════════════════════

Q: Where do I get the Anthropic API key?
A: https://console.anthropic.com/ (requires Claude API account)

Q: Can I test without the API key?
A: Yes! Run: python test_emotion_analyzer.py

Q: Port 5000 is already in use, what do I do?
A: Edit .env and change PORT=5001
   Or: PORT=5001 python app.py

Q: It says "Module not found"?
A: Make sure your venv is activated and dependencies installed:
   pip install -r requirements.txt

Q: How do I integrate with React?
A: See React example in README.md, or check cors_config.py


FILE STRUCTURE
════════════════════════════════════════════════════════════════
app.py                    ← Main Flask app (run this!)
emotion_analyzer.py       ← Emotion detection logic
claude_client.py          ← Claude API integration
requirements.txt          ← Python packages
.env                      ← API key (add yours here)
.env.example              ← Template
README.md                 ← Full documentation
test_emotion_analyzer.py  ← Test emotion detection
cors_config.py            ← CORS for frontend (optional)


ENDPOINTS
════════════════════════════════════════════════════════════════
GET  /                    - Service info
GET  /health              - Health check
POST /chat                - Main endpoint (send message)
POST /reset               - Clear emotion history


EXAMPLE REQUEST
════════════════════════════════════════════════════════════════
curl -X POST http://localhost:5000/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_input": "I'm really frustrated right now!"
  }'

EXAMPLE RESPONSE
════════════════════════════════════════════════════════════════
{
  "emotion": "Angry",
  "intensity": "High",
  "confidence": "88%",
  "response_speed": "MEDIUM",
  "ui_color": "RED",
  "emotion_history": ["Angry"],
  "normal_response": "...",
  "emotion_based_response": "..."
}


NEED HELP?
════════════════════════════════════════════════════════════════
1. Read README.md for complete documentation
2. Check troubleshooting section in README
3. Run test_emotion_analyzer.py to verify setup
4. Check error messages carefully


READY TO START?
════════════════════════════════════════════════════════════════
Terminal 1 (Backend):
  python app.py

Terminal 2 (Test):
  python test_emotion_analyzer.py

or use cURL:
  curl -X POST http://localhost:5000/chat \\
    -H "Content-Type: application/json" \\
    -d '{"user_input": "Hello!"}'


Good luck! 🚀
════════════════════════════════════════════════════════════════
""")
