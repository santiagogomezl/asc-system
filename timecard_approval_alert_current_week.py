#!/usr/bin/python3

import dbi
from datetime import datetime, timedelta
import smtp
import yaml
import logging

# Load logging configuration
with open('/home/asc/dev/asc-system/config/logging_config.yml') as f:
    logging_config = yaml.safe_load(f)

logging.basicConfig(
    filename=logging_config['filename'],
    format=logging_config['format'],
    datefmt=logging_config['datefmt'],
    level=logging.INFO
)

# Calculate current week (Monday through Sunday)
today = datetime.now()

week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)

date1 = week_start.strftime("%Y-%m-%d")
date2 = week_end.strftime("%Y-%m-%d")

logging.info(f'Checking pending timecard approvals: {date1} to {date2}')

# Select active managers with submitted timecards pending approval
managers_query = """
    SELECT DISTINCT u.manager_id, m.email
    FROM timecards t
    JOIN users u ON t.user_id = u.id
    JOIN users m ON u.manager_id = m.id
    WHERE t.start_date >= %s
      AND t.start_date <= %s
      AND t.status = 'submitted'
      AND m.status = 'active'
      AND u.manager_id IS NOT NULL
"""

managers = dbi.query_db(managers_query, (date1, date2))

# Email notification
email_subject = 'Some timecards from your team have not been approved'

email_message = """
Some timecards from your team are awaiting your approval.

Please go to the
<a href="http://asc-data.ascoffice.com/team_timecards">Team timecard</a>
page to review and approve submitted timecards.
"""

# Connect to SMTP server
smtp.connect_smtp()

try:
    for manager_id, manager_email in managers:
        try:
            smtp.send_email(
                manager_email,
                email_subject,
                email_message
            )

            logging.info(
                f'Timecard approval alert sent to: {manager_email}'
            )

        except Exception as e:
            logging.error(
                f'Failed to send approval alert to {manager_email}: {e}'
            )

finally:
    smtp.disconnect_smtp()

logging.info('Current week manager approval reminders completed.')
