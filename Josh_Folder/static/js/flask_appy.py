# import Flask and dependencies
import os
import json
import requests
import numpy as np
import pandas as pd
from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
'''dbuser = 'postgres'
dbpassword = 'password'
dbhost = 'localhost'
dbport = '5432'
dbname= 'Enterprises'

connection_string = f"{pg_user}:{pg_password}@localhost:5432/{db_name}"
engine = create_engine(f'postgresql://{connection_string}')
engine.table_names()'''

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# OR with template rendering since we have multiple html files
app = Flask(__name__, template_folder="templates")

# Create base for OOM
Base = automap_base()
Base.prepare(engine, reflect=True)

table = Base.classes.table_df
bubble = Base.classes.tablebusiness


#################################################
# Flask Routes
#################################################

# Data locations
@app.route("/static/data/")
def table():
    
    session = Session(engine)
    tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)
    bubbles = pd.read_sql(session.query(bubble.Sector, bubble.Industry, bubble.Industry_number, bubble.Business_class, bubble.INDUSTRY, bubble.Sum_of_NUMBER_OF_FIRMS, bubble.Sum_of_EMPLOYMENT, bubble.Sum_of_ANNUAL_PAYROLL, bubble.Annual_Payroll, bubble.NUMBER_OF_ESTABLISHMENTS, bubble.EMPLOYMENT, bubble.ANNUAL_PAYROLL, bubble.Employee_salary).statement, con=engine)
                                                  
    session.close()
    return jsonify(tables.to_dict(orient='records'))   

# Template rendering
@app.route("/")
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/map")
def map():
    """Serve homepage template."""
    return render_template("map.html")

@app.route("/bubble")
def bubble():
    """Serve homepage template."""
    return render_template("bubble.html")

@app.route("/table")
def table():
    """Serve homepage template."""
    return render_template("table.html")

@app.route("/temp")
def temp():
    """Serve homepage template."""
    return render_template("temp_plot.html")

@app.route("/api/data")
def data():
    session = Session(engine)
    bubbles = pd.read_sql(session.query(bubble.Sector, bubble.Industry, bubble.Industry_number, bubble.Business_class, bubble.INDUSTRY, bubble.Sum_of_NUMBER_OF_FIRMS, bubble.Sum_of_EMPLOYMENT, bubble.Sum_of_ANNUAL_PAYROLL, bubble.Annual_Payroll, bubble.NUMBER_OF_ESTABLISHMENTS, bubble.EMPLOYMENT, bubble.ANNUAL_PAYROLL, bubble.Employee_salary).statement, con=engine)
    
    session.close()
    return jsonify(tables.to_dict(orient='records')) 

@app.route("/api/table/<columns>")
def api(columns):
    split_columns = [column.upper() for column in columns.split(',')]
        
    session = Session(engine)
    bubbles = pd.read_sql(session.query([table[column] for column in split_columns ]).statement, con=engine)
    # tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)
    
    session.close()
    return jsonify(tables.to_dict(orient='records')) 
'''
if I go to localhost:5000/api/table/year,naics_code

>>> [YEAR, NAICS_CODE]


'''

if __name__ == "__main__":
    app.run(debug=True)  