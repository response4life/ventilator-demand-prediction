from flask import Flask, request
import sir
import json

app = Flask(__name__)

@app.route('/')
def calculate_sir():
    population = request.args.get('p')
    response = sir.calculate(int(population))
    return json.dumps(response)