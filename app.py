from flask import Flask, request, jsonify, render_template 
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from sqlalchemy import and_
import datetime
import plotly
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import json

Base = declarative_base()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../urgency_predictor_data/data.sqlite')
db = SQLAlchemy(app)

ma = Marshmallow(app)


class Real(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    date = db.Column(db.Date())
    value = db.Column(db.Float())

    def __init__(self, category, date, value):
        self.category = category
        self.date = date
        self.value = value


class RealSchema(ma.Schema):
    class Meta:
        fields = ('category', 'date', 'value')

class Forecasted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    date = db.Column(db.Date())
    value = db.Column(db.Float())

    def __init__(self, category, date, value):
        self.category = category
        self.date = date
        self.value = value


class ForecastedSchema(ma.Schema):
    class Meta:
        fields = ('category', 'date', 'value')


reals_schema = RealSchema(many=True)
forecasteds_schema = ForecastedSchema(many=True)

def create_plot():


    current_date = datetime.date.today()
    starting_date = current_date - datetime.timedelta(days=60)
    all_reals = Real.query.filter_by(
        category="TOTAL CAUSAS SISTEMA RESPIRATORIO").filter(
        and_(Real.date >= starting_date)).all()
    result_real = reals_schema.dump(all_reals)

    end_date = current_date + datetime.timedelta(days=60)
    all_forecasteds = Forecasted.query.filter_by(
        category="TOTAL CAUSAS SISTEMA RESPIRATORIO").filter(
        and_(Forecasted.date >= current_date,Forecasted.date <= end_date)).all()
    result_forecasted = forecasteds_schema.dump(all_forecasteds)

    df_real = pd.DataFrame.from_dict(result_real) 
    df_forecasted = pd.DataFrame.from_dict(result_forecasted) 


    data = [
        go.Line(
            x=df_real['date'], # assign x as the dataframe column 'x'
            y=df_real['value'],
            name="Real"
        ),
        go.Line(
            x=df_forecasted['date'], # assign x as the dataframe column 'x'
            y=df_forecasted['value'],
            name="Estimado"
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/real", methods=["GET"])
def get_real():
    current_date = datetime.date.today()
    try:
        days = int(request.args.get('days'))
    except:
        days = 30
    starting_date = current_date - datetime.timedelta(days=days)
    all_reals = Real.query.filter_by(
        category="TOTAL CAUSAS SISTEMA RESPIRATORIO").filter(
        and_(Real.date >= starting_date)).all()
    result = reals_schema.dump(all_reals)
    return jsonify(result)

@app.route("/forecasted", methods=["GET"])
def get_forecasted():
    current_date = datetime.date.today()
    days = int(request.args.get('days'))
    end_date = current_date + datetime.timedelta(days=days)
    all_forecasteds = Forecasted.query.filter_by(
        category="TOTAL CAUSAS SISTEMA RESPIRATORIO").filter(
        and_(Forecasted.date >= current_date,Forecasted.date <= end_date)).all()
    result = forecasteds_schema.dump(all_forecasteds)
    return jsonify(result)


@app.route("/")
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)



if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)