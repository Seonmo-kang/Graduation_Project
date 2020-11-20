import sqlite3

conn = sqlite3.connect("user.db")

cur = conn.cursor()
cur.execute("create table user(id text, password text)")


conn.close()