from mrjob.job import MRJob

class NumSectorsByEmployee(MRJob):

    def mapper(self, _, record):
        idemp, sececon, salary, year = record.split(',')
        yield idemp, sececon

    def reducer(self, idemp, sectors):
        num_sectors = len(set(sectors))
        yield idemp, num_sectors

if __name__ == '__main__':
    NumSectorsByEmployee.run()
