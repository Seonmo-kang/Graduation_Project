#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

id = input("삭제할 계정의 ID : ")
password = input("비밀번호 입력 : ")#비밀번호 확인
print("정말", id, "계정을 삭제하시려면 y를 입력해주세요 : ")
check = input()

if (check == 'y' or check == "Y"):

    conn = sqlite3.connect("user.db")
    cur = conn.cursor()
    cur.execute("delete from user where id=?", (id,))
    conn.commit()

    print("%s 계정이 삭제되었습니다." %id)


    conn.close()