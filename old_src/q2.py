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
# we got to the answer step by step
cursor.execute("""
-- now we renamed the answers
SELECT d1 as date, n1 as new_cases, l1 as location1, l2 as location2
FROM (
-- now we crossed the 2 tables, and removed duplicates
SELECT *
FROM  (
       (
			-- we renamed the the columns
              SELECT location  AS l1 ,
                     date      AS d1,
                     new_cases AS n1
              FROM   (
							-- now we filtered any cases that are smaller or equal to 1000
                            SELECT location,
                                   date,
                                   new_cases
                            FROM   (
										-- takes the first 1000 rows from the table
                                          SELECT *
                                          FROM   covid_deaths LIMIT 1000) AS covid_1000
                            WHERE  new_cases>1000) AS covid_1000_2) AS ads ,
       (
			-- we renamed the the columns
              SELECT location  AS l2 ,
                     date      AS d2,
                     new_cases AS n2
              FROM   (
							-- now we filtered any cases that are smaller or equal to 1000
                            SELECT location,
                                   date,
                                   new_cases
                            FROM   (
										-- takes the first 1000 rows from the table
                                          SELECT *
                                          FROM   covid_deaths limit 1000) AS covid_10002
                            WHERE  new_cases>1000) AS covid_1000_22) AS ads2)
                            WHERE l1 < l2 and d1 = d2 and n1=n2 
                            )AS S
		
""")
print(', '.join(str(row) for row in cursor.fetchall()))
