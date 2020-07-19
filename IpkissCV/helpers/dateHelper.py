from datetime import datetime


def str_date(date, time):
    dt = []
    ymd = date.split('-')
    hmsm = time.replace('.', ':')
    hmsm = hmsm.split(':')

    for x in ymd:
        dt.append(int(x))
    for y in hmsm:
        dt.append(int(y))

    return datetime(year=dt[0], month=dt[1], day=dt[2], hour=dt[3], minute=dt[4], second=dt[5], microsecond=dt[6])
