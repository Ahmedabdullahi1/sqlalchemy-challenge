# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def Hi():
    return (
        f" This is the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/yyyy-mm-dd<br/>"
        
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)




@app.route("/api/v1.0/precipitation")
def precipitation():
    
    twelve_month_prcp = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= '2016-08-23').\
                        order_by(Measurement.date).all()
    
    session.close()

    precipitation = list(np.ravel(twelve_month_prcp ))
    return jsonify(precipitation=precipitation)



@app.route("/api/v1.0/tobs")
def tobs(): 
    temp_observation = session.query(Measurement.tobs).\
    filter(Measurement.date>='2016-08-23').\
    filter(Station.station == Measurement.station).\
    filter(Station.station== 'USC00519281').all()

    session.close()

    tobs= list(np.ravel( temp_observation  ))
    return jsonify(tobs=tobs)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start(start=None,end=None):
    if not end:
        datetime_object = datetime.strptime(start,"%m%d%Y")
        date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

        session.close()

        start = list(np.ravel( date ))
        return jsonify(start =start )
    
    
    date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    session.close()

    start = list(np.ravel( date ))
    return jsonify(start =start )


if __name__ == '__main__':
    app.run(debug=True)

