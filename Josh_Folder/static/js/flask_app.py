# import Flask and dependencies
import os
import json
import requests
import numpy as np
import pandas as pd
from pprint import pprint
from flask import Flask, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

dbuser = 'postgres'
dbpassword = 'password'
dbhost = 'localhost'
dbport = '5432'
dbname= 'Enterprises'

connection_string = f"{pg_user}:{pg_password}@localhost:5432/{db_name}"
engine = create_engine(f'postgresql://{connection_string}')
engine.table_names()

# Create DataFrames from SQL Query
bus_df = pd.read_sql_query('select * from "BUSINESSES"', con=engine)
naics_df = pd.read_sql_query('select * from "NAICS"', con=engine)
states_df = pd.read_sql_query('select * from "STATES"', con=engine)

# Back to Pandas
# Refine Business Dataframe to only rows with employment values (where 'Employment Range Flag' is null)
bus_df1 = bus_df[pd.isnull(bus_df['EMPLOYMENT RANGE FLAG'])]
bus_df2 = bus_df1.copy()

#Refine Business Dataframe to only rows with relevant Enterprise Employment range categories
# bus_df['ENTERPRISE EMPLOYMENT SIZE 2'].unique()
bus_df2['ENTERPRISE EMPLOYMENT SIZE 2'] = bus_df2['ENTERPRISE EMPLOYMENT SIZE 2'].astype(str).str.strip()

good_data = ['0--4','5--9', '10--19', '20--99','100--499','500+']
bad_data = ['Total',' <20','<500' ,'<20','<5']

bus_df2 = bus_df2.loc[~bus_df2['ENTERPRISE EMPLOYMENT SIZE 2'].isin(bad_data)]

# Refine Business Dataframe to only rows with relevant Industry names
remove_data = ['Total', 'X']
bus_df2 = bus_df2.loc[~bus_df2['NAICS DESCRIPTION'].isin(remove_data)]

# Create column to classify Enterprise Employment ranges into Small & Large Business categories
def classifier(row):
    if row["ENTERPRISE EMPLOYMENT SIZE 2"] in ['0--4', '20--99', '10--19', '5--9','100--499']:
        return "Small Business"
    elif row["ENTERPRISE EMPLOYMENT SIZE 2"] == '500+':
        return "Large Business" 
    else:
        return "N/A"
    
bus_df2["BUSINESS_CLASSIFICATION"] = bus_df2.apply(classifier, axis = 1)

# Create 'BC Code' for Concatenated Column for Visualization
def bc_code(row):
    if row["ENTERPRISE EMPLOYMENT SIZE 2"] in ['0--4', '20--99', '10--19', '5--9','100--499']:
        return "S"
    elif row["ENTERPRISE EMPLOYMENT SIZE 2"] == '500+':
        return "L" 
    else:
        return "N/A"
    
bus_df2["BC_CODE"] = bus_df2.apply(bc_code, axis = 1)

# Create column for color grouping to be used in Bubble Visualization
def color_grouping(row):
    if row["ENTERPRISE EMPLOYMENT SIZE 2"] in ['0--4', '20--99', '<20', '10--19', '5--9','100--499']:
        return 1
    elif row["ENTERPRISE EMPLOYMENT SIZE 2"] == '500+':
        return 2 
    else:
        return "N/A"

bus_df2["COLOR_GROUP"] = bus_df2.apply(color_grouping, axis=1)   

# Create column for Sector grouping to be used in Bubble Visualization
bus_df2['SECTOR'] = bus_df2["BC_CODE"] + bus_df2['NAICS CODE']

# Convert Payroll column to real value from rounded value
bus_df2['ANNUAL PAYROLL'] = bus_df2['ANNUAL PAYROLL ($1,000)'] * 1000

# Refine Business & States Dataframes to only include relevant columns
business_df = bus_df2[[ 'STATE DESCRIPTION', 'NAICS CODE', 'ENTERPRISE EMPLOYMENT SIZE 2', 'SECTOR', 'BUSINESS_CLASSIFICATION', 'NUMBER OF FIRMS', 'NUMBER OF ESTABLISHMENTS', 'EMPLOYMENT', 'ANNUAL PAYROLL', 'YEAR', 'COLOR_GROUP']].copy()


states_df = states_df.rename(columns={'STATE':'STATE DESCRIPTION'})
states_df = states_df[["STATE DESCRIPTION","STATE CODE"]]

# Create joins to establish consolidated dataframe
business_df1 = pd.merge(business_df,naics_df,on='NAICS CODE',how='left')
business_df1= pd.merge(business_df1,states_df,on='STATE DESCRIPTION',how='left')

# Reorder Dataframe
business_df1 = business_df1[['YEAR','STATE DESCRIPTION', 'STATE CODE', 'NAICS CODE', 'NAME', 'ENTERPRISE EMPLOYMENT SIZE 2', 'BUSINESS_CLASSIFICATION', 'SECTOR', 'NUMBER OF FIRMS', 'NUMBER OF ESTABLISHMENTS', 'EMPLOYMENT', 'ANNUAL PAYROLL', 'COLOR_GROUP']].copy()

