from mrjob.job import MRJob

class AccionesSeguras(MRJob):
    def mapper(self, _,line):
        company, price, date = line.strip().split(',')
        yield(company, (price, date))

    def reducer(self, company, values):
        prev_price = None
        goodMovement = True
        for price, date in values:
            if prev_price is not None and price < prev_price:
                goodMovement = False
                break
            prev_price = price
        yield company, goodMovement

if __name__ == '__main__':
    AccionesSeguras.run()
