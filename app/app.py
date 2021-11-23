import config as CONFIG

from flask import Flask
from utils import load_csv, db_import, run_io_tasks_in_parallel, create_db_scheme, execute_query


app = Flask(__name__)
# app.run(debug=True)


@app.before_first_request
def setup_database():
    """Create db-setup"""
    print('setting up database..')
    create_db_scheme()
    data_impr = load_csv('./files/impressions.csv')
    data_clicks = load_csv('./files/clicks.csv')
    run_io_tasks_in_parallel([
        lambda: db_import(data_impr['rows'], 'impressions', CONFIG.QUERY_INSERT_IMPRESSION),
        lambda: db_import(data_clicks['rows'], 'clicks', CONFIG.QUERY_INSERT_CLICK),
    ])


@app.route('/')
def main():
    return 'Welcome to seznam.czc.manzes ot emocleW'


@app.route('/clicks')
def get_clicks():
    """Get number of clicks"""
    date = '2021-04-21'
    query = CONFIG.QUERY_GET_CLICKS.format(date=date)
    return {'clicks_count': execute_query(query)}


@app.route('/impressions')
def get_impressions():
    """Get number of impressions"""
    date = '2021-04-21'
    ad_id = 2
    query = CONFIG.QUERY_GET_IMPRESSIONS.format(ad_id=ad_id, date=date)
    return {'impressions_count': execute_query(query)}
