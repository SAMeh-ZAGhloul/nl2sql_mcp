from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
from functools import wraps

app = Flask(__name__)

DB_PATH = "../../db/hr.db"

def mcp_endpoint(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        return f(*args, **kwargs)
    return decorated_function

def get_schema_info():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tables = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for (table,) in cursor.fetchall():
        cursor.execute(f"PRAGMA table_info({table});")
        cols = [col[1] for col in cursor.fetchall()]
        tables[table] = cols
    conn.close()
    return tables

@app.route("/schema", methods=["GET"])
def get_schema():
    try:
        schema = get_schema_info()
        schema_text = "\n".join(
            [f"Table: {table}\n- " + ", ".join(columns) for table, columns in schema.items()]
        )
        return jsonify({
            "schema": schema_text,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route("/query", methods=["POST"])
@mcp_endpoint
def execute_query():
    data = request.get_json()
    
    if "sql" not in data:
        return jsonify({"error": "Missing required field: sql"}), 400
    
    sql = data["sql"]
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(sql, conn)
        conn.close()
        
        return jsonify({
            "result": df.to_dict(orient="records"),
            "columns": df.columns.tolist(),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5557)
