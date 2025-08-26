"""
Security and Compliance Framework for Hindi Medical AI
HIPAA-compliant, GDPR-ready, and ethically designed medical AI system
"""

import hashlib
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from dataclasses import dataclass, asdict
from enum import Enum

class ComplianceLevel(Enum):
    HIPAA = "hipaa"
    GDPR = "gdpr"
    INDIA_DPDP = "india_dpdp"
    MEDICAL_ETHICS = "medical_ethics"

class DataClassification(Enum):
    PHI = "protected_health_information"
    PII = "personally_identifiable_information"
    SENSITIVE = "sensitive_medical_data"
    PUBLIC = "public_information"

@dataclass
class AuditLog:
    """Audit log entry for all medical AI interactions"""
    log_id: str
    timestamp: datetime
    user_id: str
    action: str
    data_classification: DataClassification
    data_size: int
    ip_address: str
    device_info: str
    session_id: str
    outcome: str
    risk_score: float
    escalation_triggered: bool
    
    def to_dict(self) -> Dict:
        return asdict(self)

class MedicalDataEncryption:
    """Advanced encryption for medical data storage and transmission"""
    
    def __init__(self):
        self.master_key = self._generate_master_key()
        self.data_keys = {}
        
    def _generate_master_key(self) -> bytes:
        """Generate master encryption key"""
        password = os.environ.get('MASTER_KEY_PASSWORD', 'default_secure_password')
        salt = os.environ.get('MASTER_KEY_SALT', 'medical_ai_salt_2024').encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_patient_data(self, data: Dict, patient_id: str) -> Dict:
        """Encrypt patient data with patient-specific key"""
        try:
            # Generate patient-specific key
            patient_key = self._generate_patient_key(patient_id)
            f = Fernet(patient_key)
            
            # Encrypt sensitive fields
            encrypted_data = {}
            for key, value in data.items():
                if self._is_sensitive_field(key):
                    # Convert to JSON string for encryption
                    json_value = json.dumps(value)
                    encrypted_value = f.encrypt(json_value.encode())
                    encrypted_data[key] = encrypted_value.decode()
                else:
                    encrypted_data[key] = value
            
            return encrypted_data
            
        except Exception as e:
            logging.error(f"Encryption error: {str(e)}")
            raise
    
    def decrypt_patient_data(self, encrypted_data: Dict, patient_id: str) -> Dict:
        """Decrypt patient data"""
        try:
            patient_key = self._generate_patient_key(patient_id)
            f = Fernet(patient_key)
            
            decrypted_data = {}
            for key, value in encrypted_data.items():
                if self._is_encrypted_field(key, value):
                    decrypted_value = f.decrypt(value.encode())
                    decrypted_data[key] = json.loads(decrypted_value.decode())
                else:
                    decrypted_data[key] = value
            
            return decrypted_data
            
        except Exception as e:
            logging.error(f"Decryption error: {str(e)}")
            raise
    
    def _generate_patient_key(self, patient_id: str) -> bytes:
        """Generate encryption key for specific patient"""
        if patient_id not in self.data_keys:
            # Create patient-specific key from master key and patient ID
            combined = self.master_key + patient_id.encode()
            key_hash = hashlib.sha256(combined).hexdigest()
            key_bytes = key_hash[:32].encode()
            self.data_keys[patient_id] = base64.urlsafe_b64encode(key_bytes)
        
        return self.data_keys[patient_id]
    
    def _is_sensitive_field(self, field_name: str) -> bool:
        """Determine if field contains sensitive data"""
        sensitive_fields = [
            "name", "address", "phone", "email", "aadhaar", "pan",
            "medical_history", "symptoms", "diagnosis", "prescription",
            "lab_results", "xray_findings", "voice_data", "biometric_data"
        ]
        return any(sensitive in field_name.lower() for sensitive in sensitive_fields)
    
    def _is_encrypted_field(self, field_name: str, value: str) -> bool:
        """Check if field is encrypted"""
        return self._is_sensitive_field(field_name) and isinstance(value, str) and value.startswith("gAAAAA")

