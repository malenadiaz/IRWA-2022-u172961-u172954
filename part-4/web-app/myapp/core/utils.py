import datetime
import json
from random import random
import csv
import requests

from faker import Faker

fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def load_json_file(path):
    """Load JSON content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    JSON: a JSON object
    """

    # Load the file into a unique string
    with open(path) as fp:
        text_data = fp.readlines()[0]
    # Parse the string into a JSON object
    json_data = json.loads(text_data)
    return json_data

def load_csv_file(path):
    """Load CSV content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    CSV: a CSV object
    """
    csv_dict = {}
    with open(path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            try:
                csv_dict[row[0]] = row[1:]
            except:
                continue
    return csv_dict

def write_csv_file(path, data):
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row, data[row]])

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data