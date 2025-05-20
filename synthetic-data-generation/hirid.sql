-- hirid_hospital_c.sql

CREATE TABLE patient_metadata (
    patient_id VARCHAR(12) PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    icu_admission DATE
);

CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(12),
    timestamp TIMESTAMP,
    variable_name TEXT,
    value FLOAT
);

CREATE TABLE pharma (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(12),
    timestamp TIMESTAMP,
    medication TEXT,
    dose FLOAT,
    unit TEXT
);

-- Sample data
INSERT INTO patient_metadata VALUES
('HC01', 60, 'Male', '2023-05-10'),
('HC02', 45, 'Female', '2023-06-02');

INSERT INTO observations (patient_id, timestamp, variable_name, value) VALUES
('HC01', '2023-05-10 08:00', 'HR', 110),
('HC01', '2023-05-10 08:30', 'TEMP', 38.2),
('HC02', '2023-06-02 09:00', 'HR', 95);

INSERT INTO pharma (patient_id, timestamp, medication, dose, unit) VALUES
('HC01', '2023-05-10 08:30', 'Norepinephrine', 0.1, 'mcg/kg/min'),
('HC02', '2023-06-02 09:30', 'Dopamine', 2.5, 'mcg/kg/min');
