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
SELECT continent
FROM (
    -- Step 1: Calculate the average of new_cases for each continent
    SELECT continent, AVG(new_cases) AS continent_avg_cases
    FROM covid_deaths
    WHERE continent IS NOT NULL AND continent <> ''
    GROUP BY continent
) AS continent_avgs
WHERE continent_avg_cases >
(
    -- Step 2: Calculate the average of new_cases for locations
    -- whose average population is lower than the global average population
    SELECT AVG(new_cases)
    FROM covid_deaths d
    WHERE d.location IN (
        -- Step 3: Get only locations with an average population lower than the global average
        SELECT location
        FROM (
            -- Step 4: Calculate the average population for each location
            SELECT location, AVG(population) AS avg_pop
            FROM covid_deaths
            GROUP BY location
        ) AS location_avg
        WHERE avg_pop < (
            -- Step 5: Calculate the global average population
            SELECT AVG(population)
            FROM covid_deaths
        )
    )
);
""")
print(', '.join(str(row) for row in cursor.fetchall()))
