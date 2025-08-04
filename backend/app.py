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

def prepare_chart_data(df):
    """Prepare data for chart visualization based on query results."""
    if df.empty:
        return [], []
    
    # If we have numeric data, use it for visualization
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        # Use the first string/object column as labels if available
        label_col = df.select_dtypes(include=['object']).columns[0] if len(df.select_dtypes(include=['object']).columns) > 0 else df.index
        value_col = numeric_cols[0]
        
        # Group by label column if it exists
        if label_col is not df.index:
            chart_data = df.groupby(label_col)[value_col].sum().tolist()
            chart_labels = df.groupby(label_col)[value_col].sum().index.tolist()
        else:
            chart_data = df[value_col].tolist()
            chart_labels = [str(x) for x in df.index.tolist()]
    else:
        # If no numeric columns, count occurrences of first column
        first_col = df.columns[0]
        counts = df[first_col].value_counts()
        chart_data = counts.tolist()
        chart_labels = counts.index.tolist()
    
    return chart_data, chart_labels

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
            df = pd.DataFrame(data["result"], columns=data["columns"])
            return df
        else:
            raise Exception(data.get("error", "Unknown error"))
    except Exception as e:
        raise Exception(f"Error executing SQL: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    result = query = error = None
    chart_data = []
    chart_labels = []
    schema = get_schema_info()

    if request.method == "POST":
        question = request.form["question"]
        schema_text = "\n".join(
            [f"Table: {table}\n- " + ", ".join(columns) for table, columns in schema.items()]
        )
        try:
            query = nl_to_sql(question, schema_text)
            df = execute_sql(query)
            result = df.to_html(classes="table table-bordered", index=False)
            chart_data, chart_labels = prepare_chart_data(df)
        except Exception as e:
            error = str(e)

    return render_template("index.html", 
                         query=query, 
                         result=result, 
                         error=error, 
                         schema=schema,
                         chart_data=chart_data,
                         chart_labels=chart_labels)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
