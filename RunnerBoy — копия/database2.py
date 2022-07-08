import sqlite3
import pygame
import sys

db = sqlite3.connect('RunnerBoy.db')

sql = db.cursor()

sql.execute('''CREATE TABLE if not exists users(name TEXT, score BIGINT)''')

db.commit()
users_name = input('Enter name: ')


sql.execute('SELECT name, score FROM users')
if sql.fetchone() is None:
    sql.execute('INSERT INTO users VALUES(?,?)', (users_name,0))
    db.commit()
print ('User complete')




