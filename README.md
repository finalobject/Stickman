原文在<a href="http://finalobject.cn/lucario/stickman">finalObject</a>

这个也是和<a href="http://finalobject.cn/lucario/hoddle">弹球游戏</a>一样的环境，python3+tkinter，所以环境配置可以参考前一篇。火柴人比前一篇就是多了个一个动画效果，已经更加麻烦的体积碰撞，还有上升下落的物理模拟，还有一个就是游戏成功的检测。<!--more-->

<img class="size-medium wp-image-213 aligncenter" src="http://finalobject.cn/wp-content/uploads/2018/09/stickman-2-300x300.jpg" alt="" width="300" height="300" />
<h1>动画效果</h1>
不像之前的弹球游戏，只有长方形和圆心，直接在程序中绘制就行，这个火柴人里的一些元素图片都需要自己提前准备的。然后<a id="78805a221a988e79ef3f42d7c5bfd418-677e0f078a027273c1e9b7cd1213c400f7d30e92" class="js-navigation-open" title="image" href="https://github.com/finalObject/stickman/tree/master/image">image</a>里就是自己绘制的元素，有点简陋。

<img class="size-medium wp-image-212 aligncenter" src="http://finalobject.cn/wp-content/uploads/2018/09/stickman-1-300x89.jpg" alt="" width="300" height="89" />

承载小人的平台是设定之后就不会变更了的，但是小人和门是存在一个动画效果的。不过门的动画比较特殊，只有在游戏结束的时候才会触发一次，所以比较简单。而小人是需要不断变换图像，从而显示出奔跑状态的。

下面就是小人的动画函数
<pre class="lang:python decode:true ">def animate(self):
        if self.x != 0 and self.y ==0:
            #每0.1s更换一下图片，刷新自身图片
            #不把刷新做在整体的update里面，可以让不同精灵拥有不同的刷新频率
            if time.time() - self.last_time &gt;0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                #图片更换的顺序为1-&gt;2-&gt;3-&gt;2-&gt;1-&gt;2...这样连贯一点
                if self.current_image &gt;=2:
                    self.current_image_add =-1
                if self.current_image &lt;=0:
                    self.current_image_add =1
        # 如果速度方向向左
        if self.x&lt;0:
            # 但是如果在起跳状态下，直接是固定的起跳图片
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_left[2])
            # 不是的话，那就在朝左的图片中依次变换
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_left[self.current_image])
        # 和速度向左同理
        elif self.x&gt;0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_right[self.current_image])</pre>
游戏中一个对应的元素（Sprite对象），在画布中创建图像时，会返回一个对象，然后就这个对象储存在self.image中。
<pre class="lang:python decode:true">self.image = game.canvas.create_image(x,y,image = self.photo_image1,anchor='nw')</pre>
如果需要更改图像，需要
<pre class="lang:python decode:true ">self.game.canvas.itemconfig(self.image,image=self.photo_image2)</pre>
如果直接重新创建，会导致原画和新画都出现在屏幕上，而使用itemconfig函数，可以抹出原画，只留下新画。
<h1>体积碰撞</h1>
体积碰撞基础函数写在<a id="f9d2ac11444f74a9e3f939698cf2ae4e-1c9f4066769febeb12c722ab889899e07fb7464b" class="js-navigation-open" title="coords.py" href="https://github.com/finalObject/stickman/blob/master/src/coords.py">coords.py</a>里，包含左右上下坐标是否重叠的检测，在class StickSprite的move()函数里，就基于简单的检测，实现了和画布边缘以及其他Sprite的碰撞检测。
<pre class="lang:python decode:true ">def move(self):
    #首先根据现有状态更新动画，可以放在开头，也可以放在函数最后
    self.animate()
    # 如果小人处于上升状态，那么会不停的计数，等到一定时间之后，小人的速度会向下，模拟重力嘛，但是速度不是连续变化的
    if self.y &lt;0:
        self.jump_count += 1
        if self.jump_count &gt;20:
            self.y =4
    # 下面这个判断之前代码的这么写的，但是今天写备注的时候发现没啥意义，注释之后同样正常工作
    # if self.y &gt;0:
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
    if self.y &gt;0 and co.y2 &gt;=self.game.canvas_height:
        self.y = 0
        bottom = False
    elif self.y &lt;0 and co.y1 &lt;=0:
        self.y=0
        top = False
    if self.x &gt;0 and co.x2 &gt;= self.game.canvas_width:
        self.x =0
        right = False
    elif self.x &lt;0 and co.x1 &lt;=0:
        self.x =0
        left = False
    # for循环开始判断和其他精灵的碰撞
    for sprite in self.game.sprites:
        if sprite == self:
            continue
        sprite_co = sprite.coords()
        if top and self.y&lt;0 and collided_top(co,sprite_co):
            self.y=-self.y
            top=False
        if bottom and self.y &gt;0 and collided_bottom(self.y,co,sprite_co):
            self.y=sprite_co.y1-co.y2
            if self.y&lt;0:
                self.y=0
            bottom=False
            top=False
        if bottom and falling and self.y ==0 \
           and co.y2&lt;self.game.canvas_height \
           and collided_bottom(1,co,sprite_co):
            falling = False
        if left and self.x &lt;0 and collided_left(co,sprite_co):
            self.x=0
            left = False
            # 这个是判断游戏标志，如果碰触到了endgame为True的，running就会呗设置为False，小人就不能跑了，认为游戏结束。同时，对应的这个精灵，其实就是门，也需要执行changeEndImage，修改为开门状态。
            if sprite.endgame:
                self.game.running = False
                sprite.changeEndImage()
        if right and self.x &gt;0 and collided_right(co,sprite_co):
            self.x=0
            right = False
    if falling and bottom and self.y ==0 \
       and co.y2 &lt; self.game.canvas_height:
        self.y=4
    # 根据速度移动位置
    self.game.canvas.move(self.image,self.x,self.y)</pre>
