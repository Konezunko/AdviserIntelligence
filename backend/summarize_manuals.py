
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.rag import get_full_context

# Load env variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Configure API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("API Key not found.")
    sys.exit(1)

genai.configure(api_key=api_key)

print("Loading manuals...")
context = get_full_context()
if not context:
    print("No content found in manuals.")
    sys.exit(0)

print(f"Loaded context length: {len(context)} chars")

print("Generating summary...")
try:
    model = genai.GenerativeModel('models/gemini-flash-latest')
    prompt = f"""
    以下のマニュアルの内容を日本語で要約してください。
    どのような製品のマニュアルか、主なトピックは何か、そしてユーザーにとって重要な注意点は何かを含めてください。
    
    マニュアルテキスト:
    {context[:100000]} (Truncated if extremely large)
    """
    
    response = model.generate_content(prompt)
    print("\n--- Summary ---")
    print(response.text)
    print("--- End Summary ---")

except Exception as e:
    print(f"Error generating summary: {e}")
