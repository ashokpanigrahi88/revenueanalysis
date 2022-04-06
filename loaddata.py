import config
import loadutils

def load_data():
    loadutils.csv_to_table(config.CALENDAR_FILE,loadutils.f_insert_calendar,p_schema=config.CALENDAR_SCHEMA,p_date=['CALENDAR_DATE'])
    loadutils.csv_to_table(config.REVENUE_FILE,loadutils.f_insert_revenue,p_schema=config.REVENUE_SCHEMA,p_date=['ACTIVITY_DATE'])
    loadutils.insert_missing_calendar()