# Graduation-FCAI-V2
- to run the program run this `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
A comprehensive AI system that combines multiple components for face recognition, voice-to-text conversion, and retrieval-augmented generation (RAG).

## Components

### 1. Face Recognition
Located in `/face_recognition2/`
- Facial recognition system with model training capabilities
- Image capture functionality
- MVC architecture with controllers, models and helper utilities

### 2. Voice to Text
Located in `/voice2txt/`
- Speech-to-text conversion system
- MVC architecture with Controllers, Models and Services

### 3. RAG Models
Located in `/rag_model/`
- Two versions of RAG implementation:
  - agno_rag_v00: Initial implementation
  - Agno_RAG_v01: Enhanced version with authentication and web interface
- RESTful API routes
- Service-based architecture

### 4. Middleware
Located in `/middle_ware/`
- Data pipeline implementation
- Integration layer between components

## Setup

1. Clone the repository

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment Configuration:
- Copy `.env.example` to `.env`
- Configure the environment variables according to your setup

## Project Structure

```
.
├── face_recognition2/        # Face recognition module
│   └── src/
│       ├── controllers/     # Recognition controllers
│       ├── helpers/        # Utility functions and configurations
│       └── models/         # Facial recognition models
├── middle_ware/            # Integration layer
│   └── src/
│       └── data_pipeline.py
├── rag_model/             # RAG implementations
│   ├── agno_rag_v00/     # Initial version
│   └── Agno_RAG_v01/     # Enhanced version with web interface
└── voice2txt/            # Speech-to-text module
    └── src/
        ├── Controllers/
        ├── models/
        └── Services/
```

## Usage

Each component can be used independently or as part of the integrated system.

### Face Recognition
- Face detection and recognition capabilities
- Model training functionality
- Image capture and processing

### Voice to Text
- Speech-to-text conversion
- Modular service-based architecture

### RAG Model
- Two versions available:
  - V0: Basic RAG implementation
  - V1: Enhanced version with:
    - Authentication
    - Web interface
    - RESTful API endpoints

### Middleware
- Handles data flow between components
- Implements data pipeline for integrated operations

## Main Dependencies

- Python 3.x
- Required packages are listed in `requirements.txt`

## Development

- Follow the modular architecture pattern
- Each component has its own README with specific instructions
- Use the existing MVC/Service patterns when adding new features