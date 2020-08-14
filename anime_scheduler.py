from tkinter import *
from datetime import datetime
from tkinter.font import Font
from PIL import ImageTk,Image
import random
import sqlite3
import time
import pyglet
pyglet.font.add_file('fonts/MonFnt13.ttf')
pyglet.font.add_file('fonts/MonFnt13.ttf')
pyglet.font.add_file('fonts/MonFnt14.ttf')
numList = []
root = Tk()
timerOnImage = PhotoImage(file = "TimerOn.png")
timerOffImage = PhotoImage(file = "TimerOff.png")
now = datetime.now()
releaseDay = 0
releaseHour = 0
leftDay = 0
leftHour = 0
count = 0.3
counter = []
shit = 0
gggg = 0
leftSecondList = []
leftMinuteList = []
leftDayList = []
leftHourList = []
animeList = []
animeDatabase = []
animeSorted = []
animeDatabaseSorted = []
databaseID = []
timers = []
timeColor = 8
freshStart = TRUE
day = now.strftime("%d")
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")
times = []
i = 0
deleteButtons =[]
animeNamesForDelete = []
frameForDelete = []
buttonColor = 0
hours = []
sortedArray = []
sortedIndex = []
frameColor = 9
def partition(arr,low,high): 
    m = ( low-1 )         # index of smaller element 
    pivot = arr[high][2]     # pivot 
    for j in range(low , high): 
        # If current element is smaller than the pivot 
        if   arr[j][2] < pivot: 
            # increment index of smaller element 
            m = m+1 
            arr[m],arr[j] = arr[j],arr[m]
    arr[m+1],arr[high] = arr[high],arr[m+1] 
    return ( m+1 ) 
def quickSort(arr,low,high): 
    if low < high: 
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high)
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)
def destroy():
    global i
    global count
    global timeColor
    global frameColor
    placeholder = len(animeList)
    for gg in range(placeholder):
        animeList[gg].destroy()
        #changeIDFromDatabase()
        animeNamesForDelete[gg].destroy()
        frameForDelete[gg].destroy()
        deleteButtons[gg].destroy()
        i-=1
        count-=0.1
        timeColor+=1
        frameColor+=1
    deleteButtons.clear()
    timers.clear()
    leftSecondList.clear()
    leftMinuteList.clear()
    leftDayList.clear()
    leftHourList.clear()
    animeList.clear()
    animeNamesForDelete.clear()
    frameForDelete.clear()
    counter.clear()

def sorting():
    destroy()
    quickSort(animeDatabaseSorted,0,len(animeDatabaseSorted)-1)
    build(animeDatabaseSorted)
    
def deleteLabel():
    for k in range(len(deleteButtons)):
        deleteButtons[k].configure(command = lambda k = k:[animeList[k].destroy(),changeIDFromDatabase(),animeNamesForDelete[k].destroy(),timers[k].destroy(),frameForDelete[k].destroy(),deleteButtons[k].destroy(),moveLabelsAfterDelete(animeNamesForDelete,animeList,deleteButtons,frameForDelete,counter,k),deleteLabel()])

def moveLabelsAfterDelete(name,time,delete,box,place,current):
    global i
    global count
    global frameColor
    global timeColor
    frameColor+=1
    timeColor+=1
    x = 0
    fuck = len(animeList)-1
    for l in range(current+1,len(animeList)):
        x+=1
        box[l].place(relx=0.26,rely=place[l-1],relwidth=0.47,relheight=0.08,)
        time[l].place(relx=0.75,rely=place[l-1],relwidth=0.17,relheight=0.08,)
        delete[l].place(relx=0.93,rely=place[l-1]+0.02,relwidth=0.04,relheight=0.04,)
        timers[l].place(relx=0.2,rely=place[l-1]-0.01,relwidth=0.05,relheight=0.1)
        box[fuck].config(bg='#36'+str(frameColor+x)+'eff')
        time[fuck].config(bg='#ff'+ str(timeColor+x)+'736')
        animeNamesForDelete[fuck].config(bg='#36'+str(frameColor+x)+'eff')
        fuck-=1
    timers.pop(current)
    animeDatabaseSorted.pop(current)
    deleteButtons.pop(current)
    leftSecondList.pop(current)
    leftMinuteList.pop(current)
    leftDayList.pop(current)
    leftHourList.pop(current)
    animeList.pop(current)
    animeNamesForDelete.pop(current)
    frameForDelete.pop(current)
    counter.pop()
    i-=1
    count-=0.1
    conn = sqlite3.connect('anime_scheduler.db')
    c = conn.cursor()
    c.execute("DELETE FROM animes WHERE id = ?;",[current+1],)
    conn.commit()
    conn.close()
