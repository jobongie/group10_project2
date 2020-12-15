# import Flask and dependencies
import os
import json
import numpy as np
import pandas as pd
from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
dbuser = 'postgres'
dbpassword = 'password'
dbhost = 'localhost'
dbport = '5432'
dbname= 'Enterprises'
connection_string = f"{dbuser}:{dbpassword}@localhost:5432/{dbname}"
engine = create_engine(f'postgresql://{connection_string}')
engine.table_names()

# Create base for OOM
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
table = Base.classes.DATA

session = Session(engine)

table_df = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP, table.INDUSTRY_INDEX, table.id).statement, con=engine)

session.close() 
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# # OR with template rendering since we have multiple html files
# app = Flask(__name__, template_folder="templates")
    
#################################################
# Flask Routes
#################################################

# Data locations
@app.route("/static/data/")
def data_table():
#   session = Session(engine)

# table_df = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP, table.INDUSTRY_INDEX, table.id).statement, con=engine)

# session.close()  
    
    return jsonify(table_df.to_dict(orient='records'))   

# Template rendering
@app.route("/")
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/map")
def map():
    mapp_df = table_df[["STATE_DESCRIPTION","STATE_CODE","BUSINESS_CLASSIFICATION", "YEAR", 'EMPLOYMENT','ANNUAL_PAYROLL']].copy()
    mapg_df = mapp_df.groupby(["STATE_DESCRIPTION","STATE_CODE","BUSINESS_CLASSIFICATION", "YEAR"])
    mpayroll_sum = pd.DataFrame(mapg_df['ANNUAL_PAYROLL'].sum())
    memployment_sum = pd.DataFrame(mapg_df['EMPLOYMENT'].sum())
    map_df = pd.concat([mpayroll_sum,memployment_sum],axis=1)
    map_df.sort_values(by='YEAR', inplace=True, ascending = True)
    map_df.reset_index(inplace = True)
    
    return jsonify(map_df.to_dict(orient='records'))

@app.route("/bubble")
def bubble():
    bub_df = table_df[['INDUSTRY_INDEX', 'SECTOR', 'INDUSTRY', 'BUSINESS_CLASSIFICATION', 'EMPLOYMENT','ANNUAL_PAYROLL', 'YEAR', 'COLOR_GROUP']].copy()
    bubg_df = bub_df.groupby(["INDUSTRY_INDEX","SECTOR", "INDUSTRY", 'BUSINESS_CLASSIFICATION', 'YEAR', 'COLOR_GROUP'])
    payroll_sum = pd.DataFrame(bubg_df['ANNUAL_PAYROLL'].sum())
    employment_sum = pd.DataFrame(bubg_df['EMPLOYMENT'].sum())
    bubble_df = pd.concat([payroll_sum,employment_sum],axis=1)
    bubble_df.sort_values(by='YEAR', inplace=True, ascending = True)
    bubble_df.reset_index(inplace = True)
    bubble_df['AVG_SALARY'] = bubble_df['ANNUAL_PAYROLL'] / bubble_df['EMPLOYMENT']
    bubble_df['AVG_SALARY_F'] = bubble_df['AVG_SALARY'].astype(float).map("${:,.0f}".format)

    # Match titles to Bubble Chart Code
    bubble_df = bubble_df.rename(columns={"INDUSTRY":"industry", 
                                          "COLOR_GROUP":"color_group",
                                          "INDUSTRY_INDEX":"industry_index",
                                          "AVG_SALARY_F":"avg_salary_f",
                                          "AVG_SALARY":"avg_salary",                                          
                                          "YEAR":"year",
                                          "SECTOR":"sector",
                                          "BUSINESS_CLASSIFICATION":"business_classification",
                                          "ANNUAL_PAYROLL":"annual_payroll",
                                          "EMPLOYMENT":"employment"})
    
    return jsonify(bubble_df.to_dict(orient='list'))

