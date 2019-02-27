
import sys
import time
import os
import sqlite3 as lite

def parseLineWords(words, cursor):
    cur = cursor
    cur.execute("SELECT max(TaskId) FROM Tasks")
    curTaskId = cur.fetchone()
    if curTaskId[0] is None:
        curTaskId = -1
    else:
        curTaskId = curTaskId[0]
    curTaskId += 1
    if words[0] == 'room':
        roomNumber = words[1]
        cur.execute("INSERT INTO Rooms VALUES (?)", (roomNumber,))
        if (len(words) > 2):
            firstName = words[2]
            lastName = words[3]
            cur.execute("INSERT INTO Residents VALUES(?, ?, ?)", (roomNumber, firstName, lastName))
    elif words[0] == 'wakeup':
        cur.execute("INSERT INTO TaskTimes VALUES(?, ?, ?)", (curTaskId, words[1], words[3]))
        cur.execute("INSERT INTO Tasks VALUES(?,?,?)", (curTaskId, 'wakeup', words[2]))
    elif words[0] == 'clean':
        cur.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (curTaskId, words[1], words[2]))
        cur.execute("INSERT INTO Tasks VALUES(?,?,?)", (curTaskId, 'clean', 0))
    elif words[0] == 'breakfast':
        cur.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (curTaskId, words[1], words[3]))
        cur.execute("INSERT INTO Tasks VALUES(?,?,?)", (curTaskId, 'breakfast', words[2]))



def createTables(cursor):
    cursor.execute("CREATE TABLE TaskTimes(TaskId integer PRIMARY KEY NOT NULL, DoEvery integer NOT NULL, NumTimes integer NOT NULL)")
    cursor.execute("CREATE TABLE Tasks(TaskId integer NOT NULL REFERENCES TaskTimes(TaskId), TaskName text NOT NULL, Parameter integer)")
    cursor.execute("CREATE TABLE Rooms(RoomNumber integer PRIMARY KEY NOT NULL)")
    cursor.execute("CREATE TABLE Residents(RoomNumber integer NOT NULL REFERENCES Rooms(RoomNumber), FirstName text NOT NULL, LastName text NOT NULL)")

def buildHotelDb(inputFile, cursor):
    createTables(cursor)
    for line in inputFile:
        currentWords = line.split(',')
        parseLineWords(currentWords, cursor)

def main(args):
    firstRun = False
    if not os.path.isfile('cronhoteldb.db'):
        firstRun = True
    if firstRun == False:
        return
    con = lite.connect('cronhoteldb.db')
    with con:
        cursor = con.cursor()
        if firstRun:
            inputFileName = args[1]
            with open(inputFileName) as inf:
                buildHotelDb(inf, cursor)

if __name__ == '__main__':
    main(sys.argv)