def changeIDFromDatabase():
    conn = sqlite3.connect('anime_scheduler.db')
    c = conn.cursor()
    c.execute("SELECT id FROM animes;")
    databaseID = list(c.fetchall())
    placeHolderCounter = 0
    for idNumber in databaseID:
        placeHolderCounter+=1
        c.execute("UPDATE animes SET id = ? WHERE id = ?;",(placeHolderCounter,idNumber[0]))
    conn.commit()
    conn.close()
def resetTimer(num,sub):
    numList.append(num)
    nextRelease = int(day) + 7 - abs(sub)
    conn = sqlite3.connect('anime_scheduler.db')
    c = conn.cursor()
    c.execute("UPDATE animes SET fday = ? WHERE id = ?;",(nextRelease,num+1,))
    timers[num].config(image=timerOnImage)
    conn.commit()
    conn.close()
def addAnime():
    global i
    global count
    global leftDay
    global leftHour
    global releaseTime
    global frameColor
    global timeColor
    frame = Frame(root,bg='#36'+str(frameColor)+'eff')
    frameForDelete.append(frame)
    anime = Label(frame,text=animeName.get(),bg='#36'+str(frameColor)+'eff',font=("MonFnt13",24),fg='BLACK')
    animeNamesForDelete.append(anime)
    releaseTime = Label(root,text=str(leftDay)+':'+str(abs(leftHour)) +':'+ str(minute)+':'+ str(second),bg='#ff'+ str(timeColor)+'736',font=("MonFnt13",24),fg='BLACK',)
    animeList.append(releaseTime)
    leftMinuteList.append(59)
    leftSecondList.append(59)
    leftDayList.append(int(animeDay.get()))
    leftHourList.append(int(animeHour.get()))
    timerOn = Label(root,image = timerOffImage,)
    timers.append(timerOn)
    timerOn.place(relx=0.2,rely=count-0.01,relwidth=0.05,relheight=0.1)
    anime.pack(padx = 20, side = LEFT)
    frame.place(relx=0.26,rely=count,relwidth=0.47,relheight=0.08,)
    releaseTime.place(relx=0.75,rely=count,relwidth=0.17,relheight=0.08,)
    buttonDelete = Button(root,text="X",font=("Arial",20),bg='RED',fg='WHITE')
    deleteButtons.append(buttonDelete)
    buttonDelete.place(relx=0.93,rely=count+0.02,relwidth=0.04,relheight=0.04,)
    hourDB = animeHour.get()
    dayDB = animeDay.get()
    dayDB = int(dayDB)
    hourDB = int(hour) + int(hourDB)
    if int(hourDB) >= 24:
        while hourDB >= 24:
            hourDB-=24
            dayDB+=1
    dayDB =  int(day) + int(dayDB)
    animeDatabaseSorted.append([i,animeName.get(),dayDB,hourDB,59])
    deleteLabel()
    counter.append(count)
    count+=0.1
    frameColor-=1
    timeColor-=1
    if i == 0:
        i+=1
        countDownZero()
    elif i == 1:
        i+=1
        countDownOne()
    elif i == 2:
        i+=1
        countDownTwo()
    elif i == 3:
        i+=1
        countDownThree()
    elif i == 4:
        i+=1
        countDownFour()
    elif i == 5:
        i+=1
        countDownFive()
    elif i == 6:
        i+=1
        countDownSix()
