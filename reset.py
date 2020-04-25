import sqlite3

try:
    db = sqlite3.connect('database.db', check_same_thread=False)
    cursor = db.cursor()
    fh = open('db.sql', 'r')
    script = fh.read()
    cursor.executescript(script)
	
except Exception as e:
    db.rollback()
    raise e

finally:
    db.close() 