import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from threading import Thread
from random import randint
from matplotlib.animation import FuncAnimation
import csv

from tkinter import Tk, Menu, RIGHT, BOTH, RAISED, W, E, N, DISABLED, NORMAL, Canvas, StringVar, OptionMenu

root = tk.Tk()
root.title("Real-Time Arduino Uno Serial Data read")
root.geometry('920x400')
root.resizable(width=False, height=False)

plt.style.use('fivethirtyeight')

port = 'COM3'
bauds = '9600'

labelPort = tk.Label(root, text = 'Port: ' + port + '\n' + bauds + ' Bauds')
labelPort.grid(row = 11, column = 9, padx = 10, pady = 10)

def updatePort():
    labelPort.config(text = 'Port: ' + port + '\n' + bauds + ' Bauds')


menubar = Menu(root)
root.config(menu=menubar)

settingsMenu = Menu(menubar)
fileMenu = Menu(menubar)

portMenu = Menu(settingsMenu)
baudsMenu = Menu(settingsMenu)

def setCom1():
    global port
    port='COM1'
    updatePort()
def setCom2():
    global port
    port='COM2'
    updatePort()
def setCom3():
    global port
    port='COM3'
    updatePort()
def setCom4():
    global port
    port='COM4'
    updatePort()
def setCom5():
    global port
    port='COM5'
    updatePort()
def setCom6():
    global port
    port='COM6'
    updatePort()
def setCom7():
    global port
    port='COM7'
    updatePort()
def setCom8():
    global port
    port='COM8'
    updatePort()
def setCom9():
    global port
    port='COM9'
    updatePort()
def setCom10():
    global port
    port='COM10'
    udpatePort()
def setCom11():
    global port
    port='COM11'
    udpatePort()
def setCom12():
    global port
    port='COM12'
    udpatePort()


def setBauds300():
    global bauds
    bauds='300'
    updatePort()
def setBauds600():
    global bauds
    bauds='600'
    updatePort()
def setBauds1200():
    global bauds
    bauds='1200'
    updatePort()
def setBauds2400():
    global bauds
    bauds='2400'
    updatePort()
def setBauds4800():
    global bauds
    bauds='4800'
    updatePort()
def setBauds9600():
    global bauds
    bauds='9600'
    updatePort()
def setBauds14400():
    global bauds
    bauds='14400'
    updatePort()
def setBauds19200():
    global bauds
    bauds='19200'
    updatePort()
def setBauds28800():
    global bauds
    bauds='28800'
    updatePort()
def setBauds38400():
    global bauds
    bauds='38400'
    updatePort()
def setBauds57600():
    global bauds
    bauds='57600'
    updatePort()
def setBauds115200():
    global bauds
    bauds='115200'
    updatePort()

portMenu.add_command(label="COM1", command = setCom1)
portMenu.add_command(label="COM2", command = setCom2)
portMenu.add_command(label="COM3", command = setCom3)
portMenu.add_command(label="COM4", command = setCom4)
portMenu.add_command(label="COM5", command = setCom5)
portMenu.add_command(label="COM6", command = setCom6)
portMenu.add_command(label="COM7", command = setCom7)
portMenu.add_command(label="COM8", command = setCom8)
portMenu.add_command(label="COM9", command = setCom9)
portMenu.add_command(label="COM10", command = setCom10)
portMenu.add_command(label="COM11", command = setCom11)
portMenu.add_command(label="COM12", command = setCom12)

baudsMenu.add_command(label="300", command = setBauds300)
baudsMenu.add_command(label="600", command = setBauds600)
baudsMenu.add_command(label="1200", command = setBauds1200)
baudsMenu.add_command(label="2400", command = setBauds2400)
baudsMenu.add_command(label="4800", command = setBauds4800)
baudsMenu.add_command(label="9600", command = setBauds9600)
baudsMenu.add_command(label="14400", command = setBauds14400)
baudsMenu.add_command(label="19200", command = setBauds19200)
baudsMenu.add_command(label="28800", command = setBauds28800)
baudsMenu.add_command(label="38400", command = setBauds38400)
baudsMenu.add_command(label="57600", command = setBauds57600)
baudsMenu.add_command(label="115200", command = setBauds115200)


settingsMenu.add_cascade(label='COM Port', menu=portMenu, underline=0)
settingsMenu.add_cascade(label='Bauds', menu=baudsMenu, underline=0)

menubar.add_cascade(label='File', underline=0, menu=fileMenu)
menubar.add_cascade(label="Settings", underline=0, menu=settingsMenu)

def exitApp():
    exit()

fileMenu.add_command(label = 'Exit', command= exitApp)

saveOnCsv = tk.IntVar()
csvCheckbox = tk.Checkbutton(root, text="Save data in csv \n format in real time", variable=saveOnCsv)
csvCheckbox.grid(row = 11, column = 0, padx = 20, pady = 10)

w = Canvas(root, width=25, height=25)
w.grid(row = 11, column = 10)
circle = w.create_oval(10, 10, 25, 25, outline="#A12", fill="#A12", width=2)



