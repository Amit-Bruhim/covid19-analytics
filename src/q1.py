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
# we returned the actual difference (not the absolute value)
cursor.execute("""
-- return the differnce between the total cases in febuary and march
SELECT 
	-- sum total cases on February
    SUM(CASE WHEN MONTH(date) = 2 AND DAY(date) = DAY(LAST_DAY(date)) THEN total_cases ELSE 0 END)
	-- sum total cases on March
  - SUM(CASE WHEN MONTH(date) = 3 AND DAY(date) = DAY(LAST_DAY(date)) THEN total_cases ELSE 0 END) 
    AS feb_minus_mar
FROM covid_deaths;

""")
print(', '.join(str(row) for row in cursor.fetchall()))
