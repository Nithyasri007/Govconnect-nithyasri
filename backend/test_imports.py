#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test database imports
    from database import engine, Base, SessionLocal, User, Scheme, Application, ApplicationDocument, DocumentUpload
    print("✅ Database imports successful")
    
    # Test schema imports
    from schemas import (
        UserCreate, UserLogin, Token, UserResponse, UserUpdate,
        SchemeCreate, SchemeUpdate, SchemeResponse, SchemeEligibility,
        ApplicationCreate, ApplicationUpdate, ApplicationResponse,
        DocumentUploadResponse, VoiceUploadResponse, ExtractedData,
        SchemeMatchResponse
    )
    print("✅ Schema imports successful")
    
    # Test router imports
    from routers.auth import get_current_user
    from routers.users import router as users_router
    from routers.schemes import router as schemes_router
    from routers.applications import router as applications_router
    from routers.documents import router as documents_router
    from routers.voice import router as voice_router
    print("✅ Router imports successful")
    
    # Test main app import
    from main import app
    print("✅ Main app import successful")
    
    print("\n🎉 All imports successful! The backend should work correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
