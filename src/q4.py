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
# we found the dates and the amount of new vaccinations at those dates,
# by the required conditions.
cursor.execute("""
-- Select days in Asia with more than 20M new vaccinations
SELECT 
    date,
    SUM(new_vaccinations) AS daily_vaccinations
FROM covid_vaccination
WHERE continent = 'Asia'
GROUP BY date
HAVING daily_vaccinations > 20000000
ORDER BY date;
""")
print(', '.join(str(row) for row in cursor.fetchall()))
