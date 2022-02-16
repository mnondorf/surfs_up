#Import dependencies

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from zmq import MECHANISM

# Set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# With the database reflected, we can save our references to each table. 
# Create a variable for each of the classes so that we can reference them later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database
session = Session(engine)


# Define the Flask app. (This will create a Flask application called "app.")
app = Flask(__name__)

# How to check that we are using the right file to run this code:
#     import app

# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")

#Define the welcome route:
@app.route("/")

#create function
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')

#Create route for precipitation analysis
@app.route("/api/v1.0/precipitation")

#Create precipication function
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Create route for station analysis
@app.route("/api/v1.0/stations")

#Create station function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Create route for tobs analysis
@app.route("/api/v1.0/tobs")

#Create tobs function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results)) 
    return jsonify(temps=temps)

#Create routs for summary statistics
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Create summary stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)