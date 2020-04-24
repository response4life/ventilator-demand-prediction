import csv
import json
import os
import datetime

directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
severity_index_csv_path = os.path.join(
    directory_path, 'severity/severity_index.csv')
severity_index_json_path = os.path.join(
    directory_path, 'severity/severity_index.json')


def read_csv():
    data = {
        'last_upload_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ'),
        'facilities': []
    }
    with open(severity_index_csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            facility = {
                'name': row['Hospital Name'],
                'severity_index': {
                    'day1': row['Severity 1-day'],
                    'day2': row['Severity 2-day'],
                    'day3': row['Severity 3-day'],
                    'day4': row['Severity 4-day'],
                    'day5': row['Severity 5-day'],
                    'day6': row['Severity 6-day'],
                    'day7': row['Severity 7-day'],
                },
                'county_name': row['CountyName'],
                'cms_certification_number': row['CMS Certification Number'],
                'county_fips': row['countyFIPS'],
                'state_name': row['StateName'],
                'system_affiliation': row['System Affiliation'],
                'total_deaths_hospital': row['Total Deaths Hospital'],
                'latitude': row['Latitude'],
                'longitude': row['Longitude'],
                'surge_3_day': row['Surge 3-day'],
                'predicted_new_deaths_hospital_3_day': row['Predicted New Deaths Hospital 3-day'],
                'total_deaths_county': row['Total Deaths County'],
                'predicted_new_deaths_county_3_day': row['Predicted New Deaths County 3-day'],
                'icu_beds': row['ICU Beds'],
                'hospital_employees': row['Hospital Employees']
                'rural_severity_3_day': row['Rural Severity 3-day']
            }

            data['facilities'].append(facility)

        return data


def write_data(data):
    with open(severity_index_json_path, 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))


def get_json_file():
    with open(severity_index_json_path) as file:
        data = json.load(file)

    return data
