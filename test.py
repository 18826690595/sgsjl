from datetime import datetime

today = datetime.today()
# week = today.weekday()

week = 2
if week % 2 ==0:
    print(week)
else:
    print(f"{week}+not")