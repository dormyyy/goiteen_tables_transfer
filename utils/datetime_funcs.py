from datetime import datetime


def strip_months(columns_months):
    dates = []
    for i, j in columns_months.items():
        for date in j:
            dates.append(i + ' ' + date.split('-')[0])
            dates.append(i + ' ' + date.split('-')[1])
    data = []
    for i in range(len(dates)):
        date = dates[i].split()
        day = date[2]
        year = date[1]
        if i != 0:
            if dates[i - 1].split()[2] < dates[i].split()[2]:
                month = datetime.strptime(date[0], '%B').month
            else:
                month = datetime.strptime(date[0], '%B').month + 1
        else:
            month = datetime.strptime(date[0], '%B').month
        data.append(f"{day}-{month}-{year}")
    return data


def find_today(dates):
    dates = [datetime.strptime(i, '%d-%m-%y') for i in dates]
    today = datetime.today().date().strftime('%d-%m-%y')
    today = datetime.strptime(today, '%d-%m-%y')
    inside = True
    if today not in dates:
        inside = False
        dates.append(today)
    dates.sort()
    index = dates.index(today)
    count = index + 1
    if inside:
        count += 1
    return count // 2
