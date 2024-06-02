from mrjob.job import MRJob

class MinMaxPricePerCompany(MRJob):
    def mapper(self,_,line):
        company, price, date = line.strip().split(',')
        yield company, (float(price), date)
    def reducer(self, company, values):
        min_price = float('inf')
        max_price = float('-inf')
        date_min = None
        date_max = None

        for price, date in values:
            if price < min_price:
                min_price = price
                date_min = date
            if price > max_price:
                max_price = price
                date_max = date

        yield company, ("Min Day",min_price, date_min)
        yield company, ("Max Day",max_price, date_max)

if __name__ == '__main__':
    MinMaxPricePerCompany.run()
