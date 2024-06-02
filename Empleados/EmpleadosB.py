from mrjob.job import MRJob

class AverageSalaryByEmpl(MRJob):

    def mapper(self, _, record):
        idemp, sececon, salary, year = record.split(',')
        yield idemp, salary

    def reducer(self, idemp, salaries):
        total_salary = 0
        count = 0
        for salary in salaries:
            total_salary += int(salary)
            count += 1
        average_salary_empl = total_salary / count
        yield idemp, average_salary

if __name__ == '__main__':
    AverageSalaryByEmpl.run()