class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = []
        
        self.time = []
        self.counter = 0

        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.data5 = []
        self.data6 = []
        self.data7 = []
        self.data8 = []
        self.data9 = []
        self.data10 = []
        self.data11 = []
        self.data12 = []
        self.data13 = []
        self.data14 = []
        self.data15 = []
        self.data16 = []
        self.message = []

    
        self.labelData1 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData2 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData3 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData4 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData5 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData6 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData7 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData8 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData9 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData10 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData11 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData12 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData13 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData14 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData15 = tk.Label(parent, text="", font="Arial 10",width=4)
        self.labelData16 = tk.Label(parent, text="", font="Arial 10",width=4)

        self.labelName1 = tk.Label(parent, text="Cella 1", font="Arial 6",width=5).grid(row = 2, column = 2)
        self.labelName2 = tk.Label(parent, text="Cella 2", font="Arial 6",width=5).grid(row = 2, column = 3)
        self.labelName3 = tk.Label(parent, text="Cella 3", font="Arial 6",width=5).grid(row = 2, column = 4)
        self.labelName4 = tk.Label(parent, text="Cella 4", font="Arial 6",width=5).grid(row = 2, column = 5)
        self.labelName5 = tk.Label(parent, text="Cella 5", font="Arial 6",width=5).grid(row = 4, column = 2)
        self.labelName6 = tk.Label(parent, text="Cella 6", font="Arial 6",width=5).grid(row = 4, column = 3)
        self.labelName7 = tk.Label(parent, text="Cella 7", font="Arial 6",width=5).grid(row = 4, column = 4)
        self.labelName8 = tk.Label(parent, text="Cella 8", font="Arial 6",width=5).grid(row = 4, column = 5)
        self.labelName9 = tk.Label(parent, text="Cella 9", font="Arial 6",width=5).grid(row = 6, column = 2)
        self.labelName10 = tk.Label(parent, text="Cella 10", font="Arial 6",width=5).grid(row = 6, column = 3)
        self.labelName11 = tk.Label(parent, text="Cella 11", font="Arial 6",width=5).grid(row = 6, column = 4)
        self.labelName12 = tk.Label(parent, text="Cella 12", font="Arial 6",width=5).grid(row = 6, column = 5)
        self.labelName13 = tk.Label(parent, text="Cella 13", font="Arial 6",width=5).grid(row = 8, column = 2)
        self.labelName14 = tk.Label(parent, text="Cella 14", font="Arial 6",width=5).grid(row = 8, column = 3)
        self.labelName15 = tk.Label(parent, text="Cella 15", font="Arial 6",width=5).grid(row = 8, column = 4)
        self.labelName16 = tk.Label(parent, text="Cella 16", font="Arial 6",width=5).grid(row = 8, column = 5)
        
        self.labelMessage = tk.Label(parent, text="", font="Arial 10", width=10)
        self.labelMessage.grid(row=10, column=1,sticky = W)
        
        self.labelData1.grid(row=3, column=2,padx=10, pady=10,sticky = W)
        self.labelData2.grid(row=3, column=3,padx=10, pady=10,sticky = W)
        self.labelData3.grid(row=3, column=4,padx=10, pady=10,sticky = W)
        self.labelData4.grid(row=3, column=5,padx=10, pady=10,sticky = W)
        self.labelData5.grid(row=5, column=2,padx=10, pady=10,sticky = W)
        self.labelData6.grid(row=5, column=3,padx=10, pady=10,sticky = W)
        self.labelData7.grid(row=5, column=4,padx=10, pady=10,sticky = W)
        self.labelData8.grid(row=5, column=5,padx=10, pady=10,sticky = W)
        self.labelData9.grid(row=7, column=2,padx=10, pady=10,sticky = W)
        self.labelData10.grid(row=7, column=3,padx=10, pady=10,sticky = W)
        self.labelData11.grid(row=7, column=4,padx=10, pady=10,sticky = W)
        self.labelData12.grid(row=7, column=5,padx=10, pady=10,sticky = W)
        self.labelData13.grid(row=9, column=2,padx=10, pady=10,sticky = W)
        self.labelData14.grid(row=9, column=3,padx=10, pady=10,sticky = W)
        self.labelData15.grid(row=9, column=4,padx=10, pady=10,sticky = W)
        self.labelData16.grid(row=9, column=5,padx=10, pady=10,sticky = W)

        

        self.label4 = tk.Label(parent, text="Status Message:", font="Arial 10",).grid(row=10, column=0)

        self.label = tk.Label(parent, text="Ready", font="Arial 14", width= 24)
        self.label.grid(row = 0, column = 7, padx=10, pady=10,sticky = N)
        #self.label.after(50, self.readSerial)
        
        self.fileCSV = open('Data.csv', mode = 'w+')
        self.writer = csv.writer(self.fileCSV, delimiter = ';')

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        if(serialPort.is_open):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "").split(';')

            if(len(self.data)==17):
                print(self.data)
                w.itemconfig(circle, outline="#1A2", fill="#1A2")
                # display the new time
                self.counter = self.counter + 1
                self.time.append(self.counter)

                self.data1.append(float(self.data[0]))
                self.data2.append(float(self.data[1]))
                self.data3.append(float(self.data[2]))
                self.data4.append(float(self.data[3]))
                self.data5.append(float(self.data[4]))
                self.data6.append(float(self.data[5]))
                self.data7.append(float(self.data[6]))
                self.data8.append(float(self.data[7]))
                self.data9.append(float(self.data[8]))
                self.data10.append(float(self.data[9]))
                self.data11.append(float(self.data[10]))
                self.data12.append(float(self.data[11]))
                self.data13.append(float(self.data[12]))
                self.data14.append(float(self.data[13]))
                self.data15.append(float(self.data[14]))
                self.data16.append(float(self.data[15]))
                self.message.append(self.data[16])
                
                
                self.label.configure(text= "Reading data from Arduino...")
                

                self.labelData1.configure(text= self.data[0])
                self.labelData2.configure(text= self.data[1])
                self.labelData3.configure(text= self.data[2])
                self.labelData4.configure(text= self.data[3])
                self.labelData5.configure(text= self.data[4])
                self.labelData6.configure(text= self.data[5])
                self.labelData7.configure(text= self.data[6])
                self.labelData8.configure(text= self.data[7])
                self.labelData9.configure(text= self.data[8])
                self.labelData10.configure(text= self.data[9])
                self.labelData11.configure(text= self.data[10])
                self.labelData12.configure(text= self.data[11])
                self.labelData13.configure(text= self.data[12])
                self.labelData14.configure(text= self.data[13])
                self.labelData15.configure(text= self.data[14])
                self.labelData16.configure(text= self.data[15])

                self.labelMessage.configure(text= self.data[16])
                
                if(saveOnCsv.get()):
                    self.writer.writerow(self.data)
                self.animate()
                    
            # request tkinter to call self.refresh after 1s (the delay is given in ms)
            self.label.after(50, self.readSerial)
            # fig.plot(self.data1, self.data2, self.data3)


    def animate(self):
        plt.cla()
        plt.plot(self.time, self.data1, label='Channel 1')
        plt.plot(self.time, self.data2, label='Channel 2')
        plt.plot(self.time, self.data3, label='Channel 3')
        plt.draw()
        plt.pause(0.001)
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=100)

