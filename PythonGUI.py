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
root.geometry('920x420')
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

portMenu.add_radiobutton(variable=port, label="COM1", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM2", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM3", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM4", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM5", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM6", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM7", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM8", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM9", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM10", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM11", command = updatePort)
portMenu.add_radiobutton(variable=port, label="COM12", command = updatePort)

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
csvCheckbox = tk.Checkbutton(root, text="Save data in csv \n format in real time", variable=saveOnCsv, bg='white')
csvCheckbox.grid(row = 11, column = 0, padx = 20, pady = 10)

def showplot():
    global showplotvar
    showplotvar = True

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

    
        self.labelData1 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData2 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData3 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData4 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData5 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData6 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData7 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData8 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData9 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData10 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData11 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData12 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData13 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData14 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData15 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')
        self.labelData16 = tk.Label(parent, text="", font="Arial 10",width=4, bg = 'white')

        self.labelName1 = tk.Label(parent, text="Cella 1", font="Arial 6",width=5, bg='white').grid(row = 2, column = 2)
        self.labelName2 = tk.Label(parent, text="Cella 2", font="Arial 6",width=5, bg='white').grid(row = 2, column = 3)
        self.labelName3 = tk.Label(parent, text="Cella 3", font="Arial 6",width=5, bg='white').grid(row = 2, column = 4)
        self.labelName4 = tk.Label(parent, text="Cella 4", font="Arial 6",width=5, bg='white').grid(row = 2, column = 5)
        self.labelName5 = tk.Label(parent, text="Cella 5", font="Arial 6",width=5, bg='white').grid(row = 4, column = 2)
        self.labelName6 = tk.Label(parent, text="Cella 6", font="Arial 6",width=5, bg='white').grid(row = 4, column = 3)
        self.labelName7 = tk.Label(parent, text="Cella 7", font="Arial 6",width=5, bg='white').grid(row = 4, column = 4)
        self.labelName8 = tk.Label(parent, text="Cella 8", font="Arial 6",width=5, bg='white').grid(row = 4, column = 5)
        self.labelName9 = tk.Label(parent, text="Cella 9", font="Arial 6",width=5, bg='white').grid(row = 6, column = 2)
        self.labelName10 = tk.Label(parent, text="Cella 10", font="Arial 6",width=5, bg='white').grid(row = 6, column = 3)
        self.labelName11 = tk.Label(parent, text="Cella 11", font="Arial 6",width=5, bg='white').grid(row = 6, column = 4)
        self.labelName12 = tk.Label(parent, text="Cella 12", font="Arial 6",width=5, bg='white').grid(row = 6, column = 5)
        self.labelName13 = tk.Label(parent, text="Cella 13", font="Arial 6",width=5, bg='white').grid(row = 8, column = 2)
        self.labelName14 = tk.Label(parent, text="Cella 14", font="Arial 6",width=5, bg='white').grid(row = 8, column = 3)
        self.labelName15 = tk.Label(parent, text="Cella 15", font="Arial 6",width=5, bg='white').grid(row = 8, column = 4)
        self.labelName16 = tk.Label(parent, text="Cella 16", font="Arial 6",width=5, bg='white').grid(row = 8, column = 5)
        
        self.labelMessage = tk.Label(parent, text="", font="Arial 10", width=10, bg='white')
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

            print(self.data)
            if(len(self.data)==17 and all(n.isnumeric() for n in self.data[0:16])):
                
                
               
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
                if(showplotvar):
                    self.animate()
                    
            # request tkinter to call self.refresh after 51ms (the delay is given in ms)
            self.label.after(100, self.readSerial)
            # fig.plot(self.data1, self.data2, self.data3)


    def animate(self):
        plt.cla()
        plt.plot(self.time, self.data1, label='Channel 1')
        plt.plot(self.time, self.data2, label='Channel 2')
        plt.plot(self.time, self.data3, label='Channel 3')
        plt.draw()
        plt.pause(0.002)
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=100)

#end class


def start():
   
    try:
        settingsMenu.entryconfigure('COM Port',state="disabled")
        settingsMenu.entryconfigure('Bauds',state="disabled")
        global serialPort 
        serialPort = serial.Serial(port.get(), bauds.get(), timeout=None)
        if(saveOnCsv.get()):
            reader.fileCSV = open('Data.csv', mode = 'w+')
            reader.writer = csv.writer(reader.fileCSV, delimiter = ';')
        if(serialPort.is_open is not True):
            serialPort.open()
            
        reader.label.configure(text = 'Restarting...')
        w.itemconfig(circle, outline="#DD2",fill="#DD2")
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
    w.itemconfig(circle, outline="#1A2", fill="#1A2")
startButton = tk.Button(root, text = 'Start', command = start, padx=10, pady=5, fg='white', bg='#22aa33', borderwidth=0)
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
    stopButton.config(state=DISABLED, bg='grey')
    startButton.config(state=NORMAL, bg='#22aa33')
    serialPort.__del__()


stopButton = tk.Button(root, text = 'Stop', command = stop, padx=10, pady=5, fg='white', bg='grey', borderwidth=0, state = DISABLED)
stopButton.grid(row=1, column=0, sticky='W', padx = 10)


reader = Reader(root)
root.mainloop()
