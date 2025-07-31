
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT
);

CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    job_title TEXT
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    hire_date TEXT,
    job_id TEXT,
    department_id INTEGER,
    salary REAL,
    FOREIGN KEY (job_id) REFERENCES jobs (job_id),
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

INSERT INTO departments VALUES 
(1, 'IT'),
(2, 'HR'),
(3, 'Sales'),
(4, 'Marketing'),
(5, 'Finance');

INSERT INTO jobs VALUES 
('DEV', 'Developer'),
('MGR', 'Manager'),
('ANA', 'Analyst'),
('DES', 'Designer'),
('SAL', 'Sales Representative');

INSERT INTO employees VALUES
(1, 'Alice', 'Wong', 'alice@corp.com', '2021-01-15', 'DEV', 1, 75000),
(2, 'Bob', 'Smith', 'bob@corp.com', '2022-03-20', 'MGR', 2, 85000),
(3, 'Carol', 'Johnson', 'carol@corp.com', '2021-06-10', 'ANA', 5, 65000),
(4, 'David', 'Lee', 'david@corp.com', '2023-02-15', 'DEV', 1, 72000),
(5, 'Emma', 'Brown', 'emma@corp.com', '2022-08-01', 'MGR', 3, 82000),
(6, 'Frank', 'Garcia', 'frank@corp.com', '2023-04-01', 'SAL', 3, 60000),
(7, 'Grace', 'Martinez', 'grace@corp.com', '2021-11-30', 'DES', 4, 68000),
(8, 'Henry', 'Wilson', 'henry@corp.com', '2022-09-15', 'ANA', 5, 67000),
(9, 'Isabel', 'Anderson', 'isabel@corp.com', '2023-01-20', 'DEV', 1, 73000),
(10, 'Jack', 'Taylor', 'jack@corp.com', '2021-07-01', 'SAL', 3, 63000);
