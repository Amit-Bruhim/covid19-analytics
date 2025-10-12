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
# we found the locations by the required conditions
cursor.execute("""
-- we sumed all of the new cases together
SELECT Sum(sum_new_cases) AS sum_new_cases
FROM
-- we removed the location column
(SELECT answer AS sum_new_cases
 FROM
-- we took the sum of new cases 
(SELECT Sum(covid_deaths.new_cases) AS answer,
        covid_deaths.location
 FROM   covid_deaths,
        -- we returned the locations and the sum of new cases in each location
        (SELECT location,
                Sum(new_cases)
         FROM
        -- we crossed the tables by the locations and the dates and the population
        (SELECT covid_deaths.date,
                covid_deaths.population AS population,
                location,
                new_cases
         FROM   (
                -- return the max population of every date
                SELECT date,
                       Max(population) AS M
                 FROM   covid_deaths
                 GROUP  BY date) AS x,
                covid_deaths
         WHERE  covid_deaths.date = x.date
                AND m = covid_deaths.population
                AND location IN
                    -- we filtered the locations where the averagr are smaller than 3 or equal 3
                    (SELECT location
                     FROM
                    -- average new cases by location
                    (SELECT Avg(new_cases) AS y,
                            location
                     FROM   covid_deaths
                     GROUP  BY location)AS z
                     WHERE  y > 3))AS ww
         GROUP  BY location) AS w1
 WHERE  w1.location = covid_deaths.location
 GROUP  BY covid_deaths.location) AS sss)AS x 
""")
print(', '.join(str(row) for row in cursor.fetchall()))