<h1>物理模拟</h1>
主要就是一个小人跳跃过程中的模拟，这里其实很简单地对跳跃进行计时，到达一定时间后就将速度朝小。比较机械，只是很离散的模拟。
<pre class="lang:python decode:true ">if self.y &lt;0:
    self.jump_count += 1
    if self.jump_count &gt;20:
        self.y =4</pre>
然后在检测到碰撞后（上下左右的碰撞），会把对应方向速度置0。

另外，当小人没有产生向下的碰撞时，小人会产生朝下的速度。这样就解决了小人漂浮在空中的bug。
<pre class="lang:python decode:true ">if falling and bottom and self.y ==0 \
   and co.y2 &lt; self.game.canvas_height:
    self.y=4</pre>
<h1>成功检测</h1>
在游戏初始化的时候，部分sprite的endgame属性为True，也就意味它有能力结束游戏，这个游戏里只有顶端的门有这个True。
<pre class="lang:python decode:true ">if left and self.x &lt;0 and collided_left(co,sprite_co):
    self.x=0
    left = False
    # 这个是判断游戏标志，如果碰触到了endgame为True的，running就会呗设置为False，小人就不能跑了，认为游戏结束。同时，对应的这个精灵，其实就是门，也需要执行changeEndImage，修改为开门状态。
    if sprite.endgame:
        self.game.running = False
        sprite.changeEndImage()</pre>
如果小人和门发生了碰撞，就会将running设置位False，然后执行门的结束游戏图像修改的函数，其实就是把门的图像由关变成开。running在Game类的mainloop()函数里控制着整个游戏的进行，如果变成False，小人就不能移动。
<pre class="lang:python decode:true "># 运行的时候就执行这个主循环，只要running为True，小人就会不停移动下去
def mainloop(self):
    while 1:
        if self.running == True:
            for sprite in self.sprites:
                sprite.move()
        self.tk.update_idletasks()
        self.tk.update()
        time.sleep(0.01)</pre>
之前尝试直接把while 1里面所有的东西放放入判断语句中，也就意味着如果running为False，连update和sleep函数都不会执行，但是这样做会导致程序卡死。

另外还有一个不足之处时，我的游戏检测只会在向左碰撞的函数里触发，因为这个场景下小人只可能从右往左抵达门，更加合理的方式，是应该保证发生碰撞一定会执行这个成功检测。

以上基本就是代码的全部内容了，代码已经贴的差不多了，再把全部代码贴上来会显得有点冗长，需要的请移步<a href="https://github.com/finalObject/stickman">github</a>。