# Table with all relavent data
table_df = business_df1.rename(columns = {'NAME': 'INDUSTRY','STATE DESCRIPTION': 'STATE_DESCRIPTION', 'STATE CODE' : 'STATE_CODE', 'NAICS CODE' : 'NAICS_CODE' , 'ENTERPRISE EMPLOYMENT SIZE 2' : 'ENTERPRISE_EMPLOYMENT_SIZE', 'NUMBER OF FIRMS': 'NUMBER_OF_FIRMS', 'NUMBER OF ESTABLISHMENTS' : 'NUMBER_OF_ESTABLISHMENTS', 'ANNUAL PAYROLL' : 'ANNUAL_PAYROLL' })

# Create data frame for Bubble Visualization
bub_df = table_df[['SECTOR', 'INDUSTRY', 'BUSINESS_CLASSIFICATION', 'EMPLOYMENT','ANNUAL_PAYROLL', 'YEAR', 'COLOR_GROUP']].copy()

bubg_df = bub_df.groupby(["SECTOR", "INDUSTRY", 'BUSINESS_CLASSIFICATION', 'YEAR', 'COLOR_GROUP'])
payroll_sum = pd.DataFrame(bubg_df['ANNUAL_PAYROLL'].sum())
employment_sum = pd.DataFrame(bubg_df['EMPLOYMENT'].sum())

#Create a summary data frame by concatenating the results data frames into one data frame to hold the results
bubble_df = pd.concat([payroll_sum,employment_sum],axis=1)

#Sort by total purchase count column in descending order 
bubble_df.sort_values(by='YEAR', inplace=True, ascending = True)

#Display summary data frame
bubble_df.reset_index(inplace = True)

# Create columns to show Average Salary per Employee
bubble_df['AVG_SALARY'] = bubble_df['ANNUAL_PAYROLL'] / bubble_df['EMPLOYMENT']
bubble_df['AVG_SALARY_F'] = bubble_df['AVG_SALARY'].astype(float).map("${:,.0f}".format)

# Write Dataframes to PostgreSQL DB
bubble_df.to_sql(name="BUBBLE_SUMMARY", con=engine, if_exists='replace', index=False)
table_df.to_sql(name="DATA", con=engine, if_exists='replace', index=False)

# Output file name and path
file_path = os.path.join(".","static","data","table_df.csv")
table_df.to_csv(file_path, index=False, header=True)

# Output file name and path
file_path = os.path.join(".","static","data","bubble_df.csv")
bubble_df.to_csv(file_path, index=False, header=True)


# Create base for OOM
#Base = automap_base()
#Base.prepare(engine, reflect=True)

#table_df = Base.classes.table_df

#################################################
# Flask Routes
#################################################
@app.route("/static/data/")
def table_df():
    session = Session(engine)

    data_table = pd.read_sql(session.query(table_df.YEAR, table_df.STATE_DESCRIPTION, table_df.NAICS_CODE, table_df.NAME, table_df.ENTERPRISE_EMPLOYMENT_SIZE, table_df.NUMBER_OF_FIRMS, table_df.NUMBER_OF_ESTABLISHMENTS, table_df.EMPLOYMENT, table_df.ANNUAL_PAYROLL).statement, con=engine)
    #barChart = pd.read_sql(session.query(barChart.YEAR, barChart.STATE_DESCRIPTION, barChart.NAICS_CODE, barChart.NAME, barChart.ENTERPRISE_EMPLOYMENT_SIZE, barChart.NUMBER_OF_ESTABLISHMENTS, barChart.EMPLOYMENT, barChart.ANNUAL_PAYROLL).statement, con=engine)
    #scatterPlot pd.read_sql(session.query(scatterPlot.YEAR, scatterPlot.STATE_DESCRIPTION, scatterPlot.NAICS_CODE, scatterPlot.NAME, scatterPlot.ENTERPRISE_EMPLOYMENT_SIZE, scatterPlot.EMPLOYMENT, scatterPlot.ANNUAL_PAYROLL).statement, con=engine)
    #colorMap pd.read_sql(session.query(colorMap.YEAR, colorMap.STATE_DESCRIPTION, colorMap.NAICS_CODE, colorMap.NAME, colorMap.ENTERPRISE_EMPLOYMENT_SIZE, colorMap.EMPLOYMENT, colorMap.ANNUAL_PAYROLL).statement, con=engine)

    session.close()
    return jsonify(data_table.to_dict(orient='records'))
    return render_template("index.html", data_table=data_table) #correlates to {{ data }} in index.html
    #return jsonify(barChart.to_dict(orient='records'))
    #return jsonify(scatterPlot.to_dict(orient='records'))
    #return jsonify(colorMap.to_dict(orient='records'))
    

if __name__ == "__main__":
    app.run(debug=True)  
