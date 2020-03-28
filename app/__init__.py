from flask import Flask, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from .sir import model as sir_model
from .berkeley import model as berkeley_model
import json
from werkzeug.utils import secure_filename
import os
import pdb

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'app/berkeley'
directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.config['UPLOAD_FOLDER'] = os.path.join(directory_path, UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
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
  
@app.route('/berkeley')
def get_berkeley_data():
  response = berkeley_model.get_json_file()
  return json.dumps(response)

@app.route('/berkeley/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'ventilator_demand_prediction.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = berkeley_model.read_csv()
            berkeley_model.write_data(data)
            return redirect(url_for('uploaded_file'))

            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/berkeley/auto-upload', methods=['POST'])
def auto_upload_file():
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
        if file and allowed_file(file.filename):
            filename = 'ventilator_demand_prediction.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = berkeley_model.read_csv()
            berkeley_model.write_data(data)
            return json.dumps({
              'status': 200,
              'message': 'upload successful!'
            })
        else:
          return json.dumps({
            'status': '400',
            'error': 'did not recognize file, you can only upload csv files'
          })

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