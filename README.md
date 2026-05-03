# 🎭 Emotion-Aware Chatbot

An intelligent chatbot that **detects user emotions** and **tailors AI responses** based on emotional state using OpenRouter API.

---

## 📁 Project Structure

```
sentimentanalysis/
│
├── 📂 src/                          ← Backend Source Code  
│   ├── server.py                    ← Main Flask server
│   ├── emotion_analyzer.py          ← Emotion detection (CORE)
│   ├── openrouter_client.py         ← OpenRouter API integration
│   ├── cors_config.py               ← CORS configuration
│   └── __init__.py
│
├── 📂 tests/                        ← Test Suite
│   ├── test_api.py                  ← API endpoint tests
│   ├── test_emotion_detection.py    ← Emotion detector tests
│   └── test_contextual_emotion.py   ← Contextual analysis tests
│
├── 📂 docs/                         ← Documentation
│   ├── README.md                    ← Full project documentation
│   └── EMOTION_RESPONSE_STYLES.md   ← Response examples by emotion
│
├── 📂 config/                       ← Configuration Files
│   └── .env.example                 ← Template for environment variables
│
├── 📂 frontend/                     ← React UI (3000)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── run.py                           ← ⭐ Start Backend (python run.py)
├── requirements.txt                 ← Python dependencies
├── .env                             ← Environment variables (git ignored)
└── README.md                        ← This file
```

---

## 🚀 Quick Start

### 1️⃣ Setup Backend

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example .env
# Edit .env and add: OPENROUTER_API_KEY=your-key-here
```

### 2️⃣ Run Backend

```bash
python run.py
```
Backend runs on: **http://localhost:5000**

### 3️⃣ Run Frontend

```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: **http://localhost:3000**

---

## 📊 Key Components

### Backend (src/)

| File | Purpose |
|------|---------|
| **server.py** | Flask API server with routes (/chat, /health, /reset) |
| **emotion_analyzer.py** | Detects emotion from text using contextual analysis |
| **openrouter_client.py** | Integrates with OpenRouter API for responses |
| **cors_config.py** | Enables cross-origin requests |

### Frontend (frontend/)

- React app with real-time emotion visualization
- Beauty color-coded emotion badges
- Emotion history tracking
- Chat interface with timestamp

### Tests (tests/)

```bash
# Run specific tests
python tests/test_api.py
python tests/test_emotion_detection.py
python tests/test_contextual_emotion.py
```

---

## 🎯 How It Works

```
User Input
    ↓
[src/emotion_analyzer.py] ← Detects: Urgent, Angry, Sad, Happy, Neutral
    ↓
Emotion + Intensity + Confidence
    ↓
[src/openrouter_client.py] ← Selects emotion-specific system prompt
    ↓
AI Response (tailored to emotion)
    ↓
Frontend Display (color-coded badge + response)
```

### Emotion Detection

- **Weighted Keywords**: Strong (2 pts), Medium (1.5 pts), Weak (1 pt)
- **Negation Handling**: "didn't make good" → SAD (failed positive action)
- **Contextual Analysis**: Reads full sentences, understands meaning
- **Threshold**: 1.0 points minimum to detect emotion

### Response Adaptation

| Emotion | Max Tokens | Style | Example |
|---------|-----------|-------|---------|
| **URGENT** | 120 | 1-2 sentences, action-focused | "Call 911 now" |
| **ANGRY** | 180 | Empathetic, solutions-oriented | "I understand your frustration..." |
| **SAD** | 200 | Warm, supportive, encouraging | "I'm here to help you..." |
| **HAPPY** | 200 | Enthusiastic, celebratory | "That's fantastic! Congratulations!" |
| **NEUTRAL** | 250 | Structured, informative | "Here's the information you need..." |

---

## 🔌 API Endpoints

### POST /chat
Send message and get emotion-aware response

**Request:**
```json
{
  "user_input": "I'm so happy!"
}
```

