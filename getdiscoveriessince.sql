SELECT neu.artist, neu.title, datetime(neu.time, 'unixepoch', 'localtime') datum 
FROM (SELECT * FROM recenttracks 
WHERE time > old AND time <= newnow) neu 
LEFT JOIN (SELECT * FROM recenttracks 
WHERE time <= old OR time > newnow) alt ON neu.title=alt.title AND neu.artist=alt.artist 
GROUP BY neu.artist, neu.title HAVING alt.title IS NULL 
ORDER BY neu.time ASC