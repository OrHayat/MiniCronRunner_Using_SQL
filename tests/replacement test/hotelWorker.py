import time
import sqlite3 as lite

def doClean(cursor):
    query = "SELECT t1.RoomNumber FROM Rooms t1 LEFT JOIN Residents t2 ON t1.RoomNumber = t2.RoomNumber where t2.RoomNumber is NULL"
    cursor.execute(query)
    emptyRooms = cursor.fetchall()
    emptyRoomsInts = (roomtuple[0] for roomtuple in emptyRooms)
    emptyRoomsStr = ", ".join(str(num) for num in emptyRoomsInts)
    now = time.time()
    print "Rooms " + emptyRoomsStr + " were cleaned at " + str(now)
    return now


def doBreakfast(roomNum, cur):
    cur.execute("SELECT FirstName, LastName FROM Residents WHERE RoomNumber=?", (roomNum,))
    names = cur.fetchone()
    firstName = names[0]
    lastName = names[1]
    lastName = lastName.strip('\n')
    lastName = lastName.strip(' ')
    now = time.time()
    print firstName + " " + lastName + " in room " + str(roomNum) + " has been served breakfast at " + str(now)
    return now

def doWakeup(roomNum, cursor):
    cursor.execute("SELECT FirstName, LastName FROM Residents WHERE RoomNumber=?", (roomNum,))
    names = cursor.fetchone()
    firstName = names[0]
    lastName = names[1]
    lastName = lastName.strip('\n')
    lastName = lastName.strip(' ')
    now = time.time()
    print firstName + " " + lastName + " in room " + str(roomNum) + " received a wakeup call at " + str(now)
    return now

def dohoteltask(taskType, param):
    con = lite.connect('cronhoteldb.db')
    with con:
        cursor = con.cursor()
        if taskType == 'wakeup':
            return doWakeup(param, cursor)
        elif taskType == 'breakfast':
            return doBreakfast(param, cursor)
        elif taskType == 'clean':
            return doClean(cursor)