**Response:**
```json
{
  "emotion": "Happy",
  "intensity": "Medium",
  "confidence": "85%",
  "response_speed": "MEDIUM",
  "ui_color": "GREEN",
  "normal_response": "That's wonderful!",
  "emotion_based_response": "That's fantastic! Tell me more!",
  "emotion_history": ["Neutral", "Happy"]
}
```

### GET /health
Check API status

### POST /reset
Reset emotion history

---

## 📖 Documentation

- **Full Documentation**: See [docs/README.md](docs/README.md)
- **Response Examples**: See [docs/EMOTION_RESPONSE_STYLES.md](docs/EMOTION_RESPONSE_STYLES.md)

---

## ⚙️ Configuration

### Environment Variables

```
OPENROUTER_API_KEY=your-api-key      ← Get from https://openrouter.ai
SECRET_KEY=dev-secret-key             ← Change in production
DEBUG=False                            ← Set to True for development
PORT=5000                              ← Server port
```

### Requirements

- Python 3.8+
- Node.js 14+
- OpenRouter API key (free)

---

## 🧪 Testing

```bash
# Test emotion detection
python tests/test_emotion_detection.py

# Test API endpoints
python tests/test_api.py

# Test contextual analysis
python tests/test_contextual_emotion.py
```

---

## 💡 Usage Examples

### Example 1: Urgent Query
```
Input:  "HELP! Emergency now!"
Emotion: URGENT (95%)
Speed: FAST
Output: "1-2 crisp sentences with immediate action"
```

### Example 2: Sad Query
```
Input:  "I didn't make a good food today"
Emotion: SAD (75%) ← Detected as failed positive action
Speed: SLOW
Output: "Warm, supportive, encouraging response (4-6 sentences)"
```

### Example 3: Happy Query
```
Input:  "I just got promoted!"
Emotion: HAPPY (85%)
Speed: MEDIUM
Output: "Enthusiastic celebration and encouragement"
```

---

## 🚦 Status Indicators

```
Speed:       FAST, MEDIUM, SLOW, NORMAL
Confidence:  40% - 100% (certainty in emotion detection)
Intensity:   LOW, MEDIUM, HIGH (emotional strength)
Color:       RED, ORANGE, BLUE, GREEN, GRAY
```

---

## 🔧 Development

### Adding New Emotion

1. Add keywords to `src/emotion_analyzer.py`
2. Add system prompt to `src/openrouter_client.py`
3. Add color mapping in UI
4. Test with `tests/test_emotion_detection.py`

### Changing Response Style

Edit the system prompts in `src/openrouter_client.py` for each emotion.

---

## 📚 Learn More

