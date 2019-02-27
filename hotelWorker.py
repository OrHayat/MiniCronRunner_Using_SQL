import sqlite3
import sys
import os
import time


def dohoteltask(taskname,parameter):
    DBExist=os.path.isfile('cronhoteldb.db')
    conn = sqlite3.connect('cronhoteldb.db')
    time_start = time.time()
    with conn:
        if (DBExist):
            cursor = conn.cursor()
            if (taskname == 'wakeup'):
                data_name = cursor.execute("""SELECT Residents.FirstName FROM Residents WHERE Residents.RoomNumber=(?) """,(parameter,))
                name=data_name.fetchone()
                data_last_name=cursor.execute("""SELECT Residents.LastName FROM Residents WHERE Residents.RoomNumber=(?) """,(parameter,))
                last_name=data_last_name.fetchone()
                print  str(name[0])+" "+str(last_name[0])+" in room "+str(parameter)+" recived a wakeup call at "+str(time_start)
            # do wakeup Rooms.RoomNumber
            elif (taskname == 'breakfast'):
                data_name = cursor.execute("""SELECT Residents.FirstName FROM Residents WHERE Residents.RoomNumber=(?) """,(parameter,))
                name=data_name.fetchone()
                data_last_name=cursor.execute("""SELECT Residents.LastName FROM Residents WHERE Residents.RoomNumber=(?) """,(parameter,))
                last_name=data_last_name.fetchone()
                print  str(name[0])+" "+str(last_name[0])+" in room "+str(parameter)+" has been served a breakfast at "+str(time_start)
            # do breakfast
            else:
                rooms_data=conn.execute("""SELECT Rooms.RoomNumber FROM Rooms WHERE RoomNumber NOT IN
                (SELECT Rooms.RoomNumber From Rooms INNER JOIN Residents ON Rooms.RoomNumber=Residents.RoomNumber)  ORDER BY Rooms.RoomNumber ASC """)
                rooms=""
                for room in rooms_data:
                    if(rooms==""):
                        rooms=str(room[0])
                    else:
                        rooms = rooms + ", " + str(room[0])
                print "rooms "+rooms+' were cleaned at '+str(time_start)
                #print str(rooms_data)
        conn.commit()

        return time_start
        # do cleaning