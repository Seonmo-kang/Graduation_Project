#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

def dbInsert():

    conn = sqlite3.connect("user.db")

    cur = conn.cursor()

    while True:
        id = input("ID 입력 : ") #필요없을것 같지만 혹시 모르니 중복체크

        cur.execute("Select id from user where id = ?", (id,))
        result = cur.fetchall()
        
        if result == []:
            break
        
        else:
            if result[0][0] == id:
                print("이미 사용중인 ID입니다.")

    while True:
        password = input("비밀번호 입력 : ")
        chkpassword = input("비밀번호 확인 : ")

        if password != chkpassword:
            print("비밀번호가 일치하지 않습니다.")
        else:
            break

    cur.execute("insert into user values (?, ?)", (id, password))
    conn.commit()


    conn.close()

    print("%s 계정이 생성되었습니다." %id)
    
dbInsert()