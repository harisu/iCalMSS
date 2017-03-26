#! /usr/bin python
# -*- coding: utf-8 -*-
import sys
import os
import csv
import datetime
from icalendar import Calendar, Event
import pytz

argvs = sys.argv
argc = len(argvs)

# デバッグプリント
if (argc != 3):
    print('Usage: # iCalMSS %s csvFIleName.csv output.ics' % argvs[0])
    quit()
 
print('The content of %s ...n' % argvs[1])
f = open(argvs[1], "r")
reader = csv.reader(f)
# header = next(reader)

 # カレンダーに追加
ical = Calendar()
ical.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
ical.add('version', '2.0')
ical.add('CALSCALE', 'GREGORIAN')
ical.add('METHOD', 'PUBLISH')
ical.add('X-WR-ALNAME', '明電カレンダー')
ical.add('X-WR-TIMEZONE', 'Asia/Tokyo')
ical.add('X-WR-CALDESC', '')

for row in reader:
    if (row[1] == "*"):
        tstr = row[0] #'2012/12/29'
        tdatetime = datetime.datetime.strptime(tstr, '%Y/%m/%d')
        datestart = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
        dateend = datestart + datetime.timedelta(days=1)
        print("Start = %s / End = %s", datestart, dateend)

        # イベント作成
        event = Event()
        event.add('summary', 'ほげ')
        event.add('description', 'ほげ 詳細') 

        tz_tokyo = pytz.timezone('Asia/Tokyo')
        event.add('dtstart', datestart)
        event.add('dtend', dateend)
        ical.add_component(event)
f.close()

# icsファイル出力
directory = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(directory, argvs[2]), 'wb')
f.write(ical.to_ical())
f.close()