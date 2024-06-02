from mrjob.job import MRJob
from mrjob.step import MRStep

class MoviesPerDay(MRJob):

    def mapper_get_dates(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, 1

    def reducer_count_dates(self, date, counts):
        yield None, (sum(counts), date)

    def reducer_find_extremes(self, _, date_counts):
        dates = list(date_counts)
        max_day = max(dates)
        min_day = min(dates)
        yield "Max day", max_day
        yield "Min day", min_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_dates,
                   reducer=self.reducer_count_dates),
            MRStep(reducer=self.reducer_find_extremes)
        ]
    
if __name__ == '__main__':
    MoviesPerDay.run()
