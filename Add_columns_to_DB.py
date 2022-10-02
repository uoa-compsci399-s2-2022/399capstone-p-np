import sqlite3

try:
    conn=sqlite3.connect("399courses.db")
    sql=""""ALTER TABLE majorRequirements
    ADD 200_LEVEL_POINTS INT DEFAULT 180
    ADD 300_LEVEL_POINTS INT DEFAULT 75
    ADD 300_LEVEL_POINTS_MAJOR_SPECIFIC INT DEFAULT 45
    ADD CAPSTONE_COURSE_NUMBER INT DEFAULT 399"""
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print("Altering OK")
    cursor.close()
except sqlite3.Error as e:
    print("Error while Altering",e)
finally:
    if(conn):
        conn.close()
        print("Connection Closed")
