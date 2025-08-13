from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
import json
from datetime import datetime, timezone
from PIL import Image
import pytesseract
import fitz  # PyMuPDF for PDF processing
from typing import List

from database import get_db, DocumentUpload, User
from schemas import DocumentUploadResponse, ExtractedData
from routers.auth import get_current_user

router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPG, PNG, and PDF files are allowed."
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads/documents", exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"uploads/documents/{unique_filename}"
    
    # Save file
    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Process document and extract data
    extracted_data = await process_document(file_path, file.content_type)
    
    # Create document record
    db_document = DocumentUpload(
        user_id=current_user.id,
        file_path=file_path,
        file_name=file.filename,
        file_size=len(content),
        extracted_data=json.dumps(extracted_data) if extracted_data else None
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return DocumentUploadResponse(
        id=db_document.id,
        file_name=db_document.file_name,
        file_path=db_document.file_path,
        extracted_data=extracted_data,
        uploaded_at=db_document.uploaded_at.isoformat()
    )

@router.post("/process", response_model=dict)
async def process_document_endpoint(
    file: UploadFile = File(...)
):
    # Create temporary file for processing
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    
    try:
        content = await file.read()
        with open(temp_path, "wb") as buffer:
            buffer.write(content)
        
        # Process document
        extracted_data = await process_document(temp_path, file.content_type)
        
        return {"extracted_data": extracted_data}
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

async def process_document(file_path: str, content_type: str) -> ExtractedData:
    """Process document and extract information using OCR"""
    try:
        if content_type.startswith("image/"):
            return await process_image(file_path)
        elif content_type == "application/pdf":
            return await process_pdf(file_path)
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        print(f"Error processing document: {e}")
        return ExtractedData()

async def process_image(file_path: str) -> ExtractedData:
    """Process image files using Tesseract OCR"""
    try:
        # Open image
        image = Image.open(file_path)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image, lang='eng')
        
        # Parse extracted text
        return parse_extracted_text(text)
    except Exception as e:
        print(f"Error processing image: {e}")
        return ExtractedData()

async def process_pdf(file_path: str) -> ExtractedData:
    """Process PDF files using PyMuPDF"""
    try:
        # Open PDF
        doc = fitz.open(file_path)
        text = ""
        
        # Extract text from all pages
        for page in doc:
            text += page.get_text()
        
        doc.close()
        
        # Parse extracted text
        return parse_extracted_text(text)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ExtractedData()

def parse_extracted_text(text: str) -> ExtractedData:
    """Parse extracted text to identify key information"""
    text = text.lower()
    
    extracted_data = ExtractedData()
    
    # Extract name (look for patterns like "name:", "full name:", etc.)
    name_patterns = ["name:", "full name:", "given name:", "first name:"]
    for pattern in name_patterns:
        if pattern in text:
            start_idx = text.find(pattern) + len(pattern)
            end_idx = text.find("\n", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            name = text[start_idx:end_idx].strip()
            if name and len(name) > 2:
                extracted_data.name = name.title()
                break
    
    # Extract date of birth
    import re
    dob_patterns = [
        r"dob[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"date of birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    ]
    
    for pattern in dob_patterns:
        match = re.search(pattern, text)
        if match:
            extracted_data.dob = match.group(1)
            break
    
    # Extract gender
    if "male" in text:
        extracted_data.gender = "male"
    elif "female" in text:
        extracted_data.gender = "female"
    
    # Extract phone number
    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        extracted_data.phone = phone_match.group(0)
    
    # Extract address (look for common address keywords)
    address_keywords = ["address:", "residence:", "village:", "district:", "state:"]
    for keyword in address_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            end_idx = text.find("\n", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            address = text[start_idx:end_idx].strip()
            if address and len(address) > 5:
                extracted_data.address = address.title()
                break
    
    # Extract occupation
    occupation_keywords = ["occupation:", "profession:", "work:", "job:"]
    for keyword in occupation_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            end_idx = text.find("\n", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            occupation = text[start_idx:end_idx].strip()
            if occupation and len(occupation) > 2:
                extracted_data.occupation = occupation.title()
                break
    
    return extracted_data

@router.get("/history", response_model=List[DocumentUploadResponse])
async def get_document_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = db.query(DocumentUpload).filter(
        DocumentUpload.user_id == current_user.id
    ).order_by(DocumentUpload.uploaded_at.desc()).all()
    
    return [
        DocumentUploadResponse(
            id=doc.id,
            file_name=doc.file_name,
            file_path=doc.file_path,
            extracted_data=json.loads(doc.extracted_data) if doc.extracted_data else None,
            uploaded_at=doc.uploaded_at
        )
        for doc in documents
    ]
