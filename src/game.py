from tkinter import *
import random
import time
from coords import *
from sprite import Sprite,PlatformSprite,StickSprite,DoorSprite
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr BlackSheep Run")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost",1)
        self.canvas_height=500
        self.canvas_width=500
        self.canvas = Canvas(self.tk,width=self.canvas_width,height=self.canvas_height,highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.bg = PhotoImage(file='../image/background.gif')
        w = self.bg.width()
        h = self.bg.height()
        # 设置游戏背景
        for x in range(0,5):
            for y in range(0,5):
                self.canvas.create_image(x*w ,y*h ,image=self.bg,anchor='nw')
        # 游戏所以的精灵储存在这里
        self.sprites = []
        self.running = True
    # 运行的时候就执行这个主循环，只要running为True，小人就会不停移动下去
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
# 初始化游戏，填入精灵
game = Game()
# 所以的平台精灵
platform1 = PlatformSprite(game,PhotoImage(file='../image/platform3.gif'),0,480,100,10)
platform2 = PlatformSprite(game,PhotoImage(file='../image/platform3.gif'),150,440,100,10)
platform3 = PlatformSprite(game,PhotoImage(file='../image/platform3.gif'),300,400,100,10)
platform4 = PlatformSprite(game,PhotoImage(file='../image/platform3.gif'),300,160,100,10)
platform5 = PlatformSprite(game,PhotoImage(file='../image/platform2.gif'),175,350,60,10)
platform6 = PlatformSprite(game,PhotoImage(file='../image/platform2.gif'),50,300,60,10)
platform7 = PlatformSprite(game,PhotoImage(file='../image/platform2.gif'),170,120,60,10)
platform8 = PlatformSprite(game,PhotoImage(file='../image/platform2.gif'),45,60,60,10)
platform9 = PlatformSprite(game,PhotoImage(file='../image/platform1.gif'),170,250,30,10)
platform10 = PlatformSprite(game,PhotoImage(file='../image/platform1.gif'),230,200,30,10)
# 初始化之后加入sprites数组中
game.sprites.append(platform1)
game.sprites.append(platform2)
game.sprites.append(platform3)
game.sprites.append(platform4)
game.sprites.append(platform5)
game.sprites.append(platform6)
game.sprites.append(platform7)
game.sprites.append(platform8)
game.sprites.append(platform9)
game.sprites.append(platform10)
# 主角
stick = StickSprite(game)
game.sprites.append(stick)
# 门
door = DoorSprite(game,PhotoImage(file='../image/door1.gif'),PhotoImage(file='../image/door2.gif'),45,30,40,35)
game.sprites.append(door)
# 启动游戏
game.mainloop()
