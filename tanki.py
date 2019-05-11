#!/usr/bin/env python3

import tkinter as tk
from PIL import ImageTk, Image
import sys
import time, random
import datetime

# consts
columns = 20
rows = 12

blocksNum = 5

cellSizeX = 50
cellSizeY = 50

rootWidth  = cellSizeX * (columns+4)
rootHeight = cellSizeY * (rows+1)


reloadTime = 5
bulletSpeed = 2

# global variables
resultTime = 0

Tkroot = tk.Tk()
Tkroot.title("City BattleField")
Tkroot.configure(background = 'black')
osx = (Tkroot.winfo_screenwidth() - rootWidth)/2
osy = (Tkroot.winfo_screenheight() - rootHeight)/2
Tkroot.geometry('%dx%d+%d+%d' % (rootWidth, rootHeight, osx, osy))

def start_game():

    sub = tk.Toplevel(Tkroot)
    sub.transient(Tkroot)
    sub.title('Starting game')
    sub.configure(background = 'black')
    sub.geometry('%dx%d+%d+%d' % (rootWidth, rootHeight, osx, osy)) 

    def getYes():
        sub.destroy()

    def getNo():
        startGameText.destroy()
        yes.destroy()
        no.destroy()

        waiting_text = tk.Label(sub,text="Sorry, but it's impossible!\n Waiting for you!",
                            background="black", font=('arial 45 bold'),
                            foreground="white", justify="center")
        waiting_text.place(x=rootWidth/2-8*cellSizeX, y=rootHeight/2-2*cellSizeY)

        ready = tk.Button(sub, text="Ready!", width=15, height=3, 
                        background="white", foreground="black",
                        font="Arial 20 bold", command=getYes)
        ready.place(x=rootWidth/2 -3*cellSizeX, y=rootHeight/2+cellSizeY)


    startGameText = tk.Label(sub,text="Let's start the battle!",
                                background="black", font=('arial 45 bold'),
                                foreground="white", justify="left")
    startGameText.place(x=rootWidth/2-5*cellSizeX, y=rootHeight/2 - 2*cellSizeY)

    yes = tk.Button(sub, text="Yes", width=15, height=3, 
                    background="white", foreground="black",
                    font="Arial 20 bold",command=getYes)
    yes.place(x=rootWidth/2 - 5*cellSizeX, y=rootHeight/2)

    no = tk.Button(sub, text="No", width=15, height=3, 
                    background="white", foreground="black",
                    font="Arial 20 bold",command=getNo)
    no.place(x=rootWidth/2 + 2*cellSizeX, y=rootHeight/2)

