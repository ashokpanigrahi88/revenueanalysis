# revenueanalysis
This project is created analyse revenues 
Files :
 env.bat : Sets environment variables
 db.py : Connects to oracle database  
 ddl.py : Crates table and indexes 
 loadutils.py : Has all functions needed to load and test data 
 requirements.txt : Lists out all dependencies to execute and test the code 
 loaddata.py : Loads initial data 
 test_load.py: Has got all functions to test the functionality 
 bally_rest_api.txt : Actual code created used in Django framework to access the end point 
 Note : I have not implemented security intentionally but Token Key security is already in place i.e. 
  In view I just have to add following few lines
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
 
 How to Setup : 
 Assumption : You have a Oracle database installed
 Login to oracle database and create user: 
  create user test_db identified by TEST_DB;
  Alter user test_db default tablespace users;
  grant connect,resource to TEST_DB 
  GRANT UNLIMITED TABLESPACE TO test_db;  
  grant create any view to test_db;
  
  Go to shell/command prompt
  crate a python virtual env
  create a project directory : ballystest
  Change directory to : ballystest
  Create Virtual python env : python -m venv myenv
  Activate the environment: activate.bat 
  Install dependencies : pip install requirements.txt
  Modify env.bat file and set envionments
  invoke python and command prompt
  python <entter>
  >>>import test_load   <Which sshould connect to database>
     (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=)(PORT=1521))(CONNECT_DATA=(SID=)))
  >>> test_load.run_ddl()   -- to create table and indexes
  >>> test_load.load_and_analyse_data()  --  Loads CSV file and answers Q1 
  >>> test_load.analyse_data()    -- run any time for re-testing the data 
  >>> test_load.rest_api(p_params={})        -- to test data from my database and server , Used Django framework with a Serializer/View/Url code 
        p_params = {'member_id':<>  , 'game_id':<>, 'activity_year_month':<> OR 'activity_year_month__contains':<2017>}
  >>> test_load.insert_test_data()   -- to load pre-defined test data 
  >>> import loadutils
  >>>  loadutils.ingest_test_data(p_memberid=1004,              ---- can this module to test as you wanted 
                               p_activitydate=date(year=yy,month=mm,day=10),
                               p_gameid=890,
                               p_wageramount=1.0,
                               p_banktypeid=0,
                               p_activityyearmonth=int(str("{}{:02d}".format(yy,mm))),
                               p_numberofwages=3,
                               p_winamount=20)
  

 Not sure I know this can be improved in many areas 
  like : 
   Creating tables with more indexes , partitions 
   Load Utilities can be tuned : I have done few like Bulk / Batch  Loading
   CSV File loaded to panda with pre-defined schema to optimise the memory usage
 In real live enviorment this is a big project if you have to start from scratch
 Due to time constraints with other things in my plate I have decided to finish the development at this point 
 In case you miss out the SQL statement for Q1 here is the  statement 
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
    ---
    Also created a view for rest API
 create or replace view revenue_analysis_v
            as
            select rownum id , a.*
        FROM (
        select   member_id,game_id,activity_year_month, sum(wager_amount) wager_amount, sum(number_of_wagers) number_of_wagers, 
           sum(win_amount) win_amount
        From Revenue_analysis 
        Group by member_id,game_id,activity_year_month) a 
 ----------------------
 Q1 : Sample Output 
    MEMBER_ID  CALENDAR_YEAR_MONTH   IS_ACTIVE PRIOR_MONTH_IS_ACTIVE  ... LAPSED_MONTHS  CURRENT_MONTH PRIOR_MONTH NEXT_MONTH
