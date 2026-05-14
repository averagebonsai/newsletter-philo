import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from openai import OpenAI
from google import genai
import resend

load_dotenv()

def get_tinyfish_client():
    try: 
        tinyfish_api_key = os.getenv("TINYFISH_API_KEY")
        return tinyfish_api_key
    except Exception as e:
        print(f"Error getting tinyfish api key: {e}")
        return None

def get_neon_client():
    try: 
        neon_database_url = os.getenv("NEON_DATABASE_URL")
        engine = create_engine(neon_database_url)
        return engine 
    except Exception as e: 
        print(f"Error getting database engine: {e}")
        return None 

def get_openai_client(): 
    try: 
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=openai_api_key)
        return client
    except Exception as e: 
        print(f"Error getting openai client: {e}")
        return None

def get_gemini_client(): 
    try: 
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=gemini_api_key)
        return client 
    except Exception as e: 
        print(f"Error getting gemini client: {e}")
        return None

def get_resend_client():
    try:
        resend_api_key = os.getenv("RESEND_API_KEY")
        resend.api_key = resend_api_key
        return resend
    except Exception as e:
        print(f"Error getting resend client: {e}")
        return None