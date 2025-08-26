import json
import re
from typing import List, Dict, Any
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

class HindiMedicalNLPEngine:
    """Hindi Medical NLP Engine for processing medical conversations in Hindi"""
    
    def __init__(self):
        """Initialize the Hindi Medical NLP Engine with available models"""
        
        # Use actual available models instead of placeholder names
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
        except:
            print("Warning: Using fallback tokenizer")
            self.tokenizer = None
        
        # Use pattern-based approach instead of non-existent models
        self.medical_terms = self._load_medical_terminology()
        self.symptom_mappings = self._load_symptom_mappings()
        self.cultural_context = self._load_cultural_context()
    
    def _load_medical_terminology(self) -> Dict[str, str]:
        """Load Hindi medical terminology"""
        return {
            "बुखार": "fever",
            "सीने में दर्द": "chest pain",
            "सिर दर्द": "headache",
            "सांस लेने में दिक्कत": "breathing difficulty",
            "उल्टी": "vomiting",
            "दस्त": "diarrhea",
            "घुटने में दर्द": "knee pain",
            "सूजन": "swelling",
            "खांसी": "cough",
            "जुकाम": "cold",
            "दर्द": "pain",
            "सर्दी": "cold",
            "सांस फूलना": "breathlessness",
            "पेट दर्द": "stomach pain",
            "चक्कर": "dizziness",
            "बेहोशी": "unconsciousness",
            "दौरे": "seizures",
            "रक्तस्त्राव": "bleeding",
            "उच्च रक्तचाप": "high blood pressure",
            "मधुमेह": "diabetes",
            "दमा": "asthma",
            "मलेरिया": "malaria",
            "टाइफाइड": "typhoid"
        }
    
    def _load_symptom_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Load symptom mappings with urgency levels"""
        return {
            "fever": {"urgency": "medium", "severity": 5, "category": "symptom"},
            "chest pain": {"urgency": "high", "severity": 8, "category": "emergency"},
            "headache": {"urgency": "low", "severity": 3, "category": "symptom"},
            "breathing difficulty": {"urgency": "high", "severity": 9, "category": "emergency"},
            "vomiting": {"urgency": "medium", "severity": 4, "category": "symptom"},
            "diarrhea": {"urgency": "medium", "severity": 4, "category": "symptom"},
            "knee pain": {"urgency": "low", "severity": 2, "category": "symptom"},
            "swelling": {"urgency": "low", "severity": 3, "category": "symptom"},
            "cough": {"urgency": "low", "severity": 2, "category": "symptom"},
            "cold": {"urgency": "low", "severity": 2, "category": "symptom"},
            "pain": {"urgency": "variable", "severity": 5, "category": "symptom"},
            "breathlessness": {"urgency": "high", "severity": 8, "category": "emergency"},
            "stomach pain": {"urgency": "medium", "severity": 5, "category": "symptom"},
            "dizziness": {"urgency": "medium", "severity": 4, "category": "symptom"},
            "unconsciousness": {"urgency": "critical", "severity": 10, "category": "emergency"},
            "seizures": {"urgency": "critical", "severity": 10, "category": "emergency"},
            "bleeding": {"urgency": "high", "severity": 7, "category": "emergency"},
            "high blood pressure": {"urgency": "medium", "severity": 6, "category": "condition"},
            "diabetes": {"urgency": "medium", "severity": 6, "category": "condition"},
            "asthma": {"urgency": "medium", "severity": 5, "category": "condition"},
            "malaria": {"urgency": "high", "severity": 7, "category": "condition"},
            "typhoid": {"urgency": "high", "severity": 7, "category": "condition"}
        }
    
    def _load_cultural_context(self) -> Dict[str, str]:
        """Load cultural context for better understanding"""
        return {
            "traditional_remedies": {
                "हल्दी दूध": {"english": "turmeric milk", "type": "home_remedy"},
                "अदरक की चाय": {"english": "ginger tea", "type": "home_remedy"},
                "तुलसी": {"english": "basil", "type": "ayurvedic"}
            },
            "cultural_considerations": {
                "gender_sensitivity": True,
                "family_consultation": True,
                "traditional_medicine_integration": True
            }
        }
    
    def extract_symptoms(self, text: str) -> List[Dict[str, Any]]:
        """Extract symptoms from Hindi text"""
        symptoms = []
        text_lower = text.lower()
        
        # Direct pattern matching for known symptoms
        for hindi_term, english_term in self.medical_terms.items():
            if hindi_term.lower() in text_lower:
                symptom_info = self.symptom_mappings.get(english_term, {"urgency": "medium", "severity": 5, "category": "symptom"})
                symptoms.append({
                    "hindi_term": hindi_term,
                    "english_term": english_term,
                    "urgency": symptom_info["urgency"],
                    "severity": symptom_info["severity"],
                    "category": symptom_info["category"]
                })
        
        # Extract duration and context
        context = self._extract_context(text)
        for symptom in symptoms:
            symptom.update(context)
        
        return symptoms
    
    def _extract_context(self, text: str) -> Dict[str, Any]:
        """Extract contextual information like duration, severity"""
        context = {}
        
        # Duration extraction
        duration_patterns = [
            (r'(\d+)\s*(दिन|घंटे|सप्ताह|महीने)', 'duration'),
            (r'(कल से|आज से|पिछले \d+ दिनों से)', 'duration_text')
        ]
        
        for pattern, key in duration_patterns:
            matches = re.findall(pattern, text)
            if matches:
                context[key] = matches[0] if isinstance(matches[0], str) else ''.join(matches[0])
                break
        
        # Severity extraction
        severity_keywords = {
            "high": ["बहुत", "अत्यधिक", "तीव्र", "गंभीर", "बुरी", "ज्यादा"],
            "medium": ["थोड़ा", "मध्यम", "सामान्य", "ठीक-ठाक"],
            "low": ["हल्का", "कम", "थोड़ा सा"]
        }
        
        for level, keywords in severity_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                context["severity"] = level
                break
        
        return context
    
    def analyze_urgency(self, symptoms: List[Dict[str, Any]], context: str = "") -> Dict[str, Any]:
        """Analyze urgency based on symptoms and context"""
        if not symptoms:
            return {"urgency_level": "low", "confidence": 0.5, "primary_symptoms": []}
        
        # Calculate urgency based on symptom severity
        max_severity = max([s.get("severity", 5) for s in symptoms])
        high_urgency_count = len([s for s in symptoms if s.get("urgency") == "high" or s.get("urgency") == "critical"])
        critical_count = len([s for s in symptoms if s.get("urgency") == "critical"])
        
        if critical_count > 0:
            urgency_level = "critical"
        elif high_urgency_count > 0 or max_severity >= 7:
            urgency_level = "high"
        elif max_severity >= 4:
            urgency_level = "medium"
        else:
            urgency_level = "low"
        
        confidence = min(0.9, 0.5 + (max_severity / 10))
        
        return {
            "urgency_level": urgency_level,
            "confidence": confidence,
            "primary_symptoms": [s["hindi_term"] for s in symptoms],
            "symptom_count": len(symptoms),
            "max_severity": max_severity
        }
    
    def generate_response(self, symptoms: List[Dict[str, Any]], urgency_analysis: Dict[str, Any]) -> str:
        """Generate appropriate Hindi response"""
        if not symptoms:
            return "कृपया अपनी समस्या विस्तार से बताएं"
        
        urgency = urgency_analysis["urgency_level"]
        symptom_list = ", ".join([s["hindi_term"] for s in symptoms])
        
        responses = {
            "critical": f"आपके {symptom_list} जैसे लक्षण अत्यंत गंभीर हो सकते हैं। कृपया तुरंत नजदीकी अस्पताल जाएं या 108 पर कॉल करें।",
            "high": f"आपके {symptom_list} लक्षणों पर तुरंत ध्यान देना जरूरी है। कृपया जल्द से जल्द डॉक्टर से संपर्क करें।",
            "medium": f"आपके {symptom_list} लक्षणों की निगरानी करें। यदि स्थिति बिगड़े तो डॉक्टर से सलाह लें।",
            "low": f"आपके {symptom_list} लक्षणों पर ध्यान रखें। घरेलू उपचार से आराम मिल सकता है।"
        }
        
        return responses.get(urgency, responses["low"])
    
    def process_conversation(self, text: str) -> Dict[str, Any]:
        """Process complete conversation in one call"""
        symptoms = self.extract_symptoms(text)
        urgency_analysis = self.analyze_urgency(symptoms, text)
        response = self.generate_response(symptoms, urgency_analysis)
        
        return {
            "input_text": text,
            "extracted_symptoms": symptoms,
            "urgency_analysis": urgency_analysis,
            "response": response,
            "timestamp": str(pd.Timestamp.now()) if 'pd' in globals() else "current"
        }

class MedicalEmpathyEngine:
    """Empathy and emotional support for Hindi medical conversations"""
    
    def __init__(self):
        self.empathy_responses = {
            "pain": "मैं समझ सकता हूं कि आपको कितनी तकलीफ हो रही है",
            "worry": "आपकी चिंता स्वाभाविक है, हम इस पर ध्यान देंगे",
            "fear": "मैं आपके साथ हूं, आप बिल्कुल सुरक्षित हैं",
            "confusion": "मैं आपकी बात को समझने की पूरी कोशिश कर रहा हूं"
        }
    
    def generate_empathetic_response(self, emotional_state: str, hindi_context: str) -> str:
        """Generate empathetic response in Hindi"""
        base_empathy = self.empathy_responses.get(emotional_state, "मैं आपकी बात समझ रहा हूं")
        
        if "दर्द" in hindi_context:
            return f"{base_empathy}, दर्द से राहत के लिए हम कुछ उपाय सुझाएंगे"
        elif "बुखार" in hindi_context:
            return f"{base_empathy}, बुखार से जल्दी आराम मिलेगा"
        
        return base_empathy

# Test the system
if __name__ == "__main__":
    nlp_engine = HindiMedicalNLPEngine()
    
    # Test conversations
    test_cases = [
        "मुझे तीन दिन से बुखार है और सिर में दर्द हो रहा है",
        "मेरी छाती में दर्द हो रहा है और सांस लेने में दिक्कत है",
        "मुझे हल्का खांसी और सर्दी है"
    ]
    
    for test_input in test_cases:
        print(f"\nInput: {test_input}")
        result = nlp_engine.process_conversation(test_input)
        print(f"Response: {result['response']}")
        print(f"Urgency: {result['urgency_analysis']['urgency_level']}")
        print(f"Symptoms: {[s['hindi_term'] for s in result['extracted_symptoms']]}")