0       1001               201701      Active                  None  ...           NaN     2017-01-01         NaT 2017-05-01
1       1001               201705      Active                Active  ...           4.0     2017-05-01  2017-01-01 2017-06-01
2       1001               201706      Active                Active  ...           1.0     2017-06-01  2017-05-01 2017-09-01
3       1001               201709      Active                Active  ...           3.0     2017-09-01  2017-06-01 2017-12-01
4       1001               201712      Active                Active  ...           3.0     2017-12-01  2017-09-01 2018-03-01
5       1001               201903  Non-Active                Active  ...           3.0     2018-03-01  2017-12-01        NaT
6       1002               201703      Active                  None  ...           NaN     2017-03-01         NaT 2017-04-01
7       1002               201704      Active                Active  ...           1.0     2017-04-01  2017-03-01 2017-08-01
8       1002               201708      Active                Active  ...           4.0     2017-08-01  2017-04-01 2017-09-01
9       1002               201709      Active                Active  ...           1.0     2017-09-01  2017-08-01        NaT

 Q2: Sample Output
 [{'id': 1, 'member_id': 1004, 'game_id': 890, 'activity_year_month': 201902, 'wager_amount': '1.000', 'number_of_wagers': '3.000', 'win_amount': '20.000'}, {'id': 2, 'member_id': 1001, 'game_id': 1320, 'activity_year_month': 201701, 'wager_amount': '0.200', 'number_of_wagers': '1.000', 'win_amount': '13.400'}, {'id': 3, 'member_id': 1003, 'game_id': 4326, 'activity_year_month': 201706, 'wager_amount': '1.000', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 4, 'member_id': 1001, 'game_id': 987, 'activity_year_month': 201701, 'wager_amount': '0.100', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 5, 'member_id': 1001, 'game_id': 6773, 'activity_year_month': 201706, 'wager_amount': '6.300', 'number_of_wagers': '3.000', 'win_amount': '0.000'}, {'id': 6, 'member_id': 1001, 'game_id': 7723, 'activity_year_month': 201712, 'wager_amount': '0.100', 'number_of_wagers': '1.000', 'win_amount': '16.500'}, {'id': 7, 'member_id': 1002, 'game_id': 2625, 'activity_year_month': 201703, 'wager_amount': '0.100', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 8, 'member_id': 1002, 'game_id': 2623, 'activity_year_month': 201703, 'wager_amount': '0.100', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 9, 'member_id': 1003, 'game_id': 8565, 'activity_year_month': 201707, 'wager_amount': '1.000', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 10, 'member_id': 1002, 'game_id': 6294, 'activity_year_month': 201703, 'wager_amount': '0.200', 'number_of_wagers': '1.000', 'win_amount': '43.000'}, {'id': 11, 'member_id': 1002, 'game_id': 6435, 'activity_year_month': 201708, 'wager_amount': '3.000', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 12, 'member_id': 1001, 'game_id': 1097, 'activity_year_month': 201712, 'wager_amount': '0.300', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 13, 'member_id': 1002, 'game_id': 7587, 'activity_year_month': 201704, 'wager_amount': '14.200', 'number_of_wagers': '4.000', 'win_amount': '0.000'}, {'id': 14, 'member_id': 1002, 'game_id': 5632, 'activity_year_month': 201709, 'wager_amount': '3.000', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 15, 'member_id': 1001, 'game_id': 8901, 'activity_year_month': 201903, 'wager_amount': '0.000', 'number_of_wagers': '0.000', 'win_amount': '0.000'}, {'id': 16, 'member_id': 1001, 'game_id': 1293, 'activity_year_month': 201701, 'wager_amount': '0.500', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 17, 'member_id': 1001, 'game_id': 7610, 'activity_year_month': 201705, 'wager_amount': '0.200', 'number_of_wagers': '1.000', 'win_amount': '0.200'}, {'id': 18, 'member_id': 1001, 'game_id': 2057, 'activity_year_month': 201709, 'wager_amount': '0.100', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 19, 'member_id': 1001, 'game_id': 7724, 'activity_year_month': 201712, 'wager_amount': '0.500', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 20, 'member_id': 1002, 'game_id': 7588, 'activity_year_month': 201704, 'wager_amount': '6.500', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 21, 'member_id': 1002, 'game_id': 2057, 'activity_year_month': 201704, 'wager_amount': '7.300', 'number_of_wagers': '2.000', 'win_amount': '0.000'}, {'id': 22, 'member_id': 1002, 'game_id': 7596, 'activity_year_month': 201704, 'wager_amount': '7.140', 'number_of_wagers': '2.000', 'win_amount': '7.140'}, {'id': 23, 'member_id': 1003, 'game_id': 5876, 'activity_year_month': 201706, 'wager_amount': '1.000', 'number_of_wagers': '1.000', 'win_amount': '0.000'}, {'id': 24, 'member_id': 1001, 'game_id': 2536, 'activity_year_month': 201709, 'wager_amount': '1.200', 'number_of_wagers': '2.000', 'win_amount': '0.000'}]
 ----
 >>> test_load.rest_api(p_params={'member_id':1004})
[{'id': 1, 'member_id': 1004, 'game_id': 890, 'activity_year_month': 201902, 'wager_amount': '1.000', 'number_of_wagers': '3.000', 'win_amount': '20.000'}]
 -------
 >>> test_load.rest_api(p_params={'game_id':7587})
[{'id': 13, 'member_id': 1002, 'game_id': 7587, 'activity_year_month': 201704, 'wager_amount': '14.200', 'number_of_wagers': '4.000', 'win_amount': '0.000'}]
 ------------------
 >>> test_load.rest_api(p_params={'activity_year_month__contains':2019})
[{'id': 1, 'member_id': 1004, 'game_id': 890, 'activity_year_month': 201902, 'wager_amount': '1.000', 'number_of_wagers': '3.000', 'win_amount': '20.000'}, {'id': 15, 'member_id': 1001, 'game_id': 8901, 'activity_year_month': 201903, 'wager_amount': '0.000', 'number_of_wagers': '0.000', 'win_amount': '0.000'}]
 ------------------------
>>>
   
