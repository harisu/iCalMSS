#! /usr/bin/env python
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
if argc != 3:
    print('Usage: # python3 iCalICT.py input.csv output.ics')
    quit()

print(f'Reading the content of {argvs[1]}...')
f = open(argvs[1], "r", encoding="utf-8")
reader = csv.reader(f)
header = next(reader)  # ヘッダーをスキップ

# カレンダー作成
ical = Calendar()
ical.add('prodid', '-//Custom Calendar//iCalICT 1.0//EN')
ical.add('version', '2.0')
ical.add('CALSCALE', 'GREGORIAN')
ical.add('METHOD', 'PUBLISH')
ical.add('X-WR-CALNAME', '明電舎ICT入門教育スケジュール')
ical.add('X-WR-TIMEZONE', 'Asia/Tokyo')
ical.add('X-WR-CALDESC', '')

tz_tokyo = pytz.timezone('Asia/Tokyo')

for row in reader:
    start_date = row[0]
    start_time = row[1]
    end_date = row[2]
    end_time = row[3]
    lecture_name = row[4]
    location = row[5]
    department = row[6]
    instructor = row[7]

    # 開始日時と終了日時を作成
    dtstart = tz_tokyo.localize(datetime.datetime.strptime(f"{start_date} {start_time}", '%Y/%m/%d %H:%M'))
    dtend = tz_tokyo.localize(datetime.datetime.strptime(f"{end_date} {end_time}", '%Y/%m/%d %H:%M'))

    # イベント作成
    event = Event()
    event.add('summary', lecture_name)
    event.add('location', location)
    event.add('description', f"担当部門: {department}\n講師: {instructor}")
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    ical.add_component(event)

f.close()

# icsファイル出力
output_path = os.path.join(os.getcwd(), argvs[2])
with open(output_path, 'wb') as f:
    f.write(ical.to_ical())

print(f"iCal file has been created: {output_path}")