blockImage = ImageTk.PhotoImage(Image.open("block.png"))
steel_blockImage = ImageTk.PhotoImage(Image.open("steel_block.png"))
grass_blockImage = ImageTk.PhotoImage(Image.open("grass_block.png"))
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

    def __init__(self, battleField, blocks, steel_blocks, grass_blocks):
        self.known_blocks = blocks
        self.known_steel_blocks = steel_blocks
        self.known_grass_blocks = grass_blocks
        while (True):
            x, y = random.randint(0, columns), random.randint(0,rows)
            if (not((x,y) in self.known_blocks) and
            	not((x,y) in self.known_steel_blocks) and
            	not((x,y) in self.known_grass_blocks)):
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

        if self.dir == "right":
            new_coords = (self.coords[0] + 1, self.coords[1])
            if (new_coords in self.known_grass_blocks):
                self.l["image"] = grass_blockImage
                self.coords = new_coords
            elif (new_coords[0] != columns+1 and not(new_coords in self.known_blocks)
                and not(new_coords in self.known_steel_blocks)):
                self.coords = new_coords
                self.l["image"] = imgR
        else:
            self.dir="right"
            if (self.coords[0],self.coords[1]) in self.known_grass_blocks:
            	self.l["image"] = grass_blockImage
            else:
            	self.l["image"] = imgR

        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_up (self, event):

        if self.dir == "up":
            new_coords = (self.coords[0], self.coords[1] - 1)
            if (new_coords in self.known_grass_blocks):
                self.l["image"] = grass_blockImage
                self.coords = new_coords
            elif (new_coords[1] != -1 and not(new_coords in self.known_blocks)
            and not(new_coords in self.known_steel_blocks)):
                self.coords = new_coords
                self.l["image"] = imgU
        else:
            self.dir="up"
            if (self.coords[0],self.coords[1]) in self.known_grass_blocks:
            	self.l["image"] = grass_blockImage
            else:
            	self.l["image"] = imgU

        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_left (self, event):

        if self.dir == "left":
            new_coords = (self.coords[0] - 1, self.coords[1])
            if (new_coords in self.known_grass_blocks):
                self.l["image"] = grass_blockImage
                self.coords = new_coords
            elif (new_coords[0] != -1 and not(new_coords in self.known_blocks)
            	and not(new_coords in self.known_steel_blocks)):
                self.coords = new_coords
                self.l["image"] = imgL
        else:
            self.dir="left"
            if (self.coords[0],self.coords[1]) in self.known_grass_blocks:
            	self.l["image"] = grass_blockImage
            else:
            	self.l["image"] = imgL

        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

    def tank_to_down (self, event):

        if self.dir == "down":
            new_coords = (self.coords[0], self.coords[1] + 1)
            if (new_coords in self.known_grass_blocks):
            	self.l["image"] = grass_blockImage
            	self.coords = new_coords
            elif (new_coords[1] != rows+1 and not(new_coords in self.known_blocks)
            	and not(new_coords in self.known_steel_blocks)):
                self.coords = new_coords
                self.l["image"] = imgD
        else:
            self.dir="down"
            if (self.coords[0],self.coords[1]) in self.known_grass_blocks:
            	self.l["image"] = grass_blockImage
            else:
            	self.l["image"] = imgD

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

        self.tanks = []
        self.tanks_coords = []        
        self.blocks = []
        self.steel_blocks = []
        self.grass_blocks = []
        self.blocks_coords = []
        self.steel_blocks_coords = []
        self.grass_blocks_coords = []
        self.score=0
        self.gen_blocks(columns, rows, blocksNum, self.tanks_coords)
        self.add_tank(1, self.blocks_coords, self.steel_blocks_coords,
            	      self.grass_blocks_coords)
        self.create_game_settings()
        self.creating_score_board()        

    def get_tanks_coords(self):

        self.tanks_coords = []
        for tank in self.tanks:
            self.tanks_coords.append(tank.coords)

    def add_tank (self, mode, blocks, steel_blocks, grass_blocks):

        tank = Tank(Tkroot, blocks, steel_blocks, grass_blocks)
        tank.bind_buttons(mode)
        self.tanks += [tank] 
        self.tanks_coords = self.get_tanks_coords()

    def quit (self):
        Tkroot.destroy()

    def creating_score_board(self):

        self.gameInfo_text = tk.Label(Tkroot, text="Game Info :", 
                                    bg="black", font=('arial 15 bold'),
                                    fg="white", justify="left")
        self.gameInfo_text.place(x=(columns+2)*cellSizeX-cellSizeX/2, y=2*cellSizeY)

        self.score_Text = tk.Label(Tkroot, text="Blocks left: {}".format(blocksNum - self.score),
                                    bg="black", font=('arial 15 bold'),
                                    fg="white", justify="left")
        self.score_Text.place(x=(columns+2)*cellSizeX+0.25*cellSizeX/4, y=3*cellSizeY)

        self.play_time = tk.Label(Tkroot, text="Time: {}".format(self.time),
                                    bg="black", font=('arial 15 bold'),
                                    fg="white", justify="left")
        self.play_time.place(x=(columns+2)*cellSizeX-cellSizeX/4, y=4*cellSizeY)

        self.q_btn = tk.Button(Tkroot, text=u'Завершить', font='arial 11 bold', 
                            bg="white", fg="black", width=10, height=3,
                            command=self.quit)
        self.q_btn.place(x=(columns+2)*cellSizeX-13, y=7*cellSizeY)
        
    def update_score(self):

    	if self.gamevalid == 1:
        	self.score += 1
        	self.score_Text['text']="Blocks left: {}".format(blocksNum - self.score)

    def create_game_settings(self):

        self.gamevalid=1
        time_init = datetime.datetime.now()
        self.time_init = time_init.hour*3600 + time_init.minute*60 +\
                         time_init.second
        self.time = self.time_init

    def gen_blocks(self, m, n, max, tanks_coords):

        while len(self.blocks_coords) < max:
            x, y = random.randint(0, m), random.randint(0,n)
            if not((x,y) in self.blocks_coords) and not((x,y) in tanks_coords):
                self.blocks_coords.append((x,y))
                self.blocks.append(Block(x,y))

        while len(self.steel_blocks_coords) < max/2:
            x, y = random.randint(0, m), random.randint(0,n)
            if (not((x,y) in self.blocks_coords) and not((x,y) in tanks_coords) 
                and not((x,y) in self.steel_blocks_coords)):
                self.steel_blocks_coords.append((x,y))
                self.steel_blocks.append(steel_Block(x,y))

        while len(self.grass_blocks_coords) < max/2:
            x, y = random.randint(0, m), random.randint(0,n)
            if (not((x,y) in self.blocks_coords) and not((x,y) in tanks_coords) 
                and not((x,y) in self.steel_blocks_coords)
                and not((x,y) in self.grass_blocks_coords)):
                self.grass_blocks_coords.append((x,y))
                self.grass_blocks.append(grass_Block(x,y))

    def remove_block(self, coords):
        
        for b in self.blocks:
            if b.coords == coords:
                b.l.destroy()
                self.blocks.remove(b)
                if not self.blocks:
                    
                    resultTime = self.time

                    for tank in self.tanks:
                        tank.l.destroy()
                        self.tanks.remove(tank)

                    for st_bl in self.steel_blocks:
                        st_bl.l.destroy()
                        self.steel_blocks.remove(st_bl)

                    for gr_bl in self.grass_blocks:
                        gr_bl.l.destroy()
                        self.grass_blocks.remove(gr_bl)

                    restart_game()

    def update_bullets(self):
        if self.gamevalid == 1:
            for tank in self.tanks:
                if tank.reload > 0:
                    tank.reload -= 1
                for bullet in tank.bullets:
                    if bullet.coords in self.blocks_coords:
                        self.blocks_coords.remove(bullet.coords)
                        bullet.l.destroy()
                        tank.bullets.remove(bullet)
                        self.remove_block(bullet.coords)
                        self.update_score()
                    elif bullet.coords in self.steel_blocks_coords:
                        bullet.l.destroy()
                        tank.bullets.remove(bullet)
                    elif bullet.coords in self.grass_blocks_coords:
                        bullet.l.configure(image=grass_blockImage)
                        bullet.move_bullet()
                    else:
                        bullet.move_bullet()
                        if (bullet.coords[0] < 0 or
                           bullet.coords[1] < 0 or
                           bullet.coords[0] > columns or
                           bullet.coords[1] > rows):
                            bullet.l.destroy()
                            tank.bullets.remove(bullet)

    def update_play_time(self):

        if self.gamevalid==1:
            time_now = datetime.datetime.now()
            time_now_readable_format = time_now.hour*3600 + time_now.minute*60 +\
                                         time_now.second        
            self.time = time_now_readable_format - self.time_init
            self.play_time['text']="Time: {}".format(self.time)

