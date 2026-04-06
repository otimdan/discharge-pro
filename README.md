# DischargePro - AI-Assisted Discharge Summary Generator

DischargePro is an intelligent clinical documentation assistant designed to generate complete, structured patient discharge summaries. It leverages AI to streamline the discharge documentation process in healthcare settings, with specific considerations for Ugandan clinical contexts.

## 🎯 Overview

DischargePro uses Google's ADK (Agent Development Kit) and Gemini AI to transform clinical notes and patient information into professionally formatted, structured discharge summaries. The system generates comprehensive discharge documentation including:

- Patient clinical summaries and diagnoses
- Detailed hospitalization course
- Discharge medications with complete dosing instructions
- Follow-up appointments and timelines
- Pending investigations
- Clear patient instructions in plain language
- Clinical notes for receiving providers
- Resource availability considerations for Ugandan settings

## ✨ Features

- **AI-Powered Documentation**: Automatically generates discharge summaries from clinical notes
- **Structured Output**: Produces well-organized, clinically relevant discharge information
- **Uganda-Specific**: Includes considerations for medication availability, distance to facilities, and NHIS coverage
- **Plain Language**: Patient instructions written in simple, understandable English
- **Web Interface**: User-friendly web-based UI for seamless document generation
- **RESTful API**: Backend API for integration with other systems
- **Session Management**: Maintains user sessions for continuity

## 📋 Project Structure

```
discharge_pro/
├── main.py                 # FastAPI application and routing
├── agent.py               # AI agent configuration and schema definitions
├── __init__.py            # Package initialization
├── templates/
│   └── index.html         # Web UI template
├── static/                # Static assets (CSS, JavaScript)
├── .env                   # Environment configuration
└── README.md              # This file
```

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **AI Framework**: Google ADK (Agent Development Kit)
- **Model**: Gemini 2.5 Flash
- **Frontend**: HTML/JavaScript
- **Session Management**: In-Memory Session Service
- **CORS**: Enabled for cross-origin requests

## 📦 Requirements

- Python 3.10+
- FastAPI
- Google ADK libraries
- Google Generative AI SDK
- Jinja2 (templating)
- python-dotenv

## 🚀 Getting Started

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd discharge_pro
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:

```
GOOGLE_API_KEY=your_api_key_here
```

### Running the Application

```bash
python main.py
```

Or with Uvicorn directly:

```bash
uvicorn main:app --reload
```

The application will start at `http://localhost:8000`

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:8000` in your browser
2. Enter clinical notes or patient information
3. Click "Generate Summary"
4. Review the structured discharge summary
5. Edit as needed before finalizing

### API Endpoint

**POST** `/generate`

**Request Body:**

```json
{
  "notes": "Clinical notes about the patient admission..."
}
```

**Response:**

```json
{
  "patientSummary": "32-year-old male admitted with...",
  "admissionDiagnosis": "...",
  "dischargeDiagnosis": "...",
  "conditionAtDischarge": "stable",
  "clinicalCourse": "...",
  "keyResults": [...],
  "dischargeMedications": [...],
  "followUp": [...],
  "pendingInvestigations": [...],
  "patientInstructions": [...],
  "clinicianNote": "...",
  "resourceNote": "..."
}
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required)

### Application Settings

Key configuration in `main.py`:

- `APP_NAME`: "DischargeSummary"
- `USER_ID`: "clinician"
- `PORT`: 8000 (default)

## 📊 Output Schema

The discharge summary output includes:

| Field                 | Type   | Description                                               |
| --------------------- | ------ | --------------------------------------------------------- |
| patientSummary        | string | One-sentence patient overview                             |
| admissionDiagnosis    | string | Working diagnosis on admission                            |
| dischargeDiagnosis    | string | Confirmed diagnosis at discharge                          |
| conditionAtDischarge  | enum   | Patient condition: stable/improved/guarded/against-advice |
| clinicalCourse        | string | Narrative of hospital stay (3-5 sentences)                |
| keyResults            | list   | Investigation results from admission                      |
| dischargeMedications  | list   | Medications to continue at home                           |
| followUp              | list   | Required follow-up appointments                           |
| pendingInvestigations | list   | Tests still awaited                                       |
| patientInstructions   | list   | Plain-language instructions for patient                   |
| clinicianNote         | string | Note for receiving clinician                              |
| resourceNote          | string | Uganda-specific resource considerations                   |

## 🏥 Uganda-Specific Features

The application includes considerations specific to Ugandan clinical practice:

- **Essential Drugs List (EDL)**: Tracks medications on Uganda's national EDL
- **Distance Considerations**: Accounts for geographical barriers to follow-up
- **NHIS Coverage**: Notes on National Health Insurance Scheme coverage
- **Community Health**: Integrates community health worker follow-up options
- **Resource Availability**: Highlights medication and facility accessibility

## 🤝 Contributing

Contributions are welcome. Please ensure any new features:

- Follow the existing code structure
- Include appropriate error handling
- Are tested before submission
- Include documentation updates

## 📝 License

[Specify license here]

## 📧 Support

For issues, feature requests, or questions, please open an issue in the repository.

