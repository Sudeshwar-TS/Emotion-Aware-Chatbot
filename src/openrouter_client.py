"""
OpenRouter API Integration Module
Handles communication with OpenRouter (FREE models) for response generation
"""

import os
import requests


class ClaudeResponseGenerator:
    """Generates responses using OpenRouter API"""

    def __init__(self, api_key: str = None):
        """
        Initialize OpenRouter API client

        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

        # ✅ OpenRouter endpoint
        self.url = "https://openrouter.ai/api/v1/chat/completions"

        # ✅ FREE model - Using auto mode (manually selects best free model)
        self.model = "openrouter/auto"

    def generate_normal_response(self, user_input: str) -> str:
        """Generate a standard AI response"""

        system_prompt = """You are a helpful AI assistant. Keep responses concise and clear.
Provide practical, well-structured answers with good spacing.
Use bullet points for lists. Be conversational but professional."""

        return self._call_api(system_prompt, user_input)

    def generate_emotion_based_response(
        self, user_input: str, emotion: str, intensity: str
    ) -> str:
        """Generate emotion-aware response tailored to user's emotional state"""

        # ✅ DIFFERENT SYSTEM PROMPTS FOR EACH EMOTION WITH SPECIFIC STYLE GUIDANCE
        system_prompts = {
            "Urgent": """URGENT/EMERGENCY MODE - CRITICAL INSTRUCTIONS:
You MUST respond with ABSOLUTE BREVITY and IMMEDIATE ACTION.
- Maximum 1-2 sentences. NO exceptions.
- ONLY provide the solution or action needed right now.
- NO pleasantries, NO explanations, NO background info.
- Be direct. Be Clear. Be Fast.
Example: "Call 911 now" or "Do X immediately" - that's it.""",
            
            "Angry": """ANGRY/FRUSTRATED USER - RESPOND WITH EMPATHY AND SOLUTIONS:
The user is frustrated. Your response must:
- FIRST: Acknowledge their frustration clearly ("I understand you're frustrated")
- SECOND: Validate their feelings (don't dismiss them)
- THIRD: Provide 1-2 practical solutions
- Tone: Calm, respectful, solution-focused
- Length: Brief but substantive (3-5 sentences max)
NO aggression, NO negativity, ONLY positive direction.""",
            
            "Sad": """SAD/DEPRESSED USER - RESPOND WITH WARMTH AND HOPE:
The user is sad/down. Your response must:
- Show genuine understanding and empathy
- Be warm, gentle, and supportive
- Offer perspective or hope (not toxic positivity)
- Suggest one helpful action they could take
- Tone: Caring, understanding, encouraging
- Length: Warm but concise (4-6 sentences)
Focus on: Understanding → Support → Hope""",
            
            "Happy": """HAPPY/EXCITED USER - MATCH THEIR JOY AND CELEBRATE:
The user is happy/excited! Your response must:
- Match their positive energy and enthusiasm
- Celebrate with them genuinely
- Amplify their joy (not dampen it)
- Be encouraging and uplifting
- Tone: Enthusiastic, positive, energetic
- Length: Can be a bit longer (4-6 sentences)
Focus on: Celebration → Encouragement → Positivity""",
            
            "Neutral": """NEUTRAL USER - RESPOND WITH CLARITY AND STRUCTURE:
The user is asking neutrally. Your response must:
- Provide accurate, clear information
- Organize using structure (bullets, sections if needed)
- Be professional but conversational
- Anticipate follow-up questions if relevant
- Tone: Helpful, professional, clear
- Length: Medium length as needed (5-8 sentences or with bullets)
Focus on: Accuracy → Clarity → Structure"""
        }

        system_prompt = system_prompts.get(emotion, system_prompts["Neutral"])
        
        # ✅ DYNAMIC TOKEN LIMITS BASED ON EMOTION (CRISP for URGENT, RICHER for OTHERS)
        max_tokens_map = {
            "Urgent": 80,       # Very crisp - 1 sentence max
            "Angry": 120,       # Short - focused solutions  
            "Sad": 150,         # Medium - supportive
            "Happy": 150,       # Medium - celebratory
            "Neutral": 180      # Normal - structured info
        }
        
        max_tokens = max_tokens_map.get(emotion, 250)
        system_prompt += f"\n\nIntensity Level: {intensity} | Adjust urgency/depth accordingly."

        return self._call_api(system_prompt, user_input, max_tokens)

    def _call_api(self, system_prompt: str, user_input: str, max_tokens: int = 250) -> str:
        """Internal method to call OpenRouter API
        
        Optimized with timeout and fast response handling
        """

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",  # required
                "X-Title": "Emotion Chatbot"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": max_tokens  # ✅ EMOTION-SPECIFIC TOKEN LIMIT
            }

            # ✅ TIMEOUT: 15 seconds max (prevent hanging requests)
            response = requests.post(self.url, headers=headers, json=payload, timeout=15)
            
            # Handle rate limiting
            if response.status_code == 429:
                return "System is busy. Please try again in a moment."

            data = response.json()

            # 🔴 Handle API error properly
            if "error" in data:
                error_msg = data['error'].get('message', 'Unknown error')
                return f"API Error: {error_msg}"

            return data["choices"][0]["message"]["content"].strip()

        except requests.Timeout:
            return "Response took too long. Please try a shorter question."
        except Exception as e:
            return f"Error generating response: {str(e)}"