"""
Author: Carson Ellsworth
Date Finished: 03-21-20
Reason: Wanted a good introduction project to the curses library and it is
a good way to spend time during the apocalypse /s
Instructions:
    Controls are W A S D 
    run this line below in your terminal to play the game
    python3 cursedsnake.py
have fun!
"""
import curses
import random
import time
import math

class segment():
    def __init__(self,x,y,head:bool):
        self.x = x
        self.y = y
        if(head):
            self.c = curses.COLOR_CYAN
        else:
            self.c = curses.COLOR_BLUE
            
    def __repr__(self):
        return "\u2591"
    def curse_yx(self):
        return self.y,self.x

class food():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "\u03c0"
    
def gen_food(food_list:list,snake_list:list,dim:tuple):
    food_list.clear()
    x_max,y_max = dim
    x = int(random.randint(1,x_max-2))
    y = int(random.randint(1,y_max-2))
    good = False
    while(not good):
        good = True
        for seg in snake_list:
            if (x == seg.x and y == seg.y):
                x = int(random.randint(1,x_max-2))
                y = int(random.randint(1,y_max-2))
                good = False
                break
        
    food_list.append(food(x,y))

def update_food(prtscr,food_list:list):
    bite = food_list[0]
    prtscr.addstr(bite.y,bite.x,str(bite))
    pass


def update_snake(prtscr,snake_list:list,direct:tuple,grow_flag,dim)-> bool:
    prev_pos = (0,0)
    tail_pos = (0,0)
    for seg in snake_list:
        if(seg is snake_list[0]):
            if(seg is snake_list[-1]):
                tail_pos = (seg.x,seg.y)
            prev_pos = (seg.x,seg.y)
            seg.x += direct[0]
            seg.y += direct[1]
            if(seg.x < 0 or seg.y < 0 or seg.x >= dim[0] or seg.y >= dim[1]):
                prtscr.addstr(dim[1]-1,0,"OUT OF BOUNDS")
                return False
        else:
            seg.x, seg.y,prev_pos = prev_pos[0],prev_pos[1],(seg.x,seg.y)
        prtscr.addstr(seg.curse_yx()[0],seg.curse_yx()[1],str(seg),seg.c)
    if(grow_flag):
        #grow snake
        new_tail = segment(tail_pos[0],tail_pos[1],False)
        snake_list.append(new_tail)
    return True


def valid_head(prtscr,snake_list:list,dim:tuple) -> bool:
    head=snake_list[0]
    for seg in snake_list[1:-1]:
        if(head.x == seg.x and head.y == seg.y):
            prtscr.addstr(dim[1]-1,0,"OUCH I BIT ME")
            return False
    return True


def grow_check(prtscr,snake_list:list,food_list:list,dim)->bool:
    head = snake_list[0]
    food = food_list[0]
    if(head.x == food.x and head.y == food.y):
        gen_food(food_list,snake_list,dim)
        return True #grow snake flag

def snake_win(snake_list:list,dim:tuple):
    snake_len = len(snake_list)
    area = dim[0]*dim[1]
    if(snake_len == area):
        return True
    return False

def main(stdscr):
    # Clear Screen
    stdscr.clear()
    curses.cbreak()
    stdscr.timeout(100)#nodelay on input read
    
    snake = []
    food = []
    dim = curses.COLS,curses.LINES #screen dimensions in x,y
    halfx = int(math.floor(dim[0]/2))
    halfy = int(math.floor(dim[1]/2))
    start_len = 3 #starting length of snake
    
    snake.append(segment(halfx,halfy,True))
    for x in range(1,start_len):
        snake.append(segment(halfx+x,halfy,False))
    update_snake(stdscr,snake,(0,0),False,dim)
    gen_food(food,snake,dim)
    stdscr.refresh()
    
    direct = (-1,0)

    # Calling functions once here to save on efficiency
    ordw = ord('w')
    ords = ord('s')
    orda = ord('a')
    ordd = ord('d')
    prev_key = ordd
    cur_key = orda
    while(True):
        if(cur_key != -1 and cur_key != prev_key):    
            if(cur_key==ordw and prev_key!=ords):
                direct = (0,-1)
                prev_key = cur_key
            elif(cur_key==orda and prev_key!=ordd):
                direct = (-1,0)
                prev_key = cur_key
            elif(cur_key==ords and prev_key!=ordw):
                direct = (0,1)
                prev_key = cur_key
            elif(cur_key==ordd and prev_key!= orda):
                direct = (1,0)
                prev_key = cur_key
        stdscr.clear()
        
        grow_flag = grow_check(stdscr,snake,food,dim)
        update_food(stdscr,food) 
        if(not update_snake(stdscr,snake,direct,grow_flag,dim)):
            break 
        if(not valid_head(stdscr,snake,dim)):
            break
        if(snake_win(snake,dim)):
            breakl
        stdscr.refresh()
        cur_key = stdscr.getch()
    bx,by = 20,7
    h,w = 5,40
    stdscr.refresh()
    stdscr.nodelay(0)
    time.sleep(2)
    stdscr.getkey()
    
curses.wrapper(main)
