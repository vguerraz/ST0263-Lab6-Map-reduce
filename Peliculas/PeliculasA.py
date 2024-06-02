from mrjob.job import MRJob

class MoviesPerUser(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield user, float(rating)

    def reducer(self, user, ratings):
        ratings_list = list(ratings)
        yield user, (len(ratings_list), sum(ratings_list) / len(ratings_list))

if __name__ == '__main__':
    MoviesPerUser.run()
