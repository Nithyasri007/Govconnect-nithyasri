from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database import get_db, User
from schemas import UserUpdate, UserResponse
from routers.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        dob=current_user.dob.isoformat() if current_user.dob else None,
        gender=current_user.gender,
        occupation=current_user.occupation,
        caste=current_user.caste,
        state=current_user.state,
        phone=current_user.phone,
        created_at=current_user.created_at.isoformat(),
        updated_at=current_user.updated_at.isoformat()
    )

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle datetime conversion for dob
    if 'dob' in update_data and update_data['dob']:
        if isinstance(update_data['dob'], str):
            from datetime import datetime
            update_data['dob'] = datetime.fromisoformat(update_data['dob'].replace('Z', '+00:00'))
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        dob=current_user.dob.isoformat() if current_user.dob else None,
        gender=current_user.gender,
        occupation=current_user.occupation,
        caste=current_user.caste,
        state=current_user.state,
        phone=current_user.phone,
        created_at=current_user.created_at.isoformat(),
        updated_at=current_user.updated_at.isoformat()
    )

@router.delete("/profile")
async def delete_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User profile deleted successfully"}
