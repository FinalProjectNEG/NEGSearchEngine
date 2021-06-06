from datetime import date

dict_month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}


def ScoreTime(time):

    if time != None:
        today = date.today()
        date_information = time.split()
        day = int(date_information[1])
        month = date_information[2]
        year = int(date_information[3])

        date_page = date(year, dict_month[month], day)
        year_ago_1 = date(today.year - 1, today.month, today.day)
        year_ago_10 = date(today.year - 10, today.month, today.day)
        date_today = date(today.year, today.month, today.day)

        if (year_ago_1 < date_page < date_today):
            return 5
        elif (year_ago_10 < date_page < year_ago_1):
            return 3
        elif (date_page < year_ago_10):
            return 2
    return 0

