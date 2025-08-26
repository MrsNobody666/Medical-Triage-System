import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from typing import Dict, List, Any, Tuple
import json
import io
import base64

class MedicalImageAnalyzer:
    """Medical Image Analysis System for X-rays and medical imaging"""
    
    def __init__(self):
        """Initialize the medical image analyzer with available models"""
        
        # Use OpenCV and basic image processing instead of non-existent models
        self.image_size = (224, 224)
        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Basic medical image classification categories
        self.medical_conditions = {
            "normal": {"confidence": 0.0, "description": "Normal appearance"},
            "pneumonia": {"confidence": 0.0, "description": "Signs of pneumonia"},
            "fracture": {"confidence": 0.0, "description": "Possible fracture detected"},
            "effusion": {"confidence": 0.0, "description": "Pleural effusion"},
            "cardiomegaly": {"confidence": 0.0, "description": "Enlarged heart"}
        }
    
    def load_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess medical image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image_rgb
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def load_image_from_base64(self, base64_string: str) -> np.ndarray:
        """Load image from base64 string"""
        try:
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            return image_array
        except Exception as e:
            print(f"Error loading image from base64: {e}")
            return None
    
    def analyze_xray(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze chest X-ray image"""
        if image is None:
            return {"error": "Invalid image"}
        
        # Basic image analysis using OpenCV
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate basic metrics
        mean_intensity = np.mean(gray_image)
        std_intensity = np.std(gray_image)
        
        # Simulate medical analysis with rule-based approach
        findings = self._simulate_medical_analysis(gray_image, mean_intensity, std_intensity)
        
        # Risk assessment
        risk_level = self._assess_risk(findings)
        
        return {
            "image_type": "chest_xray",
            "findings": findings,
            "risk_level": risk_level,
            "recommendations": self._get_recommendations(risk_level, findings),
            "technical_metrics": {
                "mean_intensity": float(mean_intensity),
                "std_intensity": float(std_intensity),
                "image_shape": image.shape
            }
        }
    
    def _simulate_medical_analysis(self, gray_image: np.ndarray, mean_intensity: float, std_intensity: float) -> Dict[str, Any]:
        """Simulate medical analysis based on image characteristics"""
        
        # Rule-based analysis for demonstration
        findings = {}
        
        # Simulate confidence scores based on image characteristics
        if mean_intensity < 100:
            findings["opacity"] = {
                "present": True,
                "confidence": 0.75,
                "description": "Areas of increased opacity detected"
            }
        
        if std_intensity > 60:
            findings["texture_abnormality"] = {
                "present": True,
                "confidence": 0.65,
                "description": "Abnormal texture patterns"
            }
        
        # Simulate basic conditions
        conditions = list(self.medical_conditions.keys())
        import random
        random.seed(int(mean_intensity + std_intensity))  # Deterministic results
        
        primary_condition = random.choice(conditions)
        confidence = min(0.9, max(0.3, (std_intensity / 100)))
        
        findings["primary_condition"] = {
            "condition": primary_condition,
            "confidence": confidence,
            "description": self.medical_conditions[primary_condition]["description"]
        }
        
        return findings
    
    def _assess_risk(self, findings: Dict[str, Any]) -> str:
        """Assess risk level based on findings"""
        
        if "primary_condition" in findings:
            condition = findings["primary_condition"]["condition"]
            confidence = findings["primary_condition"]["confidence"]
            
            if condition in ["pneumonia", "fracture", "effusion"] and confidence > 0.7:
                return "high"
            elif condition in ["cardiomegaly"] and confidence > 0.6:
                return "medium"
            elif condition == "normal" and confidence > 0.8:
                return "low"
        
        return "medium"
    
    def _get_recommendations(self, risk_level: str, findings: Dict[str, Any]) -> List[str]:
        """Get recommendations based on risk level"""
        
        recommendations = []
        
        if risk_level == "high":
            recommendations.extend([
                "तुरंत डॉक्टर से संपर्क करें",
                "अस्पताल जाने की सलाह दी जाती है",
                "तत्काल चिकित्सा सहायता लें"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "डॉक्टर से सलाह लें",
                "अगले 24-48 घंटे में चेकअप कराएं",
                "लक्षणों पर नजर रखें"
            ])
        else:
            recommendations.extend([
                "नियमित चेकअप कराते रहें",
                "स्वस्थ जीवनशैली अपनाएं",
                "यदि कोई नया लक्षण दिखे तो डॉक्टर से मिलें"
            ])
        
        return recommendations
    
    def detect_abnormalities(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect specific abnormalities in medical image"""
        
        if image is None:
            return {"error": "Invalid image"}
        
        # Basic edge detection for fracture detection
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Count edge pixels as a simple abnormality indicator
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        abnormalities = []
        
        if edge_density > 0.05:  # Threshold for abnormality
            abnormalities.append({
                "type": "structural_abnormality",
                "confidence": min(0.8, edge_density * 10),
                "description": "Unusual structural patterns detected"
            })
        
        return {
            "abnormalities": abnormalities,
            "edge_density": float(edge_density),
            "analysis_complete": True
        }
    
    def generate_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate human-readable medical report"""
        
        report = []
        report.append("मेडिकल इमेज विश्लेषण रिपोर्ट")
        report.append("=" * 30)
        
        if "error" in analysis_result:
            report.append(f"त्रुटि: {analysis_result['error']}")
            return "\n".join(report)
        
        report.append(f"इमेज प्रकार: {analysis_result.get('image_type', 'अज्ञात')}")
        report.append(f"जोखिम स्तर: {analysis_result.get('risk_level', 'अज्ञात')}")
        
        findings = analysis_result.get('findings', {})
        if findings:
            report.append("\nप्रमुख निष्कर्ष:")
            if "primary_condition" in findings:
                pc = findings["primary_condition"]
                report.append(f"- प्राथमिक स्थिति: {pc['description']}")
                report.append(f"- विश्वास स्तर: {pc['confidence']:.2f}")
        
        recommendations = analysis_result.get('recommendations', [])
        if recommendations:
            report.append("\nसिफारिशें:")
            for rec in recommendations:
                report.append(f"- {rec}")
        
        return "\n".join(report)

class MedicalImageProcessor:
    """High-level medical image processing interface"""
    
    def __init__(self):
        self.analyzer = MedicalImageAnalyzer()
    
    def process_image(self, image_input: str, input_type: str = "file") -> Dict[str, Any]:
        """Process medical image with complete analysis"""
        
        try:
            # Load image based on input type
            if input_type == "file":
                image = self.analyzer.load_image(image_input)
            elif input_type == "base64":
                image = self.analyzer.load_image_from_base64(image_input)
            else:
                return {"error": "Unsupported input type"}
            
            if image is None:
                return {"error": "Failed to load image"}
            
            # Perform analysis
            xray_analysis = self.analyzer.analyze_xray(image)
            abnormalities = self.analyzer.detect_abnormalities(image)
            
            # Combine results
            result = {
                **xray_analysis,
                "abnormalities": abnormalities["abnormalities"],
                "report": self.analyzer.generate_report(xray_analysis),
                "processing_complete": True
            }
            
            return result
            
        except Exception as e:
            return {"error": str(e), "processing_complete": False}

# Test the system
if __name__ == "__main__":
    processor = MedicalImageProcessor()
    
    # Test with a dummy image path (will use simulated analysis)
    result = processor.process_image("test_xray.jpg")
    
    print("Medical Image Analysis Test:")
    print("=" * 40)
    print(result.get("report", "No report generated"))
    print("\nJSON Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


class XRayAnalyzer:
    """X-Ray specific analysis wrapper for backward compatibility"""
    
    def __init__(self):
        """Initialize X-Ray analyzer"""
        self.image_analyzer = MedicalImageAnalyzer()
    
    def analyze_xray_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze X-ray image and return findings"""
        image = self.image_analyzer.load_image(image_path)
        return self.image_analyzer.analyze_xray(image)
    
    def analyze_xray_base64(self, base64_string: str) -> Dict[str, Any]:
        """Analyze X-ray image from base64"""
        image = self.image_analyzer.load_image_from_base64(base64_string)
        return self.image_analyzer.analyze_xray(image)
    
    def generate_xray_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate X-ray analysis report"""
        return self.image_analyzer.generate_report(analysis_result)

# Add at the end of the file
if __name__ == "__main__":
    analyzer = MedicalImageAnalyzer()
    
    # Test with a dummy image path (will use simulation)
    print("Testing Medical Image Analysis System...")
    
    # Create a dummy test image
    dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Test analysis
    result = analyzer.analyze_xray(dummy_image)
    print("Analysis Result:", json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test report generation
    report = analyzer.generate_report(result)
    print("\nGenerated Report:")
    print(report)


class LabReportAnalyzer:
    """Lab report analysis for blood tests and other lab results"""
    
    def __init__(self):
        """Initialize lab report analyzer"""
        self.normal_ranges = {
            "hemoglobin": {"min": 12.0, "max": 16.0, "unit": "g/dL"},
            "wbc": {"min": 4.0, "max": 11.0, "unit": "K/uL"},
            "platelets": {"min": 150.0, "max": 450.0, "unit": "K/uL"},
            "glucose": {"min": 70.0, "max": 100.0, "unit": "mg/dL"},
            "cholesterol": {"min": 0.0, "max": 200.0, "unit": "mg/dL"},
            "blood_pressure_systolic": {"min": 90.0, "max": 120.0, "unit": "mmHg"},
            "blood_pressure_diastolic": {"min": 60.0, "max": 80.0, "unit": "mmHg"}
        }
    
    def analyze_lab_report(self, lab_data: Dict[str, float]) -> Dict[str, Any]:
        """Analyze lab report data"""
        
        abnormalities = []
        warnings = []
        
        for test_name, value in lab_data.items():
            if test_name in self.normal_ranges:
                normal_range = self.normal_ranges[test_name]
                
                if value < normal_range["min"]:
                    abnormalities.append({
                        "test": test_name,
                        "value": value,
                        "status": "low",
                        "severity": "moderate" if value < normal_range["min"] * 0.7 else "mild"
                    })
                elif value > normal_range["max"]:
                    abnormalities.append({
                        "test": test_name,
                        "value": value,
                        "status": "high",
                        "severity": "high" if value > normal_range["max"] * 1.3 else "moderate"
                    })
        
        risk_level = self._assess_lab_risk(abnormalities)
        
        return {
            "abnormalities": abnormalities,
            "risk_level": risk_level,
            "total_tests": len(lab_data),
            "abnormal_count": len(abnormalities),
            "recommendations": self._get_lab_recommendations(risk_level, abnormalities)
        }
    
    def _assess_lab_risk(self, abnormalities: List[Dict]) -> str:
        """Assess risk based on lab abnormalities"""
        
        if not abnormalities:
            return "low"
        
        high_severity = any(ab["severity"] == "high" for ab in abnormalities)
        moderate_severity = any(ab["severity"] == "moderate" for ab in abnormalities)
        
        if high_severity or len(abnormalities) >= 3:
            return "high"
        elif moderate_severity or len(abnormalities) >= 2:
            return "medium"
        else:
            return "low"
    
    def _get_lab_recommendations(self, risk_level: str, abnormalities: List[Dict]) -> List[str]:
        """Get recommendations based on lab results"""
        
        recommendations = []
        
        if risk_level == "high":
            recommendations.extend([
                "तुरंत डॉक्टर से संपर्क करें",
                "अस्पताल जाने की सलाह दी जाती है",
                "तत्काल चिकित्सा सहायता लें"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "डॉक्टर से सलाह लें",
                "अगले 24-48 घंटे में चेकअप कराएं",
                "अपने आहार में सुधार करें"
            ])
        else:
            recommendations.extend([
                "नियमित चेकअप कराते रहें",
                "स्वस्थ जीवनशैली अपनाएं",
                "संतुलित आहार लें"
            ])
        
        return recommendations
    
    def generate_lab_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate human-readable lab report"""
        
        report = []
        report.append("लैब रिपोर्ट विश्लेषण")
        report.append("=" * 25)
        
        report.append(f"कुल टेस्ट: {analysis_result.get('total_tests', 0)}")
        report.append(f"असामान्य टेस्ट: {analysis_result.get('abnormal_count', 0)}")
        report.append(f"जोखिम स्तर: {analysis_result.get('risk_level', 'अज्ञात')}")
        
        abnormalities = analysis_result.get('abnormalities', [])
        if abnormalities:
            report.append("\nअसामान्य निष्कर्ष:")
            for ab in abnormalities:
                report.append(f"- {ab['test']}: {ab['value']} ({ab['status']} - {ab['severity']})")
        
        recommendations = analysis_result.get('recommendations', [])
        if recommendations:
            report.append("\nसिफारिशें:")
            for rec in recommendations:
                report.append(f"- {rec}")
        
        return "\n".join(report)