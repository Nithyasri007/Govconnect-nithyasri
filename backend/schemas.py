from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    dob: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    caste: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    caste: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

# Authentication schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Scheme schemas
class SchemeEligibility(BaseModel):
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    gender: Optional[List[str]] = None
    occupation: Optional[List[str]] = None
    caste: Optional[List[str]] = None
    state: Optional[List[str]] = None
    income_limit: Optional[float] = None

class SchemeBase(BaseModel):
    title: str
    benefits: str
    eligibility: SchemeEligibility
    required_documents: List[str]
    department: str
    description: str
    application_process: str

class SchemeCreate(SchemeBase):
    pass

class SchemeUpdate(BaseModel):
    title: Optional[str] = None
    benefits: Optional[str] = None
    eligibility: Optional[SchemeEligibility] = None
    required_documents: Optional[List[str]] = None
    department: Optional[str] = None
    description: Optional[str] = None
    application_process: Optional[str] = None
    is_active: Optional[bool] = None

class SchemeResponse(BaseModel):
    id: int
    title: str
    benefits: str
    eligibility: SchemeEligibility
    required_documents: List[str]
    department: str
    description: str
    application_process: str
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

# Application schemas
class ApplicationBase(BaseModel):
    scheme_id: int
    documents: Optional[List[str]] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    scheme_id: int
    status: str
    reference_number: str
    created_at: str
    updated_at: str
    scheme: SchemeResponse

    class Config:
        from_attributes = True

# Document schemas
class DocumentUploadResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    extracted_data: Optional[dict] = None
    uploaded_at: str

    class Config:
        from_attributes = True

# Voice processing schemas
class VoiceUploadResponse(BaseModel):
    extracted_data: dict
    message: str

# Extracted data schema
class ExtractedData(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    caste: Optional[str] = None
    state: Optional[str] = None
    income: Optional[float] = None

# Scheme matching response
class SchemeMatchResponse(BaseModel):
    schemes: List[SchemeResponse]
    total_matches: int
    user_data: ExtractedData
