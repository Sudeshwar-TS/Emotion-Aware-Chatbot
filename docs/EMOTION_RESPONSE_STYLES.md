"""
EMOTION-BASED RESPONSE STYLE COMPARISON
Demonstrates how AI output changes based on detected emotion
"""

# ============================================================================
# EXAMPLE: User asks about a technical problem
# ============================================================================

USER_INPUT = "I need to fix a critical bug in production right now!"

# ╔════════════════════════════════════════════════════════════════════════╗
# ║ EMOTION 1: URGENT (Detected: "critical", "right now")                ║
# ║ Max Tokens: 120 (CRISP - 1-2 sentences maximum)                       ║
# ╚════════════════════════════════════════════════════════════════════════╝

URGENT_SYSTEM_PROMPT = """URGENT/EMERGENCY MODE - CRITICAL INSTRUCTIONS:
You MUST respond with ABSOLUTE BREVITY and IMMEDIATE ACTION.
- Maximum 1-2 sentences. NO exceptions.
- ONLY provide the solution or action needed right now.
- NO pleasantries, NO explanations, NO background info."""

# Expected Output:
URGENT_OUTPUT = """Check the error logs immediately. Rollback the last deployment or apply an emergency patch now."""
# Note: Crisp, direct, 1-2 sentences, action-focused, NO elaboration


# ╔════════════════════════════════════════════════════════════════════════╗
# ║ EMOTION 2: ANGRY (Detected: negative action words, frustration)       ║
# ║ Max Tokens: 180 (FOCUSED - 3-5 sentences, solution-oriented)          ║
# ╚════════════════════════════════════════════════════════════════════════╝

ANGRY_SYSTEM_PROMPT = """ANGRY/FRUSTRATED USER - RESPOND WITH EMPATHY AND SOLUTIONS:
The user is frustrated. Your response must:
- FIRST: Acknowledge their frustration clearly
- SECOND: Validate their feelings
- THIRD: Provide 1-2 practical solutions
- Tone: Calm, respectful, solution-focused"""

# Expected Output:
ANGRY_OUTPUT = """I understand this is frustrating - production bugs are stressful. Let's tackle this together. 
First, check the recent deployments and error logs. If you need immediate relief, you can rollback to the last stable version. 
What details do you need help troubleshooting?"""
# Note: Acknowledges frustration, validates, provides solutions, empathetic


# ╔════════════════════════════════════════════════════════════════════════╗
# ║ EMOTION 3: SAD (Detected: negative outcomes, feelings of failure)     ║
# ║ Max Tokens: 200 (SUPPORTIVE - 4-6 sentences, warm and encouraging)    ║
# ╚════════════════════════════════════════════════════════════════════════╝

SAD_SYSTEM_PROMPT = """SAD/DEPRESSED USER - RESPOND WITH WARMTH AND HOPE:
The user is sad/down. Your response must:
- Show genuine understanding and empathy
- Be warm, gentle, and supportive
- Offer perspective or hope
- Suggest one helpful action they could take"""

# Expected Output:
SAD_OUTPUT = """I understand how frustrating it must feel when production breaks - it's a stressful situation and your concern is completely valid. 
These things happen to every developer, and it's actually an opportunity to strengthen your system. 
You've already shown good instinct by identifying it quickly. Let's work through this together step by step. 
Start with the error logs - what information are you seeing there?"""
# Note: Warm, empathetic, offers hope and perspective, encouraging


# ╔════════════════════════════════════════════════════════════════════════╗
# ║ EMOTION 4: HAPPY (Detected: positive words, excitement)               ║
# ║ Max Tokens: 200 (CELEBRATORY - 4-6 sentences, enthusiastic)           ║
# ╚════════════════════════════════════════════════════════════════════════╝

HAPPY_SYSTEM_PROMPT = """HAPPY/EXCITED USER - MATCH THEIR JOY AND CELEBRATE:
The user is happy/excited! Your response must:
- Match their positive energy and enthusiasm
- Celebrate with them genuinely
- Amplify their joy"""

