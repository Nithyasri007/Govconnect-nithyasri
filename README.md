# Government Scheme Matching Application

A comprehensive web application that helps users find and apply for government welfare schemes based on their eligibility. The application features document OCR processing, voice input processing, and intelligent scheme matching.

## Features

### Frontend (React + TypeScript + Tailwind CSS)
- **Modern UI/UX**: Beautiful, responsive interface built with Tailwind CSS
- **Document Upload**: OCR-based document information extraction
- **Voice Input**: Speech-to-text processing for user information
- **Scheme Browsing**: Browse all available government schemes
- **Scheme Matching**: Intelligent matching based on user eligibility
- **Application Management**: Submit and track scheme applications
- **User Authentication**: Secure signup/login system

### Backend (FastAPI + SQLite3)
- **RESTful API**: Comprehensive API endpoints for all functionality
- **Database**: SQLite3 with SQLAlchemy ORM
- **Authentication**: JWT-based authentication with password hashing
- **Document Processing**: OCR using Tesseract and PyMuPDF
- **Voice Processing**: Speech recognition using Google Speech API
- **File Storage**: Secure file upload and storage system
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **Icons**: Lucide React
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI
- **Database**: SQLite3 with SQLAlchemy
- **Authentication**: JWT with Passlib
- **File Processing**: Pillow, PyMuPDF, Tesseract OCR
- **Voice Processing**: SpeechRecognition, PyDub
- **Validation**: Pydantic schemas

## Project Structure

```
project-bolt-sb1-rxuolptu/
├── project/                 # Frontend React application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── services/       # API service layer
│   │   ├── types/          # TypeScript type definitions
│   │   └── data/           # Static data (schemes)
│   ├── package.json        # Frontend dependencies
│   └── vite.config.ts      # Vite configuration
├── backend/                 # FastAPI backend application
│   ├── routers/            # API route handlers
│   ├── database.py         # Database models and configuration
│   ├── schemas.py          # Pydantic schemas
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── seed_database.py    # Database seeding script
└── README.md               # This file
```

## Prerequisites

### System Requirements
- **Python 3.8+** for backend
- **Node.js 16+** for frontend
- **Tesseract OCR** for document processing
- **FFmpeg** for audio processing

### Install System Dependencies

#### Windows
```bash
# Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki

# Install FFmpeg
# Download from: https://ffmpeg.org/download.html
```

#### macOS
```bash
# Install Tesseract OCR
brew install tesseract

# Install FFmpeg
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr

# Install FFmpeg
sudo apt-get install ffmpeg
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project-bolt-sb1-rxuolptu
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create database and seed initial data
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
python seed_database.py

# Start the backend server
python run.py
# Or use the provided scripts:
# Windows: start.bat
# Linux/Mac: ./start.sh
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd project

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Documentation

Once the backend is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## Database Schema

### Users Table
- Basic user information (name, email, password_hash)
- Personal details (dob, gender, occupation, caste, state, phone)
- Timestamps (created_at, updated_at)

### Schemes Table
- Scheme information (title, benefits, description)
- Eligibility criteria (age, gender, occupation, caste, state, income)
- Required documents and application process
- Status tracking (is_active)

### Applications Table
- Application details (user_id, scheme_id, status)
- Reference number generation
- Status tracking (submitted, under_review, approved, rejected)

### Document Uploads Table
- Document processing history
- Extracted data storage
- User association

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Schemes
- `GET /api/schemes/` - Get all schemes
- `GET /api/schemes/{id}` - Get specific scheme
- `POST /api/schemes/match` - Match schemes for user

### Documents
- `POST /api/documents/process` - Process document with OCR
- `POST /api/documents/upload` - Upload and store document

### Voice Processing
- `POST /api/voice/process` - Process audio file
- `POST /api/voice/record` - Process voice recording

### Applications
- `POST /api/applications/` - Submit application
- `GET /api/applications/` - Get user applications
- `POST /api/applications/{id}/documents` - Upload application documents

## Usage

### 1. User Registration/Login
- Navigate to `/auth` to create an account or sign in
- Provide your personal details during registration

### 2. Document Upload
- Go to `/upload/document` to upload government documents
- The system will automatically extract information using OCR
- Review and edit extracted data as needed

### 3. Voice Input
- Visit `/upload/voice` to provide information via voice
- Speak clearly about your personal details
- The system will process and extract relevant information

### 4. Scheme Matching
- After providing information, the system will show matching schemes
- View eligibility scores and scheme details
- Choose schemes to apply for

### 5. Application Submission
- Click "Apply Now" on any scheme
- Upload required documents
- Submit your application
- Track application status

## Development

### Backend Development
```bash
cd backend

# Run with auto-reload
python run.py

# Run tests (if implemented)
pytest

# Database migrations (if using Alembic)
alembic upgrade head
```

### Frontend Development
```bash
cd project

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./govconnect.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Database Configuration
The application uses SQLite3 by default. For production, consider:
- PostgreSQL or MySQL for better performance
- Database connection pooling
- Regular backups

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- File type validation
- User authorization checks
- Input validation with Pydantic

## Production Deployment

### Backend
- Use production WSGI server (Gunicorn, uWSGI)
- Set up reverse proxy (Nginx, Apache)
- Use environment variables for configuration
- Implement rate limiting
- Add monitoring and logging

### Frontend
- Build optimized production bundle
- Serve static files from CDN
- Implement service worker for offline support
- Add error tracking (Sentry, etc.)

## Troubleshooting

### Common Issues

1. **Tesseract OCR not found**
   - Ensure Tesseract is installed and in PATH
   - On Windows, add Tesseract installation directory to PATH

2. **FFmpeg not found**
   - Install FFmpeg and ensure it's in PATH
   - Restart terminal after installation

3. **Database connection errors**
   - Check if SQLite file is writable
   - Ensure database directory exists

4. **CORS errors**
   - Verify backend CORS configuration
   - Check frontend proxy settings in Vite config

5. **File upload errors**
   - Check upload directory permissions
   - Verify file size limits

### Logs
- Backend logs are displayed in the terminal
- Check browser console for frontend errors
- Database queries are logged when `echo=True` in database.py

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review API documentation
- Open an issue on GitHub

## Acknowledgments

- FastAPI for the excellent backend framework
- React and Vite for the frontend tooling
- Tesseract OCR for document processing
- Google Speech Recognition for voice processing
- Tailwind CSS for the beautiful UI components
