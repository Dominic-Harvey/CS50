SELECT AVG(rating) FROM
movies JOIN ratings ON movies.id = ratings.movie_id
Where year = 2012;