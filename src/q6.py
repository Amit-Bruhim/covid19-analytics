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
-- Step 2: continents with total new_cases greater than the average
SELECT continent
FROM (
    -- calculate total new_cases per continent (filtered)
    SELECT continent, SUM(new_cases) AS total_new_cases
    FROM covid_deaths
    WHERE location NOT LIKE 'A%'  -- remove locations starting with 'A'
      AND continent <> ''          -- remove empty continents
    GROUP BY continent
) AS continent_totals
WHERE total_new_cases > (
    -- calculate average total_new_cases across continents
    SELECT AVG(total_new_cases)
    FROM (
        SELECT continent, SUM(new_cases) AS total_new_cases
        FROM covid_deaths
        WHERE location NOT LIKE 'A%' AND continent <> ''
        GROUP BY continent
    ) AS avg_table
)
""")
print(', '.join(str(row) for row in cursor.fetchall()))
