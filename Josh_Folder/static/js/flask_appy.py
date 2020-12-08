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

#################################################
# Database Setup
#################################################
dbuser = 'postgres'
dbpassword = 'password'
dbhost = 'localhost'
dbport = '5432'
dbname= 'Enterprises'

connection_string = f"{pg_user}:{pg_password}@localhost:5432/{db_name}"
engine = create_engine(f'postgresql://{connection_string}')
engine.table_names()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create base for OOM
Base = automap_base()
Base.prepare(engine, reflect=True)

table = Base.classes.table_df
bubble = Base.classes.bubble_df

#################################################
# Flask Routes
#################################################
@app.route("/static/data/")
def table():
    
    session = Session(engine)
    tables = pd.read_sql(session.query(table.YEAR, table.STATE_DESCRIPTION, table.STATE_CODE, table.NAICS_CODE, table.INDUSTRY, table.ENTERPRISE_EMPLOYMENT_SIZE, table.BUSINESS_CLASSIFICATION, table.SECTOR, table.NUMBER_OF_FIRMS, table.NUMBER_OF_ESTABLISHMENTS, table.EMPLOYMENT, table.ANNUAL_PAYROLL, table.COLOR_GROUP).statement, con=engine)
    
    session.close()
    return jsonify(tables.to_dict(orient='records'))   

    
@app.route("/static/data/")
def bubble():

    bubbles = pd.read_sql(session.query(bubble.SECTOR, .INDUSTRY,bubble.BUSINESS_CLASSIFICATION, bubble.YEAR, bubble.COLOR_GROUP, bubble.ANNUAL_PAYROLL, bubble.EMPLOYMENT, bubble.AVG_SALARY, bubble.AVG_SALARY_F).statement, con=engine)
    return jsonify(bubbles.to_dict(orient='records'))


if __name__ == "__main__":
    app.run(debug=True)  