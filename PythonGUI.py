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
root.geometry('820x340')
root.configure(bg='white')
root.resizable(width=False, height=False)
root.iconbitmap('icon.ico')
plt.style.use('fivethirtyeight')

showplotvar = False

port = tk.StringVar()
port.set('COM3')

bauds = tk.StringVar()
bauds.set('9600')

labelPort = tk.Label(root, text = 'Port: ' + port.get() + '\n' + bauds.get() + ' Bauds', bg='white')
labelPort.grid(row = 11, column = 9, padx = 10, pady = 10)

def updatePort():
    labelPort.config(text = 'Port: ' + port.get() + '\n' + bauds.get() + ' Bauds')

menubar = Menu(root, background='white')
menubar.config(bg='white')
root.config(menu=menubar)
settingsMenu = Menu(menubar, tearoff=False)
fileMenu = Menu(menubar, tearoff=False)
portMenu = Menu(settingsMenu, tearoff=False)
baudsMenu = Menu(settingsMenu, tearoff=False)

for i in range(12):
    portMenu.add_radiobutton(variable=port, label=('COM'+str(i+1)), command = updatePort)

baudsMenu.add_radiobutton(variable=bauds, label="300", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="600", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="1200", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="2400", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="4800", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="9600", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="14400", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="19200", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="28800", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="38400", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="57600", command = updatePort)
baudsMenu.add_radiobutton(variable=bauds, label="115200", command = updatePort)

settingsMenu.add_cascade(label='COM Port', menu=portMenu, underline=0)
settingsMenu.add_cascade(label='Bauds', menu=baudsMenu, underline=0)

menubar.add_cascade(label='File', underline=0, menu=fileMenu)
menubar.add_cascade(label="Settings", underline=0, menu=settingsMenu)

def exitApp():
    exit()

fileMenu.add_command(label = 'Exit', command= exitApp)
saveOnCsv = tk.IntVar()

def showplot():
    global showplotvar
    if(not showplotvar):
        showplotvar = True
        showPlotButton.config(text='Hide plot')
    else:
        showplotvar = False 
        showPlotButton.config(text='Show plot')
        plt.close()

showPlotButton = tk.Button(root, text='Show Plot', command=showplot, bg='#bb1', fg='white', borderwidth=0, padx=10, pady=5)
showPlotButton.grid(row=11, column=1)
w = Canvas(root, width=30, height=30, bg='white', highlightthickness=0)
w.grid(row = 11, column = 10)
circle = w.create_oval(10, 10, 25, 25, outline="#A12", fill="#A12", width=2)

class Reader:
    def __init__(self, parent):
        # variable storing time
        self.data = []
        self.time = []
        self.counter = 0
        self.dataCells = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.message = []
        self.labelDataCells = []
        self.labelNameCells = []
        
        for i in range(16):
            self.labelDataCells.append(tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white'))
        
        k = 0
        for i in range(16):
            if((i+4)%4==0):
                k += 2
            self.labelNameCells.append(tk.Label(parent, text=("Cella " + str(i+1)), font="Arial 6",width=5, bg='white').grid(row = k, column = ((i+4)%4+2)))
           
        
        self.labelMessage = tk.Label(parent, text="", font="Arial 10", width=10, bg='white')
        self.labelMessage.grid(row=10, column=1,sticky = W)
        
        j = 0
        for i in range(16):
            if((i+4)%4==0):
                j += 2
            self.labelDataCells[i].grid(row = j+1, column = ((i+4)%4+2))

        self.label4 = tk.Label(parent, text="Status Message:", font="Arial 10",bg='white').grid(row=10, column=0)
        self.label = tk.Label(parent, text="Ready", font="Arial 14", width= 24, bg='white')
        self.label.grid(row = 0, column = 7, padx=10, pady=10,sticky = N)
        #self.label.after(50, self.readSerial)
        if(saveOnCsv.get()):
            self.fileCSV = open('Data.csv', mode = 'w+')
            self.writer = csv.writer(self.fileCSV, delimiter = ';')

    def readSerial(self):
        """ refresh the content of the label every second """
        # increment the time
        # w.itemconfig(circle, outline="#1A2", fill="#1A2")
        if(serialPort.is_open):   
            self.data = str(serialPort.readline()).replace("'","").replace("b","").replace("\\n", "").replace("\\r", "").split(';')

            if(len(self.data)==17 and all(n.isnumeric() for n in self.data[0:16])):
                # display the new time
                w.itemconfig(circle, outline="#1A2", fill="#1A2")
                self.counter = self.counter + 1
                self.time.append(self.counter)

                for i in range(16):
                    self.dataCells[i].append(float(self.data[i]))
                
                self.message.append(self.data[16])    
                self.label.configure(text= "Reading data from Arduino...")
                
                for i in range(16):
                    self.labelDataCells[i].configure(text=self.data[i])

                self.labelMessage.configure(text= self.data[16])
                if(saveOnCsv.get()):
                    self.writer.writerow(self.data)
                if(showplotvar):
                    self.animate()
                    
            # request tkinter to call self.refresh after 51ms (the delay is given in ms)
            self.label.after(100, self.readSerial)
            # fig.plot(self.data1, self.data2, self.data3)

    def animate(self):
        plt.cla()
        plt.plot(self.time, self.dataCells[0], label='Channel 1')
        plt.plot(self.time, self.dataCells[1], label='Channel 2')
        plt.plot(self.time, self.dataCells[2], label='Channel 3')
        plt.draw()
        plt.pause(0.001)
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=100)
#end class

