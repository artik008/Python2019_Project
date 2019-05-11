#!/usr/bin/env python3

""" importing modules """
import time
import random
import datetime
import tkinter as tk
from PIL import ImageTk, Image

# consts
COLUMNS = 20
ROWS = 12

BLOCKS_NUM = 50

CELL_SIZE_X = 50
CELL_SIZE_Y = 50

ROOT_WIDTH = CELL_SIZE_X * (COLUMNS+4)
ROOT_HEIGHT = CELL_SIZE_Y * (ROWS+1)

RELOAD_TIME = 5
BULLET_SPEED = 2

TK_ROOT = tk.Tk()
TK_ROOT.title("City BattleField")
TK_ROOT.configure(background='black')
OSX = (TK_ROOT.winfo_screenwidth() - ROOT_WIDTH)/2
OSY = (TK_ROOT.winfo_screenheight() - ROOT_HEIGHT)/2
TK_ROOT.geometry('%dx%d+%d+%d' % (ROOT_WIDTH, ROOT_HEIGHT, OSX, OSY))

BLOCK_IMAGE = ImageTk.PhotoImage(Image.open("block.png"))
STEEL_BLOCK_IMAGE = ImageTk.PhotoImage(Image.open("STEEL_BLOCK.png"))
GRASS_BLOCK_IMAGE = ImageTk.PhotoImage(Image.open("GRASS_BLOCK.png"))
IMG_R = ImageTk.PhotoImage(Image.open("tank-right.png"))
IMG_LABEL = ImageTk.PhotoImage(Image.open("tank-left.png"))
IMG_U = ImageTk.PhotoImage(Image.open("tank-up.png"))
IMG_D = ImageTk.PhotoImage(Image.open("tank-down.png"))
BULL_RIGHT = ImageTk.PhotoImage(Image.open("bullet-right.png"))
BULL_LEFT = ImageTk.PhotoImage(Image.open("bullet-left.png"))
BULL_UP = ImageTk.PhotoImage(Image.open("bullet-up.png"))
BULL_DOWN = ImageTk.PhotoImage(Image.open("bullet-down.png"))


def start_game():
    """ function generating starting menu """

    sub = tk.Toplevel(TK_ROOT)
    sub.transient(TK_ROOT)
    sub.title('Starting game')
    sub.configure(background='black')
    sub.geometry('%dx%d+%d+%d' % (ROOT_WIDTH, ROOT_HEIGHT, OSX, OSY))

    def get_yes():
        """ function destroing sub frame """
        sub.destroy()

    def get_no():
        """ function destroing all widjets and generating new ones """
        start_game_text.destroy()
        yes_answer.destroy()
        no_answer.destroy()

        waiting_text = tk.Label(sub,
                                text="Sorry, but it's impossible!\n/\
                                Waiting for you!",
                                bg="black", font=('arial 45 bold'),
                                fg="white", justify="center")
        waiting_text.place(x=ROOT_WIDTH/2-8*CELL_SIZE_X,
                           y=ROOT_HEIGHT/2-2*CELL_SIZE_Y)

        ready = tk.Button(sub, text="Ready!", width=15, height=3,
                          bg="white", fg="black",
                          font="Arial 20 bold", command=get_yes)
        ready.place(x=ROOT_WIDTH/2 - 3*CELL_SIZE_X,
                    y=ROOT_HEIGHT/2 + CELL_SIZE_Y)

    start_game_text = tk.Label(sub, text="Let's start the battle!",
                               bg="black", font=('arial 45 bold'),
                               fg="white", justify="left")
    start_game_text.place(x=ROOT_WIDTH/2-5*CELL_SIZE_X,
                          y=ROOT_HEIGHT/2 - 2*CELL_SIZE_Y)

    yes_answer = tk.Button(sub, text="Yes", width=15, height=3,
                           bg="white", fg="black",
                           font="Arial 20 bold", command=get_yes)
    yes_answer.place(x=ROOT_WIDTH/2 - 5*CELL_SIZE_X, y=ROOT_HEIGHT/2)

    no_answer = tk.Button(sub, text="No", width=15, height=3,
                          bg="white", fg="black",
                          font="Arial 20 bold", command=get_no)
    no_answer.place(x=ROOT_WIDTH/2 + 2*CELL_SIZE_X, y=ROOT_HEIGHT/2)


