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
root.geometry('700x300')
root.resizable(width=False, height=False)

plt.style.use('fivethirtyeight')

ports = { 'COM1','COM2','COM3','COM4','COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10', 'COM11', 'COM12'}
tkvar = StringVar(root)
tkvar.set('COM3') # set the default option

bauds = {'300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '57600', '115200'}
tkvar2 = StringVar(root)
tkvar2.set('9600') # set the default option


labelPort = tk.Label(root, text = 'Port: ' + tkvar.get() + '\n' + tkvar2.get() + ' baud')
labelPort.grid(row = 6, column = 5, padx = 10, pady = 10)

def updatePort(event):
    labelPort.config(text = 'Port: ' + tkvar.get() + '\n' + tkvar2.get() + ' baud')


baudsMenu = OptionMenu(root, tkvar2, *bauds, command = updatePort)
baudsMenu.grid(row = 4, column = 6)

portMenu = OptionMenu(root, tkvar, *ports, command = updatePort)
portMenu.grid(row = 5, column = 6)



saveOnCsv = tk.IntVar()
csvCheckbox = tk.Checkbutton(root, text="Save data in csv \n format in real time", variable=saveOnCsv)
csvCheckbox.grid(row = 6, column = 0, padx = 20, pady = 10)

w = Canvas(root, width=25, height=25)
w.grid(row = 6, column = 6)
circle = w.create_oval(10, 10, 25, 25, outline="#A12", fill="#A12", width=2)



class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = ''
        
        self.time = []
        self.counter = 0
        self.data1 = []
        self.data2 = []
        self.data3 = []
    
        self.labelData1 = tk.Label(parent, text="", font="Arial 10",)
        self.labelData2 = tk.Label(parent, text="", font="Arial 10",)
        self.labelData3 = tk.Label(parent, text="", font="Arial 10",)
        self.stateLabel = tk.Label(parent, text="", font="Arial 10",)
        
        self.labelData1.grid(row=2, column=1,padx=10, pady=10,sticky = W)
        self.labelData2.grid(row=3, column=1,padx=10, pady=10,sticky = W)
        self.labelData3.grid(row=4, column=1,padx=10, pady=10,sticky = W)
        self.stateLabel.grid(row=5, column=1,padx=10, pady=10,sticky = W)

        self.label1 = tk.Label(parent, text="Sensore 1", font="Arial 10",).grid(row=2, column=0,padx=10, pady=10)
        self.label2 = tk.Label(parent, text="Sensore 2", font="Arial 10",).grid(row=3, column=0,padx=10, pady=10)
        self.label3 = tk.Label(parent, text="Sensore 3", font="Arial 10",).grid(row=4, column=0,padx=10, pady=10)
        self.label4 = tk.Label(parent, text="Message", font="Arial 10",).grid(row=5, column=0,padx=10, pady=10)

        self.label = tk.Label(parent, text="Ready", font="Arial 14", width= 24)
        self.label.grid(row = 0, column = 3, padx=10, pady=10,sticky = N)
        #self.label.after(50, self.readSerial)
        
        self.fileCSV = open('Data.csv', mode = 'w+')
        self.writer = csv.writer(self.fileCSV, delimiter = ';')

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        if(serialPort.is_open):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "")
            if(len(self.data.split(';'))==4):
                print(self.data)
                w.itemconfig(circle, outline="#1A2", fill="#1A2")
                # display the new time
                self.data = self.data.split(';')
                self.counter = self.counter + 1
                self.time.append(self.counter)

                self.data1.append(float(self.data[0]))
                self.data2.append(float(self.data[1]))
                self.data3.append(float(self.data[2]))
                
                
                self.label.configure(text= "Reading data from Arduino...")
                self.stateLabel.configure(text= self.data[3])

                self.labelData1.configure(text= self.data[0])
                self.labelData2.configure(text= self.data[1])
                self.labelData3.configure(text= self.data[2])

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
    reader.stateLabel.configure(text= '')
    csvCheckbox.config(state=NORMAL)
    if(saveOnCsv.get()):
        reader.fileCSV.close()
    stopButton.config(state=DISABLED)
    startButton.config(state=NORMAL)
    serialPort.__del__()


stopButton = tk.Button(root, text = 'Stop', command = stop,padx=10, pady=5)
stopButton.grid(row=0, column=0)


reader = Reader(root)
root.mainloop()