class Block:
    def __init__ (self, x, y):
        self.coords = (x, y)
        self.l=tk.Label(
              Tkroot
            , image = blockImage
            , height = cellSizeY-4
            , width = cellSizeX-4
            )
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

class steel_Block:
    def __init__ (self, x, y):
        self.coords = (x, y)
        self.l=tk.Label(
              Tkroot
            , image = steel_blockImage
            , height = cellSizeY-4
            , width = cellSizeX-4
            )
        self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)

class grass_Block:
    def __init__ (self, x, y):
        self.coords = (x, y)
        self.l=tk.Label(
              Tkroot
            , image = grass_blockImage
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
                self.l.configure(image=bullUp)
                self.coords = (self.coords[0], self.coords[1] - 1)
            if self.dir == "down":
                self.l.configure(image=bullDown)
                self.coords = (self.coords[0], self.coords[1] + 1)
            if self.dir == "left":
                self.l.configure(image=bullLeft)
                self.coords = (self.coords[0] - 1, self.coords[1])
            if self.dir == "right":
                self.l.configure(image=bullRight)
                self.coords = (self.coords[0] + 1, self.coords[1])
            self.l.place(x=self.coords[0]*cellSizeX, y=self.coords[1]*cellSizeY)
        else:
            self.speed -= 1;

def restart_game():

    sub = tk.Toplevel(Tkroot)
    sub.transient(Tkroot)
    sub.title('Starting game')
    sub.configure(background = 'black')
    sub.geometry('%dx%d+%d+%d' % (rootWidth, rootHeight, osx, osy)) 

    def getNo():
        sub.destroy()
        Tkroot.destroy()

    def getYes():
        sub.destroy()
        start_game()
        field.__init__()


    gameoverText = tk.Label(sub,text="Game over!",
                                bg="black", font=('arial 45 bold'),
                                fg="white", justify="left")
    gameoverText.place(x=rootWidth/2-5*cellSizeX, y=rootHeight/2 - 3*cellSizeY)

    resultText = tk.Label(sub, text="You broke all blocks in {} seconds".format(resultTime), 
                    bg="black", fg="white",
                    font="Arial 20 bold", justify="left")
    resultText.place(x=rootWidth/2 - 5*cellSizeX, y=rootHeight/2-cellSizeY)

    restartText = tk.Label(sub, text="Do you want to replay ?", 
                    bg="black", fg="white",
                    font="Arial 40 bold", justify="left")
    restartText.place(x=rootWidth/2 - 5*cellSizeX, y=rootHeight/2 + cellSizeY)

    yes = tk.Button(sub, text="Yes", width=15, height=3, 
                    background="white", foreground="black",
                    font="Arial 20 bold",command=getYes)
    yes.place(x=rootWidth/2 - 5*cellSizeX, y=rootHeight/2+2.5*cellSizeY)

    no = tk.Button(sub, text="No", width=15, height=3, 
                    background="white", foreground="black",
                    font="Arial 20 bold",command=getNo)
    no.place(x=rootWidth/2 + 2*cellSizeX, y=rootHeight/2+2.5*cellSizeY)

if __name__ == '__main__':
    
    Tkroot.resizable(False, False)

    start_game()

    field = Field()

    while True:
        Tkroot.update()
        Tkroot.update_idletasks()
        field.update_bullets()
        field.update_play_time()
        time.sleep(0.001)
