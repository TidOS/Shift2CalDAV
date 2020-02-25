#!/usr/bin/env python

#pip install selenium
#pip install httplib2
#pip install caldav

from selenium import webdriver
import time
import datetime
from datetime import datetime, date, timedelta
from httplib2 import Http
import caldav
from caldav.elements import dav, cdav
import configparser

#temporary holder for config options, move to file later
config = configparser.ConfigParser()
config.read("credentials.cfg")
davurl = config['url']['address']


vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:1234567890
DTSTAMP:20100510T182145Z
DTSTART:20100512T170000Z
DTEND:20100512T180000Z
SUMMARY:This is an event
END:VEVENT
END:VCALENDAR
"""
client = caldav.DAVClient(davurl)
principal = client.principal()
calendars = principal.calendars()
if len(calendars) > 0:
    calendar = calendars[0]
    print( "Using calendar", calendar)

    print ("Looking for events in 2020-02")
    results = calendar.date_search(
        datetime(2020, 2, 1), datetime(2020, 3, 1))

    for event in results:
        print("Found", event)
else:
     print("nada")