def open_image(f_path):
    """ function opening pictures """
    return ImageTk.PhotoImage(Image.open(f_path))


class Tank(object):
    """ class tank """

    def __init__(self, BLOCKS, STEEL_BLOCKS, GRASS_BLOCKS):
        self.KNOWN_BLOCKS = BLOCKS
        self.KNOWN_STEEL_BLOCKS = STEEL_BLOCKS
        self.KNOWN_GRASS_BLOCKS = GRASS_BLOCKS
        while True:
            _x, _y = random.randint(0, COLUMNS), random.randint(0, ROWS)
            if(not (_x, _y) in self.KNOWN_BLOCKS and
               not (_x, _y) in self.KNOWN_STEEL_BLOCKS and
               not (_x, _y) in self.KNOWN_GRASS_BLOCKS):
                self.coords = (_x, _y)
                break
        self.dir = "up"
        self.reload = RELOAD_TIME
        self.bullets = []
        self.label = tk.Label(
            TK_ROOT,
            image=IMG_U,
            height=CELL_SIZE_Y-4,
            width=CELL_SIZE_X-4
            )
        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def tank_to_right(self, event):
        """ tank move to the right direction """

        if self.dir == "right":
            new_coords = (self.coords[0] + 1, self.coords[1])
            if new_coords in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
                self.coords = new_coords
            elif (new_coords[0] != COLUMNS+1 and
                  new_coords not in self.KNOWN_BLOCKS
                  and new_coords not in self.KNOWN_STEEL_BLOCKS):
                self.coords = new_coords
                self.label["image"] = IMG_R
        else:
            self.dir = "right"
            if(self.coords[0], self.coords[1]) in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
            else:
                self.label["image"] = IMG_R

        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def tank_to_up(self, event):
        """ tank move to the up direction """

        if self.dir == "up":
            new_coords = (self.coords[0], self.coords[1] - 1)
            if new_coords in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
                self.coords = new_coords
            elif (new_coords[1] != -1 and new_coords not in self.KNOWN_BLOCKS
                  and new_coords not in self.KNOWN_STEEL_BLOCKS):
                self.coords = new_coords
                self.label["image"] = IMG_U
        else:
            self.dir = "up"
            if (self.coords[0], self.coords[1]) in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
            else:
                self.label["image"] = IMG_U

        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def tank_to_left(self, event):
        """ tank move to the left direction """

        if self.dir == "left":
            new_coords = (self.coords[0] - 1, self.coords[1])
            if new_coords in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
                self.coords = new_coords
            elif(new_coords[0] != -1 and new_coords not in self.KNOWN_BLOCKS
                 and new_coords not in self.KNOWN_STEEL_BLOCKS):
                self.coords = new_coords
                self.label["image"] = IMG_LABEL
        else:
            self.dir = "left"
            if (self.coords[0], self.coords[1]) in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
            else:
                self.label["image"] = IMG_LABEL

        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def tank_to_down(self, event):
        """ tank move to the down direction """

        if self.dir == "down":
            new_coords = (self.coords[0], self.coords[1] + 1)
            if new_coords in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
                self.coords = new_coords
            elif (new_coords[1] != ROWS+1 and
                  new_coords not in self.KNOWN_BLOCKS
                  and new_coords not in self.KNOWN_STEEL_BLOCKS):
                self.coords = new_coords
                self.label["image"] = IMG_D
        else:
            self.dir = "down"
            if (self.coords[0], self.coords[1]) in self.KNOWN_GRASS_BLOCKS:
                self.label["image"] = GRASS_BLOCK_IMAGE
            else:
                self.label["image"] = IMG_D

        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def tank_fire(self, event):
        """ tank fires """

        if self.reload == 0:
            _b = BULLET(self.coords, self.dir)
            self.bullets.append(_b)
            self.reload = RELOAD_TIME

    def quit(self, event):
        """ destroy all  """
        TK_ROOT.destroy()

    def bind_buttons(self, mode=1):
        """ bind buttons to all tank movements """

        if mode == 1:
            self.label.focus_set()
            self.label.bind('<Escape>', self.quit)
            self.label.bind('<Up>', self.tank_to_up)
            self.label.bind('<Right>', self.tank_to_right)
            self.label.bind('<Down>', self.tank_to_down)
            self.label.bind('<Left>', self.tank_to_left)
            self.label.bind('<space>', self.tank_fire)
        if mode == 2:
            self.label.focus_set()
            self.label.bind('<W>', self.tank_to_up)
            self.label.bind('<D>', self.tank_to_right)
            self.label.bind('<S>', self.tank_to_down)
            self.label.bind('<A>', self.tank_to_left)


