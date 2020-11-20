#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

current_pw = input("현재 비밀번호 : ")#비밀번호 확인필요
changeto_pw = input("변경할 비밀번호 :")


conn = sqlite3.connect("user.db")

cur = conn.cursor()
cur.execute("update user set password=? where password=?", (changeto_pw, current_pw))
conn.commit()

conn.close()

print("비밀번호가 변경되었습니다.")