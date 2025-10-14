# q1.py
# Query 1: Calculate the difference between total cases at the end of February and March

query = """
-- Return the difference between the total cases at the end of February and March
SELECT 
    -- Sum total cases on the last day of February
    SUM(CASE WHEN MONTH(date) = 2 AND DAY(date) = DAY(LAST_DAY(date)) THEN total_cases ELSE 0 END)
    -- Minus sum total cases on the last day of March
    - SUM(CASE WHEN MONTH(date) = 3 AND DAY(date) = DAY(LAST_DAY(date)) THEN total_cases ELSE 0 END) 
    AS feb_minus_mar
FROM covid_deaths;
"""
