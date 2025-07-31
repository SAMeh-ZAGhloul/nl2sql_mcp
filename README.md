# Natural Language to SQL Query with MCP Architecture

This project is a microservices-based Flask application that converts natural language questions into SQL queries. It uses the Model Context Protocol (MCP) architecture to separate concerns between the Gemini API service and SQLite database service.

## Architecture

The application consists of three main components:

1. **Main Application** (Port 5555)
   - Web interface for user interaction
   - Coordinates between Gemini and SQLite services
   - Displays results in a user-friendly format

2. **Gemini MCP Server** (Port 5556)
   - Handles natural language to SQL conversion
   - Communicates with Google's Gemini API
   - Provides a standardized JSON API endpoint

3. **SQLite MCP Server** (Port 5557)
   - Manages database operations
   - Provides schema information
   - Executes SQL queries
   - Returns results in a standardized format

## Features

- Convert natural language questions to SQL queries using Gemini API
- Execute SQL queries against SQLite database
- Display results in a user-friendly table format
- View database schema on web interface
- Microservices architecture for better scalability and maintenance
- Standardized JSON API endpoints

## Schema

The database contains the following tables:

- `employees` (employee_id, first_name, last_name, email, hire_date, job_id, department_id, salary)
- `departments` (department_id, department_name)
- `jobs` (job_id, job_title)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   sqlite3 hr.db < init.sql
   ```

4. **Configure the API key:**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Running the Application

Start each component in a separate terminal:

1. **Start SQLite MCP Server:**
   ```bash
   cd sqlite_server
   python3 server.py
   ```

2. **Start Gemini MCP Server:**
   ```bash
   cd gemini_server
   python3 server.py
   ```

3. **Start Main Application:**
   ```bash
   python3 app.py
   ```

Access the application at `http://localhost:5555`

## API Endpoints

### Gemini MCP Server (localhost:5556)
- `POST /nl2sql`
  - Convert natural language to SQL
  - Request body: `{"question": "string", "schema": "string"}`

### SQLite MCP Server (localhost:5557)
- `GET /schema`
  - Get database schema
- `POST /query`
  - Execute SQL query
  - Request body: `{"sql": "string"}`

## Screenshot

![Application Screenshot](sample.png)

## How to Use

1.  Open your web browser and navigate to `http://localhost:5555`.
2.  You will see the main page with the database schema displayed.
3.  Enter a question about the HR data in the input box (e.g., "Who are the employees in the IT department?").
4.  Click "Ask" to submit your question.
5.  The application will convert your question to an SQL query, execute it, and display the results in a table.
