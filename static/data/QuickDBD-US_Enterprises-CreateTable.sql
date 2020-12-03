-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/H23emM
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "NAICS" (
    "sector" VARCHAR   NOT NULL,
    "name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_NAICS" PRIMARY KEY (
        "sector"
     )
);

CREATE TABLE "BUSINESSES" (
    "fips_state_code" VARCHAR   NOT NULL,
    "state_description" VARCHAR   NOT NULL,
    "naics_code" VARCHAR   NOT NULL,
    "naics_description" VARCHAR   NOT NULL,
    "enterprise_employment_size" VARCHAR   NOT NULL,
    "number_of_firms" INTEGER   NOT NULL,
    "number_of_establishments" INTEGER   NOT NULL,
    "employment" INTEGER   NOT NULL,
    "employment_range_flag" VARCHAR   NOT NULL,
    "employment_noise_flag" VARCHAR   NOT NULL,
    "annual_payroll_($1,000)" INTEGER   NOT NULL,
    "annual_payroll_noise_flag" VARCHAR   NOT NULL,
    "year" INTEGER   NOT NULL,
    "enterprise_employment_size_2" VARCHAR   NOT NULL,
    "source_name" VARCHAR   NOT NULL
);

ALTER TABLE "NAICS" ADD CONSTRAINT "fk_NAICS_sector" FOREIGN KEY("sector")
REFERENCES "BUSINESSES" ("naics_code");

