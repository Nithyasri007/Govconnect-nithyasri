# Government Scheme Backend API

A FastAPI-based backend for the Government Scheme Matching Application with SQLite3 database.

## Features

- **User Authentication**: JWT-based authentication with signup/login
- **Document Processing**: OCR-based document information extraction
- **Voice Processing**: Speech-to-text conversion for voice input
- **Scheme Management**: CRUD operations for government schemes
- **Application Management**: User applications for schemes
- **Scheme Matching**: Intelligent matching based on user eligibility
- **File Storage**: Secure file upload and storage system

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite3 with SQLAlchemy ORM
- **Authentication**: JWT with Passlib
- **File Processing**: Pillow, PyMuPDF, Tesseract OCR
- **Voice Processing**: SpeechRecognition, PyDub
- **Validation**: Pydantic schemas

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system dependencies** (for OCR and voice processing):
   - **Tesseract OCR**: Required for document text extraction
   - **FFmpeg**: Required for audio processing

3. **Set up environment variables**:
   ```bash
   # Create .env file
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./govconnect.db
   ```

## Database Setup

1. **Create database tables**:
   ```bash
   python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

2. **Seed initial data**:
   ```bash
   python seed_database.py
   ```

## Running the Application

1. **Start the server**:
   ```bash
   python run.py
   ```

2. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `DELETE /api/users/profile` - Delete user profile

### Schemes
- `GET /api/schemes/` - Get all schemes
- `GET /api/schemes/{id}` - Get specific scheme
- `POST /api/schemes/` - Create new scheme
- `PUT /api/schemes/{id}` - Update scheme
- `DELETE /api/schemes/{id}` - Deactivate scheme
- `POST /api/schemes/match` - Match schemes for user

### Applications
- `POST /api/applications/` - Submit application
- `GET /api/applications/` - Get user applications
- `GET /api/applications/{id}` - Get specific application
- `PUT /api/applications/{id}` - Update application
- `POST /api/applications/{id}/documents` - Upload documents
- `GET /api/applications/{id}/documents` - Get application documents

### Documents
- `POST /api/documents/upload` - Upload and process document
- `POST /api/documents/process` - Process document without saving
- `GET /api/documents/history` - Get document history

### Voice Processing
- `POST /api/voice/process` - Process audio file
- `POST /api/voice/record` - Process voice recording

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

### Application Documents Table
- Document metadata (type, file_path, file_name, file_size)
- Relationship to applications

### Document Uploads Table
- Document processing history
- Extracted data storage
- User association

## File Storage

- **Uploads Directory**: `uploads/`
  - `documents/` - User uploaded documents
  - `applications/` - Application-specific documents
- **Temporary Files**: `temp/` - For processing operations

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- File type validation
- User authorization checks

## Error Handling

- Comprehensive HTTP status codes
- Detailed error messages
- Input validation with Pydantic
- Database transaction management

## Development

- Hot reload enabled
- Detailed logging
- Interactive API documentation
- Database schema visualization

## Production Considerations

- Change default SECRET_KEY
- Use environment variables for configuration
- Implement rate limiting
- Add request logging
- Use production-grade database (PostgreSQL/MySQL)
- Implement file storage service (AWS S3, etc.)
- Add monitoring and health checks
