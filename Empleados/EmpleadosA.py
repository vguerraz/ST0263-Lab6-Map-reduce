from mrjob.job import MRJob

class MRSalarioPorSector(MRJob):

    def mapper(self, _, record):
        idemp, sececon, salary, year = record.split(',')
        yield sececon, salary

    def reducer(self, sececon, salaries):
        total_salary = 0
        count = 0
        for salary in salaries:
            total_salary += int(salary)
            count += 1
        average_salary_sector = total_salary / count
        yield sececon, average_salary

if __name__ == '__main__':
    MRSalarioPorSector.run()
