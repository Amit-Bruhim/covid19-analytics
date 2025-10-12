import mysql.connector

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="covid_db",
        port='3306',
    )
cursor = mydb.cursor()
# we returned the actual difference (not the absolute value)
cursor.execute("""
-- return the differnce between the total cases in febuary and march
SELECT total_cases_feb - total_cases_mar AS feb_minus_march
FROM   (
                     (
							-- sum the amount of total cases in febuary
                            SELECT Sum(total_cases) AS total_cases_feb
                            FROM   covid_deaths
                            WHERE  Month(date)=2) AS x,
                     (
							-- sum the amount of total cases in march
                            SELECT sum(total_cases) AS total_cases_mar
                            FROM   covid_deaths
                            WHERE  month(date)=3) AS y )
""")
print(', '.join(str(row) for row in cursor.fetchall()))
