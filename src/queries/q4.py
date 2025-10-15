# q4.py
# Query 4: Select days in Asia where total new vaccinations exceeded 20 million

query = """
SELECT 
    date,
    SUM(new_vaccinations) AS daily_vaccinations
FROM covid_vaccination
WHERE continent = 'Asia'
GROUP BY date
-- Filter only days where daily vaccinations exceed 20 million
HAVING daily_vaccinations > 20000000
ORDER BY date;
"""
