import sqlite3
import datetime 

class sitia_db():
    def __init__(self) -> None:
        
        db_file = "sitia.db"

        self.con = sqlite3.connect(db_file)

        self.cur = self.con.cursor()

        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='DSIA_USERS'; "

        if self.cur.execute(sql).fetchall() == []:
            self.cur.execute("CREATE TABLE DSIA_USERS (USR_ID INTEGER PRIMARY KEY AUTOINCREMENT, USR_NAME VARCHAR(15) UNIQUE, USR_PWD VARCHAR(8), USR_LAST DATETIME);")
            self.cur.execute("INSERT INTO DSIA_USERS (USR_NAME, USR_PWD, USR_LAST) VALUES('admin', 'admin', '"+str(datetime.datetime.now())+"');")

        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='DSIA_SESSION'; "
        
        if self.cur.execute(sql).fetchall() == []: self.cur.execute("CREATE TABLE DSIA_SESSION (SES_ID INTEGER PRIMARY KEY AUTOINCREMENT, SES_DATE DATETIME, SES_FILE VARCHAR, SES_IA VARCHAR(5), SES_OPT VARCHAR(5), SES_USER INTEGER);")

        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='DSIA_HISTORY'; "
        
        if self.cur.execute(sql).fetchall() == []: self.cur.execute("CREATE TABLE DSIA_HISTORY (HIS_ID INTEGER PRIMARY KEY AUTOINCREMENT, HIS_SESSION INTEGER, HIS_USER INTEGER, HIS_OBJ INTEGER, HIS_PIXELS INTEGER, HIS_STATUS VARCHAR(20), HIS_X INTEGER, HIS_Y INTEGER, HIS_SEX_0 VARCHAR(1), HIS_CONF FLOAT, HIS_SEX_F VARCHAR(1))")

        self.con.commit()

    def check_userPwd(self, usr, pwd) -> int: 

        try:
            res = self.cur.execute("SELECT USR_ID FROM DSIA_USERS WHERE USR_NAME='"+usr+"' AND USR_PWD='"+pwd+"';").fetchall()
        except sqlite3.Error as er:
            print(er)
            return -1

        if len(res)>0: return res[0][0]
        return -1

    def update_userLastLogin(self, usr) -> bool:

        try:
            self.cur.execute("UPDATE DSIA_USERS SET USR_LAST = '" + str(datetime.datetime.now()) + "'  WHERE USR_NAME='"+usr+"';")
        except sqlite3.Error as er:
            print(er)
            return False
        
        self.con.commit()

        return True

    def insert_session(self, img_file, ia_algorithm, opt_algorithm, usr_id) -> int:

        try:
            self.cur.execute("INSERT INTO DSIA_SESSION (SES_DATE, SES_FILE, SES_IA, SES_OPT, SES_USER) VALUES('"+str(datetime.datetime.now())+"', '"+img_file+"', '"+ia_algorithm+"', '"+opt_algorithm+"', "+str(usr_id)+");")
        except sqlite3.Error as er:
            print(er)
            return -1

        self.con.commit()

        try:
            res = self.cur.execute("SELECT MAX(SES_ID) FROM DSIA_SESSION;").fetchall()
        except sqlite3.Error as er:
            print(er)
            return -1
        
        return res[0][0]

    def insert_objHistory(self, ses_id, usr_id, obj_num, obj_pix, obj_status, obj_x, obj_y, obj_sex0, obj_conf, obj_sexf) -> bool:
        
        try:
            self.cur.execute("INSERT INTO DSIA_HISTORY (HIS_SESSION, HIS_USER, HIS_OBJ, HIS_PIXELS, HIS_STATUS, HIS_X, HIS_Y, HIS_SEX_0, HIS_CONF, HIS_SEX_F) VALUES ("+str(ses_id)+", "+str(usr_id)+", "+str(obj_num)+", "+str(obj_pix)+", '"+obj_status+"', "+str(obj_x)+", "+str(obj_y)+", '"+obj_sex0+"', "+str(obj_conf)+", '"+obj_sexf+"');")
        except sqlite3.Error as er:
            print(er)
            return False

        self.con.commit()
        return True

