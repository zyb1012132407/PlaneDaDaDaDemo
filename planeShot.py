import copy
import random
import time

import pygame

#
# #都是飞着的东西
# class Base():
#     def __init__(self,windows,x,y):
#         #画画对象
#         self.windows = windows
#         #坐标
#         self.x = x
#         self.y = y
#
# #Base飞机，都是飞给
# class BasePlane(Base):
#     def __init__(self,windows,x,y):
#         #调用父类Base的东西
#         super().__init__(self,windows,x,y)
#         #遍历图片准备的
#         self.nomalIndex = 0
#         self.bombIndex = 0
#         #是不是炸了
#         self.isBomb = False
#
#     def draw(self):
#         pic = pygame.image.load(self.no)
from pygame.rect import Rect


class HeroPlane():
    def __init__(self, windows, x, y):
        # 肯定是画画的东西
        self.windows = windows
        # 坐标
        self.x = x
        self.y = y
        # 正常画面
        self.normalImageList = ['img\\hero1.png', 'img\\hero2.png']
        self.normalIndex = 0
        # Boom！
        self.bombImageList = ['img\\hero_blowup_n1.png',
                              'img\\hero_blowup_n2.png',
                              'img\\hero_blowup_n3.png',
                              'img\\hero_blowup_n4.png', ]
        self.bombIndex = 0
        # 我炸了，真的啊！
        self.isBomb = False
        # 哒哒哒哒哒！
        self.bulletList = []

    def Boom(self, bulletList):

        tempList = bulletList
        PlaneBodyRect = Rect(self.x + 36, self.y, 100 - 36, 40)
        PlaneHeadRect = Rect(self.x, self.y, 100, 124 - 40)
        for bullet in tempList:
            bulletRect = Rect(bullet.x, bullet.y, 9, 21)
            print("子弹坐标" + str(bulletRect) , "机头坐标" + str(PlaneHeadRect) ,"机身坐标" + str(PlaneBodyRect))
            if bulletRect.colliderect(PlaneBodyRect) or bulletRect.colliderect(PlaneHeadRect):
                self.isBomb = True
                bulletList.remove(bullet)

    # 画！
    def draw(self):

        if self.isBomb == False:
            # 画谁。。。。（寻找上面正常飞机图url）
            pic = pygame.image.load(self.normalImageList[self.normalIndex])
            # 画！
            self.windows.blit(pic, (self.x, self.y))
            # 换图
            self.normalIndex = (self.normalIndex + 1) % len(self.normalImageList)
            self.windows.blit(pic, (self.x, self.y))
        # Boom!
        else:
            if self.bombIndex == len(self.bombImageList):
                time.sleep(0.8)
                exit(0)
            pic = pygame.image.load(self.bombImageList[self.bombIndex])
            self.windows.blit(pic, (self.x, self.y))
            self.bombIndex = self.bombIndex + 1
            time.sleep(0.3)

        # 哒哒哒哒哒
        # 先拷贝一份，防止出问题
        tempList = copy.copy(self.bulletList)
        # 一堆哒哒哒哒哒里面循环取哒（因为子弹的轨迹都需要画出来）
        for bullet in tempList:
            # 画！
            bullet.draw()
            # 越界的不用画了
            if bullet.y < 0:
                self.bulletList.remove(bullet)

    # 飞机左歪头（修改坐标）
    def move_right(self):
        if self.x < 480 - 100:
            self.x += 3

    # 飞机右歪头（修改坐标）
    def move_left(self):
        if self.x > 0:
            self.x -= 3

    # 飞机冲了
    def fire(self):
        # 声明一个哒（生成位置肯定是相对于飞机当前的位置）
        bullet = HeroBullet(windows, self.x + 50 - 11, self.y - 22)
        # 将一个哒放到哒哒哒哒哒里面
        self.bulletList.append(bullet)


