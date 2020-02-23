import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Home():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/year-month-day start/year-month-day end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipList = []
    for date, prcp in results:
        precipDict = {}
        precipDict["date"] = date
        precipDict["precipitation"] = prcp
        precipList.append(precipDict)
    return jsonify(precipList)


@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)

    stationsN = session.query(Station.station, Station.name).all()

    session.close()

    Stations = []
    for stationNum, name in stationsN:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = stationNum
        Stations.append(station_dict)

    return jsonify(Stations)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)

    yearData = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between("2016-08-23", "2017-08-23"))

    session.close()

    tempList = []
    for station, date, tobs in stationsN:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        tempList.append(temp_dict)

    return jsonify(tempList)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):

    session =  Session(engine)

    Temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
    calctemplist = []
    for min, avg, max in Temperatures:
        calctempdict = {}
        calctempdict["min"] = min
        calctempdict["avg"] = avg
        calctempdict["max"] = max
        calctemplist.append(calctempdict)

    return jsonify(calctemplist)

if __name__ == '__main__':
    app.run(debug=True)