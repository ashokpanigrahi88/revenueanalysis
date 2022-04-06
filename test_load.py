import loaddata
import ddl
import loadutils
import requests
import pandas as pd
from datetime import date, time, datetime


def run_ddl():
    """
    run ddl to create tables and indexes
    """
    ddl.create_tables()
    ddl.create_indexes()

def load_and_analyse_data():
    """
    run every time you want to load ar reload data
    duplicate records will automatically be ignored
    """
    loaddata.load_data()
    loadutils.analyse_data()

def analyse_data():
    """
    Q1 : output is produced by invoking this module
    :return:
    """
    loadutils.analyse_data()

def rest_api(p_url="http://66.206.9.210:8080/rest-api/membersummary/?format=json",p_params:{}={}, p_format='json'):
    """
    This is all defaulted and for testing purpose only
    End point is hosted on my development server
    """
    results = requests.get(p_url,params=p_params)
    if results.status_code != 200:
        print('FAILED:',results.status_code)
        return results.status_code
    data = results.json()['results']
    if p_format == 'panda':
        df = pd.DataFrame(data)
        return df
    return data

def insert_test_data():
    """"
    Add more data to this module to ingest test records
    or call directly loadutils.ingest_test_data
    """
    mm= int(2)
    yy=int(2019)
    loadutils.ingest_test_data(p_memberid=1004,
                               p_activitydate=date(year=yy,month=mm,day=10),
                               p_gameid=890,
                               p_wageramount=1.0,
                               p_banktypeid=0,
                               p_activityyearmonth=int(str("{}{:02d}".format(yy,mm))),
                               p_numberofwages=3,
                               p_winamount=20)

    mm= int(3)
    loadutils.ingest_test_data(p_memberid=1001,
                               p_activitydate=date(year=2018,month=mm,day=1),
                               p_gameid=8901,
                               p_wageramount=0,
                               p_banktypeid=0,
                               p_activityyearmonth=int(str("{}{:02d}".format(yy,mm))),
                               p_numberofwages=0,
                               p_winamount=0)