- [Full Backend Documentation](docs/README.md)
- [Emotion Response Styles](docs/EMOTION_RESPONSE_STYLES.md)
- [OpenRouter Docs](https://openrouter.ai)

---

## 🎓 Project Features

✅ Real-time emotion detection  
✅ Contextual understanding (negations, contradictions)  
✅ Emotion-aware response generation  
✅ Dynamic token limits (crisp for urgent, descriptive for sad)  
✅ Beautiful UI with color-coded badges  
✅ Emotion history tracking  
✅ API-based architecture  
✅ Tests for all components  

---

## 📞 Support

- Check `docs/README.md` for detailed documentation
- Run tests to verify setup
- Enable `DEBUG=True` in `.env` for verbose logs

---

**Made with ❤️ - Emotion-Aware Chatbot**  
Detect feelings. Respond with empathy. 🎭
# Emotion-Aware Chatbot 🎭

An intelligent chatbot that **detects user emotions** from text and **tailors AI responses** based on emotional state.

## ⚡ Key Features

✅ **Real-time Emotion Detection** - Analyzes text for Urgent, Angry, Sad, Happy, or Neutral  
✅ **Contextual Understanding** - Reads full prompts, understands negations and contradictions  
✅ **Emotion-Based Responses** - AI adapts tone, length, and approach based on emotion  
✅ **Dynamic Response Speed** - URGENT queries get 1-2 sentence answers, SAD gets supportive responses  
✅ **Beautiful UI** - Real-time emotion visualization with color-coded badges  
✅ **Emotion History** - Tracks user emotions across conversation  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- OpenRouter API key (free - get from https://openrouter.ai)

### Installation

```bash
# 1. Clone and navigate
cd sentimentanalysis

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Copy .env.example to .env and add your OpenRouter API key
cp .env.example .env
# Edit .env and add: OPENROUTER_API_KEY=your-key-here
```

### Run Backend
```bash
python app.py
# Server runs on http://localhost:5000
```

### Run Frontend
```bash
cd frontend
npm install
npm run dev
# UI runs on http://localhost:3000
```

---

## 📊 How It Works

```
User Input → Emotion Analyzer → System Prompt Selection → AI Response → Formatted Output
   "Help!"       URGENT (95%)      IMMEDIATE ACTION         1-2 sentences    🔴 URGENT
 "I'm sad"        SAD (80%)         WARMTH & SUPPORT         Encouraging      🔵 SAD
 "So happy!"      HAPPY (85%)       CELEBRATE & MATCH         Enthusiastic     🟢 HAPPY
  "I'm mad"       ANGRY (75%)       EMPATHY & SOLUTIONS       Solutions        🟠 ANGRY
  "hello"        NEUTRAL (60%)      INFORMATIVE              Structured       ⚫ NEUTRAL
```

### Emotion Detection

The system uses **weighted contextual analysis**:
- **Strong keywords** (2 pts): "emergency", "furious", "suicidal", "fantastic"
- **Medium keywords** (1.5 pts): "good", "frustrated", "unhappy"  
- **Weak keywords** (1 pt): Supporting context words
- **Negation handling**: "I didn't make good food" → SAD (failed positive action)
- **Contradiction patterns**: "but", "however" → adjusts sentiment

### Response Generation

Each emotion triggers a unique system prompt:

| Emotion | Style | Length | Tone |
|---------|-------|--------|------|
| **URGENT** | 1-2 sentences max | **CRISP** | Direct, action-focused |
| **ANGRY** | 3-5 sentences | Problem-solving | Calm, empathetic |
| **SAD** | 4-6 sentences | Supportive | Warm, encouraging |
| **HAPPY** | 4-6 sentences | Celebratory | Enthusiastic, positive |
| **NEUTRAL** | 5-8 sentences | Structured | Clear, informative |

---

## 📁 Project Structure

```
sentimentanalysis/
├── app.py                      # Flask backend & API routes
├── emotion_analyzer.py         # Emotion detection engine (CORE)
├── claude_client.py            # OpenRouter API integration
├── cors_config.py              # CORS configuration
├── requirements.txt            # Python dependencies
├── .env                        # API key configuration
├── README.md                   # This file
├── EMOTION_RESPONSE_STYLES.md  # Response style examples
├── test_api.py                 # API testing script
├── test_emotion_analyzer.py    # Emotion detector tests
└── frontend/                   # React UI
    ├── src/
    │   ├── App.jsx            # Main app component
    │   ├── components/
    │   │   ├── ChatWindow.jsx
    │   │   ├── Message.jsx
    │   │   ├── EmotionIndicator.jsx
    │   │   ├── InputBox.jsx
    │   │   └── Header.jsx
    │   └── main.jsx
    └── package.json
```

---

## 🔧 Configuration

### Environment Variables (.env)

```
OPENROUTER_API_KEY=sk-or-your-key-here
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=False
PORT=5000
```

---

## 📚 API Endpoints

### POST /chat
Send a message and get emotion-aware response

**Request:**
```json
{
  "user_input": "I'm so happy!"
}
```

**Response:**
```json
{
  "emotion": "Happy",
  "intensity": "Medium",
  "confidence": "85%",
  "response_speed": "MEDIUM",
  "ui_color": "GREEN",
  "normal_response": "That's wonderful! What made your day?",
  "emotion_based_response": "That's fantastic! I love your energy! 🎉 Tell me more about what's making you so happy!",
  "emotion_history": ["Neutral", "Happy"],
  "timestamp": "2024-04-10T19:43:00"
}
```

### GET /health
Check API status

### POST /reset
Reset emotion history

---

## 🧪 Testing

```bash
# Test emotion detection
python test_emotion_analyzer.py

# Test API endpoints
python test_api.py

# Test new contextual analyzer
python test_emotion_new.py
```

---

## 🎨 Frontend Features

- **Real-time Emotion Display** with emoji indicators
- **Color-coded Messages** (Red=Angry, Blue=Sad, Green=Happy, Orange=Urgent, Gray=Neutral)
- **Interactive Emotion History** showing detected emotions
- **Chat Window** with timestamp and metadata
- **Clear Chat** button to reset conversation
- **Responsive Design** for desktop and tablet

---

## 🔌 API Details

**Model**: OpenRouter (using auto-selection for free models)  
**Max Tokens**: Dynamic based on emotion (120-250)  
**Response Time**: 1-3 seconds typically

---

## 📝 Example Conversations

### Example 1: Urgent Situation
```
User: "HELP! Emergency now!"
Detected: URGENT (95% confidence)
AI Response: "Call emergency services immediately. What's happening?"
Length: 1-2 sentences (CRISP)
Speed: FAST
```

### Example 2: Sad Situation
```
User: "I didn't make a good food today"
Detected: SAD (75% confidence) 
AI Response: "I understand - cooking can be frustrating! Don't worry, 
even great chefs have off days. You're learning, and that's what matters. 
What went wrong? Maybe I can help troubleshoot!"
Length: 4-6 sentences (SUPPORTIVE)
Speed: SLOW
```

### Example 3: Happy Situation
```
User: "I just got promoted!"
Detected: HAPPY (90% confidence)
AI Response: "That's absolutely amazing! Congratulations! 🎉 
Your hard work clearly paid off. You deserve this achievement!"
Length: 4-6 sentences (CELEBRATORY)
Speed: MEDIUM
```

---

## 🎯 Project Core

The **heart** of this project is the **emotion-based response generation**:

1. **Detect emotion** from user's text accurately
2. **Understand context** (negations, contradictions, failed positives)
3. **Tailor response** based on emotion (different system prompts)
4. **Adapt length** based on urgency (crisp for urgent, longer for supportive)
5. **Display metadata** so user sees their detected emotion

**Result**: Same question gets different answers based on how it's asked emotionally.

---

## 📞 Support

For issues or questions, check:
- `EMOTION_RESPONSE_STYLES.md` - Response style examples
- `test_api.py` - API usage examples
- Backend logs - Run with `DEBUG=True` for verbose output

---

## 🚀 Future Enhancements

- [ ] Multi-language emotion detection
- [ ] User preferences for response style
- [ ] Custom emotion categories
- [ ] Conversation context retention across sessions
- [ ] ML-based sentiment analysis integration

---

**Made with ❤️ - Emotion-Aware Chatbot**
  GET  /
  GET  /health
  POST /chat
  POST /reset
```

### Access API

Open browser to: `http://localhost:5000/`

---

## API Endpoints

### 1. Home Endpoint
**GET** `/`

Returns service information and available endpoints.

**Response:**
```json
{
  "status": "running",
  "service": "Emotion-Aware Chatbot API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

### 2. Health Check
**GET** `/health`

Quick health status check.

**Response:**
```json
{
  "status": "healthy",
  "claude_api_available": true
}
```

---

### 3. Chat Endpoint (Main)
**POST** `/chat`

Send user input and receive emotion-aware response.

**Request:**
```json
{
  "user_input": "I'm so frustrated with this issue!"
}
```

**Response:**
```json
{
  "emotion": "Angry",
  "intensity": "High",
  "confidence": "92%",
  "response_speed": "MEDIUM",
  "ui_color": "RED",
  "emotion_history": ["Angry"],
  "normal_response": "I understand you're facing an issue. Could you provide more details about what's happening so I can help you find a solution?",
  "emotion_based_response": "I can see this is really frustrating for you. Let's work through this together. First, can you walk me through what happened? I'm here to help find a resolution."
}
```

**Request Format:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Your message here"}'
```

---

### 4. Reset Emotion History
**POST** `/reset`

Clear the emotion history.

**Response:**
```json
{
  "status": "success",
  "message": "Emotion history reset"
}
```

---

## Response Format (Strict)

All responses follow this exact structure:

```json
{
  "emotion": "<Urgent|Angry|Sad|Happy|Neutral>",
  "intensity": "<Low|Medium|High>",
  "confidence": "<0-100%>",
  "response_speed": "<FAST|MEDIUM|SLOW|NORMAL>",
  "ui_color": "<RED|BLUE|GREEN|ORANGE|GRAY>",
  "emotion_history": ["emotion1", "emotion2", ...],
  "normal_response": "<standard AI response>",
  "emotion_based_response": "<adaptive response>"
}
```

---

## Emotion Detection Rules

### 1. Urgent
- **Keywords**: "urgent", "emergency", "help", "asap", "immediately", "critical"
- **Response Speed**: FAST
- **UI Color**: ORANGE
- **Response Style**: Very short, direct, action-focused

### 2. Angry
- **Keywords**: "angry", "furious", "hate", "frustrated", "disappointed", "fed up"
- **Response Speed**: MEDIUM
- **UI Color**: RED
- **Response Style**: Calm, respectful, empathetic, solution-oriented

### 3. Sad
- **Keywords**: "sad", "depressed", "heartbroken", "devastated", "lonely", "hopeless"
- **Response Speed**: SLOW
- **UI Color**: BLUE
- **Response Style**: Supportive, gentle, encouraging, understanding

### 4. Happy
- **Keywords**: "happy", "excited", "wonderful", "love", "awesome", "grateful"
- **Response Speed**: MEDIUM
- **UI Color**: GREEN
- **Response Style**: Energetic, friendly, warm, enthusiastic

### 5. Neutral
- **Keywords**: General questions with no emotional markers
- **Response Speed**: NORMAL
- **UI Color**: GRAY
- **Response Style**: Clear, structured, professional, balanced

---

## Intensity Detection

Intensity is calculated by analyzing:

1. **Punctuation**
   - Multiple exclamation marks: `!!!` (+3 points)
   - Multiple question marks: `???` (+2 points)
   - Caps lock: `IMPORTANT` (+2 points)

2. **Word Emphasis**
   - Intensifiers: "very", "extremely", "absolutely", "really" (+1 point)

3. **Emotional Context**
   - Urgent/Angry emotions: +1 point
   - Sad emotion: +0.5 points

**Scoring:**
- 4+ points = **High**
- 2-3 points = **Medium**
- 0-1 points = **Low**

---

## Example Usage: Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def send_message(user_input):
    """Send message to chatbot"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"user_input": user_input},
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# Test cases
test_inputs = [
    "I'm so happy today! 😊😊😊",
    "URGENT! I need help immediately!!!",
    "I'm feeling really sad and alone",
    "This is absolutely frustrating!",
    "What's the weather like?"
]

for user_input in test_inputs:
    print(f"\nUser: {user_input}")
    result = send_message(user_input)
    print(f"Emotion: {result['emotion']} ({result['confidence']})")
    print(f"Intensity: {result['intensity']}")
    print(f"UI Color: {result['ui_color']}")
    print(f"Normal Response: {result['normal_response'][:100]}...")
    print(f"Emotion Response: {result['emotion_based_response'][:100]}...")
```

---

## Example Usage: cURL

```bash
# Test Urgent emotion
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "URGENT! I need help immediately!!!"}'

# Test Happy emotion
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I am so excited and happy!"}'

# Test Angry emotion
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "This is absolutely frustrating!"}'

# Test Sad emotion
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I feel so alone and broken"}'

# Reset history
curl -X POST http://localhost:5000/reset
```

---

## Frontend Integration (React Example)

```jsx
import React, { useState } from 'react';

const ChatBot = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: input })
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
    }

    setLoading(false);
    setInput('');
  };

  const getColorClass = (color) => {
    const colorMap = {
      RED: 'bg-red-100 border-red-500',
      BLUE: 'bg-blue-100 border-blue-500',
      GREEN: 'bg-green-100 border-green-500',
      ORANGE: 'bg-orange-100 border-orange-500',
      GRAY: 'bg-gray-100 border-gray-500'
    };
    return colorMap[color] || colorMap.GRAY;
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <form onSubmit={sendMessage} className="mb-6">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="w-full px-4 py-2 border rounded"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="mt-2 px-6 py-2 bg-blue-500 text-white rounded"
        >
          {loading ? 'Loading...' : 'Send'}
        </button>
      </form>

      {response && (
        <div className={`p-4 rounded border-2 ${getColorClass(response.ui_color)}`}>
          <h3>Emotion: {response.emotion}</h3>
          <p>Intensity: {response.intensity}</p>
          <p>Confidence: {response.confidence}</p>
          <p>Speed: {response.response_speed}</p>
          
          <div className="mt-4">
            <h4 className="font-bold">Normal Response:</h4>
            <p className="text-gray-600">{response.normal_response}</p>
          </div>

          <div className="mt-4">
            <h4 className="font-bold">Emotion-Based Response:</h4>
            <p className="text-gray-800">{response.emotion_based_response}</p>
          </div>

          <div className="mt-4">
            <h4 className="font-bold">Emotion History:</h4>
            <p className="text-gray-600">{response.emotion_history.join(' → ')}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBot;
```

---

## Project Structure

```
sentimentanalysis/
├── app.py                    # Main Flask application
├── emotion_analyzer.py       # Emotion detection logic
├── claude_client.py          # Claude API integration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .env                      # Environment variables (create from .env.example)
└── README.md                 # This file
```

---

## Error Handling

The API includes comprehensive error handling:

### Missing Input
```json
{
  "error": "Missing required field: user_input"
}
```

### Empty Input
```json
{
  "error": "user_input cannot be empty"
}
```

### Input Too Large
```json
{
  "error": "user_input exceeds maximum length of 10000 characters"
}
```

### API Errors
```json
{
  "error": "Internal server error",
  "details": "Error message here"
}
```

---

## Configuration

Edit `.env` to customize:

```env
# API Configuration
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Flask Settings
SECRET_KEY=your-secret-key-here
DEBUG=False          # Set to True for development
PORT=5000

# Optional
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## Performance Notes

- Average response time: 2-5 seconds (depends on Claude API)
- Emotion detection: < 100ms
- Max input length: 10,000 characters
- Emotion history limited to session (clears on `/reset`)

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
# Check .env file exists
ls .env

# Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" >> .env
```

### Port Already in Use
```bash
# Change PORT in .env or run on different port
PORT=5001 python app.py
```

### ModuleNotFoundError
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### Claude API Errors
- Check your API key is valid
- Verify rate limits haven't been exceeded
- Check Anthropic API status

---

## Testing

Test all endpoints with the provided examples above.

Run multiple messages to see emotion history building.

Reset history with `/reset` endpoint between test sessions.

---

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py emotion_analyzer.py claude_client.py .

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t emotion-chatbot .
docker run -p 5000:5000 -e ANTHROPIC_API_KEY=sk-ant-xxxxx emotion-chatbot
```

---

## License

This project is provided as-is for educational and business use.

---

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure ANTHROPIC_API_KEY is set correctly
4. Review error messages in the API response

---

**Version**: 1.0.0  
**Last Updated**: April 2026
