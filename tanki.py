#!/usr/bin/env python3
import tkinter as tk
from PIL import ImageTk, Image

# consts

tankSizeX = 50
tankSizeY = 50
columns = 30
rows = 20

rootWidth  = tankSizeX*columns
rootHeight = tankSizeY*rows

# root

TKroot = tk.Tk ()
TKroot.title("Tanki")


class Tank:
  def __init__(self, x, y):
    self.x=x
    self.y=y
    self.img=ImageTk.PhotoImage(Image.open("tank-right.jpg"))   
    self.l=tk.Label(TKroot, image=self.img)
    self.l.place(x=x*tankSizeX, y=y*tankSizeY)
    # self.l.pack()   

class Field:
  def __init__ (self):
    self.width  = rootWidth
    self.height  = rootHeight
    self.tanks  = []
    
  def add_tank (self, x, y):
    tank=Tank(x,y)
    self.tanks+=[tank] 




def main():

  field = Field()
  field.add_tank(10, 5)
  TKroot.geometry(str(field.width) + "x" + str(field.height) + "+0+0")
  TKroot.mainloop()


main()
