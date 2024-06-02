from mrjob.job import MRJob

class UsersPerMovie(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield movie, float(rating)

    def reducer(self, movie, ratings):
        ratings_list = list(ratings)
        yield movie, (len(ratings_list), sum(ratings_list) / len(ratings_list))

if __name__ == '__main__':
    UsersPerMovie.run()