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
# we removed the locations that starts with 'a', only from the first calculations.
cursor.execute("""
-- we took only the continents which their sum of new cases is greater than the avarage
SELECT continent
FROM   
-- we removed the locations that Sum(new_cases) is lower than the average of new cases
(SELECT continent,
               Sum(new_cases) AS continent_cases
        FROM   covid_deaths
        GROUP  BY continent) AS sum_by_continent1
		WHERE  continent_cases > ALL 
							-- we took the average of new cases in the required locations
                            (SELECT Avg(continent_cases)
                              FROM   
                              -- we removed the locations that starts with 'a'
                              (SELECT continent,
                                             avg(new_cases) AS continent_cases
                                      FROM   covid_deaths
                                      WHERE  NOT location LIKE 'A%'
                                      GROUP  BY continent) AS sum_by_continent) 
""")
print(', '.join(str(row) for row in cursor.fetchall()))
