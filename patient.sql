DROP DATABASE IF EXISTS PatientMatching;
CREATE DATABASE PatientMatching;
Use PatientMatching;
CREATE TABLE patients (
    group_id INT,
    patient_id INT,
    patient_acct_num VARCHAR(50),
    fname VARCHAR(50),
    mid VARCHAR(10),
    lname VARCHAR(50),
    dob VARCHAR(50),
    sex VARCHAR(10),
    curr_street1 VARCHAR(100),
    curr_street2 VARCHAR(100),
    curr_city VARCHAR(50),
    curr_state VARCHAR(50),
    curr_zipcode VARCHAR(50),
    prev_fname VARCHAR(50),
    prev_mid VARCHAR(10),
    prev_lname VARCHAR(50),
    prev_street1 VARCHAR(100),
    prev_street2 VARCHAR(100),
    prev_city VARCHAR(50),
    prev_state VARCHAR(50),
    prev_zipcode VARCHAR(50)
);