#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk, Image
import sys
import time, random
from PIL import *

# consts
columns = 20
rows = 14
blocksNum = 300


def openImage (fPath):
  return ImageTk.PhotoImage(Image.open(fPath))

class Tank:

    def __init__(self, x, y, battleField, tankSizeX, tankSizeY):
        self.x=x
        self.y=y
        self.flagUp = True
        self.flagDown = True
        self.flagRight = True
        self.flagLeft = True
        self.tankSizeX = tankSizeX
        self.tankSizeY = tankSizeY
        self.dir="up"
        self.imgR=openImage("tank-right.png") 
        self.imgL=openImage("tank-left.png") 
        self.imgU=openImage("tank-up.png") 
        self.imgD=openImage("tank-down.png") 
        self.l=tk.Label(battleField, image=self.imgU, bd=0, height=tankSizeY-2, width=tankSizeX-2, compound="center")
        self.l.place(x=self.x*tankSizeX, y=self.y*tankSizeY)

    def tank_to_right (self, event):
        self.l["image"] = self.imgR
        if self.x < columns-1 and self.dir == "right" and self.flagRight == True:
            self.x += 1
            self.flagLeft = True
        self.dir="right"
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_up (self, event):
        self.l["image"] = self.imgU
        if self.y > 0 and self.dir == "up" and self.flagUp == True:
            self.y -= 1
            self.flagDown = True
        self.dir="up"
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_left (self, event):
        self.l["image"] = self.imgL
        if self.x > 0 and self.dir == "left" and self.flagLeft == True: 
            self.x -= 1
            self.flagRight = True
        self.dir="left"
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_down (self, event):
        self.l["image"] = self.imgD
        if self.y < rows-1 and self.dir == "down" and self.flagDown == True:
            self.y += 1
            self.flagUp = True
        self.dir="down"
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

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

    def get_tank_coords(self):
    	return [self.x, self.y, self.dir]

def gencoordinates(m, n):
    seen = []
    while len(seen)<blocksNum :
        x, y = random.randint(0, m), random.randint(0,n)
        seen.append(str(x) + "_" + str(y))
    return seen
 

class main(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) 
        self.resizable(False, False)

        self.resizeW = self.winfo_screenwidth() / 1920
        self.resizeH = self.winfo_screenheight() / 1080

        self.rootWidth  = 50 * columns * self.resizeW
        self.rootHeight = 50 * rows * self.resizeH
        self.tankSizeX = 50 * self.resizeW
        self.tankSizeY = 50 * self.resizeH

        self.geometry('%dx%d+%d+%d' % (self.rootWidth+8*self.tankSizeX, self.rootHeight, 
                        (self.winfo_screenwidth()-self.rootWidth)/2, 
                        (self.winfo_screenheight()-self.rootHeight)/2))

        self.root = Frame(self)
        self.root.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.battleField = Canvas(self.root, width=self.rootWidth, height=self.rootHeight, bd=0)
        self.battleField.grid(row=0, column=0,sticky=N+S+E+W,padx=5,pady=5, rowspan=2)

        self.tanks = []
        self.blockIds = []
        self.create_tank(0,0,1)
        self.create_playground(0,0)
        self.create_game_settings()
        self.creating_score_board()
        
    def create_tank (self, x, y, mode):

        self.tank = Tank(x, y, self.battleField, self.tankSizeX, self.tankSizeY)
        self.tank.bind_buttons(mode)
        self.tanks += [self.tank] 

    def creating_score_board(self):

        self.score_battleField = tk.Label(self.root, text="Score : {}".format(self.score))
        self.score_battleField.grid(row=0,column=1,sticky=N+S+E+W)
        return

    def update_score_battleField(self):

        self.score += 1
        self.score_battleField['text']="Score : {}".format(self.score)
        return

    def create_game_settings(self):

        self.roadmap=[(0,0)]
        self.gamevalid=1
        self.score=0
        return

    def create_playground(self, x, y):
        self.blockIds = gencoordinates(columns, rows)
        for i in range(columns):
            for j in range(rows):
                bId = str(i) + "_" + str(j)
                if self.blockIds.count(bId) > 0 and str(x)+"_"+str(y) != bId:
                    self.battleField.create_rectangle(i * self.tankSizeX, j * self.tankSizeY,
                            i * self.tankSizeX + self.tankSizeX,
                            j * self.tankSizeY + self.tankSizeY, fill='#A64B00', outline="", tag="blocks")
                else :
                    self.battleField.create_rectangle(i * self.tankSizeX, j * self.tankSizeY,
                           i * self.tankSizeX + self.tankSizeX,
                           j * self.tankSizeY + self.tankSizeY, fill='black', outline="")
        return

    def tank_location(self):

        xCord = self.tank.get_tank_coords()[0]
        yCord = self.tank.get_tank_coords()[1]
        tankDir = self.tank.get_tank_coords()[2]

        if  tankDir == "right" :

        	if self.blockIds.count(str(xCord+1)+"_"+str(yCord)) > 0 :
        		self.tank.flagRight = False
        	else :
        		self.tank.flagRight = True

        elif  tankDir == "left" :

        	if self.blockIds.count(str(xCord-1)+"_"+str(yCord)) > 0 :
        		self.tank.flagLeft = False
        	else :
        		self.tank.flagLeft = True

        elif  tankDir == "up":

        	if self.blockIds.count(str(xCord)+"_"+str(yCord-1)) > 0 :
        		self.tank.flagUp = False
        	else :
        		self.tank.flagUp = True

        elif  tankDir == "down":

        	if self.blockIds.count(str(xCord)+"_"+str(yCord+1)) > 0 :
        		self.tank.flagDown = False
        	else :
        		self.tank.flagDown = True

    def re_update(self):

        self.tank_location()
        return

    def game_loss(self):

        self.battleField.create_text(self.rootWidth/2,self.rootHeight/2,
        				text="Game Over" ,font=('arial 60 bold'),fill='red')
        self.gamevalid=0
        return


if __name__ == '__main__':
    root = main()
    while True:
        root.update()
        root.update_idletasks()
        root.re_update()
        time.sleep(0.09)
