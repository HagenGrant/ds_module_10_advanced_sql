# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd
import numpy as np

#################################################
# Database Setup
#################################################
class Hawaii():

    def __init__(self):
        # Create engine using the `hawaii.sqlite` database file
        self.engine = create_engine("sqlite:///hawaii.sqlite")
        self.Base = None
        self.init_base()
    
    # Declare a Base using `automap_base()`
    def init_base(self):
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)

    
# Use the Base class to reflect the database tables
    def query_hawaii_orm_measurement(self):
        # Save reference to the table
        Measurement = self.Base.classes.measurement
        

        # Create our session
        session = Session(self.engine)

        # Query Measurements
        measurement_results = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()

        # close session
        session.close()

        df_measurement = pd.DataFrame(measurement_results)
        data_measurement = df_measurement.to_dict(orient="records")


        return(data_measurement)
    
    def query_hawaii_orm_station(self):
        # Save reference to the table
        Station = self.Base.classes.station

        # Create our session
        session = Session(self.engine)

        # Query Stations
        station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

        # close session
        session.close()


        df_station = pd.DataFrame(station_results)
        data_station = df_station.to_dict(orient="records")

        return(data_station)
    

    def query_last_year_prcp(self):
        # Saving reference to the table.
        Measurement = self.Base.classes.measurement

        # Create our session from Python to the DB
        session = Session(self.engine)

        #Getting the last year's worth of precipitation.
        last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year)
        df_precip = pd.DataFrame(scores, columns = ['Date', 'Precipitation']).sort_values("Date")
        
        # close session
        session.close()

        data = df_precip.to_dict(orient="records")
        return(data)
    

    def query_station_count(self):
        # Saving reference to the table.
        Station = self.Base.classes.station

        # Create our session from Python to the DB
        session = Session(self.engine)

        #Getting all stations, station ids and the station names.
        df_all_stations = session.query(Station.id, Station.station, Station.name).all()
        df_all_stations = pd.DataFrame(df_all_stations, columns =['ID', 'Station', 'Name'])
        # close session
        session.close()
        

        data = df_all_stations.to_dict(orient="records")
        return(data)
    
    def query_station_tobs(self):
        # Saving reference to the table.
        Measurement = self.Base.classes.measurement

        # Create our session from Python to the DB
        session = Session(self.engine)

        # Querying the data to find the most active station within the past year.
        top_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
        top_stations = pd.DataFrame(top_stations, columns = ['station', 'count'])
        top_stations = top_stations.sort_values("count", ascending=False)

        # close session
        session.close()
        

        data = top_stations.to_dict(orient="records")
        return(data)
    
    def query_station_start(self):
        # Saving reference to the table.
        Measurement = self.Base.classes.measurement

        # Create our session from Python to the DB
        session = Session(self.engine)

        # Querying the data to find the most active station within the past year.
        prev_year = dt.date(2017, 8, 18) - dt.timedelta(days=365)
        results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date == prev_year).all()
        start_df = pd.DataFrame(results, columns =['Min', 'Max', 'Avg'])
        # close session
        session.close()
        

        data = start_df.to_dict(orient="records")
        return(data)
    
    def query_station_start_end(self):
        # Saving reference to the table.
        Measurement = self.Base.classes.measurement

        # Create our session from Python to the DB
        session = Session(self.engine)

        # Querying the data to find the most active station within the past year.
        most_recent = session.query(func.max(Measurement.date)).first()
        prev_year = dt.date(2017, 8, 18) - dt.timedelta(days=365)
        results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= prev_year).all()
        df_hist = pd.DataFrame(results, columns = ['Min', 'Max', 'Avg'])

        # close session
        session.close()
        

        data = df_hist.to_dict(orient="records")
        return(data)



