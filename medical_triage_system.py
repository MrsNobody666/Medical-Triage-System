import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import random

class MedicalKnowledgeBase:
    """Medical knowledge base with symptoms, conditions, and triage rules"""
    
    def __init__(self):
        # Medical conditions database
        self.conditions = {
            "fever": {
                "hindi_name": "बुखार",
                "severity_levels": {
                    "low": {"temp_range": (99, 100.4), "urgency": "low"},
                    "moderate": {"temp_range": (100.4, 102), "urgency": "medium"},
                    "high": {"temp_range": (102, 105), "urgency": "high"}
                },
                "keywords": ["बुखार", "fever", "ताप", "ज्वर"],
                "symptoms": ["high_temperature", "body_aches", "headache"]
            },
            "cough": {
                "hindi_name": "खांसी",
                "severity_levels": {
                    "mild": {"duration_days": (1, 3), "urgency": "low"},
                    "persistent": {"duration_days": (3, 7), "urgency": "medium"},
                    "severe": {"duration_days": (7, 30), "urgency": "high"}
                },
                "keywords": ["खांसी", "cough", "कफ", "सूखी खांसी"],
                "symptoms": ["dry_cough", "wet_cough", "chest_pain"]
            },
            "chest_pain": {
                "hindi_name": "छाती में दर्द",
                "severity_levels": {
                    "mild": {"type": "sharp", "urgency": "medium"},
                    "severe": {"type": "crushing", "urgency": "critical"}
                },
                "keywords": ["छाती दर्द", "chest pain", "दिल का दर्द", "हृदय दर्द"],
                "symptoms": ["sharp_pain", "pressure", "shortness_of_breath"]
            },
            "headache": {
                "hindi_name": "सरदर्द",
                "severity_levels": {
                    "mild": {"intensity": (1, 4), "urgency": "low"},
                    "moderate": {"intensity": (4, 7), "urgency": "medium"},
                    "severe": {"intensity": (7, 10), "urgency": "high"}
                },
                "keywords": ["सरदर्द", "headache", "माइग्रेन", "दिमाग दर्द"],
                "symptoms": ["throbbing", "pressure", "light_sensitivity"]
            },
            "breathing_difficulty": {
                "hindi_name": "सांस लेने में कठिनाई",
                "severity_levels": {
                    "mild": {"description": "slight_shortness", "urgency": "medium"},
                    "severe": {"description": "severe_shortness", "urgency": "critical"}
                },
                "keywords": ["सांस फूलना", "breathing difficulty", "shortness of breath", "दमा"],
                "symptoms": ["shortness_of_breath", "wheezing", "chest_tightness"]
            }
        }
        
        # Emergency keywords and conditions
        self.emergency_keywords = {
            "critical": [
                "heart attack", "दिल का दौरा", "cardiac arrest", "सांस रुकना",
                "severe bleeding", "heavy bleeding", "अत्यधिक खून बहना",
                "unconscious", "बेहोशी", "coma", "कोमा",
                "stroke", "पक्षाघात", "paralysis", "लकवा"
            ],
            "high": [
                "severe chest pain", "severe headache", "high fever", "high temperature",
                "difficulty breathing", "severe injury", "major accident", "poisoning"
            ],
            "medium": [
                "moderate fever", "persistent cough", "injury", "pain", "swelling",
                "infection", "allergy", "dizziness", "nausea"
            ]
        }
        
        # Triage levels and descriptions
        self.triage_levels = {
            "critical": {
                "level": 1,
                "description": "तत्काल चिकित्सा सहायता आवश्यक",
                "hindi_description": "आपातकालीन स्थिति - तुरंत अस्पताल जाएं",
                "action": "Call emergency services immediately",
                "hindi_action": "108 पर कॉल करें या तुरंत अस्पताल जाएं",
                "color": "red",
                "wait_time": "0-5 minutes"
            },
            "high": {
                "level": 2,
                "description": "जल्द चिकित्सा सहायता आवश्यक",
                "hindi_description": "गंभीर स्थिति - जल्दी डॉक्टर से मिलें",
                "action": "Visit emergency department within 1-2 hours",
                "hindi_action": "1-2 घंटे के भीतर अस्पताल जाएं",
                "color": "orange",
                "wait_time": "15-30 minutes"
            },
            "medium": {
                "level": 3,
                "description": "चिकित्सा सलाह आवश्यक",
                "hindi_description": "सावधानी आवश्यक - डॉक्टर से सलाह लें",
                "action": "Schedule doctor appointment within 24 hours",
                "hindi_action": "24 घंटे के भीतर डॉक्टर से मिलें",
                "color": "yellow",
                "wait_time": "1-2 hours"
            },
            "low": {
                "level": 4,
                "description": "सामान्य चिकित्सा सलाह",
                "hindi_description": "सामान्य स्थिति - नियमित चेकअप कराएं",
                "action": "Monitor symptoms and consult if worsening",
                "hindi_action": "लक्षणों पर नजर रखें और बिगड़ने पर डॉक्टर से मिलें",
                "color": "green",
                "wait_time": "2-4 hours"
            }
        }

