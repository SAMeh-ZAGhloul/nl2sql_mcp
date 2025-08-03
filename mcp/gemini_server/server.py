from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
from functools import wraps

# Load environment variables from .env file in parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = Flask(__name__)

# Configure the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def mcp_endpoint(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route("/nl2sql", methods=["POST"])
@mcp_endpoint
def nl_to_sql():
    data = request.get_json()
    
    if "question" not in data or "schema" not in data:
        return jsonify({"error": "Missing required fields: question and schema"}), 400

    question = data["question"]
    schema = data["schema"]
    
    prompt = f"""
You are a SQL expert working with the following SQLite schema:

{schema}

Convert the following natural language question to an SQLite query:

Question: {question}

SQL:
"""
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        response = requests.post(
            GEMINI_ENDPOINT,
            headers=headers,
            json={
                "model": "gemini-1.5-flash",
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
        )
        response.raise_for_status()
        sql_query = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Clean up the response
        if sql_query.startswith("```sqlite"):
            sql_query = sql_query.replace("```sqlite", "").strip()
        if sql_query.endswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        return jsonify({
            "sql": sql_query,
            "status": "success"
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Gemini API error: {str(e)}",
            "status": "error"
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5556)
