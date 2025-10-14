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
# we acted according to the forum, we didn't differentiate years.
cursor.execute("""
-- Calculate monthly statistics (avg, max, min) of new cases for each location, considering both year and month
SELECT 
    location,                       
    AVG(monthly_total) AS avg,      
    MAX(monthly_total) AS max_monthly,
    MIN(monthly_total) AS min_monthly
FROM (
    -- Step 1: sum new cases per year+month for each location
    SELECT 
        location,
        YEAR(date) AS year,          -- include year to separate months across years
        MONTH(date) AS month,
        SUM(new_cases) AS monthly_total
    FROM covid_deaths
    GROUP BY location, YEAR(date), MONTH(date)
) AS monthly_cases
GROUP BY location
""")
print(', '.join(str(row) for row in cursor.fetchall()))
