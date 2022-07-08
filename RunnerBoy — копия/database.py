import sqlite3
import pygame
import sys

db = sqlite3.connect('RunnerBoy.db')

sql = db.cursor()
global leaders
global lead
global users_score
global users_name
global complete
sql.execute("""CREATE TABLE if not exists users(name TEXT, score BIGINT)""")

db.commit()
users_name = ''
users_score=0
complete=False

leaders=sql.execute("""SELECT name, score FROM users
                        ORDER by score DESC
                        LIMIT 10""")

lead=sql.fetchall()
def add_user():
    if (sql.fetchone() is None) :
        sql.execute('INSERT INTO users VALUES(?,?)', (users_name,users_score))
        db.commit()
        print ('User complete')
        #sql.close()
    else:
        print("error")
    sql.close()

