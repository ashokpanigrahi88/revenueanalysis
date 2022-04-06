import os
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent.parent
FILE_DIRECTORY = "{}{}".format(BASE_DIR,'ballystest/')
CALENDAR_FILE = "{}{}".format(FILE_DIRECTORY,'Calendar_Test_Data.csv')
REVENUE_FILE = "{}{}".format(FILE_DIRECTORY,'Revenue_Analysis_Test_Data.csv')
BATCH_COMMIT_SIZE=500
CALENDAR_SCHEMA = {
    'CALENDAR_DATE': 'string' ,
    'CALENDAR_YEAR'    : 'int16',
    'CALENDAR_MONTH_NUMBER'  : 'int16',
    'CALENDAR_MONTH_NAME'    : 'string',
    'CALENDAR_DAY_OF_MONTH' : 'int16',
    'CALENDAR_DAY_OF_WEEK' : 'int16',
    'CALENDAR_DAY_NAME'    : 'string',
    'CALENDAR_YEAR_MONTH'  : 'int32',
}
REVENUE_SCHEMA = {
    'ACTIVITY_DATE': 'string' ,
    'MEMBER_ID': 'int64' ,
    'GAME_ID': 'int32' ,
    'WAGER_AMOUNT': 'float64' ,
    'NUMBER_OF_WAGERS': 'int16' ,
    'WIN_AMOUNT': 'float64' ,
    'ACTIVITY_YEAR_MONTH': 'int32' ,
    'BANK_TYPE_ID': 'int'
}