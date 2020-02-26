#!/usr/bin/env python

#pip install selenium
#pip install httplib2
#pip install caldav
#pip install ics

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

#add an event example
#ics is our ical event - in vcal format
#ics = Calendar()
#event = Event()
#event.name = "a test event"
#time zone info in RFC 5545, fix this later
#https://icalendar.org/iCalendar-RFC-5545/3-2-19-time-zone-identifier.html
#event.begin = '2020-02-28 12:30:00'
#ics.events.add(event)
#calendar.add_event(str(ics))


##############################
#####    FIREFOX STUFF   #####
##############################

browser = webdriver.Firefox()
browser.get('http://wss.target.com/selfservice')
time.sleep(2)
#sign in manually, be faster than 30 seconds.
#there is some sort of bizarre trickery to detect auto logins it seems
#the login page is dynamically generated now, the fields are not predictable
#once logged in though, eHR is still working okay with chromedriver
username = browser.find_element_by_id("loginID")
password = browser.find_element_by_id("pass")
username.send_keys(config['secrets']['employeeID'])
username.send_keys(Keys.TAB)
password.send_keys(config['secrets']['password'])  
password.send_keys(Keys.RETURN)
time.sleep(10)
#choose to answer security questions
qna = browser.find_element_by_id('sec_qna')
qna.click()
login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()
time.sleep(5)
answer = browser.find_element_by_id("answer0")
#sort of hacky, but there are 3 possible security questions and we choose a "keyword"
#out of each of the three, so like "what is your favorite restaurant?" we'd use restaurant
#and search the page.  If it's on there, we submit the answer that we gave for restaurant
#if the first 2 aren't on the page then we assume the third is what it's asking for and
#submit that.
if config['questions']['question1keyword'] in browser.page_source:
    answer.send_keys(config['questions']['question1answer'])
    #print("sending " + config['questions']['question1answer'] + " as answer")
elif config['questions']['question2keyword'] in browser.page_source:
    answer.send_keys(config['questions']['question2answer'])
    #print("sending " + config['questions']['question2answer'] + " as answer")
else:
    answer.send_keys(config['questions']['question3answer'])
    #print("sending " + config['questions']['question3answer'] + " as answer")

submit = browser.find_element_by_id("submit-button")
submit.click()
time.sleep(5)
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
