from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from .sir import model as sir_model
from . import berkeley
import json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'app/berkeley'
directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.config['UPLOAD_FOLDER'] = os.path.join(directory_path, UPLOAD_FOLDER)
app.secret_key = os.environ.get('APP_SECRET_KEY')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def json_response(body, headers=None, status=200):
    if headers is None:
        headers = {}

    headers.setdefault('Content-Type', 'application/json')
    return json.dumps({
        'statusCode': status,
        'headers': headers,
        'body': body,
    })


def upload_file(file, file_name, directory, response_type='json', http_template=None):
   # submit an empty part without filename
    if file and allowed_file(file.filename):
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], '{}/{}'.format(directory, file_name)))

        if directory == 'severity':
            data = berkeley.severity.read_csv()
            berkeley.severity.write_data(data)

        if directory == 'ventilators':
            data = berkeley.ventilators.read_csv()
            berkeley.ventilators.write_data(data)

        if response_type == 'json':
            return json_response(body={'message': 'success'})
        return True
    else:
        if response_type == 'json':
            return json_response(body={'message': 'did not recognize file, you can only upload csv files'}, status=400)
        print(file.filename)
        return False


@app.route('/sir')
def calculate_sir():
    population = request.args.get('population')
    initial_infected = request.args.get('initial_infected')
    initial_recovered = request.args.get('initial_recovered')
    recovery_rate = request.args.get('recovery_rate')
    contact_rate = request.args.get('contact_rate')
    total_days = request.args.get('days')

    query = {
        'population': population and int(population),
        'I0': initial_infected and int(initial_infected),
        'R0': initial_recovered and int(initial_recovered),
        'contact_rate': contact_rate and float(contact_rate),
        'recovery_rate': recovery_rate and float(recovery_rate),
        'days': total_days and int(total_days),
    }

    null_filtered_query = {k: v for k, v in query.items() if v is not None}

    response = sir_model.calculate(**null_filtered_query)
    return json.dumps(response)


@app.route('/berkeley/ventilators')
def get_berkeley_data():
    data = berkeley.ventilators.get_json_file()
    return json_response(data)


@app.route('/berkeley/ventilators/upload', methods=['GET', 'POST'])
def upload_ventilator_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if upload_file(file, 'ventilator_demand_prediction.csv',
                       'ventilators', 'http'):
            return redirect(url_for('uploaded_file'))
        else:
            flash('Not a csv file')
            return redirect(request.url)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/berkeley/ventilators/auto-upload', methods=['POST'])
def auto_upload_ventilator_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return json.dumps({
                'status': 400,
                'error': 'did not recognize file, you can only upload csv files'
            })
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        return upload_file(file, 'ventilator_demand_prediction.csv', 'ventilators')


@app.route('/berkeley/ventilators')
def get_berkeley_ventilator_data():
    data = berkeley.ventilators.get_json_file()
    return json_response(data)


@app.route('/berkeley/severity/upload', methods=['GET', 'POST'])
def upload_severity_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if upload_file(file, 'severity_index.csv', 'severity', 'http'):
            return redirect(url_for('uploaded_file'))
        else:
            flash('Not a csv file')
            return redirect(request.url)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/berkeley/severity/auto-upload', methods=['POST'])
def auto_upload_severity_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return json.dumps({
                'status': 400,
                'error': 'did not recognize file, you can only upload csv files'
            })
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        return upload_file(file, 'severity_index.csv', 'severity')


@app.route('/berkeley/severity')
def get_berkeley_severity_data():
    data = berkeley.severity.get_json_file()
    return json_response(data)


@app.route('/uploads/success')
def uploaded_file():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload Successful!</h1>
    <div>
      <a href="/berkeley/upload">upload another</a>
    </div>
    '''
