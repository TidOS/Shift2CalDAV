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

#acquire calendar info
client = caldav.DAVClient(davurl)
principal = client.principal()
calendars = principal.calendars()
#we are currently providing the exact calendar to use in our URL
calendar = calendars[0]

#ics is our ical event - in vcal format
ics = Calendar()
event = Event()
event.name = "a test event"
#time zone info in RFC 5545, fix this later
#https://icalendar.org/iCalendar-RFC-5545/3-2-19-time-zone-identifier.html
event.begin = '2020-02-28 12:30:00'
ics.events.add(event)
calendar.add_event(str(ics))


#############################
#####    CHROME STUFF   #####
#############################

#chromedriver must be in PATH,
#todo - detect Chrome version and download correct chromedriver?
#https://sites.google.com/a/chromium.org/chromedriver/downloads
chromeDriver = 'chromedriver.exe'
browser = webdriver.Chrome(chromeDriver)
browser.get('http://wss.target.com/selfservice')

#sign in manually, be faster than 30 seconds.
#there is some sort of bizarre trickery to detect auto logins it seems
#the login page is dynamically generated now, the fields are not predictable
#once logged in though, eHR is still working okay with chromedriver


time.sleep(60)

table = browser.find_element_by_class_name("request_table_bordered")

for x in range(2, 9):
    # this loop cycles through the week and assembles your shift information and creates the event
    days = browser.find_element_by_xpath("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[1]/td["
                                         + str(x) + "]")
    shift = browser.find_element_by_xpath("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[3]/td["
                                          + str(x) + "]")
    if not shift.text.strip():
        continue
    shift_info = (days.text + '\n' + shift.text)
    print(shift_info)

#move to the next page
next = browser.find_element_by_xpath("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[2]/tbody/tr[1]/td/div/a[2]")
next.click()

for x in range(2, 9):
    # this loop cycles through the week and assembles your shift information and creates the event
    days = browser.find_element_by_xpath("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[1]/td["
                                         + str(x) + "]")
    shift = browser.find_element_by_xpath("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[3]/td["
                                          + str(x) + "]")
    if not shift.text.strip():
        continue
    shift_info = (days.text + '\n' + shift.text)
    print(shift_info)
