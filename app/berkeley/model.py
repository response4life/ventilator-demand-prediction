import csv, json
import pdb
import os

directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ventilator_demand_prediction_csv_path = os.path.join(directory_path, 'berkeley/ventilator_demand_prediction.csv')
ventilator_demand_prediction_json_path = './ventilator_demand_prediction.json'

data = []


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
      
      data.append(facility)
    pdb.set_trace()