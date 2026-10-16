#!/usr/bin/python3

import dbi
from datetime import datetime, timedelta
import smtp
import yaml
import logging
import logging.config

# Load logging configuration
with open('/home/asc/dev/asc-system/config/logging_config.yml') as f:
    logging_config = yaml.safe_load(f)

logging.basicConfig(
    filename=logging_config['filename'],
    format=logging_config['format'],
    datefmt=logging_config['datefmt'],
    level=logging.INFO
)

# Select all active users required to submit timecards
users_query = """
    SELECT id, email
    FROM users
    WHERE timecard_needed = 'Yes'
      AND status != 'inactive'
"""

users = dbi.query_db(users_query)

# Calculate current week (Monday through Sunday)
today = datetime.now()

week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)

date1 = week_start.strftime("%Y-%m-%d")
date2 = week_end.strftime("%Y-%m-%d")

logging.info(f'Checking timecards for current week: {date1} to {date2}')

# Select users with submitted or approved timecards for current week
timecards_query = """
    SELECT DISTINCT user_id
    FROM timecards
    WHERE start_date >= %s
      AND start_date <= %s
      AND status IN ('submitted', 'approved')
"""

timecards = dbi.query_db(timecards_query, (date1, date2))

# Create a set of users who have submitted timecards
timecard_user_ids = {timecard[0] for timecard in timecards}

# Email notification
email_subject = 'Your timecard for the current week has not been entered or submitted'

email_message = """
Please go to the
<a href="http://asc-data.ascoffice.com/my_timecards">My timecard</a>
page to enter/submit your timecard for the current week.
"""

# Connect to SMTP server
smtp.connect_smtp()

try:
    # Check each employee
    for user in users:
        user_id, user_email = user

        # Send reminder if no submitted or approved timecard exists
        if user_id not in timecard_user_ids:
            try:
                smtp.send_email(
                    user_email,
                    email_subject,
                    email_message
                )

                logging.info(f'Timecard alert sent to: {user_email}')

            except Exception as e:
                logging.error(
                    f'Failed to send timecard alert to {user_email}: {e}'
                )

finally:
    # Disconnect from SMTP server
    smtp.disconnect_smtp()

logging.info('Current week timecard reminder process completed.')