class HeroBullet():
    # 新的哒出现！
    def __init__(self, windows, x, y):
        self.windows = windows
        self.x = x
        self.y = y
        self.pic = pygame.image.load("img\\bullet.png")

    # 画！
    def draw(self):
        self.windows.blit(self.pic,(self.x,self.y))
        self.move()

    # 动
    def move(self):
        self.y -= 8


# 监听键盘
def control(plane):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plane.move_left()
            elif event.key == pygame.K_RIGHT:
                plane.move_right()
            elif event.key == pygame.K_SPACE:
                plane.fire()


#
class EnemyPlane():

    def __init__(self, windows, x, y):
        self.windows = windows
        self.x = x
        self.y = y
        self.normalImageList = ['img\\enemy1.png']

        self.bombImageList = ['img\\enemy1_down1.png',
                              'img\\enemy1_down2.png',
                              'img\\enemy1_down3.png',
                              'img\\enemy1_down4.png', ]
        self.bombIndex = 0
        self.isBomb = False
        self.bulletList = []
        self.direct = 1

    def Boom(self, bulletList):
        tempList = bulletList
        PlaneBodyRect = Rect(self.x, self.y, 69, 89)
        for bullet in tempList:
            bulletRect = Rect(bullet.x, bullet.y, 22, 22)
            if bulletRect.colliderect(PlaneBodyRect):
                self.isBomb = True
                bulletList.remove(bullet)

    def draw(self):
        if self.isBomb == False:
            pic = pygame.image.load(self.normalImageList[0])
            self.windows.blit(pic, (self.x, self.y))
            self.fire()
        else:
            if self.bombIndex == len(self.bombImageList):
                time.sleep(0.8)
                exit(0)
            pic = pygame.image.load(self.bombImageList[self.bombIndex])
            self.windows.blit(pic,(self.x,self.y))
            self.bombIndex = self.bombIndex + 1
            time.sleep(0.5)

        tempList = copy.copy(self.bulletList)
        for bullet in tempList:
            bullet.draw()
            if bullet.y > 800:
                self.bulletList.remove(bullet)

    def fire(self):
        d = random.randint(1, 100)
        if d == 3 or d == 19:
            bullet = EnemyBullet(self.windows, self.x + 69 // 2 - 9 // 2, 89)
            self.bulletList.append(bullet)



    # 他的哒哒不是我想要的哒哒！（越界前会转向）
    def move(self):
        if self.direct == 1:
            self.x += 5
            if self.x > 480 - 69:
                self.direct = 0
        else:
            self.x -= 5
            if self.x <= 0:
                self.direct = 1


class EnemyBullet():
    def __init__(self, windows, x, y):
        self.windows = windows
        self.x = x
        self.y = y
        self.pic = pygame.image.load("img\\bullet-1.gif")

    def draw(self):
        self.windows.blit(self.pic,(self.x, self.y))
        self.move()

    def move(self):
        self.y += 3


# 加载相关界面
##设置窗口
windows = pygame.display.set_mode((480, 800), 0, 32)
##设置标题
pygame.display.set_caption('飞机大战')
##设置图标(获取图片 并 设置图标)
pygame.display.set_icon(pygame.image.load("img\\icon72x72.png"))
# 设置按键响应(单次按住30ms后响应，之后的操作30ms响应)
pygame.key.set_repeat(30, 30)

heroplane = HeroPlane(windows, 480 // 2 - 100 // 2, 800 - 124)
enemyplane = EnemyPlane(windows, 480 // 2 - 69 // 2, 0)
# 一直刷新
while True:
    ##加载背景(获取图片，并且初位移为(0,0))
    windows.blit(pygame.image.load("img\\background.png"), (0, 0));
    heroplane.draw()
    enemyplane.draw()
    enemyplane.move()
    heroplane.Boom(enemyplane.bulletList)
    enemyplane.Boom(heroplane.bulletList)
    pygame.display.update()
    control(heroplane)

