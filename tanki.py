#!/usr/bin/env python3
import tkinter as tk
from PIL import ImageTk, Image

# consts

tankSizeX = 50
tankSizeY = 50
columns = 28
rows = 14

rootWidth  = tankSizeX*columns
rootHeight = tankSizeY*rows

# root

TKroot = tk.Tk ()
TKroot.title("Tanki")

# images

def openImage (fPath):
  return ImageTk.PhotoImage(Image.open(fPath))


class Tank:
  def __init__(self, x, y):
    self.x=x
    self.y=y
    self.dir="up"
    self.imgR=openImage("tank-right.jpg")   
    self.imgU=openImage("tank-up.jpg") 
    self.imgL=openImage("tank-left.jpg")  
    self.imgD=openImage("tank-down.jpg")   
    self.l=tk.Label(TKroot, image=self.imgU)
    self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

  def tank_to_right (self, event):
    self.l["image"] = self.imgR
    if self.x < columns and self.dir == "right":
      self.x += 1
    self.dir="right"
    self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

  def tank_to_up (self, event):
    self.l["image"] = self.imgU
    if self.y > 0 and self.dir == "up":
      self.y -= 1
    self.dir="up"
    self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

  def tank_to_left (self, event):
    self.l["image"] = self.imgL
    if self.x > 0 and self.dir == "left": 
      self.x -= 1
    self.dir="left"
    self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

  def tank_to_down (self, event):
    self.l["image"] = self.imgD
    if self.y < rows and self.dir == "down":
      self.y += 1
    self.dir="down"
    self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

  def bind_buttons(self, mode=1):
    if mode == 1:
      self.l.focus_set()
      self.l.bind('<Up>', self.tank_to_up)
      self.l.bind('<Right>', self.tank_to_right)
      self.l.bind('<Down>', self.tank_to_down)
      self.l.bind('<Left>', self.tank_to_left)
    if mode == 2:
      self.l.focus_set()
      self.l.bind('<W>', self.tank_to_up)
      self.l.bind('<D>', self.tank_to_right)
      self.l.bind('<S>', self.tank_to_down)
      self.l.bind('<A>', self.tank_to_left)


class Field:
  def __init__ (self):
    self.width  = rootWidth
    self.height  = rootHeight
    self.tanks  = []
    
  def add_tank (self, x, y, mode):
    tank=Tank(x,y)
    tank.bind_buttons(mode)
    self.tanks+=[tank] 



def main():

  field = Field()
  field.add_tank(0, 0, 1)
  # field.add_tank(28, 14, 2)
  TKroot.geometry(str(field.width) + "x" + str(field.height) + "+0+0")
  TKroot.mainloop()


main()
