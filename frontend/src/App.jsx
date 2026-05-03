import { useState, useRef, useEffect } from "react";

// ✨ DYNAMIC EMOTION ANIMATIONS
const emotionAnimationStyles = `
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  @keyframes fadeInOut {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
  }

  @keyframes flash {
    0%, 50%, 100% { background-color: rgba(245, 158, 11, 0.2); }
    25%, 75% { background-color: rgba(245, 158, 11, 0.5); }
  }

  .emotion-angry {
    animation: shake 0.6s infinite;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.6), inset 0 0 20px rgba(239, 68, 68, 0.3);
  }

  .emotion-sad {
    animation: fadeInOut 3s infinite ease-in-out;
    opacity: 0.85;
  }

  .emotion-happy {
    animation: bounce 1.5s infinite ease-in-out;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(16, 185, 129, 0.1)) !important;
  }

  .emotion-urgent {
    animation: flash 0.8s infinite;
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.8), inset 0 0 20px rgba(245, 158, 11, 0.4);
  }

  .emotion-neutral {
    transition: all 0.3s ease;
  }

  .confidence-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
  }

  .confidence-bar-fill {
    flex: 1;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
  }

  .confidence-bar-inner {
    height: 100%;
    border-radius: 2px;
    transition: width 0.4s ease;
  }

  @keyframes typing {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
  }

  .typing-animation {
    animation: typing 1.2s infinite;
    font-style: italic;
  }
`;

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [emotion, setEmotion] = useState(null);
  const [emotionHistory, setEmotionHistory] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [emotionData, setEmotionData] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [showEmotionCard, setShowEmotionCard] = useState(true);
  const messagesEndRef = useRef(null);
  const menuRef = useRef(null);
  const chatContainerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const getEmotionEmoji = (emotion) => {
    const emojis = {
      Happy: "😊",
      Sad: "😢",
      Angry: "😠",
      Neutral: "😐",
      Urgent: "⚡",
    };
    return emojis[emotion] || "🤖";
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      Happy: "#10b981",
      Sad: "#3b82f6",
      Angry: "#ef4444",
      Neutral: "#9ca3af",
      Urgent: "#f59e0b",
    };
    return colors[emotion] || "#6366f1";
  };

  const getEmotionAnimationClass = (emotion) => {
    const animations = {
      Happy: "emotion-happy",
      Sad: "emotion-sad",
      Angry: "emotion-angry",
      Neutral: "emotion-neutral",
      Urgent: "emotion-urgent",
    };
    return animations[emotion] || "emotion-neutral";
  };

  const parseConfidence = (confidenceStr) => {
    return parseInt(confidenceStr) || 0;
  };

  const getTypingDelay = (emotion) => {
    // Returns delay in milliseconds before showing response
    const delays = {
      Urgent: 300,      // Instant - quick response
      Angry: 800,       // Fast but aggressive
      Happy: 1200,      // Normal medium speed
      Sad: 2000,        // Slow and thoughtful
      Neutral: 1200,    // Normal speed
    };
    return delays[emotion] || 1200;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = {
      text: input,
      sender: "user",
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError("");
    setIsTyping(true);

    // Add typing indicator immediately
    const typingMsg = {
      text: "💭",
      sender: "bot",
      isTyping: true,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, typingMsg]);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: input,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Server error");
      }

      // Get emotion for typing delay
      const detectedEmotion = data.emotion;
      const typingDelay = getTypingDelay(detectedEmotion);

      // Wait for emotion-based typing delay
      await new Promise((resolve) => setTimeout(resolve, typingDelay));

      // Create actual response message
      const botMsg = {
        text: data.emotion_based_response,
        sender: "bot",
        emotion: data.emotion,
        intensity: data.intensity,
        confidence: data.confidence,
        isTyping: false,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      // Replace typing indicator with actual message
      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.isTyping);
        return [...filtered, botMsg];
      });

      setEmotion(data.emotion);
      setEmotionHistory(data.emotion_history);
      setEmotionData(data);

    } catch (err) {
      console.error("Error:", err);
      setError("Failed to connect. Backend might be offline.");
      const errorMsg = {
        text: "❌ " + err.message,
        sender: "error",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      // Remove typing indicator and add error
      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.isTyping);
        return [...filtered, errorMsg];
      });
    }

    setInput("");
    setLoading(false);
    setIsTyping(false);
  };

  const clearChat = () => {
    setMessages([]);
    setEmotionHistory([]);
    setEmotion(null);
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      {/* Add Dynamic Animation Styles */}
      <style>{emotionAnimationStyles}</style>
      
      {/* Main Container */}
      <div className="w-full max-w-5xl">
        {/* Header with Hamburger Menu */}
        <div className="flex justify-between items-start mb-8 relative">
          <div className="text-left flex-1">
            <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 mb-2">
              ✨ Emotion AI
            </h1>
            <p className="text-gray-400 text-lg">
              Intelligent Emotional Response Chatbot
            </p>
          </div>

          {/* Current Emotion Display - With Animation & Scroll Hide */}
          {showEmotionCard && (
            <div
              className={`bg-gradient-to-br backdrop-blur-xl border rounded-2xl p-4 ml-4 shadow-xl h-fit transition-all duration-300 ${getEmotionAnimationClass(
                emotion
              )}`}
              style={{
                background: `linear-gradient(135deg, ${getEmotionColor(
                  emotion
                )}20, ${getEmotionColor(emotion)}10)`,
                borderColor: `${getEmotionColor(emotion)}50`,
                minWidth: "180px",
              }}
            >
            <p className="text-gray-400 text-xs font-semibold mb-2 uppercase tracking-wider">
              Current Emotion
            </p>
            <div className="flex items-center gap-2">
              <div className="text-3xl">{getEmotionEmoji(emotion)}</div>
              <div className="flex-1">
                <p
                  className="text-lg font-bold"
                  style={{ color: getEmotionColor(emotion) }}
                >
                  {emotion || "Neutral"}
                </p>
                {emotionData && (
                  <div className="text-xs text-gray-400 space-y-1">
                    <div>Intensity: <span className="font-semibold text-gray-200">{emotionData.intensity}</span></div>
                    
                    {/* Confidence Visualization */}
                    <div className="confidence-bar">
                      <span>Confidence:</span>
                      <div className="confidence-bar-fill">
                        <div
                          className="confidence-bar-inner"
                          style={{
                            width: `${parseConfidence(emotionData.confidence)}%`,
                            backgroundColor: getEmotionColor(emotion),
                            opacity: 0.8,
                          }}
                        />
                      </div>
                      <span className="font-semibold text-gray-200">{emotionData.confidence}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
            </div>
          )}

          {/* Hamburger Menu */}
          <div className="relative ml-4" ref={menuRef}>
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-gray-400 hover:text-white text-3xl p-2 transition-colors"
              title="Toggle menu"
            >
              ≡
            </button>

            {/* Dropdown Menu */}
            {menuOpen && (
              <div className="absolute right-0 top-12 bg-slate-800/95 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-4 shadow-2xl w-64 z-50">
                {/* Emotion History */}
                <div>
                  <p className="text-gray-400 text-xs font-semibold mb-3 uppercase tracking-wider">
                    📊 History
                  </p>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {emotionHistory.length === 0 ? (
                      <p className="text-gray-500 text-sm">No emotions yet</p>
                    ) : (
                      emotionHistory.map((emo, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 bg-slate-700/50 px-3 py-2 rounded-lg hover:bg-slate-700/70 transition-colors"
                        >
                          <span className="text-lg">{getEmotionEmoji(emo)}</span>
                          <span className="text-sm text-gray-300">{emo}</span>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Clear Chat Button */}
                {messages.length > 0 && (
                  <button
                    onClick={() => {
                      clearChat();
                      setMenuOpen(false);
                    }}
                    className="w-full mt-4 bg-red-900/50 hover:bg-red-900/70 text-red-200 font-semibold py-2 rounded-lg transition-all text-sm"
                  >
                    Clear Chat
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Main Content - Single Column Layout */}
        <div>
          {/* Chat Messages */}
          <div ref={chatContainerRef} className="bg-gradient-to-b from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-purple-500/30 rounded-2xl h-[500px] overflow-y-auto p-6 mb-4 shadow-2xl">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="text-6xl mb-4">💬</div>
                  <p className="text-gray-400 text-lg">
                    Start a conversation...
                  </p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`mb-4 flex ${
                      msg.sender === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-3 rounded-xl ${
                        msg.sender === "user"
                          ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-br-none"
                          : msg.sender === "error"
                          ? "bg-red-900/50 border border-red-500 text-red-200 rounded-bl-none"
                          : "bg-gray-700/50 border border-gray-600 text-gray-100 rounded-bl-none"
                      }`}
                    >
                      <p className={`text-sm ${msg.isTyping ? "typing-animation text-green-300" : ""}`}>
                        {msg.text}
                      </p>
                      {msg.emotion && (
                        <div className="mt-2 pt-2 border-t border-gray-500 text-xs opacity-80">
                          <span>
                            {getEmotionEmoji(msg.emotion)} {msg.emotion}
                          </span>
                          <span className="ml-2">
                            · {msg.intensity} · {msg.confidence}
                          </span>
                        </div>
                      )}
                      <div className="text-xs opacity-60 mt-1">
                        {msg.timestamp}
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-900/30 border border-red-500 text-red-200 p-3 rounded-lg mb-4 text-sm">
              ⚠️ {error}
            </div>
          )}

          {/* Input Section */}
          <div className="bg-gradient-to-r from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-4 shadow-2xl">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Type your message here..."
                disabled={loading}
                className="flex-1 bg-slate-700/50 border border-purple-400/30 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-500/50 transition-all disabled:opacity-50"
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold px-6 py-3 rounded-xl transition-all shadow-lg hover:shadow-xl active:scale-95"
              >
                {loading ? "..." : "Send"}
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>🚀 Powered by OpenRouter & Advanced Emotion Detection</p>
        </div>
      </div>
    </div>
  );
}

export default App;