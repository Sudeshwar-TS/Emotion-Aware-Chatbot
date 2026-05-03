"""
API Test Client
Simple Python script to test the Emotion-Aware Chatbot API

Requirements: requests library (pip install requests)

Usage:
    python test_api.py

Make sure the Flask backend is running first:
    python app.py
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:5000"

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{Colors.UNDERLINE}{text}{Colors.END}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def test_health() -> bool:
    """Test health endpoint"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print(f"  Status: {data.get('status')}")
            print(f"  Claude API Available: {data.get('claude_api_available')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server. Is Flask app running on port 5000?")
        print_info("Start the backend with: python app.py")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_chat(user_input: str, expected_emotion: str = None) -> Dict[str, Any]:
    """Test chat endpoint"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"user_input": user_input},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results
            emotion_match = ""
            if expected_emotion:
                if data["emotion"] == expected_emotion:
                    emotion_match = f" {Colors.GREEN}[EXPECTED]{Colors.END}"
                else:
                    emotion_match = f" {Colors.YELLOW}[UNEXPECTED]{Colors.END}"
            
            print(f"\n  Input: \"{Colors.CYAN}{user_input}{Colors.END}\"")
            print(f"  Emotion: {Colors.BOLD}{data['emotion']}{Colors.END}{emotion_match}")
            print(f"  Intensity: {data['intensity']}")
            print(f"  Confidence: {data['confidence']}")
            print(f"  Response Speed: {Colors.YELLOW}{data['response_speed']}{Colors.END}")
            print(f"  UI Color: {Colors.YELLOW}{data['ui_color']}{Colors.END}")
            print(f"\n  Normal Response:")
            print(f"    {Colors.BLUE}{data['normal_response'][:150]}...{Colors.END}")
            print(f"\n  Emotion-Based Response:")
            print(f"    {Colors.GREEN}{data['emotion_based_response'][:150]}...{Colors.END}")
            print(f"\n  Emotion History: {' → '.join(data['emotion_history'])}")
            
            return data
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(f"  Response: {response.json()}")
            return {}
            
    except requests.exceptions.Timeout:
        print_error("Request timed out. Claude API might be slow.")
        return {}
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server.")
        return {}
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return {}


def test_reset() -> bool:
    """Test reset endpoint"""
    print_header("TEST: Reset Emotion History")
    
    try:
        response = requests.post(f"{BASE_URL}/reset")
        if response.status_code == 200:
            data = response.json()
            print_success("Reset successful")
            print(f"  Message: {data.get('message')}")
            return True
        else:
            print_error(f"Reset failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def run_test_suite():
    """Run complete test suite"""
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     EMOTION-AWARE CHATBOT API - TEST SUITE                    ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

    print_info("Make sure Flask backend is running: python app.py")
    print_info("Testing endpoints on: " + Colors.CYAN + BASE_URL + Colors.END)

    # Test health first
    if not test_health():
        return

    # Test cases with expected emotions
    test_cases = [
        ("I'm so happy today! This is wonderful!!!", "Happy"),
        ("URGENT! I need help immediately!!!", "Urgent"),
        ("This is absolutely frustrating and disappointing!", "Angry"),
        ("I feel so alone and broken right now", "Sad"),
        ("What's the capital of France?", "Neutral"),
    ]

    print_header("TEST 2: Chat Endpoint (Multiple Emotions)")
    
    for user_input, expected_emotion in test_cases:
        test_chat(user_input, expected_emotion)
        print()

    # Test emotion history accumulation
    print_header("TEST 3: Emotion History Accumulation")
    print_info("Sending multiple messages to test history...")
    
    history_messages = [
        "I'm happy!",
        "Wait, I'm confused",
        "Actually I'm angry!"
    ]
    
    last_response = {}
    for msg in history_messages:
        response = test_chat(msg)
        last_response = response
    
    if last_response and "emotion_history" in last_response:
        print(f"\nFinal emotion history: {' → '.join(last_response['emotion_history'])}")

    # Test reset
    test_reset()
    
    # Verify history was cleared
    print("\nVerifying history reset...")
    response = test_chat("Testing after reset")
    if response and len(response.get("emotion_history", [])) == 1:
        print_success("Emotion history was successfully cleared")
    else:
        print_error("Emotion history was not cleared properly")

    print_header("TEST SUITE COMPLETE")
    print(f"{Colors.GREEN}All tests completed!{Colors.END}\n")


def interactive_mode():
    """Run in interactive mode"""
    print_header("INTERACTIVE MODE")
    print_info("Type messages to get emotion analysis")
    print_info("Type 'quit' to exit")
    print_info("Type 'reset' to clear emotion history")
    
    try:
        while True:
            user_input = input(f"\n{Colors.CYAN}You: {Colors.END}").strip()
            
            if user_input.lower() == "quit":
                print_info("Goodbye!")
                break
            elif user_input.lower() == "reset":
                test_reset()
                continue
            elif not user_input:
                continue
            
            print(f"{Colors.YELLOW}Processing...{Colors.END}")
            test_chat(user_input)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        run_test_suite()
        
        print(f"\n{Colors.CYAN}Want to chat interactively?{Colors.END}")
        print("Run: python test_api.py interactive")
