from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
import json
from datetime import datetime, timezone
import speech_recognition as sr
from pydub import AudioSegment
import io

from database import get_db, User
from schemas import VoiceUploadResponse, ExtractedData
from routers.auth import get_current_user

router = APIRouter()

@router.post("/process", response_model=VoiceUploadResponse)
async def process_voice(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    allowed_types = ["audio/wav", "audio/mp3", "audio/m4a", "audio/ogg"]
    if audio_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid audio file type. Only WAV, MP3, M4A, and OGG files are allowed."
        )
    
    try:
        # Read audio file
        audio_content = await audio_file.read()
        
        # Convert audio to text
        extracted_text = await convert_audio_to_text(audio_content, audio_file.content_type)
        
        # Parse extracted text to identify key information
        extracted_data = parse_voice_text(extracted_text)
        
        return VoiceUploadResponse(
            extracted_data=extracted_data.dict(),
            message="Voice processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice: {str(e)}"
        )

async def convert_audio_to_text(audio_content: bytes, content_type: str) -> str:
    """Convert audio file to text using speech recognition"""
    try:
        # Create temporary file for processing
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{uuid.uuid4()}"
        
        # Save audio content to temporary file
        with open(temp_path, "wb") as f:
            f.write(audio_content)
        
        try:
            # Convert audio to WAV format if needed
            if content_type != "audio/wav":
                audio = AudioSegment.from_file(temp_path, format=content_type.split("/")[1])
                wav_path = f"{temp_path}.wav"
                audio.export(wav_path, format="wav")
                temp_path = wav_path
            
            # Initialize speech recognizer
            recognizer = sr.Recognizer()
            
            # Load audio file
            with sr.AudioFile(temp_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record audio
                audio = recognizer.record(source)
            
            # Recognize speech
            text = recognizer.recognize_google(audio)
            return text
            
        finally:
            # Clean up temporary files
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(f"{temp_path}.wav"):
                os.remove(f"{temp_path}.wav")
                
    except sr.UnknownValueError:
        raise Exception("Speech could not be understood")
    except sr.RequestError as e:
        raise Exception(f"Could not request results from speech recognition service: {e}")
    except Exception as e:
        raise Exception(f"Error processing audio: {e}")

def parse_voice_text(text: str) -> ExtractedData:
    """Parse extracted voice text to identify key information"""
    text = text.lower()
    
    extracted_data = ExtractedData()
    
    # Extract name (look for patterns like "my name is", "i am", etc.)
    name_patterns = [
        "my name is",
        "i am",
        "call me",
        "this is",
        "i'm"
    ]
    
    for pattern in name_patterns:
        if pattern in text:
            start_idx = text.find(pattern) + len(pattern)
            # Look for the next sentence or phrase
            end_idx = text.find(".", start_idx)
            if end_idx == -1:
                end_idx = text.find(",", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            name = text[start_idx:end_idx].strip()
            if name and len(name) > 2:
                # Clean up the name
                name = name.replace("and", "").replace("also", "").strip()
                extracted_data.name = name.title()
                break
    
    # Extract age or date of birth
    import re
    age_patterns = [
        r"(\d{1,2})\s*years?\s*old",
        r"age\s*(\d{1,2})",
        r"i\s*am\s*(\d{1,2})",
        r"(\d{1,2})\s*age"
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            age = int(match.group(1))
            # Convert age to approximate date of birth
            from datetime import datetime, timedelta
            current_year = datetime.now().year
            birth_year = current_year - age
            extracted_data.dob = f"{birth_year}-01-01"
            break
    
    # Extract gender
    gender_indicators = {
        "male": ["male", "man", "boy", "he", "his", "him"],
        "female": ["female", "woman", "girl", "she", "her"]
    }
    
    for gender, indicators in gender_indicators.items():
        if any(indicator in text for indicator in indicators):
            extracted_data.gender = gender
            break
    
    # Extract phone number
    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        extracted_data.phone = phone_match.group(0)
    
    # Extract address
    address_keywords = [
        "live in", "from", "address", "residence", "village", 
        "district", "state", "city", "town"
    ]
    
    for keyword in address_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            # Look for the next sentence or phrase
            end_idx = text.find(".", start_idx)
            if end_idx == -1:
                end_idx = text.find(",", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            address = text[start_idx:end_idx].strip()
            if address and len(address) > 5:
                extracted_data.address = address.title()
                break
    
    # Extract occupation
    occupation_keywords = [
        "work as", "job", "occupation", "profession", "i am a",
        "working as", "employed as"
    ]
    
    for keyword in occupation_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            # Look for the next sentence or phrase
            end_idx = text.find(".", start_idx)
            if end_idx == -1:
                end_idx = text.find(",", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            occupation = text[start_idx:end_idx].strip()
            if occupation and len(occupation) > 2:
                extracted_data.occupation = occupation.title()
                break
    
    # Extract caste
    caste_keywords = ["caste", "community", "belong to"]
    for keyword in caste_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            end_idx = text.find(".", start_idx)
            if end_idx == -1:
                end_idx = text.find(",", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            caste = text[start_idx:end_idx].strip()
            if caste and len(caste) > 2:
                extracted_data.caste = caste.title()
                break
    
    # Extract state
    state_keywords = ["state", "from", "belong to"]
    for keyword in state_keywords:
        if keyword in text:
            start_idx = text.find(keyword) + len(keyword)
            end_idx = text.find(".", start_idx)
            if end_idx == -1:
                end_idx = text.find(",", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            state = text[start_idx:end_idx].strip()
            if state and len(state) > 2:
                extracted_data.state = state.title()
                break
    
    return extracted_data

@router.post("/record", response_model=VoiceUploadResponse)
async def record_voice(
    audio_blob: bytes,
    current_user: User = Depends(get_current_user)
):
    """Process voice recording from frontend"""
    try:
        # Convert audio blob to text
        extracted_text = await convert_audio_to_text(audio_blob, "audio/wav")
        
        # Parse extracted text
        extracted_data = parse_voice_text(extracted_text)
        
        return VoiceUploadResponse(
            extracted_data=extracted_data.dict(),
            message="Voice recording processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice recording: {str(e)}"
        )
