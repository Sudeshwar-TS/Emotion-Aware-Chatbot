"""
Test Script for Emotion-Aware Chatbot
Demonstrates emotion detection without requiring Flask/API to be running

Usage:
    python test_emotion_analyzer.py
"""

from emotion_analyzer import EmotionAnalyzer


def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")


def test_emotion_detector():
    """Test the emotion analyzer"""
    
    analyzer = EmotionAnalyzer()

    test_cases = [
        {
            "input": "I'm so happy today! This is wonderful!!!",
            "expected_emotion": "Happy"
        },
        {
            "input": "URGENT!!! I need help immediately!!!",
            "expected_emotion": "Urgent"
        },
        {
            "input": "This is absolutely frustrating! I hate this!",
            "expected_emotion": "Angry"
        },
        {
            "input": "I feel so alone and broken. Everything is falling apart.",
            "expected_emotion": "Sad"
        },
        {
            "input": "What is the capital of France?",
            "expected_emotion": "Neutral"
        },
        {
            "input": "I'm very excited about the new project!",
            "expected_emotion": "Happy"
        },
        {
            "input": "Can you help me with this problem?",
            "expected_emotion": "Neutral"
        },
        {
            "input": "This is extremely disappointing and absolutely unacceptable!!!",
            "expected_emotion": "Angry"
        }
    ]

    print_separator("EMOTION-AWARE CHATBOT - EMOTION DETECTION TEST")
    print(f"Testing {len(test_cases)} different inputs...\n")

    for i, test_case in enumerate(test_cases, 1):
        user_input = test_case["input"]
        expected = test_case["expected_emotion"]

        # Analyze the input
        analysis = analyzer.analyze(user_input)

        # Get metadata
        response_speed = analyzer.get_response_speed(analysis["emotion"])
        ui_color = analyzer.get_ui_color(analysis["emotion"])

        # Display results
        print(f"Test {i}:")
        print(f"  Input: \"{user_input}\"")
        print(f"  Detected Emotion: {analysis['emotion']}")
        print(f"  Expected Emotion: {expected}")
        
        match = "✓ MATCH" if analysis['emotion'] == expected else "✗ MISMATCH"
        print(f"  Result: {match}")
        
        print(f"  Intensity: {analysis['intensity']}")
        print(f"  Confidence: {analysis['confidence']}")
        print(f"  Response Speed: {response_speed}")
        print(f"  UI Color: {ui_color}")
        print()

    # Display emotion history
    print_separator("EMOTION HISTORY")
    print(f"Emotions detected: {analyzer.emotion_history}")
    print(f"\nSequence: {' → '.join(analyzer.emotion_history)}")

    # Test reset
    print_separator("TESTING RESET")
    print("Resetting emotion history...")
    analyzer.reset_history()
    print(f"History after reset: {analyzer.emotion_history}")
    print("✓ Reset successful")


def test_intensity_detection():
    """Test intensity detection"""
    
    print_separator("INTENSITY DETECTION TEST")

    analyzer = EmotionAnalyzer()

    intensity_tests = [
        {
            "input": "I'm happy",
            "expected": "Low"
        },
        {
            "input": "I'm very happy!",
            "expected": "Medium"
        },
        {
            "input": "I'M EXTREMELY HAPPY!!! THIS IS AMAZING!!!",
            "expected": "High"
        },
        {
            "input": "Help me",
            "expected": "Low"
        },
        {
            "input": "Help me now!",
            "expected": "Medium"
        },
        {
            "input": "HELP ME NOW!!! THIS IS URGENT!!!",
            "expected": "High"
        }
    ]

    for i, test in enumerate(intensity_tests, 1):
        analysis = analyzer.analyze(test["input"])
        match = "✓" if analysis['intensity'] == test['expected'] else "✗"
        print(f"{match} Test {i}: \"{test['input']}\"")
        print(f"   Expected: {test['expected']}, Got: {analysis['intensity']}")
        print()


def test_response_speed_and_color():
    """Test response speed and UI color assignment"""
    
    print_separator("RESPONSE SPEED & UI COLOR TEST")

    analyzer = EmotionAnalyzer()

    emotions_data = {
        "Urgent": {"expected_speed": "FAST", "expected_color": "ORANGE"},
        "Angry": {"expected_speed": "MEDIUM", "expected_color": "RED"},
        "Sad": {"expected_speed": "SLOW", "expected_color": "BLUE"},
        "Happy": {"expected_speed": "MEDIUM", "expected_color": "GREEN"},
        "Neutral": {"expected_speed": "NORMAL", "expected_color": "GRAY"}
    }

    for emotion, expected in emotions_data.items():
        speed = analyzer.get_response_speed(emotion)
        color = analyzer.get_ui_color(emotion)
        
        speed_match = "✓" if speed == expected["expected_speed"] else "✗"
        color_match = "✓" if color == expected["expected_color"] else "✗"
        
        print(f"Emotion: {emotion}")
        print(f"  {speed_match} Speed: {speed} (expected: {expected['expected_speed']})")
        print(f"  {color_match} Color: {color} (expected: {expected['expected_color']})")
        print()


def test_confidence_scoring():
    """Test confidence scoring"""
    
    print_separator("CONFIDENCE SCORING TEST")

    analyzer = EmotionAnalyzer()

    confidence_tests = [
        "I'm happy",  # Low: only one keyword
        "I'm very happy! This is amazing!!",  # Medium: multiple indicators
        "I absolutely HATE this!!! This is furious and extremely angry!!!",  # High: many indicators
    ]

    for test_input in confidence_tests:
        analysis = analyzer.analyze(test_input)
        print(f"Input: \"{test_input}\"")
        print(f"  Emotion: {analysis['emotion']}")
        print(f"  Confidence: {analysis['confidence']}")
        print()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  EMOTION-AWARE CHATBOT - COMPREHENSIVE TEST SUITE")
    print("="*60)

    # Run all tests
    test_emotion_detector()
    test_intensity_detection()
    test_response_speed_and_color()
    test_confidence_scoring()

    print_separator("TEST SUITE COMPLETE")
    print("✓ All tests finished!")
    print("\nTo test with Claude API responses, run: python app.py")
    print("Then use: curl -X POST http://localhost:5000/chat ...")
