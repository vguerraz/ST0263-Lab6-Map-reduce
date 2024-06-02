from mrjob.job import MRJob
from mrjob.step import MRStep

class BlackDay(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield company, (float(price), date)

    def reducer_find_min_price(self, company, values):
        min_price_date = min(values)
        yield min_price_date[1], 1

    def reducer_find_black_day(self, date, counts):
        yield "Black Day", (sum(counts), date)

    def reducer_find_max_black_day(self, _, date_counts):
        max_black_day = max(date_counts)
        yield "No. companies, day:", max_black_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer_find_min_price),
            MRStep(reducer=self.reducer_find_black_day),
            MRStep(reducer=self.reducer_find_max_black_day)
        ]

if __name__ == '__main__':
    BlackDay.run()
