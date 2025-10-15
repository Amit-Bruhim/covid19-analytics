# q6.py
# Query 6: Return continents with total new cases greater than the average,
# ignoring locations starting with 'A' and empty continents

query = """
SELECT continent
FROM (
    -- Calculate total new cases per continent (filtered)
    SELECT continent, SUM(new_cases) AS total_new_cases
    FROM covid_deaths
    WHERE location NOT LIKE 'A%'   -- remove locations starting with 'A'
      AND continent <> ''           -- remove empty continents
    GROUP BY continent
) AS continent_totals
WHERE total_new_cases > (
    -- Calculate average total new cases across continents
    SELECT AVG(total_new_cases)
    FROM (
        SELECT continent, SUM(new_cases) AS total_new_cases
        FROM covid_deaths
        WHERE location NOT LIKE 'A%' AND continent <> ''
        GROUP BY continent
    ) AS avg_table
)
"""
