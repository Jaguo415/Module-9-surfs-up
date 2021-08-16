import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
##############################
# Database Setup
##############################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model

Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#Create Our session from python to the Database

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the Precipitation data for the last year"""

    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    precip = {date:prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""

    results = session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations = stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Returns the temp observation for previous year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start = None, end = None):

    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temp = list(np.ravel(results))
        return jsonify(temps=temps)
    #Calculate Tmin TAVG TMax with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter (Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run(debug=False)