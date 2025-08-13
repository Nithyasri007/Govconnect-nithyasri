#!/usr/bin/env python3
"""
Simple test script to test backend endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_signup():
    """Test signup endpoint"""
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
        print(f"Signup: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"User ID: {result['user']['id']}")
            print(f"Token: {result['access_token'][:20]}...")
            return result['access_token']
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Signup failed: {e}")
        return None

def test_login():
    """Test login endpoint"""
    try:
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"User ID: {result['user']['id']}")
            print(f"Token: {result['access_token'][:20]}...")
            return result['access_token']
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_get_schemes():
    """Test get schemes endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/schemes/")
        print(f"Get schemes: {response.status_code}")
        if response.status_code == 200:
            schemes = response.json()
            print(f"Found {len(schemes)} schemes")
            if schemes:
                print(f"First scheme: {schemes[0]['title']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Get schemes failed: {e}")
        return False

def test_document_processing():
    """Test document processing endpoint"""
    try:
        # Create a simple test image (1x1 pixel PNG)
        import base64
        test_image_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        
        files = {'file': ('test.png', test_image_data, 'image/png')}
        response = requests.post(f"{BASE_URL}/api/documents/process", files=files)
        print(f"Document processing: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Extracted data: {result}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Document processing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing backend endpoints...")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("❌ Health check failed")
        return
    
    # Test signup
    token = test_signup()
    if not token:
        print("❌ Signup failed")
        return
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Login failed")
        return
    
    # Test get schemes
    if not test_get_schemes():
        print("❌ Get schemes failed")
        return
    
    # Test document processing
    if not test_document_processing():
        print("❌ Document processing failed")
        return
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    main()
