SQL-Alchemy and Flask API

Summary:
In this project Python and SQLAlchemy ORM queries are used to do a basic climate analysis and data exploration of climate database to help with trip planning. After the analysis a Flask API is created for different queries and better trip planning

Data Source:
(Resources/hawaii.sqlite) 

Tools used:
Python: SQLAlchemy, Pandas , Matplotlib, Flask , datetime

Flask Routes :
* "/"

  * Home page.

  * List all routes that are available.

* "/api/v1.0/precipitation"

  * Convert the query results to a Dictionary using "date" as the key and "prcp" as the value.

  * Return the JSON representation of the dictionary.

* "/api/v1.0/stations"

  * Return a JSON list of stations from the dataset.

* "/api/v1.0/tobs"
  * query for the dates and temperature observations of the most active station for the previous year of data.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* "/api/v1.0/start" and "/api/v1.0/start-end"

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate "Min", "AVG", and "MAX" for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the "TMIN", "TAVG", and "TMAX" for dates between the start and end date inclusive.


