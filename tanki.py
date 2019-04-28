#!/usr/bin/env python3

import tkinter as tk
from PIL import ImageTk, Image
import sys
import time, random

# consts
columns = 20
rows = 12

blocsNum = 50

cellSizeX = 50
cellSizeY = 50

rootWidth  = cellSizeX * (columns+1)
rootHeight = cellSizeY * (rows+1)

reloadTime = 5
bulletSpeed = 2

Tkroot = tk.Tk()
Tkroot.configure(background = 'black')

blocImage = ImageTk.PhotoImage(Image.open("bloc.png"))
imgR = ImageTk.PhotoImage(Image.open("tank-right.png"))
imgL = ImageTk.PhotoImage(Image.open("tank-left.png")) 
imgU = ImageTk.PhotoImage(Image.open("tank-up.png")) 
imgD = ImageTk.PhotoImage(Image.open("tank-down.png")) 
bullRight = ImageTk.PhotoImage(Image.open("bullet-right.png"))
bullLeft  = ImageTk.PhotoImage(Image.open("bullet-left.png")) 
bullUp    = ImageTk.PhotoImage(Image.open("bullet-up.png")) 
bullDown  = ImageTk.PhotoImage(Image.open("bullet-down.png")) 

def openImage (fPath):
  return ImageTk.PhotoImage(Image.open(fPath))

class Tank:

    def __init__(self, battleField, blocs):
        self.known_blocs = blocs
        while (True):
            x, y = random.randint(0, columns), random.randint(0,rows)
            if not((x,y) in self.known_blocs):
              self.coords = (x, y)
              break
        self.dir="up"
        self.reload = reloadTime
        self.bullets = []
        self.l=tk.Label(
            Tkroot, 
            image=imgU, 
            height=cellSizeY-4, 
            width=cellSizeX-4
            )
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_right (self, event):
        self.l["image"] = imgR
        if self.dir == "right":
            new_coords = (self.coords[0] + 1, self.coords[1])
            if new_coords[0] != columns+1 and not(new_coords in self.known_blocs):
                self.coords = new_coords
        else:
            self.dir="right"
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_up (self, event):
        self.l["image"] = imgU
        if self.dir == "up":
            new_coords = (self.coords[0], self.coords[1] - 1)
            if new_coords[1] != -1 and not(new_coords in self.known_blocs):
                self.coords = new_coords
        else:
            self.dir="up"
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_left (self, event):
        self.l["image"] = imgL
        if self.dir == "left":
            new_coords = (self.coords[0] - 1, self.coords[1])
            if new_coords[0] != -1 and not(new_coords in self.known_blocs):
                self.coords = new_coords
        else:
            self.dir="left"
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_down (self, event):
        self.l["image"] = imgD
        if self.dir == "down":
            new_coords = (self.coords[0], self.coords[1] + 1)
            if new_coords[1] != rows+1 and not(new_coords in self.known_blocs):
                self.coords = new_coords
        else:
            self.dir="down"
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_fire (self, event):
        if self.reload == 0:
            b = Bullet(self.coords, self.dir)
            self.bullets.append(b)
            self.reload = reloadTime

    def quit (self, event):
        Tkroot.destroy()

    def bind_buttons(self, mode=1):
        if mode == 1:
            self.l.focus_set()
            self.l.bind('<Escape>', self.quit)
            self.l.bind('<Up>', self.tank_to_up)
            self.l.bind('<Right>', self.tank_to_right)
            self.l.bind('<Down>', self.tank_to_down)
            self.l.bind('<Left>', self.tank_to_left)
            self.l.bind('<space>', self.tank_fire)
        if mode == 2:
            self.l.focus_set()
            self.l.bind('<W>', self.tank_to_up)
            self.l.bind('<D>', self.tank_to_right)
            self.l.bind('<S>', self.tank_to_down)
            self.l.bind('<A>', self.tank_to_left)


 

