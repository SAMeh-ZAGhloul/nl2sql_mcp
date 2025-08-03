# Natural Language to SQL Query with MCP Architecture

This project is a microservices-based Flask application that converts natural language questions into SQL queries. It uses the Model Context Protocol (MCP) architecture to separate concerns between the Gemini API service and SQLite database service.

## Project Structure

```
nl2sql_mcp/
├── backend/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── db/
│   ├── hr.db              # SQLite database
│   └── init.sql           # Database initialization script
├── frontend/
│   └── templates/
│       └── index.html     # Web interface template
└── mcp/
    ├── gemini_server/
    │   └── server.py      # Gemini MCP implementation
    └── sqlite_server/
        └── server.py      # SQLite MCP implementation
```

## Architecture

```mermaid
graph TD
    subgraph "User Interface"
        A["Web Browser"]
    end

    subgraph "Frontend (Port 5555)"
        B["Flask App"]
    end

    subgraph "MCP Servers"
        C["Gemini Server (5556)"]
        D["SQLite Server (5557)"]
    end

    subgraph "External Services"
        E["Gemini API"]
    end

    subgraph "Database"
        F["HR Database"]
    end

    A -- "HTTP Request" --> B
    B -- "NLQ-to-SQL Request" --> C
    C -- "API Call" --> E
    E -- "SQL Response" --> C
    C -- "SQL Query" --> B
    B -- "DB Schema Request" --> D
    D -- "Schema Info" --> B
    B -- "Execute SQL" --> D
    D -- "Query Result" --> B
    D -- "DB Access" --> F
    B -- "HTML Response" --> A
```

### MCP Server Details

#### 1. Gemini MCP Server (Port 5556)
- **Endpoint**: `/nl2sql`
- **Method**: POST
- **Input**:
  ```json
  {
    "question": "Natural language question",
    "schema": "Database schema description"
  }
  ```
- **Output**:
  ```json
  {
    "sql": "Generated SQL query",
    "status": "success"
  }
  ```
- **Features**:
  - Natural Language to SQL conversion
  - Context-aware query generation
  - Schema-based validation
  - Error handling with detailed messages

#### 2. SQLite MCP Server (Port 5557)
- **Endpoints**: 
  1. `/schema` (GET)
     ```json
     {
       "schema": "Table descriptions",
       "status": "success"
     }
     ```
  2. `/query` (POST)
     - Input:
       ```json
       {
         "sql": "SQL query to execute"
       }
       ```
     - Output:
       ```json
       {
         "result": ["Query results"],
         "columns": ["Column names"],
         "status": "success"
       }
       ```
- **Features**:
  - Schema introspection
  - Query execution
  - Result formatting
  - Error handling with SQL-specific details

## Key Benefits of MCP Architecture

### 1. Schema Flexibility
The system is completely database-schema agnostic. You can change the database structure without modifying any code:
- SQLite MCP automatically discovers tables and columns
- Gemini MCP adapts to any schema description
- UI dynamically updates to show new schema
- Only need to update `init.sql` and recreate `hr.db`

### 2. Separation of Concerns
Each service has a specific responsibility:
- Main App (5555): User interface and service coordination
- Gemini MCP (5556): Natural language to SQL conversion
- SQLite MCP (5557): Database operations and schema management

### 3. Standardized Interfaces
Clear, well-defined JSON API endpoints:
```
Gemini MCP:
POST /nl2sql
Request: {"question": "...", "schema": "..."}
Response: {"sql": "...", "status": "success"}

SQLite MCP:
GET /schema
Response: {"schema": "...", "status": "success"}

POST /query
Request: {"sql": "..."}
Response: {"result": [...], "columns": [...], "status": "success"}
```

### 4. Enhanced Maintainability
- Independent scaling of services
- Isolated testing of components
- Clear error handling per service
- Easy to add new features or services

## Components

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
