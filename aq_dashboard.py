"""Minimal flask app"""

from flask import Flask, render_template
import requests
from openaq import OpenAQ
from decouple import config
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
api = OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    city = DB.Column(DB.String(60), nullable=False)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DATE: {}, VALUE: {}>'.format(self.datetime, self.value)


def make_list():
    """returns a list of tuples"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    date_values = []
    results = body['results']
    for result in results:
        result_tuple = (str(result['date']['utc']), result['value'])
        date_values.append(result_tuple)

        return date_values

    return APP


@APP.route('/')
def root():
    """main route"""
    return render_template('home.html')


@APP.route('/la')
def la():
    big_values = Record.query.filter(Record.value >= 10).all()
    #, Record.city == 'Los Angeles'
    return render_template('la.html', big_values=big_values)


def new_city(city):
    """generate datetime and value for specified city"""
    api = OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    dates_values = [(result['date']['utc'], result['value']) for result in results]
    return dates_values


@APP.route('/refresh')
def refresh():
    """refresh data page"""
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    cities = ['Los Angeles']
    for city in cities:
        new_city(city)
    DB.session.commit()
    return 'Data refreshed!'
