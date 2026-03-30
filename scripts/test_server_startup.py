from src.api.server import app
import uvicorn
import threading
import time
import requests

def run_server():
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001)
    except Exception as e:
        print(f"Server failed to start: {e}")

if __name__ == "__main__":
    print("Starting server test on port 8001...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(10) 
    
    try:
        response = requests.get("http://127.0.0.1:8001/")
        print(f"Server response: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
    
    print("Test complete.")
