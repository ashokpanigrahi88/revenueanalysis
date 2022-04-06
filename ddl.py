import db

def ddl(p_ddl):
    cur = db.db_connection.cursor()
    try:
        print(p_ddl)
        cur.execute(p_ddl)
    except Exception as ex:
        print(ex)

def create_tables():
    ddl("""CREATE TABLE CALENDAR
        (
        CALENDAR_DATE           DATE NOT NULL,
        CALENDAR_YEAR           INTEGER NOT NULL,
        CALENDAR_MONTH_NUMBER   INTEGER NOT NULL,
        CALENDAR_MONTH_NAME     VARCHAR(100),
        CALENDAR_DAY_OF_MONTH   INTEGER NOT NULL,
        CALENDAR_DAY_OF_WEEK    INTEGER NOT NULL,
        CALENDAR_DAY_NAME       VARCHAR(100),
        CALENDAR_YEAR_MONTH     INTEGER NOT NULL
        )
         """)
    ddl("""CREATE TABLE REVENUE_ANALYSIS
            (
            ACTIVITY_DATE       DATE NOT NULL,
            MEMBER_ID           INTEGER NOT NULL,
            GAME_ID             SMALLINT NOT NULL,
            WAGER_AMOUNT        REAL NOT NULL,
            NUMBER_OF_WAGERS    INTEGER NOT NULL,
            WIN_AMOUNT          REAL NOT NULL,
            ACTIVITY_YEAR_MONTH INTEGER NOT NULL,
            BANK_TYPE_ID        SMALLINT DEFAULT 0 NOT NULL
            )""")

def create_indexes():
    ddl("""Create  unique index  member_active_idx on REVENUE_ANALYSIS(ACTIVITY_DATE,member_id,game_id)
        """)
    ddl("""Create unique index  calendar_date_idx on calendar(calendar_date)""")