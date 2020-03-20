# Prediction for Ventilator Demand Based on SIR model

A _REALLY_ simple flask application for returning json with prediction data based on a vew variables

## Getting Started

create a virtual environment to work in

`virtualenv <venv name>`
`source <venv name>/bin/activate`

install requirements

`pip3 inestall -r requirements.txt`

set environment variable

`export FLASK_APP=run.py`

run the application

`flask run`

You can then hit `localhost:5000` with requests and get back an array of predictions/day

example request: `http://localhost:5000/?population=950715&initial_infected=1&initial_recovered=0&recovery_rate=0.1&contact_rate=0.2&days=365`

### Viewing a plot of the data

if you'd like to plot the data using matplotlib just run `python3 sir`
