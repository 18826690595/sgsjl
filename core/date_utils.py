from datetime import datetime


class DateUtils:
    @classmethod
    def week_mun(cls):
        return datetime.today().weekday()

    @classmethod
    def day_mun(cls):
        return datetime.today().day


print(DateUtils.week_mun())
print(DateUtils.day_mun())


n = 2
print(n%2)