class FIELD(object):
    """ class Field """

    def __init__(self):

        self.tanks = []
        self.tanks_coords = []
        self.BLOCKS = []
        self.STEEL_BLOCKS = []
        self.GRASS_BLOCKS = []
        self.BLOCKS_COORDS = []
        self.STEEL_BLOCKS_COORDS = []
        self.GRASS_BLOCKS_COORDS = []
        self.score = 0
        self.gen_blocks(COLUMNS, ROWS, BLOCKS_NUM, self.tanks_coords)
        self.add_tank(1, self.BLOCKS_COORDS, self.STEEL_BLOCKS_COORDS,
                      self.GRASS_BLOCKS_COORDS)
        self.create_game_settings()
        self.creating_score_board()

    def get_tanks_coords(self):
        """ get tank coords"""

        self.tanks_coords = []
        for tank in self.tanks:
            self.tanks_coords.append(tank.coords)

    def add_tank(self, mode, BLOCKS, STEEL_BLOCKS, GRASS_BLOCKS):
        """ adding tank to game """

        tank = Tank(BLOCKS, STEEL_BLOCKS, GRASS_BLOCKS)
        tank.bind_buttons(mode)
        self.tanks += [tank]
        self.tanks_coords = self.get_tanks_coords()

    def quit(self, event):
        """ destroy all """
        TK_ROOT.destroy()

    def creating_score_board(self):
        """ creating score info """

        self.game_info_text = tk.Label(TK_ROOT, text="Game Info :",
                                       bg="black", font=('arial 15 bold'),
                                       fg="white", justify="left")
        self.game_info_text.place(x=(COLUMNS+2)*CELL_SIZE_X-CELL_SIZE_X/2,
                                  y=2*CELL_SIZE_Y)

        self.score_text = tk.Label(TK_ROOT, text="BLOCKS left: {}".
                                   format(BLOCKS_NUM - self.score),
                                   bg="black", font=('arial 15 bold'),
                                   fg="white", justify="left")
        self.score_text.place(x=(COLUMNS+2)*CELL_SIZE_X-CELL_SIZE_X/2,
                              y=3*CELL_SIZE_Y)

        self.play_time = tk.Label(TK_ROOT, text="Time: {}".format(self.time),
                                  bg="black", font=('arial 15 bold'),
                                  fg="white", justify="left")
        self.play_time.place(x=(COLUMNS+2)*CELL_SIZE_X-CELL_SIZE_X/2,
                             y=4*CELL_SIZE_Y)

        self.q_btn = tk.Button(TK_ROOT, text='Exit', font='arial 11 bold',
                               bg="white", fg="black", width=10, height=3)
        self.q_btn.bind("<Button-1>", self.quit)
        self.q_btn.place(x=(COLUMNS+2)*CELL_SIZE_X-13, y=7*CELL_SIZE_Y)

    def update_score(self):
        """ updating score boards """

        if self.gamevalid == 1:
            self.score += 1
            self.score_text['text'] = "BLOCKS left: {}".\
                                      format(BLOCKS_NUM - self.score)

    def create_game_settings(self):
        """ create time settings """

        self.gamevalid = 1
        time_init = datetime.datetime.now()
        self.time_init = time_init.hour*3600 + time_init.minute*60 +\
            time_init.second
        self.time = self.time_init

    def gen_blocks(self, _m, _n, max_value, tanks_coords):
        """ generate game field """

        while len(self.BLOCKS_COORDS) < max_value:
            _x, _y = random.randint(0, _m), random.randint(0, _n)
            if((_x, _y) not in self.BLOCKS_COORDS and
               (_x, _y) not in tanks_coords):
                self.BLOCKS_COORDS.append((_x, _y))
                self.BLOCKS.append(BLOCK(_x, _y))

        while len(self.STEEL_BLOCKS_COORDS) < max_value/2:
            _x, _y = random.randint(0, _m), random.randint(0, _n)
            if((_x, _y) not in self.BLOCKS_COORDS and
               (_x, _y) not in tanks_coords and
               (_x, _y) not in self.STEEL_BLOCKS_COORDS):
                self.STEEL_BLOCKS_COORDS.append((_x, _y))
                self.STEEL_BLOCKS.append(STEEL_BLOCK(_x, _y))

        while len(self.GRASS_BLOCKS_COORDS) < max_value/2:
            _x, _y = random.randint(0, _m), random.randint(0, _n)
            if((_x, _y) not in self.BLOCKS_COORDS and
               (_x, _y) not in tanks_coords and
               (_x, _y) not in self.STEEL_BLOCKS_COORDS and
               (_x, _y) not in self.GRASS_BLOCKS_COORDS):
                self.GRASS_BLOCKS_COORDS.append((_x, _y))
                self.GRASS_BLOCKS.append(GRASS_BLOCK(_x, _y))

    def remove_block(self, coords):
        """ deleting blocks """

        for _b in self.BLOCKS:
            if _b.coords == coords:
                _b.label.destroy()
                self.BLOCKS.remove(_b)
                if not self.BLOCKS:

                    for tank in self.tanks:
                        tank.label.destroy()
                        self.tanks.remove(tank)

                    for st_bl in self.STEEL_BLOCKS:
                        st_bl.label.destroy()
                        self.STEEL_BLOCKS.remove(st_bl)

                    for gr_bl in self.GRASS_BLOCKS:
                        gr_bl.label.destroy()
                        self.GRASS_BLOCKS.remove(gr_bl)

                    restart_game(self.time)

    def update_bullets(self):
        """ update bullet's movement """

        if self.gamevalid == 1:
            for tank in self.tanks:
                if tank.reload > 0:
                    tank.reload -= 1
                for bullet in tank.bullets:
                    if bullet.coords in self.BLOCKS_COORDS:
                        self.BLOCKS_COORDS.remove(bullet.coords)
                        bullet.label.destroy()
                        tank.bullets.remove(bullet)
                        self.remove_block(bullet.coords)
                        self.update_score()
                    elif bullet.coords in self.STEEL_BLOCKS_COORDS:
                        bullet.label.destroy()
                        tank.bullets.remove(bullet)
                    elif bullet.coords in self.GRASS_BLOCKS_COORDS:
                        bullet.label.configure(image=GRASS_BLOCK_IMAGE)
                        bullet.move_bullet()
                    else:
                        bullet.move_bullet()
                        if(bullet.coords[0] < 0 or
                           bullet.coords[1] < 0 or
                           bullet.coords[0] > COLUMNS or
                           bullet.coords[1] > ROWS):
                            bullet.label.destroy()
                            tank.bullets.remove(bullet)

    def update_play_time(self):
        """ update playing time """

        if self.gamevalid == 1:
            time_now = datetime.datetime.now()
            time_now_readable_format = time_now.hour*3600 +\
                time_now.minute*60 + time_now.second
            self.time = time_now_readable_format - self.time_init
            self.play_time['text'] = "Time: {}".format(self.time)