def countDownZero():
    if len(animeList) >= 0:
        if (leftDayList[0] <= 0 and leftHourList[0] <= 0)or leftDayList[0] <=-1 :
            resetTimer(0,leftDayList[0])
            leftDayList[0] = 6 - - abs(leftDayList[0])
            leftHourList[0] = 23
            leftMinuteList[0] = 59
            leftSecondList[0] = 59
        elif leftSecondList[0] == 0:
            leftSecondList[0] = 60
            leftMinuteList[0] -= 1
        elif leftMinuteList[0] == 0:
            leftMinuteList[0] = 59
            leftHourList[0] -= 1
        elif leftHourList[0] == 0:
            leftHourList[0] = 23
            leftDayList[0] -= 1
        leftSecondList[0] -= 1
        animeList[0].config(text=str(leftDayList[0])+':'+str(abs(leftHourList[0])) +':'+ str(leftMinuteList[0])+':'+ str(leftSecondList[0]))
        animeList[0].after(1000,countDownZero)
def countDownOne():
    if len(animeList) >= 1:
        print(leftDayList[1])
        if (leftDayList[1] <= 0 and leftHourList[1] <= 0)or leftDayList[1] <= -1:
            resetTimer(1,leftDayList[1])
            leftDayList[1] = 6 - abs(leftDayList[1])
            leftHourList[1] = 23
            leftMinuteList[1] = 59
            leftSecondList[1] = 59
        elif leftSecondList[1] == 0:
            leftSecondList[1] = 60
            leftMinuteList[1] -= 1
        elif leftMinuteList[1] == 0:
            leftMinuteList[1] = 59
            leftHourList[1] -= 1
        elif leftHourList[1] == 0:
            leftHourList[1] = 23
            leftDayList[1] -= 1
        
        leftSecondList[1] -= 1
        animeList[1].config(text=str(leftDayList[1])+':'+str(abs(leftHourList[1])) +':'+ str(leftMinuteList[1])+':'+ str(leftSecondList[1]))
        animeList[1].after(1000,countDownOne)
def countDownTwo():
    if len(animeList) > 2:
        if (leftDayList[2] <= 0 and leftHourList[2] <= 0) or leftDayList[2] <= -1:
            resetTimer(2,leftDayList[2])
            leftDayList[2] = 6 - abs(leftDayList[2])
            leftHourList[2] = 23
            leftMinuteList[2] = 59
            leftSecondList[2] = 59
        elif leftSecondList[2] == 0:
            leftSecondList[2] = 60
            leftMinuteList[2] -= 1
        elif leftMinuteList[2] == 0:
            leftMinuteList[2] = 59
            leftHourList[2] -= 1
        elif leftHourList[2] == 0:
            leftHourList[2] = 23
            leftDayList[2] -= 1
        leftSecondList[2] -= 1
        animeList[2].config(text=str(leftDayList[2])+':'+str(abs(leftHourList[2])) +':'+ str(leftMinuteList[2])+':'+ str(leftSecondList[2]))
        animeList[2].after(1000,countDownTwo)
def countDownThree():
    if len(animeList) > 3:
        if (leftDayList[3] <= 0 and leftHourList[3] <= 0)or leftDayList[3] <= -1:
            resetTimer(3,leftDayList[3])
            leftDayList[3] = 6 - abs(leftDayList[3])
            leftHourList[3] = 23
            leftMinuteList[3] = 59
            leftSecondList[3] = 59
        elif leftSecondList[3] == 0:
            leftSecondList[3] = 60
            leftMinuteList[3] -= 1
        elif leftMinuteList[3] == 0:
            leftMinuteList[3] = 59
            leftHourList[3] -= 1
        elif leftHourList[3] == 0:
            leftHourList[3] = 23
            leftDayList[3] -= 1
        leftSecondList[3] -= 1
        animeList[3].config(text=str(leftDayList[3])+':'+str(abs(leftHourList[3])) +':'+ str(leftMinuteList[3])+':'+ str(leftSecondList[3]))
        animeList[3].after(1000,countDownThree)
def countDownFour():
    if len(animeList) > 4:
        if (leftDayList[4] <= 0 and leftHourList[4] <= 0)or leftDayList[4] <= -1:
            resetTimer(4,leftDayList[4])
            leftDayList[4] = 6 - abs(leftDayList[4])
            leftHourList[4] = 23
            leftMinuteList[4] = 59
            leftSecondList[4] = 59
        elif leftSecondList[4] == 0:
            leftSecondList[4] = 60
            leftMinuteList[4] -= 1
        elif leftMinuteList[4] == 0:
            leftMinuteList[4] = 59
            leftHourList[4] -= 1
        elif leftHourList[4] == 0:
            leftHourList[4] = 23
            leftDayList[4] -= 1
        leftSecondList[4] -= 1
        animeList[4].config(text=str(leftDayList[4])+':'+str(abs(leftHourList[4])) +':'+ str(leftMinuteList[4])+':'+ str(leftSecondList[4]))
        animeList[4].after(1000,countDownFour)