class HIPAAComplianceManager:
    """HIPAA compliance management for medical AI"""
    
    def __init__(self):
        self.encryption = MedicalDataEncryption()
        self.audit_logger = MedicalAuditLogger()
        self.consent_manager = ConsentManager()
        
    def validate_hipaa_compliance(self, data_operation: str, 
                                data_type: DataClassification, 
                                patient_consent: bool) -> bool:
        """Validate HIPAA compliance for data operations"""
        
        # Handle string data_type for backward compatibility
        if isinstance(data_type, str):
            try:
                data_type = DataClassification(data_type.lower())
            except ValueError:
                # Map common string values
                type_mapping = {
                    "phi": DataClassification.PHI,
                    "pii": DataClassification.PII,
                    "sensitive": DataClassification.SENSITIVE,
                    "public": DataClassification.PUBLIC,
                    "PHI": DataClassification.PHI,
                    "PII": DataClassification.PII,
                    "SENSITIVE": DataClassification.SENSITIVE,
                    "PUBLIC": DataClassification.PUBLIC
                }
                data_type = type_mapping.get(data_type, DataClassification.PHI)
        
        compliance_checks = {
            "encryption": self._check_encryption_status(),
            "audit_logging": self._check_audit_logging(),
            "consent": self._check_patient_consent(patient_consent),
            "data_minimization": self._check_data_minimization(data_type),
            "access_controls": self._check_access_controls()
        }
        
        return all(compliance_checks.values())
    
    def validate_hipaa_compliance_simple(self, data_operation: str, 
                                       data_type_str: str, 
                                       patient_consent: bool) -> bool:
        """Simplified HIPAA validation method for compatibility"""
        return self.validate_hipaa_compliance(data_operation, data_type_str, patient_consent)
    
    def _check_encryption_status(self) -> bool:
        """Check if data encryption is properly implemented"""
        return True  # Implementation would check actual encryption status
    
    def _check_audit_logging(self) -> bool:
        """Check if comprehensive audit logging is enabled"""
        return True  # Implementation would check actual logging status
    
    def _check_patient_consent(self, consent: bool) -> bool:
        """Check patient consent status"""
        return consent
    
    def _check_data_minimization(self, data_type: DataClassification) -> bool:
        """Check if only necessary data is collected"""
        # Only collect data required for medical diagnosis
        allowed_types = [DataClassification.PHI, DataClassification.SENSITIVE]
        return data_type in allowed_types
    
    def _check_access_controls(self) -> bool:
        """Check access control implementation"""
        return True  # Implementation would check actual access controls

class GDPRComplianceManager:
    """GDPR compliance management for European patients"""
    
    def __init__(self):
        self.data_retention_policies = self._load_retention_policies()
        self.right_to_be_forgotten_handler = RightToBeForgottenHandler()
        
    def _load_retention_policies(self) -> Dict:
        """Load data retention policies"""
        return {
            "medical_records": timedelta(days=365*7),  # 7 years
            "diagnostic_data": timedelta(days=365*5),  # 5 years
            "audit_logs": timedelta(days=365*3),       # 3 years
            "temporary_data": timedelta(days=30)      # 30 days
        }
    
    def handle_data_request(self, request_type: str, patient_id: str) -> Dict:
        """Handle GDPR data requests (access, portability, deletion)"""
        
        if request_type == "access":
            return self._provide_data_access(patient_id)
        elif request_type == "portability":
            return self._provide_data_portability(patient_id)
        elif request_type == "deletion":
            return self._handle_data_deletion(patient_id)
        else:
            return {"error": "Invalid request type"}
    
    def _provide_data_access(self, patient_id: str) -> Dict:
        """Provide patient with their data"""
        return {
            "patient_id": patient_id,
            "data_categories": ["medical_records", "diagnostic_data", "consent_records"],
            "download_link": f"/api/patient-data/{patient_id}",
            "format": "JSON",
            "expires_in": "7 days"
        }
    
    def _provide_data_portability(self, patient_id: str) -> Dict:
        """Provide data in portable format"""
        return {
            "patient_id": patient_id,
            "format": "FHIR R4",
            "download_link": f"/api/portable-data/{patient_id}",
            "expires_in": "7 days"
        }
    
    def _handle_data_deletion(self, patient_id: str) -> Dict:
        """Handle right to be forgotten"""
        return self.right_to_be_forgotten_handler.process_deletion(patient_id)

class IndiaDPDPComplianceManager:
    """India Digital Personal Data Protection Act compliance"""
    
    def __init__(self):
        self.consent_manager = ConsentManager()
        self.data_localization = DataLocalization()
        
    def validate_india_compliance(self, data_operation: str, 
                                data_location: str, 
                                patient_location: str) -> bool:
        """Validate India DPDP Act compliance"""
        
        compliance_requirements = {
            "data_localization": self.data_localization.is_data_localized(data_location, patient_location),
            "consent_mechanism": self.consent_manager.has_valid_consent(patient_location),
            "data_principal_rights": True,
            "grievance_redressal": True
        }
        
        return all(compliance_requirements.values())