# Example if user said: "I just fixed a major bug and got promoted!"
HAPPY_OUTPUT = """That's fantastic! Congratulations on both the bug fix AND the promotion - you earned it! 🎉
Your problem-solving skills clearly didn't go unnoticed. Fixing critical bugs takes real skill and dedication. 
Keep riding this momentum - you're clearly crushing it in your role!"""
# Note: Enthusiastic, celebratory, amplifies their joy, energetic


# ╔════════════════════════════════════════════════════════════════════════╗
# ║ EMOTION 5: NEUTRAL (No specific emotional tone detected)              ║
# ║ Max Tokens: 250 (STRUCTURED - 5-8 sentences, informative)             ║
# ╚════════════════════════════════════════════════════════════════════════╝

NEUTRAL_SYSTEM_PROMPT = """NEUTRAL USER - RESPOND WITH CLARITY AND STRUCTURE:
The user is asking neutrally. Your response must:
- Provide accurate, clear information
- Organize using structure (bullets, sections)
- Be professional but conversational"""

# Example if user said: "How do I fix a production bug?"
NEUTRAL_OUTPUT = """Here are the steps to fix a production bug:

1. Identify the Issue:
   - Check error logs and monitoring
   - Reproduce the bug locally

2. Fix the Issue:
   - Write a patch or hotfix
   - Test thoroughly before deploying

3. Deploy:
   - Use your deployment protocol
   - Monitor the system post-deployment

4. Communicate:
   - Notify stakeholders of the fix
   - Document the root cause"""
# Note: Structured, clear, organized, informative, professional


# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║           EMOTION-BASED RESPONSE STYLE COMPARISON                         ║
╠═════════════╦══════════╦═════════════╦═══════════════╦═══════════════════╣
║   Emotion   ║ Max Toks ║   Tone      ║   Style       ║   Focus           ║
╠═════════════╬══════════╬═════════════╬═══════════════╬═══════════════════╣
║  URGENT     ║   120    ║ Direct      ║ 1-2 sentences ║ Immediate action  ║
║   (RED)     ║          ║ Crisp       ║ (VERY BRIEF)  ║ only              ║
╠═════════════╬══════════╬═════════════╬═══════════════╬═══════════════════╣
║  ANGRY      ║   180    ║ Empathetic  ║ 3-5 sentences ║ Acknowledge +     ║
║  (ORANGE)   ║          ║ Calm        ║ Solution-fold ║ Solutions         ║
╠═════════════╬══════════╬═════════════╬═══════════════╬═══════════════════╣
║  SAD        ║   200    ║ Warm        ║ 4-6 sentences ║ Empathy +         ║
║   (BLUE)    ║          ║ Supportive  ║ Encouraging   ║ Hope + Action     ║
╠═════════════╬══════════╬═════════════╬═══════════════╬═══════════════════╣
║  HAPPY      ║   200    ║ Enthusiast  ║ 4-6 sentences ║ Celebrate +       ║
║  (GREEN)    ║          ║ Positive    ║ Energetic     ║ Amplify joy       ║
╠═════════════╬══════════╬═════════════╬═══════════════╬═══════════════════╣
║  NEUTRAL    ║   250    ║ Professional║ 5-8 sentences ║ Accuracy +        ║
║   (GRAY)    ║          ║ Clear       ║ Structured    ║ Structure         ║
╚═════════════╩══════════╩═════════════╩═══════════════╩═══════════════════╝
""")

print("\n✅ PROJECT CORE WORKING:")
print("   1. Emotion Detection: Analyzes user prompt → detects emotion")
print("   2. System Prompt Selection: Uses emotion-specific instructions")
print("   3. Token Limit: Adjusts brevity based on emotion")
print("   4. AI Response: Generates tone-appropriate response")
print("   5. Frontend Display: Shows emotion badge + customized response")
print("\n🎯 Result: SAME QUESTION → DIFFERENT ANSWER based on emotion!")
