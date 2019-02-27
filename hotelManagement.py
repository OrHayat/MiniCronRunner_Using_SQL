import sqlite3
import sys
import os

unique_id=1

def main(args):
    DBExist=os.path.isfile('cronhoteldb.db')
    if(not(DBExist)):
        conn = sqlite3.connect('cronhoteldb.db')
        with conn:
            conn.text_factory=bytes
            cursor=conn.cursor()
            create_tables(cursor)
            my_file=open(args[1],'r')
            line=my_file.readline()
            while line != "":
                line=line.strip('\n')
                string=line.split(',')
                insert_line(cursor,string)
                line = my_file.readline()
            


def print_db(cursor):
    list_TaskTime = cursor.execute("""SELECT * FROM Tasks """)
    x = list_TaskTime.fetchall()
    for t in x:
        print t
    list_TaskTime=cursor.execute("""SELECT * FROM TaskTimes """)
    x=list_TaskTime.fetchall()
    for t in x:
         print t

    list_TaskTime=cursor.execute("""SELECT * FROM Rooms """)
    x=list_TaskTime.fetchall()
    for t in x:
         print t
    list_TaskTime=cursor.execute("""SELECT * FROM Residents """)
    x=list_TaskTime.fetchall()
    for t in x:
         print t





def insert_line(cursor,string):
    if (string[0] == 'room'):
        insert_room(cursor,string)#add to rooms,if resident exsist enter into residnets
    elif(string[0]=='breakfast'or string[0]=='clean'or string[0]=='wakeup'):#insert into task times with new id,insert into tasks.
        insert_task(cursor,string)

def insert_task(cursor,string):
    global unique_id

    if(string[0]=='clean'):
        name = string[0]  # clean
        param = 0
        interval = string[1]
        times = string[2]
        cursor.execute("""INSERT INTO TaskTimes (TaskId,DoEvery,NumTimes) VALUES (?,?,?) """
                       ,[unique_id,interval,times])

        cursor.execute("""INSERT INTO Tasks (TaskId,TaskName,Parameter) VALUES (?,?,?) """
                       ,[unique_id,name,param])
    elif(string[0]=='breakfast' or string[0]=='wakeup'):
        name = string[0]  # clean
        interval = string[1]
        room = string[2]
        times = string[3]
        cursor.execute("""INSERT INTO TaskTimes (TaskId,DoEvery,NumTimes) VALUES (?,?,?) """
                       , [unique_id, interval, times])

        cursor.execute("""INSERT INTO Tasks (TaskId,TaskName,Parameter) VALUES (?,?,?) """
                       , [unique_id, name, room])
    unique_id = unique_id + 1


def insert_room(corsur,string):
    if(len(string)==2):        #insert into rooms only
        corsur.execute("""
          INSERT INTO Rooms (RoomNumber) VALUES (?)
        """, [string[1]])
    if(len(string)==4):
        corsur.execute("""
                INSERT INTO Rooms (RoomNumber) VALUES (?)
              """, [string[1]])
        #inserted into room insert into resident
        corsur.execute("""
          INSERT INTO Residents (RoomNumber,FirstName,LastName) VALUES (?,?,?)
        """, [string[1],string[2],string[3]]
                       )









def create_tables(cursor):
    cursor.executescript("""
            CREATE TABLE TaskTimes (
                TaskId   integer PRIMARY KEY NOT NULL,
                DoEvery  integer NOT NULL,
                NumTimes integer NOT NULL
            );
            CREATE TABLE Tasks (
                TaskId    integer     NOT NULL REFERENCES TaskTimes(TaskId),
                TaskName  text    NOT NULL,
                Parameter integer
            );

            CREATE TABLE Rooms (
                RoomNumber   integer    PRIMARY KEY NOT NULL
            );
             CREATE TABLE Residents (
            RoomNumber    integer     NOT NULL REFERENCES Rooms(RoomNumber),
            FirstName     text    NOT NULL,
            LastName      text    NOT NULL
            );
         """)


def close_db(conn):
    conn.commit()
    conn.close()
if __name__=='__main__':
    main(sys.argv)
