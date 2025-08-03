import requests, os
from flask import Flask, request, render_template

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend/templates'))
app = Flask(__name__, template_folder=template_dir)

GEMINI_SERVER = "http://localhost:5556"
SQLITE_SERVER = "http://localhost:5557"

def get_schema_info():
    try:
        response = requests.get(f"{SQLITE_SERVER}/schema")
        response.raise_for_status()
        schema_data = response.json()
        if schema_data["status"] == "success":
            schema_text = schema_data["schema"]
            # Convert schema text back to dictionary format for template
            tables = {}
            current_table = None
            for line in schema_text.split("\n"):
                if line.startswith("Table: "):
                    current_table = line.replace("Table: ", "").strip()
                elif line.startswith("- ") and current_table:
                    tables[current_table] = line.replace("- ", "").split(", ")
            return tables
        else:
            raise Exception(schema_data.get("error", "Unknown error"))
    except Exception as e:
        print(f"Error getting schema: {e}")
        return {}

def nl_to_sql(question, schema):
    try:
        response = requests.post(
            f"{GEMINI_SERVER}/nl2sql",
            json={"question": question, "schema": schema}
        )
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["sql"]
        else:
            raise Exception(data.get("error", "Unknown error"))
    except Exception as e:
        raise Exception(f"Error converting to SQL: {e}")

def execute_sql(query):
    try:
        response = requests.post(
            f"{SQLITE_SERVER}/query",
            json={"sql": query}
        )
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            import pandas as pd
            return pd.DataFrame(data["result"], columns=data["columns"])
        else:
            raise Exception(data.get("error", "Unknown error"))
    except Exception as e:
        raise Exception(f"Error executing SQL: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    result = query = error = None
    schema = get_schema_info()

    if request.method == "POST":
        question = request.form["question"]
        schema_text = "\n".join(
            [f"Table: {table}\n- " + ", ".join(columns) for table, columns in schema.items()]
        )
        try:
            query = nl_to_sql(question, schema_text)
            result = execute_sql(query).to_html(classes="table table-bordered", index=False)
        except Exception as e:
            error = str(e)

    return render_template("index.html", query=query, result=result, error=error, schema=schema)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
