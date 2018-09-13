#from sprite import *
#from game import *
from coords import *
from tkinter import *
import time
# 这个叫做精灵🧚‍♀️，哈哈我也不知道为什么叫做这个，就是用来表示一个窗口里面的各个元素，作为之后一些元素的父类
class Sprite:
    def __init__(self,game):
        self.game = game
        # 这个东西都判断游戏结束的标签，只有小人抵达终点才能是True，所以只有在代表终点的门里，这个endGame才会等于True
        self.endgame = False
        # 坐标
        self.coordinates = None
    #一般的精灵都是不会的，所以默认都是pass
    def move(self):
        pass
    def coords(self):
        return self.coordinates
class DoorSprite(Sprite):
    # 输入的参数就是两个不同状态下门的图片，关门和开门，默认关门，之后小人抵达门的时候才会变成开门状态
    # 别的参数就是坐标，宽度，高度
    def __init__(self,game,photo_image1,photo_image2,x,y,width,height):
        Sprite.__init__(self,game)
        self.x = x
        self.y = y
        self.photo_image1 = photo_image1
        self.photo_image2 = photo_image2
        # 这句话就可以在画布上创建一个门，并把这个门的图像返回给self.image，之后需要修改图片的时候操作这个image就行，如果是自己直接创建，就会导致原来的门还在，又出现了一个新的门。
        self.image = game.canvas.create_image(x,y,image = self.photo_image1,anchor='nw')
        self.coordinates = Coords(x,y,x+(width/2),y+height)
        # 门是游戏的重点！所以门的endGame是True
        self.endgame = True
    # 当小人碰到门的时候，执行这个函数，从image1变到image2，这是门精灵特有的函数
    def changeEndImage(self):
        self.game.canvas.itemconfig(self.image,image=self.photo_image2)
# 这个就是平台，游戏里可以承载小人的平台
class PlatformSprite(Sprite):
    def __init__(self,game,photo_image,x,y,width,height):
        Sprite.__init__(self,game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x,y,image=self.photo_image,anchor='nw')
        self.coordinates = Coords(x,y,x+width,y+height)
# 这个就是火柴人啦，我们的主角
class StickSprite(Sprite):
    def __init__(self,game):
        Sprite.__init__(self,game)
        # 小人图片是提前设定好的，而不是初始化的时候输入的
        # 分别就是向左跑的三个动作和向右跑的三个动作
        self.images_left = [
            PhotoImage(file='../image/stick-L1.gif'),
            PhotoImage(file='../image/stick-L2.gif'),
            PhotoImage(file='../image/stick-L3.gif')
        ]
        self.images_right = [
            PhotoImage(file='../image/stick-R1.gif'),
            PhotoImage(file='../image/stick-R2.gif'),
            PhotoImage(file='../image/stick-R3.gif')
        ]
        # 初始化是默认为向右跑的第一个动作
        self.image = game.canvas.create_image(0,450,image=self.images_left[0],anchor='nw')
        # 初始速度
        self.x = 0
        self.y = 0
        # 当前图像
        self.current_image = 0
        # 图片变换的方向，步长
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        # 绑定操作
        game.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        game.canvas.bind_all('<space>',self.jump)
    def turn_left(self,evt):
       # if self.y == 0:
        self.x = -2
    def turn_right(self,evt):
        #if self.y == 0:
        self.x = 2
    #跳跃函数
    def jump(self,evt):
        #只有在没有跳跃的状态才能进行起跳，防止二连跳
        if self.y ==0:
            self.y = -4
            self.jump_count = 0
    def animate(self):
        if self.x != 0 and self.y ==0:
            #每0.1s更换一下图片，刷新自身图片
            #不把刷新做在整体的update里面，可以让不同精灵拥有不同的刷新频率
            if time.time() - self.last_time >0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                #图片更换的顺序为1->2->3->2->1->2...这样连贯一点
                if self.current_image >=2:
                    self.current_image_add =-1
                if self.current_image <=0:
                    self.current_image_add =1
        # 如果速度方向向左
        if self.x<0:
            # 但是如果在起跳状态下，直接是固定的起跳图片
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_left[2])
            # 不是的话，那就在朝左的图片中依次变换
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_left[self.current_image])
        # 和速度向左同理
        elif self.x>0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_right[self.current_image])
    # 小人的体积都是预设的
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0]+27
        self.coordinates.y2 = xy[1]+30
        return self.coordinates
    # 小人的move应该就是整个精髓所在了
    def move(self):
        #首先根据现有状态更新动画，可以放在开头，也可以放在函数最后
        self.animate()
        # 如果小人处于上升状态，那么会不停的计数，等到一定时间之后，小人的速度会向下，模拟重力嘛，但是速度不是连续变化的
        if self.y <0:
            self.jump_count += 1
            if self.jump_count >20:
                self.y =4
        # 下面这个判断之前代码的这么写的，但是今天写备注的时候发现没啥意义，注释之后同样正常工作
        # if self.y >0:
        #     self.jump_count -= 1
        # 获取自身坐标，为接下来的碰撞检测做准备
        co = self.coords()
        # 四个方向是否可以继续走！
        # 为True表示这个方向没有碰到边界，为False表示触碰到了边界，可以是画布边界，也可以是其他精灵的边界
        left = True
        right = True
        top = True
        bottom = True
        # 是否正在下落
        falling = True
        # 下面四个if是用来判断和画布边缘碰撞的
        if self.y >0 and co.y2 >=self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y <0 and co.y1 <=0:
            self.y=0
            top = False
        if self.x >0 and co.x2 >= self.game.canvas_width:
            self.x =0
            right = False
        elif self.x <0 and co.x1 <=0:
            self.x =0
            left = False
        # for循环开始判断和其他精灵的碰撞
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y<0 and collided_top(co,sprite_co):
                self.y=-self.y
                top=False
            if bottom and self.y >0 and collided_bottom(self.y,co,sprite_co):
                self.y=sprite_co.y1-co.y2
                if self.y<0:
                    self.y=0
                bottom=False
                top=False
            if bottom and falling and self.y ==0 \
               and co.y2<self.game.canvas_height \
               and collided_bottom(1,co,sprite_co):
                falling = False
            if left and self.x <0 and collided_left(co,sprite_co):
                self.x=0
                left = False
                # 这个是判断游戏标志，如果碰触到了endgame为True的，running就会呗设置为False，小人就不能跑了，认为游戏结束。同时，对应的这个精灵，其实就是门，也需要执行changeEndImage，修改为开门状态。
                if sprite.endgame:
                    self.game.running = False
                    sprite.changeEndImage()
            if right and self.x >0 and collided_right(co,sprite_co):
                self.x=0
                right = False
        if falling and bottom and self.y ==0 \
           and co.y2 < self.game.canvas_height:
            self.y=4
        # 根据速度移动位置，移动
        self.game.canvas.move(self.image,self.x,self.y)
