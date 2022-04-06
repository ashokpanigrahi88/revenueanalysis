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
  >>> test_load.rest_api()        -- to test data from my database and server , Used Django framework with a Serializer/View/Url code 
        p_params = {'member_id':<>  , 'game_id':<>, 
  