csvCheckbox = tk.Checkbutton(root, text="Save data in csv \n format in real time", variable=saveOnCsv, bg='white')
csvCheckbox.grid(row = 11, column = 0, padx = 20, pady = 10)

def start():
   
    try:
        reader.label.configure(text = 'Restarting...')
        w.itemconfig(circle, outline="#DD2",fill="#DD2")
        settingsMenu.entryconfigure('COM Port',state="disabled")
        settingsMenu.entryconfigure('Bauds',state="disabled")
        global serialPort 
        serialPort = serial.Serial(port.get(), bauds.get(), timeout=None)
        if(saveOnCsv.get()):
            reader.fileCSV = open('Data.csv', mode = 'w+')
            reader.writer = csv.writer(reader.fileCSV, delimiter = ';')
        if(serialPort.is_open is not True):
            
            serialPort.open()
            
        
        reader.readSerial()   
        
        csvCheckbox.config(state=DISABLED)
        startButton.config(state=DISABLED, bg='grey')
        stopButton.config(state=NORMAL, bg='#dd2233')
    except Exception as e:
        if(e.__class__.__name__ == 'SerialException'):
            tk.messagebox.showerror(title='Serial error', message='Impossibile collegarsi alla porta ' + port.get() +', assicurarsi di aver scelto la porta COM corretta')
        # else:
        #     tk.messagebox.showerror(title='Generic error', message='Generic error: ' + e.__class__.__name__)
        settingsMenu.entryconfigure('COM Port',state="normal")
        settingsMenu.entryconfigure('Bauds',state="normal")    
        stopButton.config(state=DISABLED, bg='grey')
        startButton.config(state=NORMAL, bg='#22aa33')
    
startButton = tk.Button(root, text = 'Start', command = start, padx=10, pady=5, fg='white', bg='#22aa33', borderwidth=0)
startButton.grid(row=0, column=0, sticky='W', padx=10)

def stop(): 
    w.itemconfig(circle, outline="#A12",  fill="#A12")
    settingsMenu.entryconfigure('COM Port',state="normal")
    settingsMenu.entryconfigure('Bauds',state="normal")
    # serialPort.close()
    reader.label.configure(text = 'Stopped')

    for i in range(16):
        reader.labelDataCells[i].configure(text='')

    reader.labelMessage.configure(text= '')

    csvCheckbox.config(state=NORMAL)
    if(saveOnCsv.get()):
        reader.fileCSV.close()
    stopButton.config(state=DISABLED, bg='grey')
    startButton.config(state=NORMAL, bg='#22aa33')
    serialPort.__del__()


stopButton = tk.Button(root, text = 'Stop', command = stop, padx=10, pady=5, fg='white', bg='grey', borderwidth=0, state = DISABLED)
stopButton.grid(row=1, column=0, sticky='W', padx = 10)


reader = Reader(root)
root.mainloop()
