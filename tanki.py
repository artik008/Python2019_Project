#!/usr/bin/env python3
from tkinter import *

TKroot = Tk()
TKroot.title("Tanki")


class Field:
  def __init__ (self):
    self.width = 640
    self.heght = 480
    self.tanks = []

def main():

  field = Field()

  TKroot.geometry(str(field.width) + "x" + str(field.heght) + "+200+100")
  TKroot.mainloop()

main()