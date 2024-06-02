from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingPerDay(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_compute_average),
            MRStep(reducer=self.reducer_find_extremes)
        ]

    def mapper_get_ratings(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, float(rating)

    def reducer_compute_average(self, date, ratings):
        ratings_list = list(ratings)
        yield None, (sum(ratings_list) / len(ratings_list), date)

    def reducer_find_extremes(self, _, date_ratings):
        date_ratings_list = list(date_ratings)
        max_rating = max(date_ratings_list)
        min_rating = min(date_ratings_list)
        yield "Best rating day", max_rating
        yield "Worst rating day", min_rating

if __name__ == '__main__':
    RatingPerDay.run()