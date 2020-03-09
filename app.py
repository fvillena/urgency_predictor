from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from sqlalchemy import and_
import datetime

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


@app.route("/real", methods=["GET"])
def get_real():
    current_date = datetime.date.today()
    days = int(request.args.get('days'))
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
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)