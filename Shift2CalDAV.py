#!/usr/bin/env python

import datetime
from datetime import datetime, date, timedelta
import configparser
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import caldav

# from caldav.elements import dav, cdav
# pylint suggest cdav unused
from caldav.elements import dav

from ics import Calendar, Event

# unused
# from dateutil import tz


# get calendar specific info from credentials.cfg
config = configparser.ConfigParser()
config.read("credentials.cfg")
davurl = config['url']['address']
davname = config['url']['user']
davpass = config['url']['pass']
calname = config['url']['name']

client = caldav.DAVClient(url=davurl, username=davname, password=davpass)
# a principal holds calendars, there can be multiple
principal = client.principal()
calendars = principal.calendars()
calendar = calendars[0]
# since there can be multiple calendars, we need the one that is matched
# in our URL from credentials.cfg
# note:  if correct calendar is not found, the first calendar from the
# principal will be used.  This may be undesirable!
for i in calendars:
    if calname in i.get_properties(props=[dav.Href()])["{DAV:}href"]:
        calendar = i
        break


class Shift:
    ''' A Shift has a start and end date and can add events to the global calendar'''

    def __init__(self, day, date, position, start_time, end_time):
        self.day = day
        self.date = date
        self.position = position
        self.start_time = datetime.strptime(start_time, "%I:%M%p").strftime("%H:%M:%S")
        self.end_time = datetime.strptime(end_time, "%I:%M%p").strftime("%H:%M:%S")

    def make_event(self):

        ics = Calendar()
        event = Event()

        # check for existing work shift
        # if there is one, delete it and replace with the new one
        # because it's possible the shift has changed
        split = self.date.split('-')
        # print("looking in calendar for date: " + self.date)

        try:
            todayshift = calendar.date_search(datetime(int(split[0]),
                                                       int(split[1]),
                                                       int(split[2])),
                                              datetime(int(split[0]),
                                                       int(split[1]),
                                                       int(split[2]) + 1))
        except ValueError:
            print("it's next month for next day.")
            todayshift = calendar.date_search(datetime(int(split[0]),
                                                       int(split[1]),
                                                       int(split[2])),
                                              datetime(int(split[0]),
                                                       int(split[1]) + 1, 1))
        for e in todayshift:
            e.load()
            if "<SUMMARY{}work" in str(e.instance.vevent):
                # print("deleting existing shift")
                e.delete()
        event.name = "work - " + self.position
        event.begin = self.date + " " + self.start_time
        event.end = self.date + " " + self.end_time
        ics.events.add(event)
        # we need to get rid of the Z in the times because it implies we're using UTC
        # we are just using 'local' time, no time zone and ics module only supports UTC
        calendar.add_event(str(ics).replace("Z", ""))


##############################
#####    CHROME  STUFF   #####
##############################

if config['options']['headless'] == "yes":
    print("headless mode enabled")
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    browser = webdriver.Chrome(options=options)
else:
    browser = webdriver.Chrome()

browser.get('http://wss.target.com/selfservice')
timeout = 20
waittime = timeout
try:
    element_present = EC.presence_of_element_located((By.ID, 'loginID'))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load or login failed?")
time.sleep(1)
print("entering username and password...")
username = browser.find_element_by_id("loginID")
password = browser.find_element_by_id("pass")
username.click()
username.send_keys(config['secrets']['employeeID'])
username.send_keys(Keys.TAB)
username.click()
password.send_keys(config['secrets']['password'])
password.click()
# password.send_keys(Keys.RETURN)
loginbutton = browser.find_element_by_name("Login")
loginbutton.submit()
try:
    element_present = EC.presence_of_element_located((By.ID, 'sec_qna'))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for security question option.")
time.sleep(1)
print("selecting Q+A button...")
# choose to answer security questions
qna = browser.find_element_by_id('sec_qna')
qna.click()
login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()

try:
    element_present = EC.presence_of_element_located((By.ID, 'answer0'))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for actual security question.")
time.sleep(1)
print("answering security question...")
answer = browser.find_element_by_id("answer0")
# sort of hacky, but there are 3 possible security questions and we choose a "keyword"
# out of each of the three, so like "what is your favorite restaurant?" we'd use restaurant
# and search the page.  If it's on there, we submit the answer that we gave for restaurant
# if the first 2 aren't on the page then we assume the third is what it's asking for and
# submit that.
if config['questions']['question1keyword'] in browser.page_source:
    answer.send_keys(config['questions']['question1answer'])
    # print("sending " + config['questions']['question1answer'] + " as answer")
elif config['questions']['question2keyword'] in browser.page_source:
    answer.send_keys(config['questions']['question2answer'])
    # print("sending " + config['questions']['question2answer'] + " as answer")
else:
    answer.send_keys(config['questions']['question3answer'])
    # print("sending " + config['questions']['question3answer'] + " as answer")

submit = browser.find_element_by_id("submit-button")
submit.click()

try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'request_table_bordered'))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for schedule to appear.")
time.sleep(1)

table = browser.find_element_by_class_name("request_table_bordered")

# current week
if config['options']['thisweek'] == "yes":
    for x in range(2, 9):
        # this loop cycles through the week and assembles your shift information 
        # and creates the event
        days = browser.find_element_by_xpath \
            ("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[1]/td["
             + str(x) + "]")
        shift = browser.find_element_by_xpath \
            ("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[3]/td["
             + str(x) + "]")
        if not shift.text.strip():
            continue
        shift_info = (days.text + '\n' + shift.text)
        # print(shift_info)
        workday = Shift(shift_info.splitlines()[0],
                        datetime.strptime(shift_info.splitlines()[1],
                                          "%m/%d/%y").strftime("%Y-%m-%d"),
                        shift_info.splitlines()[2],
                        shift_info.splitlines()[3].split('-')[0].strip(),
                        shift_info.splitlines()[3].split('-')[1].strip())
        workday.make_event()
        print("made shift for " + shift_info.splitlines()[0])

# next week
if config['options']['nextweek'] == "yes":
    nextButton = browser.find_element_by_xpath \
        ("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[2]/tbody/tr[1]/td/div/a[2]")
    nextButton.click()

    for x in range(2, 9):
        # this loop cycles through the week and assembles your shift information
        # and creates the event
        days = browser.find_element_by_xpath \
            ("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[1]/td["
             + str(x) + "]")
        shift = browser.find_element_by_xpath \
            ("//*[@id='page_content']/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[3]/td["
             + str(x) + "]")
        if not shift.text.strip() or "Unpaid" in shift.text.strip():
            continue
        shift_info = (days.text + '\n' + shift.text)
        # print(shift_info)
        workday = Shift(shift_info.splitlines()[0],
                        datetime.strptime(shift_info.splitlines()[1],
                                          "%m/%d/%y").strftime("%Y-%m-%d"),
                        shift_info.splitlines()[2],
                        shift_info.splitlines()[3].split('-')[0].strip(),
                        shift_info.splitlines()[3].split('-')[1].strip())
        workday.make_event()
        print("made shift for " + shift_info.splitlines()[0])

browser.quit()
