from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime, timezone

from database import get_db, Scheme, User
from schemas import SchemeCreate, SchemeUpdate, SchemeResponse, ExtractedData, SchemeMatchResponse, SchemeEligibility
from routers.auth import get_current_user

router = APIRouter()

def db_scheme_to_response(scheme: Scheme) -> SchemeResponse:
    """Convert database scheme to response schema"""
    # Parse JSON strings back to lists
    eligibility_gender = json.loads(scheme.eligibility_gender) if scheme.eligibility_gender else None
    eligibility_occupation = json.loads(scheme.eligibility_occupation) if scheme.eligibility_occupation else None
    eligibility_caste = json.loads(scheme.eligibility_caste) if scheme.eligibility_caste else None
    eligibility_state = json.loads(scheme.eligibility_state) if scheme.eligibility_state else None
    required_documents = json.loads(scheme.required_documents) if scheme.required_documents else []
    
    # Create eligibility object
    eligibility = SchemeEligibility(
        min_age=scheme.eligibility_min_age,
        max_age=scheme.eligibility_max_age,
        gender=eligibility_gender,
        occupation=eligibility_occupation,
        caste=eligibility_caste,
        state=eligibility_state,
        income_limit=scheme.eligibility_income_limit
    )
    
    return SchemeResponse(
        id=scheme.id,
        title=scheme.title,
        benefits=scheme.benefits,
        eligibility=eligibility,
        required_documents=required_documents,
        department=scheme.department,
        description=scheme.description,
        application_process=scheme.application_process,
        is_active=scheme.is_active,
        created_at=scheme.created_at.isoformat(),
        updated_at=scheme.updated_at.isoformat()
    )

@router.get("/", response_model=List[SchemeResponse])
async def get_all_schemes(db: Session = Depends(get_db)):
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    return [db_scheme_to_response(scheme) for scheme in schemes]

@router.get("/{scheme_id}", response_model=SchemeResponse)
async def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id, Scheme.is_active == True).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return db_scheme_to_response(scheme)

@router.post("/", response_model=SchemeResponse)
async def create_scheme(
    scheme_data: SchemeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Convert eligibility data to JSON strings for storage
    scheme_dict = scheme_data.dict()
    eligibility = scheme_dict.pop('eligibility')
    
    db_scheme = Scheme(
        **scheme_dict,
        eligibility_min_age=eligibility.min_age,
        eligibility_max_age=eligibility.max_age,
        eligibility_gender=json.dumps(eligibility.gender) if eligibility.gender else None,
        eligibility_occupation=json.dumps(eligibility.occupation) if eligibility.occupation else None,
        eligibility_caste=json.dumps(eligibility.caste) if eligibility.caste else None,
        eligibility_state=json.dumps(eligibility.state) if eligibility.state else None,
        eligibility_income_limit=eligibility.income_limit,
        required_documents=json.dumps(scheme_data.required_documents)
    )
    
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return db_scheme_to_response(db_scheme)

@router.put("/{scheme_id}", response_model=SchemeResponse)
async def update_scheme(
    scheme_id: int,
    scheme_update: SchemeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    update_data = scheme_update.dict(exclude_unset=True)
    
    # Handle eligibility updates
    if 'eligibility' in update_data:
        eligibility = update_data.pop('eligibility')
        if eligibility.min_age is not None:
            scheme.eligibility_min_age = eligibility.min_age
        if eligibility.max_age is not None:
            scheme.eligibility_max_age = eligibility.max_age
        if eligibility.gender is not None:
            scheme.eligibility_gender = json.dumps(eligibility.gender)
        if eligibility.occupation is not None:
            scheme.eligibility_occupation = json.dumps(eligibility.occupation)
        if eligibility.caste is not None:
            scheme.eligibility_caste = json.dumps(eligibility.caste)
        if eligibility.state is not None:
            scheme.eligibility_state = json.dumps(eligibility.state)
        if eligibility.income_limit is not None:
            scheme.eligibility_income_limit = eligibility.income_limit
    
    # Handle other updates
    for field, value in update_data.items():
        if field == 'required_documents' and value is not None:
            setattr(scheme, field, json.dumps(value))
        else:
            setattr(scheme, field, value)
    
    scheme.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(scheme)
    return db_scheme_to_response(scheme)

@router.delete("/{scheme_id}")
async def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    scheme.is_active = False
    db.commit()
    return {"message": "Scheme deactivated successfully"}

@router.post("/match", response_model=SchemeMatchResponse)
async def match_schemes(user_data: ExtractedData, db: Session = Depends(get_db)):
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    matching_schemes = []
    
    for scheme in schemes:
        if is_eligible(scheme, user_data):
            matching_schemes.append(db_scheme_to_response(scheme))
    
    return SchemeMatchResponse(
        schemes=matching_schemes,
        total_matches=len(matching_schemes),
        user_data=user_data
    )

def is_eligible(scheme: Scheme, user_data: ExtractedData) -> bool:
    # Age check
    if user_data.dob and scheme.eligibility_min_age:
        try:
            dob = datetime.strptime(user_data.dob, "%Y-%m-%d")
            age = (datetime.now() - dob).days // 365
            if age < scheme.eligibility_min_age:
                return False
        except:
            pass
    
    if user_data.dob and scheme.eligibility_max_age:
        try:
            dob = datetime.strptime(user_data.dob, "%Y-%m-%d")
            age = (datetime.now() - dob).days // 365
            if age > scheme.eligibility_max_age:
                return False
        except:
            pass
    
    # Gender check
    if user_data.gender and scheme.eligibility_gender:
        try:
            allowed_genders = json.loads(scheme.eligibility_gender)
            if user_data.gender.lower() not in [g.lower() for g in allowed_genders]:
                return False
        except:
            pass
    
    # Occupation check
    if user_data.occupation and scheme.eligibility_occupation:
        try:
            allowed_occupations = json.loads(scheme.eligibility_occupation)
            user_occ = user_data.occupation.lower()
            if not any(occ.lower() in user_occ for occ in allowed_occupations):
                return False
        except:
            pass
    
    # Caste check
    if user_data.caste and scheme.eligibility_caste:
        try:
            allowed_castes = json.loads(scheme.eligibility_caste)
            if user_data.caste.lower() not in [c.lower() for c in allowed_castes]:
                return False
        except:
            pass
    
    # State check
    if user_data.state and scheme.eligibility_state:
        try:
            allowed_states = json.loads(scheme.eligibility_state)
            if user_data.state.lower() not in [s.lower() for s in allowed_states]:
                return False
        except:
            pass
    
    return True
