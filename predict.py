import os
import joblib
import numpy as np
import pandas as pd
from config import config

class StudyPredictor:
    """Production classification boundary inference interface."""
    def __init__(self):
        self.model_path = os.path.join(config.MODEL_DIR, 'best_model.pkl')
        self.scaler_path = os.path.join(config.MODEL_DIR, 'scaler.pkl')
        
        if not os.path.exists(self.model_path) or not os.path.exists(self.scaler_path):
            raise RuntimeError("Engine artifacts absent. Ensure train.py executes without validation breaks.")
            
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        
    def generate_recommendations(self, productivity_level, stress_level, break_count):
        """Generates contextual actions and high-impact custom workflows."""
        quotes = {
            'High': "Outstanding execution velocity. Leverage this cognitive flow state to conquer complex architecture objectives.",
            'Medium': "Consistent pacing found. A minor adjustment to systematic structures will maximize retention optimization.",
            'Low': "Cognitive exhaustion detected. Recalibrate and optimize your routine to restore your operational peak."
        }
        
        suggestions = []
        if productivity_level == 'High':
            suggestions = [
                "Execute your most complex problem-solving modules right now.",
                "Maintain your current cognitive state and document your core learning objectives.",
                "Dedicate the next 45 minutes to deep, uninterrupted deep work."
            ]
        elif productivity_level == 'Medium':
            suggestions = [
                "Deploy the Pomodoro Framework: 25 minutes of deep focus followed by a structured 5-minute break.",
                "Minimize external noise parameters and clear secondary workspace tabs.",
                "Review immediate concept maps before proceeding to advanced material."
            ]
        else:
            suggestions = [
                "Initiate an immediate 15-minute off-screen neuro-reset break.",
                "Break down your current task into smaller, manageable micro-objectives.",
                "Reduce environmental stress factors and ensure adequate hydration levels."
            ]
            
        if stress_level >= 7:
            suggestions.append("Critical stress levels monitored. Introduce diaphragmatic breath control exercises or a short walk.")
        if break_count < 2:
            suggestions.append("Low break frequency detected. Scheduled pacing prevents system cognitive burnout.")
            
        return {
            'quote': quotes.get(productivity_level, "Keep moving forward."),
            'suggestions': suggestions
        }

    def infer_productivity(self, sleep_hours, study_hours, stress_level, mood, break_count):
        """Processes real-time multi-variant vector inputs to map accurate productivity cohorts."""
        feature_names = ['Sleep_Hours', 'Study_Hours', 'Stress_Level', 'Mood', 'Break_Count']
        raw_input_df = pd.DataFrame([[sleep_hours, study_hours, stress_level, mood, break_count]], columns=feature_names)
        
        scaled_input = self.scaler.transform(raw_input_df)
        
        prediction = self.model.predict(scaled_input)[0]
        probabilities = self.model.predict_proba(scaled_input)[0]
        
        # Map target confidence metric
        class_labels = list(self.model.classes_)
        predicted_idx = class_labels.index(prediction)
        confidence = float(probabilities[predicted_idx]) * 100
        
        insights = self.generate_recommendations(prediction, stress_level, break_count)
        
        return {
            'productivity_level': prediction,
            'confidence': round(confidence, 2),
            'quote': insights['quote'],
            'suggestions': insights['suggestions']
        }