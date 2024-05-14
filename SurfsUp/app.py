import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
station=Base.classes.station
measurement =Base.classes.measurement

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
        f"Welcome to the Climate App - Flask API <br/>"
        f"..........................................<br/>"
        f"Available Routes:<br/>"
        f'1. Last 12 months of precipitation data:<br/> '
        f"/api/v1.0/precipitation<br/>"
        f'2. List of stations: <br/>'
        f"/api/v1.0/stations<br/>"
        f'3. Observations for most active station for previous year:<br/>'
        f"/api/v1.0/tobs<br/>"
        f'4.Minimum, Maximum and average temperature for a specified start and start-end range<br/>'
        f"/api/v1.0/start<br/>"
        f'/api/v1.0/start-end <br/>'
    )
@app.route("/api/v1.0/precipitation")
def preciptation():
    session = Session(engine)
    #Find most recent date from measurement table
    recent_date_measurement =session.query(measurement.date).order_by(measurement.date.desc()).first().date

    #calculate last year date
    last_year_date= dt.datetime.strptime(recent_date_measurement,'%Y-%m-%d') - dt.timedelta(days=365)

    # Query precipitation data for last year between the dates
    prcp_data= session.query(measurement.date,measurement.prcp).\
        filter(measurement.date>= last_year_date).order_by(measurement.date).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    lastyear_precipitation=[]
    
    for date , prcp in prcp_data:
        prcp_dict= {}
        prcp_dict[date]= prcp
        lastyear_precipitation.append(prcp_dict)
        
    return jsonify(lastyear_precipitation)

#Return a list of stations
@app.route("/api/v1.0/stations")
def sations():
    session = Session(engine)
    """Return a list of stations."""
    station_result = session.query(station.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_result))

    return jsonify(all_stations)

# 4.Query the dates and temperature observations of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")

def temperature():
    session = Session(engine)
     #Find most recent date from measurement table
    recent_date_measurement =session.query(measurement.date).order_by(measurement.date.desc()).first().date

    #calculate last year date
    last_year_date= dt.datetime.strptime(recent_date_measurement,'%Y-%m-%d') - dt.timedelta(days=365)

    active_station= session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    most_active = active_station[0][0]

     # Query to get the dates and temperature data for the  most active station

    most_active_temperature=session.query(measurement.date,measurement.tobs).\
                                    filter(measurement.date>= last_year_date).\
                                    filter(measurement.station== most_active).all()
    session.close()

    all_temp = []
    for date, temp in most_active_temperature:
        temp_dict={}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = temp
        all_temp.append(temp_dict)

    return jsonify(all_temp)

#5.Return a JSON list of the minimum temperature, the average temperature 
##and the maximum temperature for a specified start

@app.route('/api/v1.0/start')

def start(start = None):
    # input from user
    start = input("Enter the start date (yyyy-mm-dd):")

    #Retrieve temperature data from data base
    session = Session(engine)
    temp_data = session.query(func.min(measurement.tobs),
                              func.avg(measurement.tobs),
                              func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    start_temp =[]
    for min,avg, max in temp_data:
        start_dict={}
        start_dict["Min"]= min
        start_dict["Average"] = avg
        start_dict["Max"]= max
        start_temp.append(start_dict)

    return jsonify(start_temp)

#Return a JSON list of the minimum temperature, the average temperature 
##and the maximum temperature for a specified start and end date

@app.route("/api/v1.0/start-end") 

def start_end(start=None,end=None):

    # Input start and end date from user
    start= input("Enter the start date (yyyy-mm-dd): ")
    end = input("Enter the end date (yyyy-mm-dd): ")

    #Comparing that the end date should be the latest date or ahead of the start date
    if end > start :
        #Retrieve temperature data between dates TMIN, TMAX, TAVG
        session = Session(engine)
        #Query finding temp stats between the dates
        temp_stats_startend= session.query(func.min(measurement.tobs),
                              func.avg(measurement.tobs),
                              func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date<= end).all()
        session.close()

        # Create a dictionary from the row data and append to a list
        start_end_stats= []

        for min,avg, max in temp_stats_startend:
            startend_dict={}
            startend_dict["TMIN"] = min
            startend_dict["TAVG"] = avg
            startend_dict["TMAX"] = max
            start_end_stats.append(startend_dict)
        return jsonify(start_end_stats)
    else:
       return (f"End date should be ahead of the Start date")

  

if __name__ == '__main__':
    app.run(debug=True)
