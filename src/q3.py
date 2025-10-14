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
-- Compute the average number of new tests on days where the positive rate is above average
SELECT AVG(new_tests) AS avg_new_tests_above_avg_positive_rate
FROM (
    -- Filter rows where new_tests and positive_rate are not empty and positive_rate > overall average
    SELECT 
        new_tests,
        positive_rate
    FROM covid_vaccination
    WHERE new_tests <> '' 
      AND positive_rate <> ''
      AND positive_rate > (
          -- Compute the overall average positive_rate considering only valid rows
          SELECT AVG(positive_rate)
          FROM covid_vaccination
          WHERE new_tests <> ''
            AND positive_rate <> ''
      )
) AS filtered_days;

""")
print(', '.join(str(row) for row in cursor.fetchall()))
