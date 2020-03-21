from flask import Flask, request
from flask_cors import CORS
from .sir import model as sir_model
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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