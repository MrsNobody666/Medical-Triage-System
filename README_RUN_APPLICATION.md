# Hindi Personal Voice AI Doctor - Complete Running Guide

## 🩺 Overview
This guide provides complete instructions for running the Hindi Personal Voice AI Doctor system, a comprehensive medical triaging application designed specifically for Hindi-speaking patients.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10/11, Linux, or macOS
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space for models and data

### Required Python Packages
Install dependencies using:
```bash
pip install torch transformers pandas numpy opencv-python scikit-learn
pip install pydicom pillow reportlab cryptography
pip install indic-nlp-library spacy
```

### Optional Dependencies (for enhanced functionality)
```bash
pip install flask flask-cors  # For web interface
pip install speechrecognition   # For voice input
pip install pyttsx3            # For voice output
```

## 🚀 Quick Start

### 1. Basic Demo Mode
Run the complete system demonstration:
```bash
python run_hindi_ai_doctor.py --mode demo
```

### 2. Interactive Mode
Start interactive Hindi conversation mode:
```bash
python run_hindi_ai_doctor.py --mode interactive
```

### 3. Batch Processing
Process multiple patients from a JSON file:
```bash
python run_hindi_ai_doctor.py --mode batch --input sample_batch_input.json
```

### 4. System Testing
Run comprehensive system tests:
```bash
python run_hindi_ai_doctor.py --mode test
```

## 🔧 Running Modes Explained

### Demo Mode (--mode demo)
- **Purpose**: Complete system demonstration
- **Features**: 
  - Simulated patient conversation in Hindi
  - Real-time triaging
  - Image analysis demonstration
  - Risk assessment display
- **Duration**: ~30 seconds
- **Output**: Console display with medical assessment

### Interactive Mode (--mode interactive)
- **Purpose**: Real patient interaction
- **Features**:
  - Live Hindi conversation
  - Instant medical triaging
  - Personalized recommendations
  - Emergency detection
- **Usage**: Type Hindi symptoms and receive medical advice
- **Example Input**: "नमस्ते डॉक्टर, मुझे सीने में दर्द हो रहा है"

### Batch Mode (--mode batch)
- **Purpose**: Process multiple patients automatically
- **Features**:
  - JSON input file processing
  - Bulk triaging
  - Results export
  - Audit logging
- **Input Format**: JSON array of patient records
- **Output**: JSON file with triaging results

### Test Mode (--mode test)
- **Purpose**: System validation
- **Features**:
  - Component testing
  - Model validation
  - Security checks
  - Performance metrics

## 📁 File Structure

```
Hindi-AI-Doctor/
├── run_hindi_ai_doctor.py          # Main application runner
├── hindi_medical_nlp_system.py     # Hindi NLP engine
├── medical_image_analysis.py       # Image analysis system
├── medical_triage_system.py        # Triage and risk assessment
├── security_compliance_framework.py # Security & compliance
├── implementation_roadmap.py       # Deployment strategy
├── sample_batch_input.json         # Sample batch input
├── README_RUN_APPLICATION.md       # This guide
└── hindi_ai_doctor.log            # Application logs
```

## 🎯 Usage Examples

### Example 1: Interactive Session
```bash
$ python run_hindi_ai_doctor.py --mode interactive

🩺 Hindi Personal Voice AI Doctor - Interactive Mode
Type 'exit' to quit, 'help' for commands
==================================================

🗣️ आपकी समस्या बताइए: मुझे सीने में दर्द हो रहा है और सांस लेने में दिक्कत

📊 **Medical Assessment Results**
Urgency Level: HIGH
Risk Score: 8.2/10
Action Required: IMMEDIATE_CONSULTATION

💡 **Recommendations:**
  • Contact doctor immediately
  • Go to nearest hospital
  • Do not delay treatment

⏰ Follow-up Required: 1 hours
⚠️  **ESCALATION REQUIRED** - Contact doctor immediately
```

### Example 2: Batch Processing
```bash
$ python run_hindi_ai_doctor.py --mode batch --input sample_batch_input.json

📊 Processing batch file: sample_batch_input.json
Processing patient 1/3
Processing patient 2/3
Processing patient 3/3
✅ Batch processing complete. Results saved to: batch_results_20241225_143022.json
```

