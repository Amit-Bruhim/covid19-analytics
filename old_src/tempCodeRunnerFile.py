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