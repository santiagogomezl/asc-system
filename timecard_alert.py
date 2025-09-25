#!/usr/bin/python3

import dbi
from datetime import datetime, timedelta
import smtp
import yaml
import logging
import logging.config

logging_config = yaml.safe_load(open('/home/asc/dev/asc-system/config/logging_config.yml'))

logging.basicConfig(
    filename= logging_config['filename'], 
    format= logging_config['format'],
    datefmt=logging_config['datefmt'],
    level=logging.INFO
 
)

#select all active users that need to submit timcard
users_query = ("SELECT id, email FROM users WHERE timecard_needed='Yes' AND status!='inactive' ")
users = dbi.query_db(users_query)

date1 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
date2 = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

#select the users that have a submitted or approved timecard
timecards_query = ("SELECT user_id FROM timecards WHERE start_date <= %s AND start_date > %s AND (status='submitted' || status ='approved') ")
timecards = dbi.query_db(timecards_query, (date1, date2))

timecard_user_id = [timecard[0] for timecard in timecards]

email_subject = 'Your timecard for previous week has not been entered or submitted'
email_message = 'Please go to <a href="http://asc-data.ascoffice.com/my_timecards">My timecard</a> page to enter/submit your timecard'

smtp.connect_smtp()

# for user in users:
for user in users:
    user_id, user_email = user
    #if user has not submitted a timecard
    if user_id not in timecard_user_id:
        smtp.send_email(user_email, email_subject, email_message)
        logging.info(f'Timecard alert sent to: {user_email}')

smtp.disconnect_smtp()


