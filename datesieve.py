#!/usr/bin/env python3

from datetime import datetime as dt

# demo times
times = [
    "2018-03-08T07:16:28UTC",
    "2018-04-26T05:26:54UTC",
    "2018-07-26T06:11:58UTC",
    "2018-09-16T22:00:03UTC",
    "2018-09-23T22:00:02UTC",
    "2018-09-30T22:00:03UTC",
    "2018-10-03T22:00:01UTC",
    "2018-10-04T22:00:01UTC",
    "2018-10-05T22:00:01UTC",
    "2018-10-06T22:00:01UTC",
    "2018-10-07T22:00:02UTC",
    "2018-10-07T22:00:02UTC",
    "2018-10-08T22:00:01UTC",
    "2018-10-09T07:00:02UTC",
    "2018-10-09T08:00:01UTC",
    "2018-10-09T09:00:02UTC",
    "2018-10-09T10:00:01UTC",
    "2018-10-09T11:00:02UTC",
    "2018-10-09T12:00:01UTC",
    "2018-10-09T13:00:01UTC",
    "2018-10-09T14:00:01UTC",
    "2018-10-09T15:00:01UTC",
    "2018-10-09T16:00:01UTC",
    "2018-10-09T17:00:01UTC",
    "2018-10-09T18:00:01UTC",
    "2018-10-09T19:00:01UTC",
    "2018-10-09T20:00:01UTC",
    "2018-10-09T21:00:01UTC",
    "2018-10-09T22:00:02UTC",
    "2018-10-09T22:00:02UTC",
    "2018-10-09T23:00:00UTC",
    "2018-10-10T00:00:02UTC",
    "2018-10-10T01:00:02UTC",
    "2018-10-10T02:00:02UTC",
    "2018-10-10T03:00:01UTC",
    "2018-10-10T04:00:01UTC",
    "2018-10-10T05:00:02UTC",
    "2018-10-10T06:00:02UTC",
    "2018-08-08T08:08:08UTC",
]
times = [dt.strptime(t, "%Y-%m-%dT%H:%M:%SUTC") for t in times]


class bucket:
    def __init__(self, formatter, capacity):
        self.set = set()
        self.cap = capacity
        self.fmt = formatter

    def add(self, date):
        if self.cap > 0:
            f = self.fmt(date)
            if f not in self.set:
                self.set.add(f)
                self.cap -= 1
                return True
        return False


def datesieve(elements, key, days=7, weeks=2, months=2, years=1):
    elements.sort(key=key, reverse=True)
    buckets = [
        bucket(lambda d: d.strftime("%Y"), years),
        bucket(lambda d: d.strftime("%Y%m"), months),
        bucket(lambda d: d.strftime("%Y%W"), weeks),
        bucket(lambda d: d.strftime("%Y%m%d"), days),
    ]
    sieved = []
    for el in elements:
        if True in [b.add(key(el)) for b in buckets]:
            sieved.append(el)
    return sieved


def printdates(list):
    for e in list:
        print(e.isoformat())


print("ALL DATES")
printdates(times)

print("SIEVED DATES")
printdates(datesieve(times, lambda e: e, months=1, days=1, weeks=8, years=1))
