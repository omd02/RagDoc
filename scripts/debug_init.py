import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def test_init():
    start = time.time()
    api_key = os.environ.get("GROQ_API_KEY")
    print(f"Key found: {'Yes' if api_key else 'No'}")
    
    try:
        # Just init the client
        client = Groq(api_key=api_key)
        print(f"Init time: {time.time() - start:.4f}s")
    except Exception as e:
        print(f"Init error: {e}")

if __name__ == "__main__":
    test_init()
