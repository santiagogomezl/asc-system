#!/usr/bin/python3

import dbi
import re
import datetime

users_requests_query = "SELECT created_at, controller_name, user_id, action FROM users_requests WHERE controller_name!='ajax'"

def get_users_requests(report_date):
    users_requests = dbi.query_db(users_requests_query + "AND created_at > %(rd)s", {'rd':report_date})
    #CONTINUE HERE
    return None

def get_users_requests_archive():
    return None

def main():
    date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$"
    print("Enter from which date to run report in format YYYY-MM-DD: ")
    report_date = input()

    if re.search(date_regex, report_date) == None:
        print("Invalid input. Enter date in format YYYY-MM-DD e.g 2025-06-15")
        return

    #select first row date from users_requests
    first_request = dbi.query_db(users_requests_query + " LIMIT 1")
    first_date = first_request[0][0]
    report_date += " 00:00:00"
    if first_date > datetime.datetime.strptime(report_date, '%Y-%m-%d %H:%M:%S'):
        get_users_requests(report_date)
    # else:
    #     get_users_requests_archive()
    #     get_users_requests()

if __name__ == "__main__":
  #Run as main program
  main()

