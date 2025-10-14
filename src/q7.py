# q7.py
# Query 7: For each location, calculate monthly average, max, and min of new cases
# considering year+month separately

query = """
SELECT 
    location,
    AVG(monthly_total) AS avg,         -- monthly average of new cases per location
    MAX(monthly_total) AS max_monthly, -- maximum monthly total per location
    MIN(monthly_total) AS min_monthly  -- minimum monthly total per location
FROM (
    -- Sum new cases per location per year+month
    SELECT 
        location,
        YEAR(date) AS year,            -- separate months across different years
        MONTH(date) AS month,
        SUM(new_cases) AS monthly_total
    FROM covid_deaths
    GROUP BY location, YEAR(date), MONTH(date)
) AS monthly_cases
GROUP BY location
"""
