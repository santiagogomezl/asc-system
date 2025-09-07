#!/usr/bin/python3

import sys
import dbi
import re
import datetime

"""
Todo: 
Generate report with username instead of ID
Get count of each controller using a dict
"""

users_requests_query = (
    "SELECT created_at, controller_name, user_id, action "
    "FROM users_requests WHERE controller_name!='ajax'"
)
current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_users_requests(report_date):
    users_requests = dbi.query_db(users_requests_query + " AND created_at > %s", (report_date,))
    generate_report(users_requests)

def get_users_requests_archive(report_date):
    users_requests_archive_query = (
        "SELECT created_at, controller_name, user_id, action " 
        "FROM users_requests_archive WHERE controller_name!='ajax' AND created_at > %s"
    )
    users_requests_archive = dbi.query_db(users_requests_archive_query, (report_date,))
    generate_report(users_requests_archive)

def generate_report(report_data):
    with open('reports/users_requests_report_'+current_datetime+'.csv', 'a') as f:
        for d in report_data:
            created_at, controller_name, user_id, action = d
            f.write(created_at.strftime('%Y-%m-%d %H:%M:%S')+"\t"+controller_name+"\t"+str(user_id)+"\t"+action+"\n")

def main():
    if len(sys.argv) == 2:
        report_date = sys.argv[1]
        date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
        if not re.search(date_regex, report_date):
            print("Invalid input. Run script passing report date YYYY-MM-DD as argument  e.g users_requests_report 2025-06-15")
            return

        #select first row date from users_requests
        first_request = dbi.query_db(users_requests_query + " LIMIT 1")
        first_date = first_request[0][0]
        report_date += " 00:00:00"
        if first_date < datetime.datetime.strptime(report_date, '%Y-%m-%d %H:%M:%S'):
            get_users_requests(report_date)
        else:
            get_users_requests_archive(report_date)
            get_users_requests(report_date)
    else:
        print("Invalid input. Run script passing 1 argument e.g users_requests_report 2025-06-15")
        return

if __name__ == "__main__":
  main()

