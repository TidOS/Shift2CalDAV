# Shift2CalDAV
Takes shifts from eHR at Target and pushes them to a webdav calendar.  It was made because I hate manually putting in my shifts to my calendar each week.
## Requirements

 - Python 3.x
 - A DAV-enabled calendar with write access
 - Firefox
 - [Geckodriver](https://github.com/mozilla/geckodriver/releases) in your PATH 

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
## To-Dos (more of a wishlist, probably will not maintain this)
 - Replace ics with icalendar, to support timezones properly
 - Implement the WebDriverWait to wait on elements to show up instead of guessing how long the pages take to generate (currently after each submit we wait 20 seconds and usually this is too long)
 - Since webdriver works the same with different browsers, add a choice of browser in config file
	 - if that's done, need to get it working in Chrome
 - clean up/speed up code.  It's pretty ugly but it works
 - Before adding a shift, check the calendar to make sure there's not already a "work" shift there.  As it stands, it will just add a second shift even if there's already one there
