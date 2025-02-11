# Agno RAG Application

A modern Retrieval-Augmented Generation (RAG) application built with the Agno framework and Supabase for vector storage. This application allows users to manage and query documents using state-of-the-art language models and vector search capabilities.

## Features

- 🔐 User Authentication with JWT
- 📄 Document Management
  - Upload text files
  - Add documents programmatically
  - Delete documents
- 🔍 Semantic Search
  - Vector-based document retrieval
  - User-specific document access
- 🤖 AI-powered Question Answering
  - Google PaLM integration
  - Context-aware responses
- 🔒 Secure Data Storage with Supabase

## Prerequisites

- Python 3.8+
- Supabase account
- Google Cloud Platform account with PaLM API access

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Agno_RAG
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your credentials:
- Supabase URL and API key
- Google PaLM API key
- JWT secret key
- Other configuration options

5. Set up Supabase:
- Create a new Supabase project
- Enable Vector storage
- Create the following tables:
  - users
  - documents (with pgvector extension)
  - embeddings

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new user
- POST `/auth/login` - Login and get JWT token
- GET `/auth/me` - Get current user info

### Document Management
- POST `/rag/documents/add` - Add documents
- POST `/rag/documents/upload` - Upload text files
- POST `/rag/documents/delete` - Delete documents
- POST `/rag/query` - Query the RAG system

## Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password"}'
```

### Add Documents
```bash
curl -X POST http://localhost:8000/rag/documents/add \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Your document content here",
        "metadata": {"source": "example"}
      }
    ]
  }'
```

### Query the System
```bash
curl -X POST http://localhost:8000/rag/query \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Your question here",
    "k": 3
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Agno Framework](https://github.com/agno)
- [Supabase](https://supabase.io)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Google PaLM API](https://developers.generativeai.google/)
