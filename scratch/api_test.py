import sys
import os
import requests
import time

sys.path.append(r"d:\SEARCHX\backend")
import db

BASE_URL = "http://localhost:5000/api"

def print_step(step):
    print(f"\n[{step}]")

def test_api():
    test_user = {
        "username": "apitestuser",
        "email": "apitestuser@example.com",
        "password": "Password123!",
        "full_name": "API Test User"
    }
    
    # Clean up user if exists
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PENDING_USERS WHERE email = :email", {'email': test_user['email']})
    cursor.execute("DELETE FROM USERS WHERE email = :email", {'email': test_user['email']})
    conn.commit()

    # 1. Register Initiate
    print_step("1. Testing Registration (Initiate)")
    res = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}")
    assert res.status_code == 200, "Registration initiation failed"

    # 2. Get OTP
    print_step("2. Retrieving OTP from Database")
    cursor.execute("SELECT otp FROM PENDING_USERS WHERE email = :email", {'email': test_user['email']})
    row = cursor.fetchone()
    assert row is not None, "OTP not found in database"
    otp = row[0]
    print(f"Found OTP: {otp}")

    # 3. Register Verify
    print_step("3. Testing OTP Verification")
    res = requests.post(f"{BASE_URL}/auth/register/verify", json={"email": test_user['email'], "otp": otp})
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}")
    assert res.status_code == 201, "OTP verification failed"
    token = res.json().get("token")
    assert token, "Token missing from verification response"

    # 4. Login
    print_step("4. Testing Login")
    res = requests.post(f"{BASE_URL}/auth/login", json={"username": test_user['username'], "password": test_user['password']})
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}")
    assert res.status_code == 200, "Login failed"
    token = res.json().get("token")
    assert token, "Token missing from login response"

    headers = {"Authorization": f"Bearer {token}"}

    # 5. Document Upload
    print_step("5. Testing Document Upload (Pasted Text)")
    upload_data = {
        "title": "API Test Document",
        "category": "Contract",
        "jurisdiction": "Corporate",
        "language_id": "1",
        "pasted_text": "This is a strictly confidential API test contract document. It includes obligations and terms for running tests."
    }
    res = requests.post(f"{BASE_URL}/upload", data=upload_data, headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}")
    assert res.status_code == 201, "Document upload failed"
    doc_id = res.json().get("doc_id")

    # 6. Search
    print_step("6. Testing Search Engine")
    time.sleep(1) # small delay for any processing
    res = requests.get(f"{BASE_URL}/search?q=confidential", headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}...")
    assert res.status_code == 200, "Search failed"
    search_data = res.json()
    assert search_data.get("count", 0) > 0, "No results found for search"

    # 7. Analytics
    print_step("7. Testing Analytics Dashboard")
    res = requests.get(f"{BASE_URL}/analytics", headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}...")
    assert res.status_code == 200, "Analytics failed"
    
    # 8. Document Listing
    print_step("8. Testing Document Listing")
    res = requests.get(f"{BASE_URL}/documents", headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:150]}...")
    assert res.status_code == 200, "Document list failed"
    
    print("\nALL API TESTS PASSED SUCCESSFULLY!")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    test_api()
