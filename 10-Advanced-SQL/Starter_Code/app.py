from flask import Flask, jsonify
import pandas as pd
import numpy as np
from apphelper import Hawaii




#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sql = Hawaii()

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/hawaii_orm_measurement<br/>"
        f"/api/hawaii_orm_station<br/>"
        f"/api/last_year_prcp<br/>"
        f"/api/station_count<br/>"
        f"/api/station_tobs<br/>"
        f"/api/station_start<br/>"
        f"/api/station_start_end<br/>"
    )

# SQL Queries
@app.route("/api/hawaii_orm_measurement")
def hawaii_orm_measurement():
    data = sql.query_hawaii_orm_measurement()
    return(jsonify(data))

@app.route("/api/hawaii_orm_station")
def hawaii_orm_station():
    data = sql.query_hawaii_orm_station()
    return(jsonify(data))

@app.route("/api/last_year_prcp")
def last_year_prcp():
    data = sql.query_last_year_prcp()
    return(jsonify(data))

@app.route("/api/station_count")
def station_count():
    data = sql.query_station_count()
    return(jsonify(data))

@app.route("/api/station_tobs")
def station_tobs():
    data = sql.query_station_tobs()
    return(jsonify(data))

@app.route("/api/station_start")
def station_start():
    data = sql.query_station_start()
    return(jsonify(data))

@app.route("/api/station_start_end")
def station_start_end():
    data = sql.query_station_start_end()
    return(jsonify(data))

# Run the App
if __name__ == '__main__':
    app.run(debug=True)