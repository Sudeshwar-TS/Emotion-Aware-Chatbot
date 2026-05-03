"""
Emotion Detection and Analysis Module (Transformer-Based)
Uses pretrained Hugging Face model: j-hartmann/emotion-english-distilroberta-base
Analyzes user input for emotion classification and intensity level
Core feature: Context-aware emotion detection using ML
"""

import re
from typing import Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers/torch not installed. Install with: pip install -r requirements.txt")


class EmotionAnalyzer:
    """Analyzes user input for emotion using pretrained transformer model"""

    # Model configuration
    MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
    
    # Map model outputs to system emotions
    MODEL_TO_SYSTEM_EMOTIONS = {
        "anger": "Angry",
        "sadness": "Sad",
        "joy": "Happy",
        "fear": "Urgent",
        "neutral": "Neutral",
        "surprise": "Happy",
        "love": "Happy",
        "disgust": "Angry"
    }

    # Punctuation intensity markers (used for intensity calculation)
    EXCLAMATION_MARKS = r"!{2,}"
    QUESTION_MARKS = r"\?{2,}"
    CAPS_LOCK = r"\b[A-Z]{2,}\b"
    
    # Intensifiers
    INTENSIFIERS = ["very", "extremely", "absolutely", "definitely", "so", "really",
                    "incredibly", "totally", "completely", "utterly", "way", "much"]

    def __init__(self):
        """Initialize the transformer-based emotion analyzer"""
        self.emotion_history = []
        self.model_loaded = False
        self.classifier = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                # Load pretrained model - uses CPU by default, very efficient
                self.classifier = pipeline(
                    "text-classification",
                    model=self.MODEL_NAME,
                    top_k=None,  # Get all predictions with scores
                    device=-1  # Use CPU (set to 0 for GPU if available)
                )
                self.model_loaded = True
                logger.info(f"✅ Loaded transformer model: {self.MODEL_NAME}")
            except Exception as e:
                logger.error(f"Failed to load transformer model: {e}")
                logger.info("Falling back to keyword-based detection")
                self.model_loaded = False
        else:
            logger.warning("Transformers not available. Using fallback keyword detection")

    def analyze(self, user_input: str) -> dict:
        """
        Analyze user input for emotion using transformer model
        
        Args:
            user_input: User's text input
            
        Returns:
            Dictionary with emotion, intensity, and confidence
        """
        if not user_input.strip():
            return {
                "emotion": "Neutral",
                "intensity": "Low",
                "confidence": "60%",
                "emotion_history": self.emotion_history.copy()
            }

        # Detect emotion using model
        emotion, model_score = self._detect_emotion_ml(user_input)

        # Detect intensity based on text features and model confidence
        intensity = self._detect_intensity(user_input, model_score, emotion)

        # Calculate confidence based on model score and text features
        confidence = self._calculate_confidence(model_score, intensity)

        # Add to history
        self.emotion_history.append(emotion)

        return {
            "emotion": emotion,
            "intensity": intensity,
            "confidence": confidence,
            "emotion_history": self.emotion_history.copy()
        }

    def _detect_emotion_ml(self, user_input: str) -> tuple:
        """
        Detect emotion using transformer model
        Falls back to keyword detection if model unavailable
        
        Args:
            user_input: User's text input
            
        Returns:
            Tuple of (emotion_label, confidence_score)
        """
        
        # Truncate very long inputs (model has length limits)
        input_text = user_input[:512]
        
        if self.model_loaded and self.classifier is not None:
            try:
                # Get model predictions
                predictions = self.classifier(input_text)
                
                # predictions is a list of lists: [[{"label": "...", "score": ...}, ...]]
                if predictions and len(predictions) > 0:
                    # Get top prediction
                    top_pred = predictions[0][0]
                    model_emotion = top_pred["label"].lower()
                    model_score = top_pred["score"]
                    
                    # Map to system emotion
                    system_emotion = self.MODEL_TO_SYSTEM_EMOTIONS.get(model_emotion, "Neutral")
                    
                    # Post-processing: check for urgent patterns even if model didn't detect
                    if system_emotion != "Urgent":
                        urgent_score = self._check_urgent_patterns(user_input.lower())
                        if urgent_score > 0.7:
                            system_emotion = "Urgent"
                            model_score = urgent_score
                    
                    logger.debug(f"Model detected: {model_emotion} ({model_score:.2f}) → {system_emotion}")
                    return system_emotion, model_score
                    
            except Exception as e:
                logger.error(f"Model inference error: {e}")
        
        # Fallback: keyword-based detection
        logger.debug("Using fallback keyword-based detection")
        return self._detect_emotion_fallback(user_input.lower()), 0.6

    def _check_urgent_patterns(self, text_lower: str) -> float:
        """
        Post-processing to catch urgent patterns model might miss
        
        Args:
            text_lower: Lowercased text
            
        Returns:
            Score 0-1 indicating urgency
        """
        urgent_keywords = [
            "urgent", "emergency", "help", "911", "bleeding", "accident", "crisis",
            "critical", "desperate", "asap", "immediately", "now", "hurry"
        ]
        
        matches = sum(1 for kw in urgent_keywords if kw in text_lower)
        
        # If multiple urgent keywords or exact phrases
        if "help me" in text_lower or "911" in text_lower:
            return 0.9
        if matches >= 2:
            return 0.8
        if matches >= 1 and len(text_lower.split()) <= 5:  # Short urgent message
            return 0.75
        
        return 0.0

    def _detect_emotion_fallback(self, text_lower: str) -> str:
        """
        Fallback keyword-based emotion detection
        Used when transformer model is unavailable
        
        Args:
            text_lower: Lowercased text
            
        Returns:
            Detected emotion
        """
        
        emotion_keywords = {
            "Urgent": ["urgent", "emergency", "help", "911", "crisis", "critical", "asap", "immediately"],
            "Angry": ["angry", "furious", "hate", "mad", "infuriated", "frustrated", "annoyed"],
            "Sad": ["sad", "depressed", "heartbroken", "devastated", "lonely", "suffering", "unhappy"],
            "Happy": ["happy", "thrilled", "excited", "amazing", "wonderful", "love", "grateful"]
        }
        
        scores = {emotion: 0 for emotion in emotion_keywords}
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[emotion] += 1
        
        max_emotion = max(scores, key=scores.get)
        if scores[max_emotion] > 0:
            return max_emotion
        
        return "Neutral"

    def _detect_intensity(self, text_raw: str, model_score: float, emotion: str) -> str:
        """
        Detect emotional intensity level
        Combines model confidence with textual intensity markers
        
        Args:
            text_raw: Raw text
            model_score: Model confidence score (0-1)
            emotion: Detected emotion
            
        Returns:
            One of: Low, Medium, High
        """
        
        intensity_score = 0
        text_lower = text_raw.lower()

        # Model confidence contributes to intensity
        # High confidence in any emotion = at least medium intensity
        if model_score >= 0.9:
            intensity_score += 3
        elif model_score >= 0.7:
            intensity_score += 2
        elif model_score >= 0.5:
            intensity_score += 1

        # Punctuation markers
        if re.search(self.EXCLAMATION_MARKS, text_raw):  # Multiple !!
            intensity_score += 4
        elif text_raw.count("!") > 0:  # Single !
            intensity_score += 1

        if re.search(self.QUESTION_MARKS, text_raw):  # Multiple ??
            intensity_score += 2

        # CAPS LOCK
        if re.search(self.CAPS_LOCK, text_raw):
            intensity_score += 3

        # Intensifier words (very, extremely, etc.)
        if any(intensifier in text_lower for intensifier in self.INTENSIFIERS):
            intensity_score += 2

        # Emotion baseline
        if emotion in ["Urgent", "Angry"]:
            intensity_score += 1
        
        # Short intense messages
        words = text_raw.split()
        if len(words) <= 3 and intensity_score >= 2:
            intensity_score += 1

        # CLASSIFY
        if emotion == "Neutral":
            return "Low"
        elif intensity_score >= 6:
            return "High"
        elif intensity_score >= 3:
            return "Medium"
        else:
            return "Low"

    def _calculate_confidence(self, model_score: float, intensity: str) -> str:
        """
        Calculate confidence percentage
        Based on model score and intensity level
        
        Args:
            model_score: Model's confidence score (0-1)
            intensity: Detected intensity level
            
        Returns:
            Confidence as percentage string
        """
        
        # Base confidence from model score
        confidence = int(model_score * 100)
        
        # Boost for high intensity
        if intensity == "High":
            confidence = min(confidence + 10, 100)
        
        # Minimum 55% confidence
        confidence = max(confidence, 55)
        
        return f"{confidence}%"

    def get_response_speed(self, emotion: str) -> str:
        """Get response speed based on emotion"""
        speed_map = {
            "Urgent": "FAST",
            "Angry": "MEDIUM",
            "Happy": "MEDIUM",
            "Sad": "SLOW",
            "Neutral": "NORMAL"
        }
        return speed_map.get(emotion, "NORMAL")

    def get_ui_color(self, emotion: str) -> str:
        """Get UI color based on emotion"""
        color_map = {
            "Angry": "RED",
            "Sad": "BLUE",
            "Happy": "GREEN",
            "Urgent": "ORANGE",
            "Neutral": "GRAY"
        }
        return color_map.get(emotion, "GRAY")

    def reset_history(self):
        """Reset emotion history"""
        self.emotion_history = []
