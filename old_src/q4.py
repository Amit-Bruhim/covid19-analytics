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
-- we filtered the new_vaccinations that are smaller than 20000000,
-- and printed only those dates and the amount of new vaccinations at this date.
SELECT date ,
       answer AS daily_vaccinations
FROM  (
       (
				-- we sumed the new_vaccinations only for asia, and grouped by date
                SELECT   date,
                         Sum(new_vaccinations) AS answer
                FROM     covid_vaccination
                WHERE    continent="ASIA"
                GROUP BY date)AS s)
WHERE  answer > 20000000
""")
print(', '.join(str(row) for row in cursor.fetchall()))