class SymptomExtractor:
    """Extract and process symptoms from patient descriptions"""
    
    def __init__(self):
        self.knowledge_base = MedicalKnowledgeBase()
    
    def extract_symptoms(self, description: str) -> Dict[str, Any]:
        """Extract symptoms from patient description in Hindi or English"""
        
        description_lower = description.lower()
        extracted_symptoms = []
        
        # Check for emergency keywords first
        emergency_level = self._check_emergency_keywords(description_lower)
        
        # Extract symptoms based on keywords
        for condition, info in self.knowledge_base.conditions.items():
            for keyword in info["keywords"]:
                if keyword.lower() in description_lower:
                    severity = self._assess_symptom_severity(condition, description_lower)
                    extracted_symptoms.append({
                        "condition": condition,
                        "hindi_name": info["hindi_name"],
                        "keyword": keyword,
                        "severity": severity
                    })
        
        return {
            "symptoms": extracted_symptoms,
            "emergency_level": emergency_level,
            "description": description,
            "language": self._detect_language(description)
        }
    
    def _check_emergency_keywords(self, text: str) -> str:
        """Check for emergency keywords and return urgency level"""
        text_lower = text.lower()
        
        for level, keywords in self.knowledge_base.emergency_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return level
        
        return "low"
    
    def _assess_symptom_severity(self, condition: str, description: str) -> str:
        """Assess severity of specific symptom based on description"""
        
        # Severity indicators
        severity_indicators = {
            "critical": ["severe", "बहुत ज्यादा", "extreme", "अत्यधिक", "unbearable", "बर्दाश्त नहीं"],
            "high": ["high", "ज्यादा", "persistent", "लगातार", "constant", "स्थिर"],
            "medium": ["moderate", "ठीक-ठाक", "mild", "हल्का", "some", "कुछ"],
            "low": ["slight", "हल्का सा", "mild", "occasional", "कभी-कभी"]
        }
        
        description_lower = description.lower()
        
        for severity, indicators in severity_indicators.items():
            for indicator in indicators:
                if indicator.lower() in description_lower:
                    return severity
        
        return "medium"  # Default severity
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is primarily Hindi or English"""
        hindi_chars = set('ऀँंःऄअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहऺऻ़ऽािीुूृॄॅॆेैॉॊोौ्ॎॏॐ॒॑॓॔ॕॖॗक़ख़ग़ज़ड़ढ़फ़य़ॠॡॢॣ')
        
        hindi_count = sum(1 for char in text if char in hindi_chars)
        english_count = sum(1 for char in text if char.isalpha() and char.isascii())
        
        return "hindi" if hindi_count > english_count else "english"

class MedicalTriageSystem:
    """Main medical triage system for patient assessment"""
    
    def __init__(self):
        self.knowledge_base = MedicalKnowledgeBase()
        self.symptom_extractor = SymptomExtractor()
    
    def triage_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform complete medical triage based on patient data
        
        Args:
            patient_data: Dictionary containing:
                - symptoms: str - patient description
                - age: int - patient age
                - gender: str - patient gender
                - vitals: dict - vital signs
                - duration: int - symptom duration in days
        
        Returns:
            Dict with triage results
        """
        
        try:
            # Extract symptoms
            symptom_analysis = self.symptom_extractor.extract_symptoms(
                patient_data.get("symptoms", "")
            )
            
            # Determine triage level
            triage_level = self._determine_triage_level(
                symptom_analysis,
                patient_data
            )
            
            # Generate recommendations
            recommendations = self._generate_triage_recommendations(
                triage_level,
                symptom_analysis,
                patient_data
            )
            
            # Calculate risk factors
            risk_factors = self._assess_risk_factors(patient_data)
            
            # Create comprehensive report
            report = self._create_triage_report(
                triage_level,
                symptom_analysis,
                recommendations,
                risk_factors
            )
            
            return {
                "triage_level": triage_level,
                "triage_details": self.knowledge_base.triage_levels[triage_level],
                "symptoms_analyzed": symptom_analysis,
                "recommendations": recommendations,
                "risk_factors": risk_factors,
                "report": report,
                "timestamp": datetime.now().isoformat(),
                "triage_complete": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "triage_complete": False,
                "fallback_recommendation": "Please consult a healthcare provider immediately"
            }
    
    def _determine_triage_level(self, symptom_analysis: Dict, patient_data: Dict) -> str:
        """Determine triage level based on symptoms and patient data"""
        
        emergency_level = symptom_analysis.get("emergency_level", "low")
        
        # Emergency keywords take highest priority
        if emergency_level == "critical":
            return "critical"
        elif emergency_level == "high":
            return "high"
        
        # Check symptom severity
        symptoms = symptom_analysis.get("symptoms", [])
        max_severity = "low"
        
        for symptom in symptoms:
            severity = symptom.get("severity", "low")
            if severity == "critical":
                return "critical"
            elif severity == "high" and max_severity != "critical":
                max_severity = "high"
            elif severity == "medium" and max_severity == "low":
                max_severity = "medium"
        
        # Age-based risk assessment
        age = patient_data.get("age", 30)
        if age > 65 or age < 5:
            if max_severity == "high":
                return "high"
            elif max_severity == "medium":
                return "medium"
        
        # Vital signs assessment
        vitals = patient_data.get("vitals", {})
        if self._assess_vital_signs(vitals) == "critical":
            return "critical"
        elif self._assess_vital_signs(vitals) == "high":
            return "high"
        
        # Duration-based assessment
        duration = patient_data.get("duration", 0)
        if duration > 7 and max_severity == "high":
            return "high"
        elif duration > 3 and max_severity == "medium":
            return "medium"
        
        return max_severity
    
    def _assess_vital_signs(self, vitals: Dict[str, Any]) -> str:
        """Assess urgency based on vital signs"""
        
        if not vitals:
            return "low"
        
        # Temperature assessment
        temp = vitals.get("temperature", 98.6)
        if temp > 103:
            return "high"
        elif temp > 101:
            return "medium"
        
        # Blood pressure assessment
        bp = vitals.get("blood_pressure", "120/80")
        if "/" in str(bp):
            systolic = int(str(bp).split("/")[0])
            if systolic > 180 or systolic < 90:
                return "high"
            elif systolic > 160 or systolic < 100:
                return "medium"
        
        # Heart rate assessment
        hr = vitals.get("heart_rate", 70)
        if hr > 120 or hr < 50:
            return "high"
        elif hr > 100 or hr < 60:
            return "medium"
        
        return "low"
    
    def _assess_risk_factors(self, patient_data: Dict[str, Any]) -> List[str]:
        """Assess additional risk factors"""
        
        risk_factors = []
        
        age = patient_data.get("age", 30)
        if age > 65:
            risk_factors.append("Advanced age (>65 years)")
        elif age < 5:
            risk_factors.append("Very young age (<5 years)")
        
        # Pregnancy
        if patient_data.get("gender", "").lower() == "female" and patient_data.get("pregnancy", False):
            risk_factors.append("Pregnancy")
        
        # Chronic conditions
        chronic_conditions = patient_data.get("chronic_conditions", [])
        if chronic_conditions:
            risk_factors.extend(chronic_conditions)
        
        # Recent surgery or hospitalization
        if patient_data.get("recent_surgery", False):
            risk_factors.append("Recent surgery")
        
        return risk_factors
    
    def _generate_triage_recommendations(self, triage_level: str, 
                                       symptom_analysis: Dict, 
                                       patient_data: Dict) -> Dict[str, Any]:
        """Generate specific recommendations based on triage level"""
        
        triage_details = self.knowledge_base.triage_levels[triage_level]
        
        recommendations = {
            "immediate_actions": [],
            "follow_up": [],
            "monitoring": [],
            "hindi_recommendations": []
        }
        
        # Immediate actions
        if triage_level == "critical":
            recommendations["immediate_actions"] = [
                "Call emergency services (108)",
                "Do not delay seeking care",
                "Have someone stay with patient"
            ]
            recommendations["hindi_recommendations"] = [
                "108 पर तुरंत कॉल करें",
                "देरी न करें",
                "किसी को साथ रखें"
            ]
        elif triage_level == "high":
            recommendations["immediate_actions"] = [
                "Visit emergency department within 1-2 hours",
                "Bring medical records",
                "Have someone accompany"
            ]
            recommendations["hindi_recommendations"] = [
                "1-2 घंटे में अस्पताल जाएं",
                "मेडिकल रिकॉर्ड्स लाएं",
                "किसी को साथ लाएं"
            ]
        elif triage_level == "medium":
            recommendations["immediate_actions"] = [
                "Schedule doctor appointment within 24 hours",
                "Monitor symptoms closely",
                "Rest and stay hydrated"
            ]
            recommendations["hindi_recommendations"] = [
                "24 घंटे में डॉक्टर से मिलें",
                "लक्षणों पर नजर रखें",
                "आराम करें और पानी पिएं"
            ]
        else:  # low
            recommendations["immediate_actions"] = [
                "Monitor symptoms",
                "Rest and home care",
                "Consult doctor if symptoms worsen"
            ]
            recommendations["hindi_recommendations"] = [
                "लक्षणों पर नजर रखें",
                "घर पर आराम करें",
                "लक्षण बिगड़ने पर डॉक्टर से मिलें"
            ]
        
        # Follow-up recommendations
        recommendations["follow_up"] = [
            "Keep symptom diary",
            "Note any changes in condition",
            "Follow medication instructions"
        ]
        
        # Monitoring recommendations
        recommendations["monitoring"] = [
            "Check temperature twice daily",
            "Monitor pain levels",
            "Watch for new symptoms"
        ]
        
        return recommendations
    
    def _create_triage_report(self, triage_level: str, 
                            symptom_analysis: Dict, 
                            recommendations: Dict, 
                            risk_factors: List[str]) -> str:
        """Create comprehensive triage report"""
        
        report = []
        report.append("मेडिकल ट्राइएज रिपोर्ट")
        report.append("=" * 30)
        
        # Triage level
        triage_details = self.knowledge_base.triage_levels[triage_level]
        report.append(f"ट्राइएज स्तर: {triage_level.upper()}")
        report.append(f"हिंदी: {triage_details['hindi_description']}")
        report.append(f"प्रतीक्षा समय: {triage_details['wait_time']}")
        report.append("")
        
        # Symptoms
        symptoms = symptom_analysis.get("symptoms", [])
        if symptoms:
            report.append("पहचाने गए लक्षण:")
            for symptom in symptoms:
                report.append(f"- {symptom['hindi_name']} ({symptom['severity']} severity)")
        
        # Risk factors
        if risk_factors:
            report.append("\nजोखिम कारक:")
            for factor in risk_factors:
                report.append(f"- {factor}")
        
        # Recommendations
        report.append("\nसिफारिशें:")
        for rec in recommendations["hindi_recommendations"]:
            report.append(f"- {rec}")
        
        return "\n".join(report)

