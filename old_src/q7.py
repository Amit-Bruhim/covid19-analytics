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
-- we took the average, max and min of the new cases, per each location
SELECT location,
       Avg(amount) AS avg,
       Max(amount) AS max_monthly,
       Min(amount) AS min_monthly
FROM   
		-- we sumed the new cases for every month, per each location
		(SELECT location,
               Month(date)   AS month,
               Sum(new_cases)AS amount
        FROM   covid_deaths
        GROUP  BY location,
                  month)AS new_cases_per_month
GROUP  BY location 
""")
print(', '.join(str(row) for row in cursor.fetchall()))