### Example 3: System Testing
```bash
$ python run_hindi_ai_doctor.py --mode test

🧪 Running system tests...

1. Testing Hindi NLP system...
   ✅ NLP system working

2. Testing triaging system...
   ✅ Triage system working

3. Testing image analysis...
   ⚠️  Image analysis requires actual image files
   ✅ Image analysis framework ready

4. Testing security framework...
   ✅ Security framework working

🎯 Test Results: 4/4 tests passed
```

## 🏗️ Creating Custom Batch Input

### JSON Format Specification
```json
[
  {
    "id": "unique_patient_id",
    "age": 45,
    "gender": "male|female|other",
    "symptoms": [
      {
        "hindi_term": "सीने में दर्द",
        "english_term": "chest pain",
        "urgency": "high|medium|low"
      }
    ],
    "vital_signs": {
      "temperature": 37.2,
      "blood_pressure": "140/90",
      "heart_rate": 95
    },
    "medical_history": ["hypertension", "diabetes"],
    "duration_hours": 6,
    "severity_score": 8.5,
    "xray_findings": {"image_path": "xray.jpg", "findings": "description"},
    "lab_results": {"report_path": "lab.pdf", "findings": {"key": "value"}}
  }
]
```

## 🔒 Security and Privacy

### Data Protection
- All patient data is encrypted using AES-256
- HIPAA compliance validation
- Audit logging for all interactions
- Right to be forgotten implementation

### Privacy Features
- No data retention without consent
- Automatic data expiration
- Secure session management
- Encrypted communication channels

## 🚨 Emergency Detection

The system automatically detects medical emergencies:
- **HIGH PRIORITY**: Chest pain, breathing difficulty, severe bleeding
- **MEDIUM PRIORITY**: High fever, persistent pain, unusual symptoms
- **LOW PRIORITY**: Minor aches, routine checkups

Emergency triggers immediate escalation recommendations.

## 📊 Output Files

### Log Files
- `hindi_ai_doctor.log`: Complete application logs
- Security audit logs in `security_logs/` directory

### Batch Results
- `batch_results_[timestamp].json`: Batch processing results
- Format includes risk scores, recommendations, and follow-up times

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# If you see "Import error: No module named..."
pip install -r requirements.txt  # (if available)
pip install torch transformers pandas numpy
```

#### 2. Memory Issues
```bash
# Reduce memory usage
python run_hindi_ai_doctor.py --mode demo
# Avoid loading large models simultaneously
```

#### 3. Hindi Text Encoding
```bash
# Ensure UTF-8 encoding
export PYTHONIOENCODING=utf-8
# On Windows: set PYTHONIOENCODING=utf-8
```

#### 4. Permission Errors
```bash
# Ensure write permissions for logs
chmod 755 .  # Linux/Mac
# Or run as administrator on Windows
```

### Debug Mode
Enable verbose logging for troubleshooting:
```bash
python run_hindi_ai_doctor.py --mode demo --verbose
```

## 📞 Support and Contact

### Getting Help
1. **Check logs**: Review `hindi_ai_doctor.log` for error details
2. **Run tests**: Use `--mode test` to validate system
3. **Documentation**: Refer to individual module docstrings
4. **Sample files**: Use provided `sample_batch_input.json` as template

### Technical Support
- **Email**: support@hindi-ai-doctor.com
- **Documentation**: See individual Python files for detailed APIs
- **Updates**: Check for model updates and security patches

## 🔄 Next Steps

### Production Deployment
1. **Scaling**: Use cloud deployment (AWS, Azure, GCP)
2. **Load Balancing**: Implement for high-traffic scenarios
3. **Monitoring**: Set up health checks and alerts
4. **Backup**: Regular data backup and disaster recovery

### Advanced Features
- **Voice Integration**: Add speech-to-text for voice input
- **Web Interface**: Deploy as web application
- **Mobile App**: Create mobile applications
- **API Service**: RESTful API for integration

## ✅ System Verification Checklist

Before going live, ensure:
- [ ] All dependencies installed successfully
- [ ] Demo mode runs without errors
- [ ] Interactive mode handles Hindi text correctly
- [ ] Batch processing works with sample data
- [ ] Security tests pass
- [ ] Log files are being generated
- [ ] Emergency detection triggers correctly
- [ ] Patient data is properly encrypted
- [ ] Audit logging captures all interactions
- [ ] System handles edge cases gracefully

---

**🩺 Ready to serve Hindi-speaking patients with AI-powered medical triaging!**