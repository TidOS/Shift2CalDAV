#!/usr/bin/env python

#pip install selenium
#pip install httplib2
#pip install caldav
#pip install ics

from selenium import webdriver
import time
import datetime
from datetime import datetime, date, timedelta
from httplib2 import Http
import caldav
from caldav.elements import dav, cdav
import configparser
from ics import Calendar, Event

#temporary holder for config options, move to file later
config = configparser.ConfigParser()
config.read("credentials.cfg")
davurl = config['url']['address-test']
print(davurl)

#example vcal
#vcal = """BEGIN:VCALENDAR
#VERSION:2.0
#PRODID:-//Example Corp.//CalDAV Client//EN
#BEGIN:VEVENT
#UID:1234567890
#DTSTAMP:20100510T182145Z
#DTSTART:20100512T170000Z
#DTEND:20100512T180000Z
#SUMMARY:This is an event
#END:VEVENT
#END:VCALENDAR
#"""
client = caldav.DAVClient(davurl)
principal = client.principal()
calendars = principal.calendars()

ics = Calendar()
event = Event()
event.name = "a test event"
#time zone info in RFC 5545, fix this later
#https://icalendar.org/iCalendar-RFC-5545/3-2-19-time-zone-identifier.html
event.begin = '2020-02-28 12:30:00'
ics.events.add(event)
#print(ics)

#we are currently providing the exact calendar to use in our URL
calendar = calendars[0]
calendar.add_event(str(ics))