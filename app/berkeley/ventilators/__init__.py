import csv
import json
import os
import datetime

directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ventilator_demand_prediction_csv_path = os.path.join(
    directory_path, 'ventilators/ventilator_demand_prediction.csv')
ventilator_demand_prediction_json_path = os.path.join(
    directory_path, 'ventilators/ventilator_demand_prediction.json')


def day_data_object():
    days = ['day1', 'day3', 'day5']
    return dict((day, {
        'vent_needed': 0,
        'vent_demand': 0,
        'vent_supply': 0,
    }) for day in days)


def facility_dict():
    return {
        'name': '',
        'ventilator_data': day_data_object(),
        'county_name': '',
        'TIN': '',
        'FIPS': ''
    }


def read_csv():
    data = {
        'last_upload_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ'),
        'facilities': []
    }
    with open(ventilator_demand_prediction_csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            facility = facility_dict()
            facility['name'] = row['Facility Name']
            facility['county_name'] = row['County Name']
            facility['TIN'] = row['TIN']
            facility['FIPS'] = row['countyFIPS']
            facility['ventilator_data']['day1'] = {
                'vent_needed': row['Vent Needed 1-day'],
                'vent_demand': row['Vent Demand 1-day'],
                'vent_supply': row['Vent Supply 1-day']
            }
            facility['ventilator_data']['day3'] = {
                'vent_needed': row['Vent Needed 3-day'],
                'vent_demand': row['Vent Demand 3-day'],
                'vent_supply': row['Vent Supply 3-day']
            }
            facility['ventilator_data']['day5'] = {
                'vent_needed': row['Vent Needed 5-day'],
                'vent_demand': row['Vent Demand 5-day'],
                'vent_supply': row['Vent Supply 5-day']
            }

            data['facilities'].append(facility)

        return data


def write_data(data):
    with open(ventilator_demand_prediction_json_path, 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))


def get_json_file():
    with open(ventilator_demand_prediction_json_path) as file:
        data = json.load(file)

    return data
