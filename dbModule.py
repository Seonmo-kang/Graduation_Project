import pymysql
"""
callproc 함수는 인자로 주어진 저장된 함수를 실행
close 함수는 커서를 닫음
execute 함수는 질의문을 실행하고 결과 집합을 반환
executemany 함수는 질의문을 반복해서 실행하고 결과집합을 반환
"""
class Database():
    def __init__(self):
        self.db=pymysql.connect(host='localhost',port=3306,user='iot_tester',password='adminadmin123',charset='utf8',db='mode_db')
        self.cursor=self.db.cursor(pymysql.cursors.DictCursor)
        self.d_check = True
    def excute(self,query,args=()):
        self.cursor.execute(query,args)

    def excuteOne(self,query,args=()):
        self.cursor.execute(query,args)
        row = self.cursor.fetchone()
        return row
    def excuteOne(self,query,args=()):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def show(self,name):
        #sql ="select * from custom WHERE module_name=%s",(name)
        self.cursor.execute("select * from custom WHERE module_name=%s",(name))
        while True:
            phone = self.cursor.fetchone()
            if not phone: break
            return phone
            #print(phone)

    def showAll(self):
        self.cursor.execute("SELECT * FROM custom")
        setting = self.cursor.fetchall()
        return setting

    def insert(self,args=()): # args = 6 name, l_led, m_led, g_led , window, g_window
        self.cursor.execute("insert into custom values (%s,%s,%s,%s,%s,%s)",(args[0],args[1],args[2],args[3],args[4],args[5]))
        self.db.commit()

    def check(self,name):
        self.cursor.execute("select * from custom WHERE module_name = %s",name)
        if self.cursor.fetchone():
            self.d_check=False
            return ('해당 명령어는 이미 등록되어있습니다!')
        else: return True