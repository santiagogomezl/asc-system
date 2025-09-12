#!/usr/bin/python3


import dbi
from datetime import datetime, timedelta
import smtp
import yaml
import logging
# import logging.config

logging_config = yaml.safe_load(open('/home/asc/dev/asc-system/.config/logging_config.yml'))

logging.basicConfig(
    filename= logging_config['filename'], 
    format= logging_config['format'],
    datefmt=logging_config['datefmt'],
    level=logging.INFO
 
)

#select all active users that need to submit timcard
users_query = ("SELECT id, email FROM users WHERE status='active'")
users = dbi.query_db(users_query)

date1 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
date2 = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")

managers_query = (
    "SELECT u.manager_id FROM timecards t, users u "
    "WHERE t.user_id=u.id "
    "AND t.start_date <= %s AND t.start_date > %s "
    "AND t.status='submitted'"
)
managers = dbi.query_db(managers_query, (date1, date2))
#select manager_id only once
managers_id = set(manager[0] for manager in managers) 

email_subject = 'Some timecards from your team have not been approved'
email_message = 'Please go to <a href="http://asc-data.ascoffice.com/team_timecards">Team timecard</a> page to approve timecards'

smtp.connect_smtp()

for user in users:
    user_id, user_email = user
    #if user is a manager
    if user_id in managers_id:
        print(user_email)
        smtp.send_email(user_email, email_subject, email_message)
        logging.info(f'Timecard approval alert sent to: {user_email}')

smtp.disconnect_smtp()

