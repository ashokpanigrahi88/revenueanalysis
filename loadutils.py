import time
import numpy as np
import pandas as pd
import db
import config
import time
from datetime import date,  datetime
"""
separate function for each table
"""

def f_insert_calendar(p_rows: [] = [], p_conn=db.db_connection):
    start = time.time()
    print('connection:', p_conn)
    try:
        cur = p_conn.cursor()
        cur.executemany("""insert into /*+ APPEND */ 
                        CALENDAR(CALENDAR_DATE,CALENDAR_YEAR,CALENDAR_MONTH_NUMBER,
                        CALENDAR_MONTH_NAME,CALENDAR_DAY_OF_MONTH,CALENDAR_DAY_OF_WEEK,
                        CALENDAR_DAY_NAME,CALENDAR_YEAR_MONTH) 
                        values(:1,:2,:3,:4,:5,:6,:7,:8)
                        """, p_rows, batcherrors=True)
        p_conn.commit()
    except Exception as ex:
        print('insert calendar',ex)
    end = time.time()


def f_insert_revenue(p_rows: [] = [], p_conn=db.db_connection):
    start = time.time()
    print('connection:', p_conn)
    try:
        cur = p_conn.cursor()
        cur.executemany("""insert into /*+ APPEND */ 
                        REVENUE_ANALYSIS(ACTIVITY_DATE, MEMBER_ID,GAME_ID,
                    WAGER_AMOUNT,NUMBER_OF_WAGERS, WIN_AMOUNT,ACTIVITY_YEAR_MONTH,BANK_TYPE_ID) 
                        values(:1,:2,:3,:4,:5,:6,:7,:8)
                        """, p_rows, batcherrors=True)
        p_conn.commit()
    except Exception as ex:
        print('insert calendar',ex)
    end = time.time()


def insert_missing_calendar(p_conn=db.db_connection):
    start = time.time()
    cur = p_conn.cursor()
    cur.execute("""
    insert into calendar
        select activity_date,to_char(activity_date,'YYYY'),
        to_char(activity_date,'MM'),
        to_char(activity_date,'Month'),
        to_char(activity_date,'dd'),
        to_char(activity_date,'dw'),
        to_char(activity_date,'Day'),
        to_char(activity_date,'YYYYMM')
        FROM( 
        select activity_date from REVENUE_ANALYSIS
        MINUS
        select calendar_date   from CALENDAR 
        )
        """)
    p_conn.commit()
    end = time.time()


def csv_to_table(p_file, p_table_func, p_schema: {} = {}, p_date: [] = [], p_header: int = 0, p_commitsize=config.BATCH_COMMIT_SIZE):
    data_df = pd.read_csv(p_file, header=p_header, parse_dates=p_date, dtype=p_schema)
    print(data_df.info(memory_usage=True))
    data_rows, data_cols = data_df.shape
    print('Number of rows', data_rows)
    print('Number of columns', data_cols)
    for from_row in range(0, data_rows, p_commitsize):
        to_row = (from_row + p_commitsize - 1)
        print(from_row, to_row)
        data_list = list(data_df.iloc[from_row:to_row, ].itertuples(index=False, name=None))
        p_table_func(data_list)

def analyse_data(p_memberid = None):
    analysis_sql = """
    With
    members_trans as
    (
    Select  m1.activity_date , m1.member_id member_id, m1.Activity_year_month, wager_amount 
    from   REVENUE_ANALYSIS m1
    )
    ,
    monthly_calendar as
    (
    select m.member_Id, m.ACTIVITY_YEAR_MONTH yyyymm,  c1.CALENDAR_MONTH_NUMBER mm, c1.calendar_year yyyy,
           to_date('01-'||c1.CALENDAR_MONTH_NUMBER||'-'|| c1.calendar_year,'DD-MM-YYYY') current_month,
           min(wager_amount) wager_amount_mm,
            case 
          When nvl(min(wager_amount),0) > 0 Then 'Active'
          else 'Non-Active'
        End is_active
    From  members_trans m
    LEFT OUTER JOIN calendar c1 on m.activity_date = c1.calendar_date 
    GROUP BY m.member_Id, m.ACTIVITY_YEAR_MONTH ,  c1.CALENDAR_MONTH_NUMBER , c1.calendar_year 
    )
    ,
    analysis  as
    (
    select  c.Member_ID, c.yyyymm, c.mm ,c.wager_amount_mm , is_active,
          min(c.yyyymm) OVER ( PARTITION by c.member_id )  first_month_of_trans,
          max(c.yyyymm) OVER ( PARTITION by c.member_id ) last_moth_of_trans,
        lag(current_month)  OVER ( PARTITION by c.member_id order by c.MEMBER_ID,c.yyyymm) AS prior_month,
        c.current_month current_month,
        lead(current_month)  OVER ( PARTITION by c.member_id order by c.MEMBER_ID,c.yyyymm) AS next_month,
        c.yyyy - lag(c.yyyy)  OVER ( PARTITION by c.member_id order by c.MEMBER_ID,c.yyyy) AS last_year,
        lag(c.is_active)  OVER ( PARTITION by c.member_id order by c.MEMBER_ID,c.yyyymm) AS prior_month_is_active  
    From monthly_calendar c
    Order by c.Member_ID, c.yyyymm, c.mm 
    )
    Select a.MEMBER_ID,
          a.yyyymm CALENDAR_YEAR_MONTH,
          a.is_active, a.prior_month_is_active ,
    case 
     When a.prior_month is Null then 'New'
     When  round(Months_between(a.current_month , a.prior_month)) = 1 and (a.prior_month_is_active =  'Active' and is_active = 'Active') then  'Retained'
     When   round(Months_between(a.current_month , a.prior_month)) = 1 and (a.prior_month_is_active =  'Active' and is_active = 'Non-Active') then  'UnRetained'
      When ( round(Months_between(a.current_month , a.prior_month)) = 2)  and a.prior_month_is_active = 'Active' then  'Retained'
      When ( round(Months_between(a.current_month , a.prior_month)) = 2) and (a.prior_month_is_active <>  'Active' and is_active = 'Active')  then  'Reactivated'
      when (a.prior_month_is_active = 'Active' and is_active = 'Active') then 'Reactivated'
      else 'Lapsed'
    End MEMBER_LIFECYCLE_STATUS,
     abs(round(Months_between(a.current_month , a.prior_month)))  Lapsed_months,
     current_month, prior_month,next_month
    from analysis a
    """
    if p_memberid is not None:
        analysis_sql = "{}{}{}".format(analysis_sql,"Where member_id = ",p_memberid)
    analysis_df = pd.read_sql(analysis_sql, db.db_connection)
    print(analysis_df.head(10))
    return analysis_df

def ingest_test_data(p_memberid:int,
                     p_gameid:int,
                     p_activitydate:date,
                     p_wageramount:float,
                     p_numberofwages:int,
                     p_winamount:float,
                     p_activityyearmonth:int,
                     p_banktypeid:int):
    rows = [(p_activitydate,p_memberid,p_gameid,p_wageramount,p_numberofwages,p_winamount,p_activityyearmonth,p_banktypeid)]
    print(rows)
    # delete rows before inserting
    try:
        with db.db_connection.cursor() as cur:
            cur.execute('delete REVENUE_ANALYSIS where member_id = :1 and  game_id = :2 and activity_date = :3',[p_memberid,p_gameid,p_activitydate])
            db.db_connection.commit()
    except Exception as ex:
        print(ex)
    f_insert_revenue(p_rows=rows)
    print('Rows Inserted, please ensure you have an entry in calendar')