#end class


def start():
    try:
        settingsMenu.entryconfigure('COM Port',state="disabled")
        settingsMenu.entryconfigure('Bauds',state="disabled")
        global serialPort 
        serialPort = serial.Serial(port, bauds, timeout=0)
        if(saveOnCsv.get()):
            reader.fileCSV = open('Data.csv', mode = 'w+')
            reader.writer = csv.writer(reader.fileCSV, delimiter = ';')
        if(serialPort.is_open is not True):
            serialPort.open()
            
        reader.label.configure(text = 'Restarting...')
        w.itemconfig(circle, outline="#DD2",fill="#DD2")
        reader.readSerial()   
        
        csvCheckbox.config(state=DISABLED)
        startButton.config(state=DISABLED)
        stopButton.config(state=NORMAL)
    except Exception as e:
        if(e.__class__.__name__ == 'SerialException'):
            tk.messagebox.showerror(title='Serial error', message='Impossibile collegarsi alla porta ' + port +', assicurarsi di aver scelto la porta COM corretta')
        else:
            tk.messagebox.showerror(title='Generic error', message='Generic error: ' + e.__class__.__name__)
        settingsMenu.entryconfigure('COM Port',state="normal")
        settingsMenu.entryconfigure('Bauds',state="normal")    
        stopButton.config(state=DISABLED)
        startButton.config(state=NORMAL)

startButton = tk.Button(root, text = 'Start', command = start, padx=10, pady=5)
startButton.grid(row=0, column=0, sticky='W', padx=10)

def stop(): 
    w.itemconfig(circle, outline="#A12",  fill="#A12")
    settingsMenu.entryconfigure('COM Port',state="normal")
    settingsMenu.entryconfigure('Bauds',state="normal")
    # serialPort.close()
    reader.label.configure(text = 'Stopped')
    reader.labelData1.configure(text= '')
    reader.labelData2.configure(text= '')
    reader.labelData3.configure(text= '')
    reader.labelData4.configure(text= '')
    reader.labelData5.configure(text= '')
    reader.labelData6.configure(text= '')
    reader.labelData7.configure(text= '')
    reader.labelData8.configure(text= '')
    reader.labelData9.configure(text= '')
    reader.labelData10.configure(text= '')
    reader.labelData11.configure(text= '')
    reader.labelData12.configure(text= '')
    reader.labelData13.configure(text= '')
    reader.labelData14.configure(text= '')
    reader.labelData15.configure(text= '')
    reader.labelData16.configure(text= '')

    reader.labelMessage.configure(text= '')

    csvCheckbox.config(state=NORMAL)
    if(saveOnCsv.get()):
        reader.fileCSV.close()
    stopButton.config(state=DISABLED)
    startButton.config(state=NORMAL)
    serialPort.__del__()


stopButton = tk.Button(root, text = 'Stop', command = stop, padx=10, pady=5)
stopButton.grid(row=1, column=0, sticky='W', padx = 10)


reader = Reader(root)
root.mainloop()
