import sqlite3
import sys
import os
import time
import hotelWorker

def main(args):
    DBExist=os.path.isfile('cronhoteldb.db')
    if(not DBExist):
        sys.exit()
    conn = sqlite3.connect('cronhoteldb.db')
    time_start = time.time()
    cursor = conn.cursor()
    with conn:
        list=cursor.execute("""SELECT Tasks.TaskId,Tasks.TaskName,Tasks.Parameter,TaskTimes.DoEvery FROM TaskTimes INNER JOIN Tasks ON Tasks.TaskId=TaskTimes.TaskId
        WHERE TaskTimes.NumTimes>0""")
        tasklist=list.fetchall()
        tasksToDo=[]
        for x in tasklist:
            time_q=hotelWorker.dohoteltask(x[1],x[2])+x[3]
            tasksToDo.append([x[0] , time_q])
            update(conn, x[0])

        while (DBExist and tasklist is not None and len(tasklist) > 0):
            list = cursor.execute("""SELECT Tasks.TaskId,Tasks.TaskName,Tasks.Parameter,TaskTimes.DoEvery FROM TaskTimes INNER JOIN Tasks ON Tasks.TaskId=TaskTimes.TaskId
            WHERE TaskTimes.NumTimes>0""")
            tasklist = list.fetchall()
            for x in tasklist:
                for t in tasksToDo:
                    if(t[0]==x[0]):
                        task=t
                if (time.time() - task[1] >= 0):
                    time_q = hotelWorker.dohoteltask(x[1], x[2]) + x[3]
                    tasksToDo.append([x[0], time_q])
                    update(conn, x[0])

            DBExist = os.path.isfile('cronhoteldb.db')


def update(conn,Task_id):
    NUMTIMES=conn.execute("""SELECT TaskTimes.NumTimes  FROM TaskTimes  WHERE TaskTimes.TaskId=(?)""",(Task_id,))
    x=NUMTIMES.fetchone()
    y=x[0]-1
    tmp=(y,Task_id)
    conn.execute("""UPDATE TaskTimes SET NumTimes=(?) WHERE TaskTimes.TaskId=(?) """,tmp)
    conn.commit()



if __name__=='__main__':
    main(sys.argv)
