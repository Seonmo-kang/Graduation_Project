#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect("user.db")

cur = conn.cursor()
cur.execute("select * from user")
for row in cur:
    print(row)


conn.close()