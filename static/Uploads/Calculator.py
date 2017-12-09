##this is to test gui interaction with functions behind them
#from tkinter import Tk, Label, Button, W
#import tkinter.ttk as ttk
#
#class GUI:
#    def __init__(self, master, firstNum):
#        self.master = master
#        self.firstNum = firstNum
#       
#        master.title("Calculator")
#        self.label = Label(master, text="Display goes here")
#        self.label.pack()
#        self.zero = ttk.Button(master, text = '0', command = self.func() )
#        self.zero.pack()
#    def func(firstNum):
#        print('func ran success')
#
#  
#def main():
#    root = Tk()
#    my_gui = GUI(root, '0')
#    root.mainloop()    
#    
#main()

from tkinter import *
from tkinter import ttk
VCalc = Tk()
VCalc.title("V-Calc")
VCalc.configure(background='#E6F3FE')


global firstNum, secondNum, operation, phase, display
display = StringVar()
def initstate():
    global firstNum, secondNum, operation, phase, display
    firstNum = ''
    secondNum = ''
    operation = ''
    phase = 1
    #display = StringVar()
    #display.set('_')

initstate()
    
def one():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '1'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '1'
        display.set(secondNum)

def two():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '2'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '2'
        display.set(secondNum)

def three():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '3'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '3'
        display.set(secondNum)

def four():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '4'
        display.set(firstNum)     
    if phase == 2:
        secondNum = secondNum + '4'
        display.set(secondNum)

def five():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '5'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '5'
        display.set(secondNum)

def six():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '6'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '6'
        display.set(secondNum)
        
def seven():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '7'
        display.set(firstNum)

    if phase == 2:
        secondNum = secondNum + '7'
        display.set(secondNum)

def eight():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '8'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '8'
        display.set(secondNum)
        
def nine():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '9'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '9'
        display.set(secondNum)

def zero():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        firstNum = firstNum + '0'
        display.set(firstNum)
    if phase == 2:
        secondNum = secondNum + '0'
        display.set(secondNum)

def times():
    global firstNum, secondNum, operation, phase, display
    if phase == 1:
        phase += 1
        operation = '*'
    else:
        operation = '*'
        #print('review this, unsure what the behavious should be')

def divide():
    global firstNum, secondNum, operation, phase, display
    if phase == 1:
        phase += 1
        operation = '/'
    else:
        operation = '/'
        #print('review this, unsure what the behavious should be')

def add():
    global firstNum, secondNum, operation, phase, display
    if phase == 1:
        phase += 1
        operation = '+'
    else:
        operation = '+'
        #print('review this, unsure what the behavious should be')

def minus():
    global firstNum, secondNum, operation, phase, display
    if phase == 1:
        phase += 1
        operation = '-'
    else:
        operation = '-'
        #print('review this, unsure what the behavious should be')

def enter():
    global firstNum, secondNum, operation, phase, display
    if phase ==1:
        pass
        #display = firstNum?
    elif phase ==2: #and secondNum not null?
        calculate()

def clear():
    initstate()
    display.set('_')

def calculate():
    global firstNum, secondNum, operation, phase, display
    result = 0 
    if operation == '+':
        result = int(firstNum) + int(secondNum)
    elif operation == '-':
        result = int(firstNum) - int(secondNum)
    elif operation == '*':
        result = int(firstNum) * int(secondNum)
    elif operation == '/':
        if int(secondNum) ==0:
            print('Stop trying to divide by 0')
            #main()
        else:
            result = int(firstNum)/int(secondNum)
    #print(result)
    phase = phase + 1
    display.set(result)
    initstate()



nupp = ttk.Button(VCalc, text="1", command= one)
nupp.grid(column=1, row=1, padx=3, pady=3, sticky=(N, S, W, E))

nupp2 = ttk.Button(VCalc, text="2", command=two)
nupp2.grid(column=2, row=1, padx=3, pady=3, sticky=(N, S, W, E))

nupp3 = ttk.Button(VCalc, text="3", command=three)
nupp3.grid(column=3, row=1, padx=3, pady=3, sticky=(N, S, W, E))

nupp4 = ttk.Button(VCalc, text="4", command=four)
nupp4.grid(column=1, row=2, padx=3, pady=3, sticky=(N, S, W, E))

nupp5 = ttk.Button(VCalc, text="5", command=five)
nupp5.grid(column=2, row=2, padx=3, pady=3, sticky=(N, S, W, E))

nupp6 = ttk.Button(VCalc, text="6", command=six)
nupp6.grid(column=3, row=2, padx=3, pady=3, sticky=(N, S, W, E))

nupp7 = ttk.Button(VCalc, text="7", command=seven)
nupp7.grid(column=1, row=3, padx=3, pady=3, sticky=(N, S, W, E))

nupp8 = ttk.Button(VCalc, text="8", command=eight)
nupp8.grid(column=2, row=3, padx=3, pady=3, sticky=(N, S, W, E))

nupp9 = ttk.Button(VCalc, text="9", command=nine)
nupp9.grid(column=3, row=3, padx=3, pady=3, sticky=(N, S, W, E))

nupp0 = ttk.Button(VCalc, text="0", command=zero)
nupp0.grid(column=1, row=4, padx=3, pady=3, sticky=(N, S, W, E))

nuppStar = ttk.Button(VCalc, text="*", command= times)
nuppStar.grid(column=4, row=1, padx=3, pady=3, sticky=(N, S, W, E))

nuppDivide = ttk.Button(VCalc, text="/", command= divide)
nuppDivide.grid(column=4, row=2, padx=3, pady=3, sticky=(N, S, W, E))

nuppMinus = ttk.Button(VCalc, text="-", command= minus)
nuppMinus.grid(column=4, row=3, padx=3, pady=3, sticky=(N, S, W, E))

nuppAdd= ttk.Button(VCalc, text="+", command= add)
nuppAdd.grid(column=4, row=4, padx=3, pady=3, sticky=(N, S, W, E))

nuppEnt = ttk.Button(VCalc, text="Enter", command= enter)
nuppEnt.grid(column=2, row=4, padx=3, pady=3, sticky=(N, S, W, E))

nuppEnt = ttk.Button(VCalc, text="Clear", command= clear)
nuppEnt.grid(column=3, row=4, padx=3, pady=3, sticky=(N, S, W, E))

displayOut = Label(VCalc, textvariable = display)
displayOut.grid(column = 1, row = 0,padx=3, pady=3, sticky=(N, S, W, E))

VCalc.mainloop()