class BLOCK(object):
    """ class Block """

    def __init__(self, _x, _y):
        self.coords = (_x, _y)
        self.label = tk.Label(
            TK_ROOT,
            image=BLOCK_IMAGE,
            height=CELL_SIZE_Y-4,
            width=CELL_SIZE_X-4
            )
        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)


class STEEL_BLOCK(object):
    """ class Steel Block """

    def __init__(self, _x, _y):
        self.coords = (_x, _y)
        self.label = tk.Label(
            TK_ROOT,
            image=STEEL_BLOCK_IMAGE,
            height=CELL_SIZE_Y-4,
            width=CELL_SIZE_X-4
            )
        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)


class GRASS_BLOCK(object):
    """ class Grass Block """

    def __init__(self, _x, _y):

        self.coords = (_x, _y)
        self.label = tk.Label(
            TK_ROOT,
            image=GRASS_BLOCK_IMAGE,
            height=CELL_SIZE_Y-4,
            width=CELL_SIZE_X-4
            )
        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)


class BULLET(object):
    """ class Bullet """

    def __init__(self, coords, direction):

        self.speed = BULLET_SPEED
        self.dir = direction

        if direction == "up":
            bull_im = BULL_UP
            self.coords = (coords[0], coords[1] - 1)
        if direction == "left":
            bull_im = BULL_LEFT
            self.coords = (coords[0] - 1, coords[1])
        if direction == "right":
            bull_im = BULL_RIGHT
            self.coords = (coords[0] + 1, coords[1])
        if direction == "down":
            bull_im = BULL_DOWN
            self.coords = (coords[0], coords[1] + 1)

        self.label = tk.Label(
            TK_ROOT,
            image=bull_im,
            height=CELL_SIZE_Y-4,
            width=CELL_SIZE_X-4
            )
        self.label.place(x=self.coords[0]*CELL_SIZE_X,
                         y=self.coords[1]*CELL_SIZE_Y)

    def move_bullet(self):
        """ moving bullet """

        if self.speed == 0:
            self.speed = BULLET_SPEED
            if self.dir == "up":
                self.label.configure(image=BULL_UP)
                self.coords = (self.coords[0], self.coords[1] - 1)
            if self.dir == "down":
                self.label.configure(image=BULL_DOWN)
                self.coords = (self.coords[0], self.coords[1] + 1)
            if self.dir == "left":
                self.label.configure(image=BULL_LEFT)
                self.coords = (self.coords[0] - 1, self.coords[1])
            if self.dir == "right":
                self.label.configure(image=BULL_RIGHT)
                self.coords = (self.coords[0] + 1, self.coords[1])
            self.label.place(x=self.coords[0]*CELL_SIZE_X,
                             y=self.coords[1]*CELL_SIZE_Y)
        else:
            self.speed -= 1


