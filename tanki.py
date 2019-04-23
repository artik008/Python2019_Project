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


PLAYGROUND_WIDTH=700
PLAYGROUND_HEIGHT=400
PLAYGROUND_COLOR='powder blue'
SNAKE_HEAD_COLOR="red"
SNAKE_MOVING_SPEED=8

def openImage (fPath):
  return ImageTk.PhotoImage(Image.open(fPath))

class Tank:

    def __init__(self, x, y, battleField, tankSizeX, tankSizeY):
        self.x=x
        self.y=y
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
        if self.x < columns-1 and self.dir == "right":
            self.x += 1
        self.dir="right"
        print(self.x, " - ",self.y)
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_up (self, event):
        self.l["image"] = self.imgU
        if self.y > 0 and self.dir == "up":
            self.y -= 1
        self.dir="up"
        print(self.x, " - ",self.y)
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_left (self, event):
        self.l["image"] = self.imgL
        if self.x > 0 and self.dir == "left": 
            self.x -= 1
        self.dir="left"
        print(self.x, " - ",self.y)
        self.l.place(x=self.x*self.tankSizeX, y=self.y*self.tankSizeY)

    def tank_to_down (self, event):
        self.l["image"] = self.imgD
        if self.y < rows-1 and self.dir == "down":
            self.y += 1
        self.dir="down"
        print(self.x, " - ",self.y)
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


def gencoordinates(m, n):
    seen = []
    while len(seen)<blocksNum :
        x, y = random.randint(1, m), random.randint(1,n)
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

        self.create_playground()
        self.create_game_settings()
        self.creating_score_board()
        self.tanks = []
        self.create_tank(2,2,1)
        #self.bind('<Any-KeyPress>',self.connecting_head_with_keys)

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

    # Creating Snake Moving Settings
    def create_game_settings(self):

        self.roadmap=[(0,0)]
        self.gamevalid=1
        self.score=0
        return

    def create_playground(self):
        blockIds = gencoordinates(rows,columns)
        for i in range(columns):
            for j in range(rows):
                bId = str(j) + "_" + str(i)
                if blockIds.count(bId) > 0 :
                    self.battleField.create_rectangle(i * self.tankSizeX, j * self.tankSizeY,
                            i * self.tankSizeX + self.tankSizeX,
                            j * self.tankSizeY + self.tankSizeY, fill='#A64B00', outline="")
                else :
                    self.battleField.create_rectangle(i * self.tankSizeX, j * self.tankSizeY,
                           i * self.tankSizeX + self.tankSizeX,
                           j * self.tankSizeY + self.tankSizeY, fill='black', outline="")
        return

    def tank_location(self):

        self.battleField.move(self.tank,self.x,self.y)
        x1,y1,x2,y2=self.battleField.coords(self.tank)
        if x1<=0 or y1<=0:
            self.x=0
            self.y=0
            self.game_loss()
        elif self.rootHeight<=y2 or self.rootWidth<=x2:
            self.x=0
            self.y=0
            self.game_loss()
        return

    def tank_block_location(self):
        
        if self.snake_target:
            x1,y1,x2,y2=self.battleField.coords(self.snake_target)
            if len(self.battleField.find_overlapping(x1,y1,x2,y2))!=1:
                self.ba.delete("food")
                self.update_score_board()
        return

    def re_update(self):

        self.tank_location()
        self.tank_block_location()
        return

    def game_loss(self):

        self.battleField.create_text(self.rootWidth/2,self.rootHeight/2,text="Game Over"
                                ,font=('arial 60 bold'),fill='red')
        self.gamevalid=0
        return


if __name__ == '__main__':
    root=main()
    while True:
        root.update()
        root.update_idletasks()
       # root.re_update()
        time.sleep(0.09)