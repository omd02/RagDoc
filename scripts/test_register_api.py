import requests
import uvicorn
import threading
import time
from src.api.server import app
import os

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8002)

if __name__ == "__main__":
    if os.path.exists("storage/app.db"):
        # os.remove("storage/app.db") # Don't remove for now, let's see what happens
        pass
        
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(15) # Wait for startup
    
    email = "test_reg@example.com"
    password = "password123"
    
    print(f"Testing registration for {email}...")
    try:
        response = requests.post(
            "http://127.0.0.1:8002/register",
            json={"email": email, "password": password}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
    except Exception as e:
        print(f"Registration request failed: {e}")
    
    print("Test complete.")
