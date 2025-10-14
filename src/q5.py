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
-- Calculate total new cases for locations with the highest population per date,
-- only if the average new cases in that location is greater than 3
SELECT SUM(total_new_cases) AS sum_new_cases
FROM (
    -- Sum new cases per location
    SELECT SUM(d.new_cases) AS total_new_cases
    FROM covid_deaths d
    JOIN (
        -- Select locations that had the maximum population on any date
        SELECT DISTINCT d2.location
        FROM covid_deaths d2
        JOIN (
            -- Find the max population per date
            SELECT date, MAX(population) AS max_pop
            FROM covid_deaths
            GROUP BY date
        ) AS max_pop_table
        ON d2.date = max_pop_table.date AND d2.population = max_pop_table.max_pop
    ) AS max_pop_locations
    ON d.location = max_pop_locations.location
    GROUP BY d.location
    HAVING AVG(d.new_cases) > 3  -- Only include locations with average new cases > 3
) AS final;

""")
print(', '.join(str(row) for row in cursor.fetchall()))
