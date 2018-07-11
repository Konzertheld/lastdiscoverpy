SELECT neu.artist, neu.title, datetime(neu.time, 'unixepoch', 'localtime') datum FROM (SELECT * FROM recenttracks WHERE time > 1522540800) neu LEFT JOIN (SELECT * FROM recenttracks WHERE time <= 1522540800) alt ON neu.title=alt.title AND neu.artist=alt.artist GROUP BY neu.artist, neu.title HAVING alt.title IS NULL ORDER BY neu.time ASC