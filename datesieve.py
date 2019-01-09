#!/usr/bin/env python3

from datetime import datetime

DEMODATES = [datetime.strptime(t, "%Y-%m-%dT%H:%M:%SUTC") for t in ["2018-03-08T07:16:28UTC","2017-01-01T03:12:34UTC","2018-04-26T05:26:54UTC","2018-07-26T06:11:58UTC","2018-09-16T22:00:03UTC","2018-09-23T22:00:02UTC","2018-09-30T22:00:03UTC","2018-10-03T22:00:01UTC","2018-10-04T22:00:01UTC","2018-10-05T22:00:01UTC","2018-10-06T22:00:01UTC","2018-10-07T22:00:02UTC","2018-10-07T22:00:02UTC","2018-10-08T22:00:01UTC","2018-10-09T07:00:02UTC","2018-10-09T08:00:01UTC","2018-10-09T09:00:02UTC","2018-10-09T10:00:01UTC","2018-10-09T11:00:02UTC","2018-10-09T12:00:01UTC","2018-10-09T13:00:01UTC","2018-10-09T14:00:01UTC","2018-10-09T15:00:01UTC","2018-10-09T16:00:01UTC","2018-10-09T17:00:01UTC","2018-10-09T18:00:01UTC","2018-10-09T19:00:01UTC","2018-10-09T20:00:01UTC","2018-10-09T21:00:01UTC","2018-10-09T22:00:02UTC","2018-10-09T22:00:02UTC","2018-10-09T23:00:00UTC","2018-10-10T00:00:02UTC","2018-10-10T01:00:02UTC","2018-10-10T02:00:02UTC","2018-10-10T03:00:01UTC","2018-10-10T04:00:01UTC","2018-10-10T05:00:02UTC","2018-10-10T06:00:02UTC","2018-08-08T08:08:08UTC"]]

# set with formatted dates and capacity to check if desired number of
# entries per timespan is already reached
class bucket:
    def __init__(self, format, capacity):
        self.bucket = set()
        self.capacity = capacity
        self.format = format

    # try to add date to buckets, returns True if there was capacity in any of them
    def add(self, date):
        if self.capacity > 0:
            element = date.strftime(self.format)
            if element not in self.bucket:
                self.bucket.add(element)
                self.capacity -= 1
                return True
        return False

# sieve a number of dates with timespan buckets
class sieve:

    # initialize a sieve with timespan buckets with given capacities
    def __init__(self, minutes=0, hours=0, days=0, weeks=0, months=0, years=0):
        self.buckets = [
            bucket("%Y%m%d%H%M", minutes),
            bucket("%Y%m%d%H", hours),
            bucket("%Y%m%d", days),
            bucket("%Y%W", weeks),
            bucket("%Y%m", months),
            bucket("%Y", years),
        ]

    # try to add a date, returns True if there was capacity, False if sieved out
    def add(self, date):
        return True in [b.add(date) for b in self.buckets]

    # all-in-one to directly sieve a list of elements and return result
    @staticmethod
    def sieve(elements, key=lambda e: e, minutes=0, hours=0, days=0, weeks=0, months=0, years=0):

        # init sieve
        s = sieve(minutes, hours, days, weeks, months, years)

        # copy and sort elements
        elements = list(elements)
        elements.sort(key=key, reverse=True)

        # return a list of sieved elements, which fit in the timespans
        return [el for el in elements if s.add(key(el))]

# line-based pipe operation when called interactively
if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser()

    buckets = parser.add_argument_group('timespan buckets')
    buckets.add_argument('--minutes', help='number of minutes to keep', type=int, metavar='int', default=0)
    buckets.add_argument('--hours', help='number of hours to keep', type=int, metavar='int', default=0)
    buckets.add_argument('--days', help='number of days to keep', type=int, metavar='int', default=0)
    buckets.add_argument('--weeks', help='number of weeks to keep', type=int, metavar='int', default=0)
    buckets.add_argument('--months', help='number of months to keep', type=int, metavar='int', default=0)
    buckets.add_argument('--years', help='number of years to keep', type=int, metavar='int', default=0)

    parser.add_argument('--strptime', help='format string to parse date, otherwise fuzzy with dateutil', metavar='format')
    parser.add_argument('--sort', help='read all lines and sort by date first', action='store_true')
    #parser.add_argument('--deleted', help='show sieved-out elements instead of remaining', action='store_true')

    args = parser.parse_args()

    # set dateparser depending on whether a specific strptime format string was given or not
    if args.strptime is None:
        import dateutil.parser
        parse = lambda s: dateutil.parser.parse(s, fuzzy=True, dayfirst=True)
    else:
        parse = lambda s: datetime.strptime(s, args.strptime)

    # simple instantiated class to hold original line and parsed date
    class dateline:
        def __init__(self, line):
            self.line = line.rstrip('\n')
            self.date = parse(line)

    # whether to read all lines and sort or use piped line-by-line operation
    if args.sort:

        inlist = [dateline(line) for line in sys.stdin]
        sieved = sieve.sieve(inlist, lambda e: e.date, args.minutes, args.hours, args.days, args.weeks, args.months, args.years)
        for s in sieved:
            print(s.line)

    else:
        
        s = sieve(args.minutes, args.hours, args.days, args.weeks, args.months, args.years)
        for line in sys.stdin:
            el = dateline(line)
            if s.add(el.date):
                print(el.line)