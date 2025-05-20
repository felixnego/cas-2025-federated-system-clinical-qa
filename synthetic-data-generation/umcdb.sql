-- amsterdam_hospital_b.sql

CREATE TABLE admissions (
    admission_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(12),
    age INT,
    gender VARCHAR(10),
    admission_date DATE,
    reason TEXT
);

CREATE TABLE drugitems (
    id SERIAL PRIMARY KEY,
    admission_id VARCHAR(12),
    time TIMESTAMP,
    drug_name TEXT,
    dose VARCHAR(50),
    route VARCHAR(20)
);

CREATE TABLE freetextitems (
    id SERIAL PRIMARY KEY,
    admission_id VARCHAR(12),
    time TIMESTAMP,
    note TEXT
);

-- Sample data
-- Insert data
INSERT INTO admissions VALUES
('B001', 'PB01', 72, 'Female', '2023-05-20', 'Urosepsis'),
('B002', 'PB02', 65, 'Male', '2023-06-01', 'COPD Exacerbation');

INSERT INTO drugitems (admission_id, time, drug_name, dose, route) VALUES
('B001', '2023-05-20 12:00', 'Ceftriaxone', '1g', 'IV'),
('B002', '2023-06-01 11:30', 'Salbutamol', '5mg', 'Nebulizer');

INSERT INTO freetextitems (admission_id, time, note) VALUES
('B001', '2023-05-20 13:00', 'Patient admitted with fever and dysuria. IV antibiotics started.'),
('B002', '2023-06-01 14:00', 'Shortness of breath improved after bronchodilator therapy.');