import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Starting Backend Verification...")
    
    # 1. Create Target
    print("\n1. Creating Target...")
    res = requests.post(f"{BASE_URL}/api/targets/", json={
        "email": "employee@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT"
    })
    if res.status_code == 201:
        print("Success:", res.json())
        target_id = res.json()['id']
    elif res.status_code == 400:
        print("Target likely already exists:", res.json())
    else:
        print("Failed:", res.text)
        return

    # 2. Generate Template (Mocking AI or using real if key works)
    # We will just create a template manually to save API quota in test or ensure speed
    print("\n2. Creating Template (Manual)...")
    res = requests.post(f"{BASE_URL}/api/templates/", json={
        "name": "Test Phish",
        "subject": "Urgent: Update Password",
        "body_content": "<p>Click here</p>",
        "is_ai_generated": False
    })
    if res.status_code == 201:
        print("Success:", res.json())
        template_id = res.json()['id']
    else:
        print("Failed:", res.text)
        return

    # 3. Create Campaign
    print("\n3. Creating Campaign...")
    res = requests.post(f"{BASE_URL}/api/campaigns/", json={
        "name": "Q4 Phishing Test",
        "template_id": template_id
    })
    if res.status_code == 201:
        print("Success:", res.json())
        campaign_id = res.json()['id']
    else:
        print("Failed:", res.text)
        return

    # 4. Launch Campaign
    print("\n4. Launching Campaign...")
    res = requests.post(f"{BASE_URL}/api/campaigns/{campaign_id}/launch")
    if res.status_code == 200:
        print("Success:", res.json())
    else:
        print("Failed:", res.text)
        return

    # 5. Get Stats
    print("\n5. Getting Stats...")
    res = requests.get(f"{BASE_URL}/api/campaigns/{campaign_id}/stats")
    if res.status_code == 200:
        print("Success:", res.json())
    else:
        print("Failed:", res.text)

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the server is running!")
