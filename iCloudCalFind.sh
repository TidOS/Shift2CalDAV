#!/bin/bash
BASEURL=`grep "caldav.icloud.com" ~/Library/Calendars/*/*.plist | grep principal | sed 's/http/\nhttp/g' | grep "https" | cut -f 1 -d "<" | rev | cut -d / -f3- | rev`
CALENDAR=`grep "caldav.icloud.com" ~/Library/Calendars/*/*.plist | grep principal | cut -d "/" -f 6`
clear
for i in `grep "calendars/" ~/Library/Calendars/$CALENDAR/*/*.plist | awk {'printf("%s\n",$2)'} | cut -d / -f 4`; do echo $BASEURL/calendars/$i; done
