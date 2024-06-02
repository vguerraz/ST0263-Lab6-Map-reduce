from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingPerGenre(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_collect_ratings),
            MRStep(reducer=self.reducer_find_extremes)
        ]

    def mapper_get_ratings(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield genre, (movie, float(rating))

    def reducer_collect_ratings(self, genre, movie_ratings):
        movie_ratings_list = list(movie_ratings)
        ratings_dict = {}
        for movie, rating in movie_ratings_list:
            if movie in ratings_dict:
                ratings_dict[movie].append(rating)
            else:
                ratings_dict[movie] = [rating]
        for movie, ratings in ratings_dict.items():
            yield genre, (movie, sum(ratings) / len(ratings))

    def reducer_find_extremes(self, genre, movie_ratings):
        movie_ratings_list = list(movie_ratings)
        max_rating = max(movie_ratings_list, key=lambda x: x[1])
        min_rating = min(movie_ratings_list, key=lambda x: x[1])
        yield genre, ("Best rated", max_rating)
        yield genre, ("Worst rated", min_rating)

if __name__ == '__main__':
    RatingPerGenre.run()