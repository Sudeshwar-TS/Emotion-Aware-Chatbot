"""
Test the new contextual emotion analyzer
"""

from emotion_analyzer import EmotionAnalyzer

analyzer = EmotionAnalyzer()

# Test cases
test_cases = [
    ("I didn't make a good food today", "Sad"),
    ("this was a good day", "Happy"),
    ("I'm so happy!", "Happy"),
    ("I'm not happy", "Neutral"),
    ("hello", "Neutral"),
    ("This sucks! I'm furious!", "Angry"),
    ("Help! Emergency!", "Urgent"),
    ("I love this, it's fantastic", "Happy"),
    ("I couldn't make it work", "Sad"),
    ("I didn't enjoy it but tried my best", "Neutral"),
]

print("=" * 70)
print("EMOTION ANALYZER TEST - CONTEXTUAL UNDERSTANDING")
print("=" * 70)

for prompt, expected in test_cases:
    result = analyzer.analyze(prompt)
    emotion = result["emotion"]
    confidence = result["confidence"]
    intensity = result["intensity"]
    
    status = "✓" if emotion == expected else "✗"
    print(f"\n{status} Input: \"{prompt}\"")
    print(f"  Expected: {expected} | Got: {emotion} ({confidence}) [{intensity}]")

print("\n" + "=" * 70)
