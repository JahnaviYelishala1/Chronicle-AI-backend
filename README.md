# Chronicle AI - Backend

A comprehensive backend service for video and meeting transcription, analysis, and intelligent search using RAG (Retrieval-Augmented Generation) with AI-powered insights.

## Features

- **Video Transcription**: Support for video files and YouTube links using Whisper
- **Meeting Insights**: Extract key decisions, action items, and follow-ups from meetings
- **RAG-Powered Search**: Intelligent semantic search across transcribed content
- **Chat Interface**: Interactive chat with meeting context for Q&A
- **Embeddings**: High-quality text embeddings for semantic understanding
- **PDF Support**: Process and analyze PDF documents
- **Feedback Loop**: Collect and learn from user feedback
- **Multi-source Integration**: Handle various input formats (video files, YouTube, local files)

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── api/                    # API endpoints
│   ├── chat.py            # Chat functionality
│   ├── feedback.py        # User feedback endpoints
│   ├── report.py          # Report generation
│   ├── transcription.py   # Transcription endpoints
│   ├── upload.py          # File upload handling
│   ├── video.py           # Video management
│   ├── videos.py          # Videos list and operations
│   └── youtube.py         # YouTube integration
├── core/                  # Core utilities
│   └── supabase.py        # Supabase client configuration
├── db/                    # Database layer
│   ├── database.py        # Database client and queries
│   └── init_db.py         # Database initialization
├── models/                # Data models
│   ├── transcript.py      # Transcript model
│   ├── meeting_insight.py # Meeting insights
│   ├── chat_feedback.py   # Chat feedback
│   ├── action_item.py     # Action items
│   ├── decision.py        # Decisions
│   ├── follow_up.py       # Follow-ups
│   ├── embedding.py       # Embeddings
│   └── ...
├── schemas/               # Pydantic schemas for API
│   ├── chat.py           # Chat request/response schemas
│   ├── video.py          # Video schemas
│   └── youtube.py        # YouTube schemas
└── services/              # Business logic
    ├── chunking/         # Text chunking
    ├── embeddings/       # Embedding generation
    ├── llm/              # LLM integration
    ├── pdf/              # PDF processing
    ├── rag/              # RAG services
    ├── transcription/    # Transcription services
    └── youtube/          # YouTube handling
```

## Installation

### Prerequisites
- Python 3.9+
- Virtual environment (venv)
- PostgreSQL/Supabase account
- API keys for:
  - OpenRouter (LLM)
  - Other external services as needed

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd chronicle-ai
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file in the project root:
```
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# LLM
OPENROUTER_API_KEY=your_openrouter_key

# Optional: Other service keys
YOUTUBE_API_KEY=your_youtube_key
```

5. **Initialize database**
```bash
python -m app.db.init_db
```

## Running the Application

### Development Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Deploying on Render

This repo includes a `render.yaml` blueprint and `.python-version` pin for Render.

### Option 1: Blueprint Deploy
1. Push this repository to GitHub/GitLab/Bitbucket.
2. In Render, choose **New > Blueprint**.
3. Select this repository.
4. Render will detect `render.yaml` and create the web service.
5. Add the required secret environment variables when prompted.

### Option 2: Manual Web Service
Use these settings if you create the service manually:

```text
Runtime: Python 3
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /
```

### Render Environment Variables
Set these in the Render service environment:

```text
DATABASE_URL=your_postgres_or_supabase_database_url
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
SUPABASE_BUCKET=your_supabase_storage_bucket
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=google/gemma-4-31b-it:free
CORS_ORIGINS=https://your-frontend-domain.com,http://localhost:5173
```

After deploy, open:

```text
https://your-render-service.onrender.com/
https://your-render-service.onrender.com/docs
```

Note: Render's filesystem is ephemeral. Keep uploaded/transcribed assets in Supabase Storage or add a Render persistent disk if you need local files to survive deploys/restarts.

## API Endpoints

### Transcription
- `POST /api/transcription` - Create transcription from file
- `POST /api/transcription/youtube` - Transcribe YouTube video

### Chat
- `POST /api/chat` - Send chat message with context

### Video Management
- `GET /api/videos` - List all videos
- `GET /api/videos/{video_id}` - Get video details
- `POST /api/videos/{video_id}` - Update video metadata

### Insights
- `GET /api/videos/{video_id}/insights` - Get meeting insights
- `GET /api/videos/{video_id}/decisions` - Get decisions
- `GET /api/videos/{video_id}/action-items` - Get action items

### Feedback
- `POST /api/feedback` - Submit feedback on chat responses

## Testing

Run the test suite:
```bash
# All tests
pytest

# Specific test file
pytest app/test_chat.py

# With coverage
pytest --cov=app
```

Test files available:
- `test_chat.py` - Chat functionality
- `test_chunking.py` - Text chunking
- `test_db.py` - Database operations
- `test_embedding.py` - Embedding generation
- `test_insight.py` - Insight extraction
- `test_openrouter.py` - LLM integration
- `test_search.py` - Search functionality
- `test_whisper.py` - Transcription

## Key Services

### Transcription Service
Handles audio transcription using OpenAI's Whisper model. Supports:
- Local audio files
- YouTube videos (auto-download)
- Remote files

### Embedding Service
Generates semantic embeddings for text chunks using configured LLM.

### RAG Service
Provides semantic search and retrieval-augmented generation for intelligent Q&A.

### Chat Service
Interactive chat interface with context from meetings, powered by LLM.

### PDF Service
Extract and process text from PDF documents.

## Development

### Adding New Features
1. Create models in `models/` for new data types
2. Create schemas in `schemas/` for API contracts
3. Implement business logic in `services/`
4. Add API endpoints in `api/`
5. Write tests in `test_*.py` files

### Code Style
Follow PEP 8 conventions. Use type hints for all functions.

## Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Activate correct environment
.venv\Scripts\Activate.ps1
```

### Database Connection Issues
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check network connectivity
- Ensure database is initialized

### Transcription Errors
- Check file format compatibility with Whisper
- Verify sufficient disk space for downloads
- Check API rate limits

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Supabase** - Database
- **OpenAI** - Whisper, embeddings
- **PyPDF2** - PDF processing

## License

[Add your license here]

## Support

For issues or questions, please open an issue or contact the development team.
