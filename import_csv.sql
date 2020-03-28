-- LOAD DATA INFILE 'PatientMatchingData.csv'
-- INTO TABLE patients
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- BULK INSERT patients
-- FROM 'PatientMatchingData.csv'
-- WITH
-- (
--     FIRSTROW = 2,
--     FIELDTERMINATOR = ',',  --CSV field delimiter
--     ROWTERMINATOR = '\n',   --Use to shift the control to next row
--     TABLOCK
-- );