def countDownFive():
    if len(animeList) > 5:
        if (leftDayList[5] <= 0 and leftHourList[5] <= 0)or leftDayList[5] <= -1:
            resetTimer(5,leftDayList[5])
            leftDayList[5] = 6 - abs(leftDayList[5])
            leftHourList[5] = 23
            leftMinuteList[5] = 59
            leftSecondList[5] = 59
        elif leftSecondList[5] == 0:
            leftSecondList[5] = 60
            leftMinuteList[5] -= 1
        elif leftMinuteList[5] == 0:
            leftMinuteList[5] = 59
            leftHourList[5] -= 1
        elif leftHourList[5] == 0:
            leftHourList[5] = 23
            leftDayList[5] -= 1
        leftSecondList[5] -= 1
        animeList[5].config(text=str(leftDayList[5])+':'+str(abs(leftHourList[5])) +':'+ str(leftMinuteList[5])+':'+ str(leftSecondList[5]))
        animeList[5].after(1000,countDownFive)
def countDownSix():
    if len(animeList) > 6:
        if (leftDayList[6] <= 0 and leftHourList[6] <= 0) or leftDayList[6] <= -1:
            resetTimer(6,leftDayList[6])
            leftDayList[6] = 6 - abs(leftDayList[6])
            leftHourList[6] = 23
            leftMinuteList[6] = 59
            leftSecondList[6] = 59
        elif leftSecondList[6] == 0:
            leftSecondList[6] = 60
            leftMinuteList[6] -= 1
        elif leftMinuteList[6] == 0:
            leftMinuteList[6] = 59
            leftHourList[6] -= 1
        elif leftHourList[6] == 0:
            leftHourList[6] = 23
            leftDayList[6] -= 1
        leftSecondList[6] -= 1
        animeList[6].config(text=str(leftDayList[6])+':'+str(abs(leftHourList[6])) +':'+ str(leftMinuteList[6])+':'+ str(leftSecondList[6]))
        animeList[6].after(1000,countDownSix)
def writeToDatabase(nameDB,hourDB,dayDB):
    conn = sqlite3.connect('anime_scheduler.db')
    c = conn.cursor()
    dayDB = int(dayDB)
    hourDB = int(hour) + int(hourDB)
    if int(hourDB) >= 24:
        while hourDB >= 24:
            hourDB-=24
            dayDB+=1
    dayDB =  int(day) + int(dayDB)
    try:
        c.execute("""CREATE TABLE animes(id integer PRIMARY KEY,fname text,fday integer,fhour integer,fminute integer)""")
    except:
        pass
    c.execute("INSERT INTO animes (fname,fday,fhour,fminute) VALUES(?,?,?,?);",(nameDB,dayDB,hourDB,59))
    conn.commit()
    conn.close()