class MedicalTriageEngine:
    """High-level medical triage engine for backward compatibility"""
    
    def __init__(self):
        """Initialize the triage engine"""
        self.triage_system = MedicalTriageSystem()
    
    def triage_patient(self, patient_data: Dict[str, Any]) -> object:
        """Assess patient and return triage results with expected interface"""
        # Convert PatientData to dict format expected by triage_system
        if hasattr(patient_data, 'to_dict'):
            patient_dict = patient_data.to_dict()
        else:
            patient_dict = patient_data
        
        # Handle symptoms parameter - convert list to string if needed
        symptoms = patient_dict.get('symptoms', '')
        if isinstance(symptoms, list):
            # Convert list of symptom dicts to string
            symptom_strings = []
            for symptom in symptoms:
                if isinstance(symptom, dict):
                    symptom_strings.append(symptom.get('hindi_term', str(symptom)))
                else:
                    symptom_strings.append(str(symptom))
            symptoms = ' '.join(symptom_strings)
        
        # Prepare data for triage system
        triage_input = {
            'symptoms': symptoms,
            'age': patient_dict.get('age', 30),
            'gender': patient_dict.get('gender', 'unknown'),
            'vitals': patient_dict.get('vitals', patient_dict.get('vital_signs', {})),
            'duration': patient_dict.get('duration_hours', 24) // 24  # Convert hours to days
        }
        
        result = self.triage_system.triage_patient(triage_input)
        
        # Create a response object with all required attributes
        class TriageResponse:
            def __init__(self, data):
                self.triage_level = data['triage_level']
                self.urgency_level = type('UrgencyLevel', (), {'value': data['triage_level']})()
                self.risk_score = 0.8 if data['triage_level'] == 'critical' else \
                                0.6 if data['triage_level'] == 'high' else \
                                0.4 if data['triage_level'] == 'medium' else 0.2
                self.recommendations = data['recommendations']['hindi_recommendations']
                self.follow_up_hours = 0 if data['triage_level'] == 'critical' else \
                                      2 if data['triage_level'] == 'high' else \
                                      24 if data['triage_level'] == 'medium' else 48
                self.specialist_needed = data['triage_level'] in ['critical', 'high']
                self.escalation_required = data['triage_level'] in ['critical', 'high']
                self.report = data['report']
                self.triage_complete = data.get('triage_complete', True)
                self.risk_factors = data.get('risk_factors', [])
                self.symptoms_analyzed = data.get('symptoms_analyzed', {})
                
                # Add triage_action attribute for compatibility
                self.triage_action = type('TriageAction', (), {'value': data['triage_details']['hindi_action']})()
        
        return TriageResponse(result)
    
    def generate_triage_report(self, assessment: Dict[str, Any]) -> str:
        """Generate triage report"""
        return assessment.get('report', '')
    
    def process_symptoms(self, symptoms_text: str) -> Dict[str, Any]:
        """Process symptoms text and return analysis"""
        return self.triage_system.symptom_extractor.extract_symptoms(symptoms_text)

