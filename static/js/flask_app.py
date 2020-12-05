# import Flask and dependencies
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import numpy as np
import pandas as pd

app = Flask(__name__)

dbuser = 'postgres'
dbpassword = 'password'
dbhost = 'localhost'
dbport = '5432'
dbname= 'Enterprises'

engine = create_engine(f"postgres://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}")

Base = automap_base()

Base.prepare(engine, reflect=True)

data = Base.classes.data_df

#################################################
# Flask Routes
#################################################
@app.route("/")
def states_electoral_df():
    session = Session(engine)

    # HTML Display
    data_table = pd.read_sql(session.query(data.YEAR, data.STATE_DESCRIPTION, data.NAICS_CODE, data.NAME, data.ENTERPRISE_EMPLOYMENT_SIZE, data.NUMBER_OF_FIRMS, data.NUMBER_OF_ESTABLISHMENTS, data.EMPLOYMENT, data.ANNUAL_PAYROLL).statement, con=engine)
    barChart = pd.read_sql(session.query(data.YEAR, data.STATE_DESCRIPTION, data.NAICS_CODE, data.NAME, data.ENTERPRISE_EMPLOYMENT_SIZE, data.NUMBER_OF_ESTABLISHMENTS, data.EMPLOYMENT, data.ANNUAL_PAYROLL).statement, con=engine)
    scatterPlot pd.read_sql(session.query(data.YEAR, data.STATE_DESCRIPTION, data.NAICS_CODE, data.NAME, data.ENTERPRISE_EMPLOYMENT_SIZE, data.EMPLOYMENT, data.ANNUAL_PAYROLL).statement, con=engine)
    colorMap pd.read_sql(session.query(data.YEAR, data.STATE_DESCRIPTION, data.NAICS_CODE, data.NAME, data.ENTERPRISE_EMPLOYMENT_SIZE, data.EMPLOYMENT, data.ANNUAL_PAYROLL).statement, con=engine)

    session.close()
    return jsonify(data_table.to_dict(orient='records'))
    return jsonify(barChart.to_dict(orient='records'))
    return jsonify(scatterPlot.to_dict(orient='records'))
    return jsonify(colorMap.to_dict(orient='records'))

    

if __name__ == "__main__":
    app.run(debug=True)  