def restart_game(result_time):
    """ restarting game to replay """

    sub = tk.Toplevel(TK_ROOT)
    sub.transient(TK_ROOT)
    sub.title('Starting game')
    sub.configure(background='black')
    sub.geometry('%dx%d+%d+%d' % (ROOT_WIDTH, ROOT_HEIGHT, OSX, OSY))

    def get_no():
        """ destroy all frames """
        sub.destroy()
        TK_ROOT.destroy()

    def get_yes():
        """ restart game """
        sub.destroy()
        start_game()
        FIELD_.__init__()

    gameover_text = tk.Label(sub, text="Game over!",
                             bg="black", font=('arial 45 bold'),
                             fg="white", justify="left")
    gameover_text.place(x=ROOT_WIDTH/2-5*CELL_SIZE_X,
                        y=ROOT_HEIGHT/2 - 3*CELL_SIZE_Y)

    result_text = tk.Label(sub, text="You broke all BLOCKS in {} seconds".
                           format(result_time),
                           bg="black", fg="white",
                           font="Arial 20 bold", justify="left")
    result_text.place(x=ROOT_WIDTH/2 - 5*CELL_SIZE_X,
                      y=ROOT_HEIGHT/2-CELL_SIZE_Y)

    restart_text = tk.Label(sub, text="Do you want to replay ?",
                            bg="black", fg="white",
                            font="Arial 40 bold", justify="left")
    restart_text.place(x=ROOT_WIDTH/2 - 5*CELL_SIZE_X,
                       y=ROOT_HEIGHT/2 + CELL_SIZE_Y)

    yes_answer = tk.Button(sub, text="Yes", width=15, height=3,
                           background="white", foreground="black",
                           font="Arial 20 bold", command=get_yes)
    yes_answer.place(x=ROOT_WIDTH/2 - 5*CELL_SIZE_X,
                     y=ROOT_HEIGHT/2+2.5*CELL_SIZE_Y)

    no_answer = tk.Button(sub, text="No", width=15, height=3,
                          background="white", foreground="black",
                          font="Arial 20 bold", command=get_no)
    no_answer.place(x=ROOT_WIDTH/2 + 2*CELL_SIZE_X,
                    y=ROOT_HEIGHT/2+2.5*CELL_SIZE_Y)


if __name__ == '__main__':

    TK_ROOT.resizable(False, False)

    start_game()

    FIELD_ = FIELD()

    while True:
        TK_ROOT.update()
        TK_ROOT.update_idletasks()
        FIELD_.update_bullets()
        FIELD_.update_play_time()
        time.sleep(0.001)
