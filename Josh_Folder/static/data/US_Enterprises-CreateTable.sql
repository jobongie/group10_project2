-- Step 1 - Drop existing tables if any

DROP TABLE "NAICS";
DROP TABLE "BUSINESSES";
DROP TABLE "STATES";

-- Step 2 - Create NAICS Look up Table
CREATE TABLE "NAICS" (
    "NAICS CODE" VARCHAR PRIMARY KEY, 
    "NAME" VARCHAR UNIQUE
);

-- Step 3 - Create Fact Table
CREATE TABLE "BUSINESSES" (
    "FIPS STATE CODE" VARCHAR,
    "STATE DESCRIPTION" VARCHAR,
    "NAICS CODE" VARCHAR,
    "NAICS DESCRIPTION" VARCHAR,
    "ENTERPRISE EMPLOYMENT SIZE" VARCHAR,
    "NUMBER OF FIRMS" INTEGER,
    "NUMBER OF ESTABLISHMENTS" INTEGER,
    "EMPLOYMENT" INTEGER,
    "EMPLOYMENT RANGE FLAG" VARCHAR,
    "EMPLOYMENT NOISE FLAG" VARCHAR,
    "ANNUAL PAYROLL ($1,000)" INTEGER,
    "ANNUAL PAYROLL NOISE FLAG" VARCHAR,
    "YEAR" INTEGER,
    "ENTERPRISE EMPLOYMENT SIZE 2" VARCHAR,
    "Source_Name" VARCHAR
);

-- Step 4 - Create State Lookup table
CREATE TABLE "STATES" (
    "STATE" VARCHAR PRIMARY KEY,
    "ABBREV" VARCHAR UNIQUE,
    "STATE CODE" VARCHAR UNIQUE
);

-- Step 5 - Alter Fact Tables to include NAICS Foreign Key
ALTER TABLE "BUSINESSES" ADD CONSTRAINT "fk_BUSINESSES_NAICS CODE" FOREIGN KEY("NAICS CODE")
REFERENCES "NAICS" ("NAICS CODE");

-- Step 6 - Alter Fact Tables to include State Foreign Key
ALTER TABLE "BUSINESSES" ADD CONSTRAINT "fk_BUSINESSES_STATE DESCRIPTION" FOREIGN KEY("STATE DESCRIPTION")
REFERENCES "STATES" ("STATE");


-- Step 7 - Import the three data tables from csv files starting with "2017_NAICS_Structure_Summary.csv" "NAICS" table,
--           "state_codes.csv" to "STATES" table, "Consolidated State_NAISC Sector 2008-2017" to BUSINESSES" table.

-- Step 8 - NOTE: You have to import data first!!!!! Alter Fact Table to include Primary Key id column 
ALTER TABLE "BUSINESSES"
ADD COLUMN id SERIAL PRIMARY KEY;

-- Step 9 - Validate tables loaded correctly by running each one of the queries below:
SELECT * 
FROM "BUSINESSES";

SELECT * 
FROM "STATES";

SELECT * 
FROM "NAICS";

