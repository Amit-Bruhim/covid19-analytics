import mysql.connector

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="covid_db",
        port='3307',
    )
cursor = mydb.cursor()
# we selected the required continents.
# we joined the covid_deaths table with the table we created.
cursor.execute("""
-- we took only the continents where the average of new cases is greater than
-- the average on new cases in the required locations
SELECT continent
FROM   
		-- get the average of new cases for every continent
		(SELECT continent,
               Avg (new_cases) AS avg4
        FROM   covid_deaths
        GROUP  BY continent) AS con_avg
WHERE  avg4 > ALL 
       -- we got the average of new case, only for the required locations
       (SELECT Avg(new_cases) AS avg2
                       FROM   covid_deaths,
								-- get only the locations where the average population is smaller
                                -- than the total poplation average 
                              (SELECT location
                               FROM   
                               -- get the average population by location 
                               (SELECT Avg(population) AS avg1,
                                              location
                                       FROM   covid_deaths
                                       GROUP  BY location) AS loc_avg
                               WHERE  avg1 < ALL 
                               -- get the average population
                               (SELECT Avg(population)
                                                  FROM   covid_deaths)) AS
                              valid_locations
                       WHERE  valid_locations.location = covid_deaths.location) 
""")
print(', '.join(str(row) for row in cursor.fetchall()))