class Field():
    
    def __init__(self):
        self.root = tk.Frame(Tkroot, width=2*cellSizeX, height=(rows+1)*cellSizeY)
        self.root.place(x=(columns+1)*cellSizeX, y=0, )

        self.tanks = []
        self.tanks_coords = []        
        self.blocs = []
        self.blocs_coords = []
        self.gen_blocs(columns,rows, blocsNum, self.tanks_coords)
        self.add_tank(1, self.blocs_coords)
        self.create_game_settings()
        self.creating_score_board()
        
    def get_tanks_coords(self):

        self.tanks_coords = []
        for tank in self.tanks:
            self.tanks_coords.append(tank.coords)


    def add_tank (self, mode, blocs):

        tank = Tank(Tkroot, blocs)
        tank.bind_buttons(mode)
        self.tanks += [tank] 
        self.tanks_coords = self.get_tanks_coords()


    def creating_score_board(self):
        
        self.board = tk.Frame(Tkroot)
        self.score_battleField = tk.Label(Tkroot, text="Score : {}".format(self.score))
        self.score_battleField.place(x=(columns+1)*cellSizeX, y=cellSizeY)


    def update_score_battleField(self):

        self.score += 1
        self.score_battleField['text']="Score : {}".format(self.score)


    def create_game_settings(self):

        self.roadmap=[(0,0)]
        self.gamevalid=1
        self.score=0


    def gen_blocs(self, m, n, max, tanks_coords):
        while len(self.blocs_coords) < max:
            x, y = random.randint(0, m), random.randint(0,n)
            if not((x,y) in self.blocs_coords) and not((x,y) in tanks_coords):
                self.blocs_coords.append((x,y))
                self.blocs.append(Bloc(x, y))

    def remove_bloc(self, coords):
        for b in self.blocs:
            if b.coords == coords:
                b.l.destroy()
                self.blocs.remove(b)


    def update_bullets(self):
        
        for tank in self.tanks:
            if tank.reload > 0:
                tank.reload -= 1
            for bullet in tank.bullets:
                if bullet.coords in self.blocs_coords:
                    self.blocs_coords.remove(bullet.coords)
                    bullet.l.destroy()
                    self.remove_bloc(bullet.coords)
                    tank.bullets.remove(bullet)
                    self.update_score_battleField()
                else:
                    bullet.move_bullet()
                    if (bullet.coords[0] < 0 or
                       bullet.coords[1] < 0 or
                       bullet.coords[0] > columns or
                       bullet.coords[1] > rows):
                        bullet.l.destroy()
                        tank.bullets.remove(bullet)



    def game_loss(self):

        self.battleField.create_text(self.rootWidth/2,self.rootHeight/2,
        				text="Game Over" ,font=('arial 60 bold'),fill='red')
        self.gamevalid=0
        return

class Bloc:
    def __init__ (self, x, y):
        self.coords = (x, y)
        self.l=tk.Label(
              Tkroot
            , image = blocImage
            , height = cellSizeY-4
            , width = cellSizeX-4
            )
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

class Bullet:
    def __init__(self, coords, dir):
        self.speed = bulletSpeed
        self.dir = dir
        if dir == "up":
          bullIm = bullUp
          self.coords = (coords[0], coords[1] - 1)
        if dir == "left":
          bullIm = bullLeft
          self.coords = (coords[0] - 1, coords[1])
        if dir == "right":
          bullIm = bullRight
          self.coords = (coords[0] + 1, coords[1])
        if dir == "down":
          bullIm = bullDown
          self.coords = (coords[0], coords[1] + 1)
        self.l=tk.Label(
              Tkroot
            , image = bullIm
            , height = cellSizeY-4
            , width = cellSizeX-4
            )
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def move_bullet (self):
        if self.speed == 0:
            self.speed = bulletSpeed
            if self.dir == "up":
                self.coords = (self.coords[0], self.coords[1] - 1)
            if self.dir == "down":
                self.coords = (self.coords[0], self.coords[1] + 1)
            if self.dir == "left":
                self.coords = (self.coords[0] - 1, self.coords[1])
            if self.dir == "right":
                self.coords = (self.coords[0] + 1, self.coords[1])
            self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)
        else:
            self.speed -= 1;

if __name__ == '__main__':
    Tkroot.resizable(False, False)

    Tkroot.geometry(str(rootWidth + 2*cellSizeX) + "x" + str(rootHeight) + "+0+0")
    field = Field()

    while True:
        Tkroot.update()
        Tkroot.update_idletasks()
        field.update_bullets()
        time.sleep(0.09)
