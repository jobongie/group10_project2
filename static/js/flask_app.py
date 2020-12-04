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

states = Base.classes.states_electoral_df

#################################################
# Flask Routes
#################################################
@app.route("/")
def states_electoral_df():
    session = Session(engine)
    
    results_df = pd.read_sql(session.query(states.State, states.Pollster, states.Clinton, states.Trump, states.clinton_adjusted, states.trump_adjusted, states.Winner, states.electoral_votes).statement, con=engine)
    
    session.close()
    return jsonify(results_df.to_dict(orient='records'))