@app.route("/linechart")
def linechart():
    businesses_df = table_df[["YEAR", "STATE_DESCRIPTION","STATE_CODE", 'NAICS_CODE', 'INDUSTRY', "BUSINESS_CLASSIFICATION",  'EMPLOYMENT','ANNUAL_PAYROLL']].copy()
    remove_datas = ['Large Business', 'X']
    remove_datab = ['Small Business', 'X']
    s_businesses_df = businesses_df.loc[~businesses_df["BUSINESS_CLASSIFICATION"].isin(remove_datas)]
    b_businesses_df = businesses_df.loc[~businesses_df["BUSINESS_CLASSIFICATION"].isin(remove_datab)]
    sg_businesses_df = s_businesses_df.groupby(["YEAR", "STATE_DESCRIPTION","STATE_CODE", 'NAICS_CODE', 'INDUSTRY', "BUSINESS_CLASSIFICATION"])
    s_payroll_sum = pd.DataFrame(sg_businesses_df['ANNUAL_PAYROLL'].sum())
    s_employment_sum = pd.DataFrame(sg_businesses_df['EMPLOYMENT'].sum())
    s_business_df = pd.concat([s_payroll_sum,s_employment_sum],axis=1)
    s_business_df.sort_values(by='YEAR', inplace=True, ascending = True)
    s_business_df.reset_index(inplace = True)
    s_business_df['AVG_SALARY_S'] = s_business_df['ANNUAL_PAYROLL'] / s_business_df['EMPLOYMENT']
    s_business_df = s_business_df.rename(columns = {'ANNUAL_PAYROLL': 'ANNUAL_PAYROLL_S','EMPLOYMENT': 'EMPLOYMENT_S', "BUSINESS_CLASSIFICATION": "BUSINESS_CLASSIFICATION_S"}) 
    bg_businesses_df = b_businesses_df.groupby(["YEAR", "STATE_DESCRIPTION","STATE_CODE", 'NAICS_CODE', 'INDUSTRY', "BUSINESS_CLASSIFICATION"])
    b_payroll_sum = pd.DataFrame(bg_businesses_df['ANNUAL_PAYROLL'].sum())
    b_employment_sum = pd.DataFrame(bg_businesses_df['EMPLOYMENT'].sum())
    b_business_df = pd.concat([b_payroll_sum,b_employment_sum],axis=1)
    b_business_df.sort_values(by='YEAR', inplace=True, ascending = True)
    b_business_df.reset_index(inplace = True)
    b_business_df['AVG_SALARY_B'] = b_business_df['ANNUAL_PAYROLL'] / b_business_df['EMPLOYMENT']
    b_business_df = b_business_df.rename(columns = {'ANNUAL_PAYROLL': 'ANNUAL_PAYROLL_B','EMPLOYMENT': 'EMPLOYMENT_B', "BUSINESS_CLASSIFICATION": "BUSINESS_CLASSIFICATION_B"}) 
    merge = pd.merge(s_business_df,b_business_df,  how='left', left_on=["YEAR", "STATE_DESCRIPTION","STATE_CODE", 'NAICS_CODE', 'INDUSTRY'], right_on = ["YEAR", "STATE_DESCRIPTION","STATE_CODE", 'NAICS_CODE', 'INDUSTRY'])
    merge.dropna(subset = ["BUSINESS_CLASSIFICATION_B"], inplace=True)

    merge = merge.rename(columns={"ANNUAL_PAYROLL_B":"annual_payroll_b", 
                                        "ANNUAL_PAYROLL_S":"annual_payroll_s",
                                        "AVG_SALARY_B":"avg_salary_b",
                                        "AVG_SALARY_S":"avg_salary_s",
                                        "BUSINESS_CLASSIFICATION_B":"business_classification_b",                                          
                                        "BUSINESS_CLASSIFICATION_S":"business_classification_s",
                                        "EMPLOYMENT_B":"employment_b",
                                        "EMPLOYMENT_S":"employment_s",
                                        "INDUSTRY":"industry",
                                        "NAICS_CODE":"naics_code",
                                        "STATE_CODE":"state_code",
                                        "STATE_DESCRIPTION":"state_description",
                                        "YEAR":"year"})

    return jsonify(merge.to_dict(orient='list'))
    

@app.route("/api/data")
def data():
    # session = Session(engine)
    # tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)
    # session.close()
    return jsonify(table_df.to_dict(orient='records'))

@app.route("/scatter")
def scatter():
    pmobs_df = table_df[['YEAR', 'SECTOR', 'INDUSTRY', 'NUMBER_OF_FIRMS', 'EMPLOYMENT','ANNUAL_PAYROLL']].copy()
    remove_data = ['Industries not classified', 'X']
    pmobs_df = pmobs_df.loc[~pmobs_df["INDUSTRY"].isin(remove_data)]
    pmobg_df = pmobs_df.groupby(['YEAR', 'SECTOR', 'INDUSTRY', ])
    ppayroll_sum = pd.DataFrame(pmobg_df['ANNUAL_PAYROLL'].sum())
    pemployment_sum = pd.DataFrame(pmobg_df['EMPLOYMENT'].sum())
    pfirms_sum = pd.DataFrame(pmobg_df['NUMBER_OF_FIRMS'].sum())
    pmob_df = pd.concat([ppayroll_sum,pemployment_sum, pfirms_sum],axis=1)
    pmob_df.sort_values(by='YEAR', inplace=True, ascending = True)
    pmob_df.reset_index(inplace = True)
    return jsonify(pmob_df.to_dict(orient='records'))


@app.route("/charts")
def charts():
    return render_template("bubble.html")

if __name__ == "__main__":
    app.run(debug=True)  

