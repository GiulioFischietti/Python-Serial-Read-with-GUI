import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from threading import Thread
from random import randint
from matplotlib.animation import FuncAnimation
import csv

from tkinter import Tk, RIGHT, BOTH, RAISED, W, E, N, DISABLED, NORMAL, Canvas, StringVar, OptionMenu

root = tk.Tk()
root.title("Real-Time Arduino Uno Serial Data read")
root.geometry('950x350')
root.resizable(width=False, height=False)

plt.style.use('fivethirtyeight')

ports = { 'COM1','COM2','COM3','COM4','COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10', 'COM11', 'COM12'}
tkvar = StringVar(root)
tkvar.set('COM3') # set the default option

bauds = {'300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '57600', '115200'}
tkvar2 = StringVar(root)
tkvar2.set('9600') # set the default option


labelPort = tk.Label(root, text = 'Port: ' + tkvar.get() + '\n' + tkvar2.get() + ' baud')
labelPort.grid(row = 7, column = 9, padx = 10, pady = 10)

def updatePort(event):
    labelPort.config(text = 'Port: ' + tkvar.get() + '\n' + tkvar2.get() + ' baud')


baudsMenu = OptionMenu(root, tkvar2, *bauds, command = updatePort)
baudsMenu.grid(row = 5, column = 10)

portMenu = OptionMenu(root, tkvar, *ports, command = updatePort)
portMenu.grid(row = 6, column = 10)



saveOnCsv = tk.IntVar()
csvCheckbox = tk.Checkbutton(root, text="Save data in csv \n format in real time", variable=saveOnCsv)
csvCheckbox.grid(row = 7, column = 0, padx = 20, pady = 10)

w = Canvas(root, width=25, height=25)
w.grid(row = 7, column = 10)
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
        
        self.labelMessage = tk.Label(parent, text="", font="Arial 10")
        self.labelMessage.grid(row=6, column=2,padx=10, pady=10,sticky = W)
        
        self.labelData1.grid(row=2, column=2,padx=10, pady=10,sticky = W)
        self.labelData2.grid(row=2, column=3,padx=10, pady=10,sticky = W)
        self.labelData3.grid(row=2, column=4,padx=10, pady=10,sticky = W)
        self.labelData4.grid(row=2, column=5,padx=10, pady=10,sticky = W)
        self.labelData5.grid(row=3, column=2,padx=10, pady=10,sticky = W)
        self.labelData6.grid(row=3, column=3,padx=10, pady=10,sticky = W)
        self.labelData7.grid(row=3, column=4,padx=10, pady=10,sticky = W)
        self.labelData8.grid(row=3, column=5,padx=10, pady=10,sticky = W)
        self.labelData9.grid(row=4, column=2,padx=10, pady=10,sticky = W)
        self.labelData10.grid(row=4, column=3,padx=10, pady=10,sticky = W)
        self.labelData11.grid(row=4, column=4,padx=10, pady=10,sticky = W)
        self.labelData12.grid(row=4, column=5,padx=10, pady=10,sticky = W)
        self.labelData13.grid(row=5, column=2,padx=10, pady=10,sticky = W)
        self.labelData14.grid(row=5, column=3,padx=10, pady=10,sticky = W)
        self.labelData15.grid(row=5, column=4,padx=10, pady=10,sticky = W)
        self.labelData16.grid(row=5, column=5,padx=10, pady=10,sticky = W)

        

        self.label1 = tk.Label(parent, text="Sensore 1", font="Arial 10",).grid(row=2, column=0,padx=10, pady=10)
        self.label2 = tk.Label(parent, text="Sensore 2", font="Arial 10",).grid(row=3, column=0,padx=10, pady=10)
        self.label3 = tk.Label(parent, text="Sensore 3", font="Arial 10",).grid(row=4, column=0,padx=10, pady=10)
        self.label4 = tk.Label(parent, text="Message", font="Arial 10",).grid(row=6, column=0,padx=10, pady=10)

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
    global serialPort 
    serialPort = serial.Serial(tkvar.get(), tkvar2.get(), timeout=0)
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
    
startButton = tk.Button(root, text = 'Start', command = start,padx=10, pady=5)
startButton.grid(row=0, column=1)

def stop(): 
    w.itemconfig(circle, outline="#A12",  fill="#A12")
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
stopButton.grid(row=0, column=0)


reader = Reader(root)
root.mainloop()