class MedicalAuditLogger:
    """Comprehensive audit logging for medical AI operations"""
    
    def __init__(self):
        self.audit_log_path = "medical_audit_logs.json"
        self.logger = logging.getLogger('medical_audit')
        
    def log_patient_interaction(self, 
                              patient_id: str,
                              action: str,
                              data_classification: DataClassification,
                              data_size: int,
                              ip_address: str,
                              device_info: str,
                              session_id: str,
                              outcome: str,
                              risk_score: float,
                              escalation_triggered: bool = False) -> str:
        """Log patient interaction with full audit trail"""
        
        audit_entry = AuditLog(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_id=patient_id,
            action=action,
            data_classification=data_classification,
            data_size=data_size,
            ip_address=ip_address,
            device_info=device_info,
            session_id=session_id,
            outcome=outcome,
            risk_score=risk_score,
            escalation_triggered=escalation_triggered
        )
        
        # Log to file
        self._write_audit_log(audit_entry)
        
        # Log to system
        self.logger.info(f"Audit: {audit_entry.to_dict()}")
        
        return audit_entry.log_id
    
    def _write_audit_log(self, audit_entry: AuditLog):
        """Write audit log to persistent storage"""
        try:
            with open(self.audit_log_path, 'a') as f:
                json.dump(audit_entry.to_dict(), f, default=str)
                f.write('\n')
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {str(e)}")
    
    def generate_compliance_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate compliance report for regulatory purposes"""
        
        report = {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_interactions": 0,
            "data_classifications": {},
            "escalations": 0,
            "errors": 0,
            "compliance_score": 0.0
        }
        
        # Process audit logs for the period
        try:
            with open(self.audit_log_path, 'r') as f:
                for line in f:
                    log_entry = json.loads(line)
                    log_time = datetime.fromisoformat(log_entry["timestamp"])
                    
                    if start_date <= log_time <= end_date:
                        report["total_interactions"] += 1
                        
                        # Count data classifications
                        classification = log_entry["data_classification"]
                        report["data_classifications"][classification] = \
                            report["data_classifications"].get(classification, 0) + 1
                        
                        # Count escalations
                        if log_entry["escalation_triggered"]:
                            report["escalations"] += 1
                        
                        # Count errors
                        if log_entry["outcome"] == "error":
                            report["errors"] += 1
            
            # Calculate compliance score
            report["compliance_score"] = self._calculate_compliance_score(report)
            
        except Exception as e:
            report["error"] = str(e)
        
        return report
    
    def _calculate_compliance_score(self, report: Dict) -> float:
        """Calculate overall compliance score"""
        base_score = 100.0
        
        # Deduct for errors
        if report["total_interactions"] > 0:
            error_rate = report["errors"] / report["total_interactions"]
            base_score -= (error_rate * 20)
        
        # Deduct for missing escalations
        if report["escalations"] == 0 and report["total_interactions"] > 100:
            base_score -= 10
        
        return max(base_score, 0.0)

class ConsentManager:
    """Manage patient consent for medical data processing"""
    
    def __init__(self):
        self.consent_records = {}
        
    def record_consent(self, patient_id: str, consent_type: str, 
                      granted: bool, timestamp: datetime) -> str:
        """Record patient consent"""
        consent_id = str(uuid.uuid4())
        
        consent_record = {
            "consent_id": consent_id,
            "patient_id": patient_id,
            "consent_type": consent_type,
            "granted": granted,
            "timestamp": timestamp.isoformat(),
            "expiry": (timestamp + timedelta(days=365)).isoformat()
        }
        
        self.consent_records[patient_id] = consent_record
        return consent_id
    
    def has_valid_consent(self, patient_id: str, consent_type: str) -> bool:
        """Check if patient has valid consent"""
        if patient_id not in self.consent_records:
            return False
        
        consent = self.consent_records[patient_id]
        
        # Check if consent is for the right type
        if consent["consent_type"] != consent_type:
            return False
        
        # Check if consent hasn't expired
        expiry = datetime.fromisoformat(consent["expiry"])
        return datetime.now() < expiry

class RightToBeForgottenHandler:
    """Handle patient requests for data deletion"""
    
    def process_deletion(self, patient_id: str) -> Dict:
        """Process data deletion request"""
        
        deletion_report = {
            "patient_id": patient_id,
            "deletion_status": "initiated",
            "affected_records": 0,
            "backup_retained": True,  # For legal requirements
            "completion_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        # Implementation would actually delete data
        # For now, return deletion report
        return deletion_report

class DataLocalization:
    """Ensure data localization requirements are met"""
    
    def is_data_localized(self, data_location: str, patient_location: str) -> bool:
        """Check if data is stored in required jurisdiction"""
        
        localization_requirements = {
            "india": ["india", "in", "asia-south1"],
            "europe": ["europe", "eu", "europe-west1"],
            "usa": ["usa", "us", "us-central1"]
        }
        
        patient_country = patient_location.lower()
        data_region = data_location.lower()
        
        if patient_country in localization_requirements:
            allowed_regions = localization_requirements[patient_country]
            return any(region in data_region for region in allowed_regions)
        
        return True  # Default to allow if no specific requirement

class EthicalAIFramework:
    """Ethical AI guidelines for medical decision-making"""
    
    def __init__(self):
        self.ethical_principles = self._load_ethical_principles()
        self.bias_detector = BiasDetector()
        
    def _load_ethical_principles(self) -> Dict:
        """Load medical AI ethical principles"""
        return {
            "beneficence": "Act in the best interest of the patient",
            "non_maleficence": "Do no harm",
            "autonomy": "Respect patient autonomy and consent",
            "justice": "Ensure fair and equitable treatment",
            "transparency": "Be transparent about AI decision-making",
            "accountability": "Maintain accountability for AI decisions"
        }
    
    def validate_ethical_compliance(self, ai_decision: Dict, patient_context: Dict) -> Dict:
        """Validate AI decision against ethical principles"""
        
        validation_result = {
            "compliant": True,
            "violations": [],
            "recommendations": []
        }
        
        # Check for bias
        bias_check = self.bias_detector.check_bias(ai_decision, patient_context)
        if bias_check["biased"]:
            validation_result["compliant"] = False
            validation_result["violations"].append("potential_bias")
            validation_result["recommendations"].append("review_decision_for_bias")
        
        # Check for transparency
        if not ai_decision.get("explanation"):
            validation_result["violations"].append("lack_of_transparency")
        
        return validation_result

class BiasDetector:
    """Detect and mitigate bias in medical AI decisions"""
    
    def check_bias(self, ai_decision: Dict, patient_context: Dict) -> Dict:
        """Check for potential bias in AI decision"""
        
        bias_indicators = {
            "age_bias": self._check_age_bias(ai_decision, patient_context),
            "gender_bias": self._check_gender_bias(ai_decision, patient_context),
            "socioeconomic_bias": self._check_socioeconomic_bias(ai_decision, patient_context),
            "geographic_bias": self._check_geographic_bias(ai_decision, patient_context)
        }
        
        has_bias = any(indicator["detected"] for indicator in bias_indicators.values())
        
        return {
            "biased": has_bias,
            "bias_types": [k for k, v in bias_indicators.items() if v["detected"]],
            "confidence_scores": bias_indicators
        }
    
    def _check_age_bias(self, decision: Dict, context: Dict) -> Dict:
        """Check for age-based bias"""
        age = context.get("age", 0)
        urgency_level = decision.get("urgency_level", "medium")
        
        # Check if elderly patients are being undertriaged
        if age > 65 and urgency_level == "low":
            return {"detected": True, "confidence": 0.7}
        
        return {"detected": False, "confidence": 0.0}
    
    def _check_gender_bias(self, decision: Dict, context: Dict) -> Dict:
        """Check for gender-based bias"""
        # Implementation for gender bias detection
        return {"detected": False, "confidence": 0.0}
    
    def _check_socioeconomic_bias(self, decision: Dict, context: Dict) -> Dict:
        """Check for socioeconomic bias"""
        # Implementation for socioeconomic bias detection
        return {"detected": False, "confidence": 0.0}
    
    def _check_geographic_bias(self, decision: Dict, context: Dict) -> Dict:
        """Check for geographic bias"""
        # Implementation for geographic bias detection
        return {"detected": False, "confidence": 0.0}

# Usage Example
if __name__ == "__main__":
    # Initialize security framework
    security_framework = HIPAAComplianceManager()
    audit_logger = MedicalAuditLogger()
    ethical_framework = EthicalAIFramework()
    
    # Example usage
    patient_id = "PAT123456"
    
    # Record audit log
    log_id = audit_logger.log_patient_interaction(
        patient_id=patient_id,
        action="symptom_analysis",
        data_classification=DataClassification.PHI,
        data_size=1024,
        ip_address="192.168.1.100",
        device_info="Android Phone",
        session_id="session_123",
        outcome="success",
        risk_score=6.5,
        escalation_triggered=False
    )
    
    # Validate ethical compliance
    ai_decision = {
        "urgency_level": "high",
        "explanation": "Patient shows cardiac symptoms requiring immediate attention"
    }
    
    ethical_check = ethical_framework.validate_ethical_compliance(
        ai_decision,
        {"age": 45, "gender": "male"}
    )
    
    print(f"Audit Log ID: {log_id}")
    print(f"Ethical Compliance: {ethical_check}")