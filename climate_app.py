# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date<br/>"
    )

@app.route("/api/v1.0/precipitations")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Measurement data including the date and precipitation of each measurement"""
    # Query all Measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict[date] = prcp
   
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations including the station id and name of each station"""
    # Query all Measurements
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_stations = []
    for station_id, name in results:
        station_dict = {}
        station_dict[station_id] = name
   
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Temperature Observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    recent_date = session.query(Measurement.date).\
                    order_by(Measurement.date.desc()).\
                    first()[0].\
                    split("-")
    # Calculate the date one year from the last date in data set.
    recent_date = dt.date(int(recent_date[0]), int(recent_date[1]), int(recent_date[2]))
    one_year_ago = recent_date - dt.timedelta(days=365)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    active_stations_desc = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    # List the stations and the counts in descending order.
    active_station = active_stations_desc[0][0]
    active_stations_desc


    """Return a list of Stations including the station id and name of each station"""
    # Query all Measurements
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == active_station)

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
   
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Start Date Query
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations including the station id and name of each station"""
    date = start.split("-")
    start_date = dt.date(int(date[0]), int(date[1]), int(date[2]))
    # Query all Measurements
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date)

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_tobs = []
    for date, min_tobs, max_tobs, avg_tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Min"] = min_tobs
        tobs_dict["Max"] = max_tobs
        tobs_dict["Avg"] = avg_tobs
   
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Start Date Query
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations including the station id and name of each station"""
    st_date = start.split("-")
    ed_date = end.split("-")
    start_date = dt.date(int(st_date[0]), int(st_date[1]), int(st_date[2]))
    end_date = dt.date(int(ed_date[0]), int(ed_date[1]), int(ed_date[2]))
    # Query all Measurements
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date)

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_tobs = []
    for date, min_tobs, max_tobs, avg_tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Min"] = min_tobs
        tobs_dict["Max"] = max_tobs
        tobs_dict["Avg"] = avg_tobs
   
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)    

if __name__ == '__main__':
    app.run(debug=True)