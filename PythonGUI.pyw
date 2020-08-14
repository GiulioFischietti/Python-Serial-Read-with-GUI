import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from threading import Thread
from random import randint
from matplotlib.animation import FuncAnimation

from tkinter import Tk, RIGHT, BOTH, RAISED, W, E, N

root = tk.Tk()
root.title("Real-Time Arduino Uno data read")
root.geometry('600x300')
plt.style.use('fivethirtyeight')
serialPort = serial.Serial('COM3', 9600, timeout=0)
class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = ''
        
        self.time = []
        self.counter = 0
        self.data1 = []
        self.data2 = []
        self.data3 = []

        self.labelData1 = tk.Label(parent, text="", font="Arial 12",)
        self.labelData2 = tk.Label(parent, text="", font="Arial 12",)
        self.labelData3 = tk.Label(parent, text="", font="Arial 12",)
        
        self.labelData1.grid(row=2, column=1,padx=10, pady=10,sticky = W)
        self.labelData2.grid(row=3, column=1,padx=10, pady=10,sticky = W)
        self.labelData3.grid(row=4, column=1,padx=10, pady=10,sticky = W)

        self.label1 = tk.Label(parent, text="Sensore 1", font="Arial 12",).grid(row=2, column=0,padx=10, pady=10)
        self.label2 = tk.Label(parent, text="Sensore 2", font="Arial 12",).grid(row=3, column=0,padx=10, pady=10)
        self.label3 = tk.Label(parent, text="Sensore 3", font="Arial 12",).grid(row=4, column=0,padx=10, pady=10)

        self.label = tk.Label(parent, text="", font="Arial 16")
        self.label.grid(row = 0, column = 3, padx=10, pady=10,sticky = N)
        self.label.after(50, self.readSerial)

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        if(serialPort.is_open and (str(self.data) != 'tempo;dato1;dato2')):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "")
            #print(self.data)
            # display the new time
            if(len(self.data)<50):   
                print(self.data)
                self.data = self.data.split(';')

                if(len(self.data)==3):
                    
                    self.counter = self.counter + 1
                    self.time.append(self.counter)
                    self.data1.append(float(self.data[0]))
                    self.data2.append(float(self.data[1]))
                    self.data3.append(float(self.data[2]))
                    print(self.data2[self.counter-1])
                    self.label.configure(text= "Reading data from Arduino...")

                    self.labelData1.configure(text= self.data[0])
                    self.labelData2.configure(text= self.data[1])
                    self.labelData3.configure(text= self.data[2])

                    self.animate()
                    
            # request tkinter to call self.refresh after 1s (the delay is given in ms)
            self.label.after(50, self.readSerial)
            # fig.plot(self.data1, self.data2, self.data3)


    def animate(self):
        plt.cla()
        plt.plot(self.time, self.data1, label='Channel 1')
        plt.plot(self.time, self.data2, label='Channel 2')
        plt.plot(self.time, self.data3, label='Channel 2')
        plt.draw()
        plt.pause(0.001)
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=100)

#end class

def start():
    if(serialPort.is_open is not True):
        serialPort.open()
        reader.label.configure(text = 'Restarting...')
        reader.readSerial()

startButton = tk.Button(root, text = 'Start', command = start,padx=10, pady=5)
startButton.grid(row=0, column=1,padx=10, pady=10,sticky = E)

def stop(): 
    serialPort.close()
    reader.label.configure(text = 'Stopped')
    reader.labelData1.configure(text= '')
    reader.labelData2.configure(text= '')
    reader.labelData3.configure(text= '')


stopButton = tk.Button(root, text = 'Stop', command = stop,padx=10, pady=5)
stopButton.grid(row=0, column=0,padx=10, pady=10,sticky = E)


reader = Reader(root)
root.mainloop()


