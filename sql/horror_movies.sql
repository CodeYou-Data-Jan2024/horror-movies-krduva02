SELECT id, name, imdb_rating 
FROM movies
WHERE year < 1986
    AND genre = 'horror'
ORDER BY imdb_rating DESC
LIMIT 3;