# Add compatibility aliases
TriageSystem = MedicalTriageSystem
SymptomAnalyzer = SymptomExtractor

# Test the system
if __name__ == "__main__":
    triage_system = MedicalTriageSystem()
    
    # Test cases
    test_cases = [
        {
            "symptoms": "मुझे बुखार है और सरदर्द है",
            "vital_signs": {"temperature": 102.5, "blood_pressure": "120/80"},
            "age": 35,
            "medical_history": ["diabetes"]
        },
        {
            "symptoms": "I have severe chest pain and difficulty breathing",
            "vital_signs": {"temperature": 98.6, "blood_pressure": "140/90"},
            "age": 45,
            "medical_history": ["hypertension"]
        }
    ]
    
    print("Testing Medical Triage System...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        result = triage.assess_patient(test_case)
        print(f"Triage Level: {result['triage_level']}")
        print(f"Risk Score: {result['risk_score']}")
        print(f"Recommendations: {result['recommendations']}")
        print("-" * 50)


class PatientData:
    """Data class for patient information"""
    
    def __init__(self, name: str = "", age: int = 0, gender: str = "", 
                 symptoms: str = "", medical_history: List[str] = None,
                 vitals: Dict[str, Any] = None, vital_signs: Dict[str, Any] = None,
                 duration_hours: int = 0, severity_score: float = 0.0,
                 xray_findings: List[str] = None, lab_results: Dict[str, Any] = None):
        self.name = name
        self.age = age
        self.gender = gender
        self.symptoms = symptoms
        self.medical_history = medical_history or []
        
        # Handle both vitals and vital_signs parameters for backward compatibility
        if vital_signs is not None:
            self.vitals = vital_signs
        else:
            self.vitals = vitals or {}
            
        # Additional parameters for test compatibility
        self.duration_hours = duration_hours
        self.severity_score = severity_score
        self.xray_findings = xray_findings or []
        self.lab_results = lab_results or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "symptoms": self.symptoms,
            "medical_history": self.medical_history,
            "vitals": self.vitals,
            "vital_signs": self.vitals,  # Backward compatibility
            "duration_hours": self.duration_hours,
            "severity_score": self.severity_score,
            "xray_findings": self.xray_findings,
            "lab_results": self.lab_results,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PatientData':
        """Create PatientData from dictionary"""
        patient = cls(
            name=data.get("name", ""),
            age=data.get("age", 0),
            gender=data.get("gender", ""),
            symptoms=data.get("symptoms", ""),
            medical_history=data.get("medical_history", []),
            vitals=data.get("vitals", data.get("vital_signs", {})),
            duration_hours=data.get("duration_hours", 0),
            severity_score=data.get("severity_score", 0.0),
            xray_findings=data.get("xray_findings", []),
            lab_results=data.get("lab_results", {})
        )
        if "timestamp" in data:
            patient.timestamp = datetime.fromisoformat(data["timestamp"])
        return patient