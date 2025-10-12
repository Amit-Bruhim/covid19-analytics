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
# we used the function "avg" to calculate the average amount of new tests, by the required conditions
cursor.execute("""
-- return the avg of the new tests in our group
SELECT Avg(new_tests)
FROM
-- we filtered the positive rates that are smaller than the average,
-- and new tests are not null
(SELECT new_tests,
        positive_rate
 FROM   covid_vaccination
 WHERE  new_tests <> ''
        AND positive_rate <> ''
        AND positive_rate > ALL
            -- this is the average of positive_rate
            (SELECT Avg (positive_rate) AS avg_positive_rate
             FROM   covid_vaccination
             WHERE  new_tests <> ''
                    AND positive_rate <> '')) AS X 
""")
print(', '.join(str(row) for row in cursor.fetchall()))
