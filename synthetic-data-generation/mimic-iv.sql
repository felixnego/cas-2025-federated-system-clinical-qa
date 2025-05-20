-- mimic_hospital_a.sql

CREATE TABLE patients (
    patient_id VARCHAR(12) PRIMARY KEY,
    gender VARCHAR(10),
    dob DATE
);

CREATE TABLE admissions (
    admission_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(12),
    admission_time TIMESTAMP,
    discharge_time TIMESTAMP,
    diagnosis TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE vitals (
    id SERIAL PRIMARY KEY,
    admission_id VARCHAR(12),
    time TIMESTAMP,
    heart_rate INT,
    blood_pressure VARCHAR(15),
    temperature FLOAT,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE notes (
    note_id SERIAL PRIMARY KEY,
    admission_id VARCHAR(12),
    time TIMESTAMP,
    text TEXT,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

-- Sample data
INSERT INTO patients VALUES
('P001', 'Male', '1985-03-22'),
('P002', 'Female', '1990-11-10'),
('P003', 'Other', '1975-07-04');

INSERT INTO admissions VALUES
('A001', 'P001', '2023-06-01 14:00', '2023-06-05 10:00', 'Pneumonia'),
('A002', 'P002', '2023-06-10 09:00', '2023-06-12 15:00', 'Heart failure'),
('A003', 'P003', '2023-07-01 08:00', '2023-07-04 14:00', 'Sepsis');

INSERT INTO vitals (admission_id, time, heart_rate, blood_pressure, temperature) VALUES
('A001', '2023-06-01 14:30', 102, '130/85', 38.5),
('A001', '2023-06-02 08:00', 98, '125/80', 37.8),
('A002', '2023-06-10 10:00', 110, '140/90', 37.2),
('A003', '2023-07-01 09:00', 120, '135/88', 39.0);

INSERT INTO notes (admission_id, time, text) VALUES
('A001', '2023-06-01 15:00', 'Patient presented with fever and productive cough. Antibiotics started.'),
('A002', '2023-06-10 12:00', 'Dyspnea and edema noted. Lasix administered. Monitoring response.'),
('A003', '2023-07-01 10:30', 'Suspected sepsis. Broad-spectrum antibiotics initiated. Blood cultures drawn.');
