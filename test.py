from tkinter import *

def ok():
	print('ok')

rGui = Tk()

Button(rGui, text="Add", command=ok).grid( row=y,column=1 )