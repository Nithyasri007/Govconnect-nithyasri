from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime, timezone

from database import get_db, Application, ApplicationDocument, User, Scheme
from schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from routers.auth import get_current_user
from routers.schemes import db_scheme_to_response

router = APIRouter()

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if scheme exists
    scheme = db.query(Scheme).filter(Scheme.id == application_data.scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Generate reference number
    reference_number = f"GC{datetime.now(timezone.utc).strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
    
    # Create application
    db_application = Application(
        user_id=current_user.id,
        scheme_id=application_data.scheme_id,
        reference_number=reference_number,
        status="submitted"
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    # Return application with scheme details
    return ApplicationResponse(
        id=db_application.id,
        user_id=db_application.user_id,
        scheme_id=db_application.scheme_id,
        status=db_application.status,
        reference_number=db_application.reference_number,
        created_at=db_application.created_at.isoformat(),
        updated_at=db_application.updated_at.isoformat(),
        scheme=db_scheme_to_response(scheme)
    )

@router.get("/", response_model=List[ApplicationResponse])
async def get_user_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    applications = db.query(Application).filter(Application.user_id == current_user.id).all()
    
    result = []
    for app in applications:
        scheme = db.query(Scheme).filter(Scheme.id == app.scheme_id).first()
        result.append(ApplicationResponse(
            id=app.id,
            user_id=app.user_id,
            scheme_id=app.scheme_id,
            status=app.status,
            reference_number=app.reference_number,
            created_at=app.created_at.isoformat(),
            updated_at=app.updated_at.isoformat(),
            scheme=db_scheme_to_response(scheme)
        ))
    
    return result

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    scheme = db.query(Scheme).filter(Scheme.id == application.scheme_id).first()
    
    return ApplicationResponse(
        id=application.id,
        user_id=application.user_id,
        scheme_id=application.scheme_id,
        status=application.status,
        reference_number=application.reference_number,
        created_at=application.created_at,
        updated_at=application.updated_at,
        scheme=scheme
    )

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update status
    if application_update.status:
        application.status = application_update.status
        application.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(application)
    
    scheme = db.query(Scheme).filter(Scheme.id == application.scheme_id).first()
    
    return ApplicationResponse(
        id=application.id,
        user_id=application.user_id,
        scheme_id=application.scheme_id,
        status=application.status,
        reference_number=application.reference_number,
        created_at=application.created_at.isoformat(),
        updated_at=application.updated_at.isoformat(),
        scheme=db_scheme_to_response(scheme)
    )

@router.post("/{application_id}/documents")
async def upload_application_documents(
    application_id: int,
    document_type: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if application exists and belongs to user
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads/applications", exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"uploads/applications/{unique_filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create document record
    db_document = ApplicationDocument(
        application_id=application_id,
        document_type=document_type,
        file_path=file_path,
        file_name=file.filename,
        file_size=len(content)
    )
    
    db.add(db_document)
    db.commit()
    
    return {
        "message": "Document uploaded successfully",
        "document_id": db_document.id,
        "file_name": file.filename
    }

@router.get("/{application_id}/documents")
async def get_application_documents(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if application exists and belongs to user
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    documents = db.query(ApplicationDocument).filter(
        ApplicationDocument.application_id == application_id
    ).all()
    
    return [
        {
            "id": doc.id,
            "document_type": doc.document_type,
            "file_name": doc.file_name,
            "file_size": doc.file_size,
            "uploaded_at": doc.uploaded_at
        }
        for doc in documents
    ]
