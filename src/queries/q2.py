# q2.py
# Query 2: Find matching new_cases (>1000) for two different locations on the same date
# Only the first 1000 rows of the table are considered

query = """
-- Select matching new_cases (>1000) for two different locations on the same date
-- the date of the reported cases
-- number of new cases on that date
-- first location in the pair
-- second location in the pair
SELECT
    t1.date,
    t1.new_cases,
    t1.location AS location1,
    t2.location AS location2
FROM
    (
        -- Take first 1000 rows from covid_deaths as first table
        SELECT * 
        FROM covid_deaths
        LIMIT 1000
    ) AS t1
JOIN
    (
        -- Take first 1000 rows from covid_deaths as second table
        SELECT * 
        FROM covid_deaths
        LIMIT 1000
    ) AS t2
  ON 
      -- match rows with the same date
      t1.date = t2.date
      -- match rows with the same number of new cases
      AND t1.new_cases = t2.new_cases
      -- avoid duplicate pairs and self-pairing
      AND t1.location < t2.location
WHERE 
    -- filter only rows where new_cases > 1000
    t1.new_cases > 1000
ORDER BY 
    -- sort for readability
    t1.date, t1.location, t2.location;

"""
