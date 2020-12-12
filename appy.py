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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# OR with template rendering since we have multiple html files
app = Flask(__name__, template_folder="templates")

# Create base for OOM
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

session = Session(engine)
table = Base.classes.DATA
session.close()
#################################################
# Flask Routes
#################################################

# Data locations
@app.route("/static/data/")
def data_table():
    
    tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)
    
    return jsonify(tables.to_dict(orient='list'))   

# Template rendering
@app.route("/")
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/map")
def map():
    """Serve homepage template."""
    return render_template("map.html")

'''@app.route("/bubble")
def bubble():
    """Serve homepage template."""
    return render_template("bubble.html")'''

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

    return jsonify(bubble_df.to_dict(orient='list'))

@app.route("/temp")
def temp():
    """Serve homepage template."""
    return render_template("temp_plot.html")

@app.route("/api/data")
def data():

    tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)

    return jsonify(tables.to_dict(orient='list')) 

'''@app.route("/api/table/<columns>")
def api(columns):
    split_columns = [column.upper() for column in columns.split(',')]
        
    session = Session(engine)
    tables = pd.read_sql(session.query([table[column] for column in split_columns ]).statement, con=engine)
    
    session.close()
    return jsonify(tables.to_dict(orient='records')) '''
'''
if I go to localhost:5000/api/tables/year,naics_code
>>> [YEAR, NAICS_CODE]
'''

if __name__ == "__main__":
    app.run(debug=True)  

