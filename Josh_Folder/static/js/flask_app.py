# import Flask and dependencies
import os
import json
import requests
import itertools
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

engine = create_engine(f"postgres://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}")

Base = automap_base()

Base.prepare(engine, reflect=True)

table_df = Base.classes.table_df
#barChart = Base.classes.barChart
##scatterPlot = Base.classes.scatterPlot
colorMap = Base.classes.colorMap

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