def readFromDatabase():
    conn = sqlite3.connect('anime_scheduler.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM animes")
        for row in c.fetchall():
            animeDatabase.append(list(row))
    except:
        pass
    conn.commit()
    conn.close()
root.title("Mykes")
root.iconbitmap("6head.ico")
root.geometry("1280x720")
root.resizable(width=False,height=False)
bigFont = Font(family="MonFnt14", size=25)
searchFont = Font(family="Arial", size=20,)
smallFont = Font(family="MonFnt13", size=18)
animeFont = Font(family="MonFnt13", size=24)



animeHour = Entry(root,width=10,font=("Arial",20),fg='BLACK',justify=CENTER)
animeDay = Entry(root,width=10,font=("Arial",20),fg='BLACK',justify=CENTER)
animeName = Entry(root,width=10,font=("Arial",20),fg='BLACK',justify=CENTER)
nameLabel = Label(root,text="ANIME TITLE:",font=("MonFnt13",18),fg='BLACK')
timeLabel = Label(root,text="DAY & HOUR:",font=("MonFnt13",18),fg='BLACK')
search = Entry(root,width=10,font=("Arial",20),fg='BLACK')
search.insert(1,'Search...')
search.bind("<FocusIn>", lambda args: search.delete('0', 'end'))
readFromDatabase()
# RECONSTRUCT
def build(arr):
    global i
    global count
    global frameColor
    global timeColor
    xD = 0
    if len(arr) != 0:
        for row in arr:
            if row[3] < int(hour):      # 14 - 12 = 2            2 - 1 = 1
                row[3] += 24
                row[2] -= 1
            elif row[4] < int(minute):  # 1 - 22 = 21       24+1 = 25 - 22 = 3
                row[4]+=60
                row[3] -= 1
            leftDayList.append(row[2]-int(day)) 
            leftHourList.append(row[3]-int(hour)) 
            leftMinuteList.append(abs(row[4] - (int(minute) + random.randint(1,20))))
            leftSecondList.append(random.randint(10,59))
            frame = Frame(root,bg='#36'+str(frameColor)+'eff')
            frameForDelete.append(frame)
            timerOn = Label(root,image = timerOffImage,)
            if int(day) == row[2] and (row[3]-int(hour)) == 0:
                timerOn.config(image=timerOnImage)
            timers.append(timerOn)
            timerOn.place(relx=0.2,rely=count-0.01,relwidth=0.05,relheight=0.1)
            anime = Label(frame,text=row[1],bg='#36'+str(frameColor)+'eff',font=("MonFnt13",24),fg='BLACK')
            animeNamesForDelete.append(anime)
            releaseTime = Label(root,text=str(row[2])+':'+str(row[3]) +':'+ str(row[4])+':'+ str(random.randint(1,57)),bg='#ff'+ str(timeColor) +'736',font=("MonFnt13",24),fg='BLACK',)
            animeList.append(releaseTime)
            anime.pack(padx = 20, side = LEFT)
            frame.place(relx=0.26,rely=count,relwidth=0.47,relheight=0.08,)
            releaseTime.place(relx=0.75,rely=count,relwidth=0.17,relheight=0.08,)
            buttonDelete = Button(root,text="X",font=("Arial",20),bg='RED',fg='WHITE')
            buttonDelete.place(relx=0.93,rely=count+0.02,relwidth=0.04,relheight=0.04,)
            deleteButtons.append(buttonDelete)
            counter.append(count)
            count+=0.1
            frameColor-=1
            timeColor-=1
            xD+=1
            if i == 0:
                i+=1
                countDownZero()
            elif i == 1:
                i+=1
                countDownOne()
            elif i == 2:
                i+=1
                countDownTwo()
            elif i == 3:
                i+=1
                countDownThree()
            elif i == 4:
                i+=1
                countDownFour()
            elif i == 5:
                i+=1
                countDownFive()
            elif i == 6:
                i+=1
                countDownSix()
        deleteLabel()
for data in animeDatabase:
    animeDatabaseSorted.append(list(data))
if len(animeDatabase) != 0:
    build(animeDatabaseSorted)
    
buttonAdd = Button(root,text="ADD",compound=CENTER,command=lambda:[writeToDatabase(animeName.get(),animeHour.get(),animeDay.get()),addAnime(),],font=("MonFnt14", 25),bg='#21ff56',fg='BLACK')
buttonSort = Button(root,command = lambda:sorting(),text="SORT",font=("MonFnt13",24),bg='#c96bff',fg='BLACK')
buttonSort.place(relx=0.88,rely=0.07,relwidth=0.08,relheight=0.08,)
search.place(relx=0.26,rely=0.06,relwidth=0.5,relheight=0.06,)
buttonAdd.place(relx=0.02,rely=0.27,relwidth=0.16,relheight=0.13,)
animeName.place(relx=0.02,rely=0.07,relwidth=0.16,relheight=0.06,)
nameLabel.place(relx=0.02,rely=0.02,relwidth=0.16,relheight=0.05,)
timeLabel.place(relx=0.02,rely=0.13,relwidth=0.16,relheight=0.05,)
animeDay.place(relx=0.02,rely=0.18,relwidth=0.07,relheight=0.06,)
animeHour.place(relx=0.11,rely=0.18,relwidth=0.07,relheight=0.06,)


root.mainloop()