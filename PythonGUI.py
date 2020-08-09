<<<<<<< HEAD
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from threading import Thread
from random import randint
from matplotlib.animation import FuncAnimation

serialPort = serial.Serial(port = "COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

root = tk.Tk()
root.title('Python GUI')
root.geometry('900x500')
plt.style.use('fivethirtyeight')

class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = ''
        
        self.time = []
        self.counter = 0
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.label = tk.Label(parent, text="", font="Arial 16", width=200)
        self.label.pack()
        self.label.after(1000, self.readSerial)

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        if(serialPort.is_open and str(self.data) != 'tempo;dato1;dato2'):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "")
            #print(self.data)
            # display the new time
            if(len(self.data)<50):   

                self.data = self.data.split(';')

                if(len(self.data)==3):
                    self.counter = self.counter + 1
                    self.time.append(self.counter)
                    self.data1.append(int(self.data[0]))
                    self.data2.append(int(self.data[1]))
                    self.data3.append(int(self.data[2]))
                    #print(self.data1)
                    self.label.configure(text= "Reading data from Arduino...")
                    self.animate()
                    
            # request tkinter to call self.refresh after 1s (the delay is given in ms)
            self.label.after(1000, self.readSerial)
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

startButton = tk.Button(root, text = 'start', command = start)
startButton.pack()

def stop(): 
    serialPort.close()
    reader.label.configure(text = 'Stopped')
stopButton = tk.Button(root, text = 'Stop', command = stop)
stopButton.pack()

reader = Reader(root)
root.mainloop()


=======
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from threading import Thread
from random import randint
from matplotlib.animation import FuncAnimation

serialPort = serial.Serial(port = "COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

root = tk.Tk()
root.title('Python GUI')
root.geometry('900x500')
plt.style.use('fivethirtyeight')

class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = ''
        
        self.time = []
        self.counter = 0
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.label = tk.Label(parent, text="", font="Arial 16", width=200)
        self.label.pack()
        self.label.after(1000, self.readSerial)

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        if(serialPort.is_open and str(self.data) != 'tempo;dato1;dato2'):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "")
            #print(self.data)
            # display the new time
            if(len(self.data)<50):   

                self.data = self.data.split(';')

                if(len(self.data)==3):
                    self.counter = self.counter + 1
                    self.time.append(self.counter)
                    self.data1.append(int(self.data[0]))
                    self.data2.append(int(self.data[1]))
                    self.data3.append(int(self.data[2]))
                    #print(self.data1)
                    self.label.configure(text= "Reading data from Arduino...")
                    self.animate()
                    
            # request tkinter to call self.refresh after 1s (the delay is given in ms)
            self.label.after(1000, self.readSerial)
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

startButton = tk.Button(root, text = 'start', command = start)
startButton.pack()

def stop(): 
    serialPort.close()
    reader.label.configure(text = 'Stopped')
stopButton = tk.Button(root, text = 'Stop', command = stop)
stopButton.pack()

reader = Reader(root)
root.mainloop()


>>>>>>> e15817f47b0e30428583397cb84c5c42c65c0a67
