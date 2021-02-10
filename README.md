# Shift2CalDAV
Takes shifts from eHR at Target and pushes them to a webdav calendar.  It was made because I hate manually putting in my shifts to my calendar each week.
## Requirements

 - Python 3.x
 - A DAV-enabled calendar with write access
 - Chrome
 - [Chromedriver](https://chromedriver.chromium.org/downloads) in your PATH 

## Usage
First, copy sample.cfg to credentials.cfg 
In it, edit the URL to your calendar, your employee ID and your Target SSO password
In the [questions] section, you need to change the "keyword" lines to words that appear in your security questions when you sign in.  This won't be the same for everyone, but don't choose a word like "the" or something that will appear elsewhere in the source code.

Next, run 

    pip install -r requirements.txt
   This will install all the imports you'll need to use the script.  You'll get:
   

 - [selenium](https://selenium-python.readthedocs.io/) 
 - [caldav](https://pythonhosted.org/caldav/)
 - [ics](https://icspy.readthedocs.io/)
 
 More important steps
 - Chromedriver is detected by the site as a bot and so logins will fail.  
 - According to [this](https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver_) StackOverflow post, there are some javascript variables sites use to detect web drivers like chromedriver
 - So, we need to run 
 ```
    perl -pi -e 's/cdc_/dog_/g' /path/to/chromedriver
```
 - This just renames some variables so that the site doesn't know we're using a web driver.
 - This repository contains a "patched" chromedriver for macOS

 
## To-Dos (more of a wishlist, probably will not maintain this)
 - Replace ics with icalendar, to support timezones properly
 - Fix case where year rolls into next year
 - Fix case where there is a workcenter change or second shift, currently only the first shift shows
 - Handle days that previously had shifts but now do not
 - Currently headless mode not working - fails at finding security q+a button - Chrome/chromedriver 88
