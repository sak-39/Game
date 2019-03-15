#maze game
import pygame
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)
NAVY = (0,0,128)
WIDTH = 640
HEIGHT = 480


# 幅と奥行きの設定 (どちらも奇数である必要がある)
print("\n\n###### 宝探しゲームへようこそ ######\n\nはじめに縦横5x5以上の奇数を入力してください\n\n\n")
#height = 35 #25
height = int(input("(height):"))
#width = 45  #35
width = int(input("(width) :"))
maze = [[1 if 0<i<width-1 else 0 for i in range(width)] if 0<j<height-1 else [0 for i in range(width)] for j in range(height)] #通路:0 壁:1



pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myfont = pygame.font.Font(None,48)
myclock = pygame.time.Clock()
bgx = 0 # BG offset
bgy = 0
size = 32 #sprite size

#sprite class
class Spclass(pygame.sprite.Sprite):
    def __init__(self,x,y,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey)
        self.x = x
        self.y = y
        self.walking = 0
        self.rect = self.image.get_rect()

#player
class Player(Spclass):
    def update(self):
        global bgx,bgy

        x1 = [0,1,0,-1]
        y1 = [-1,0,1,0]
        if self.walking == 0:
            newdir = -1
            press = pygame.key.get_pressed()
            if press[pygame.K_UP]: newdir = 0
            if press[pygame.K_RIGHT]: newdir = 1
            if press[pygame.K_DOWN]: newdir = 2
            if press[pygame.K_LEFT]: newdir = 3
            if newdir != -1:
                newx = int(self.x/size) + x1[newdir]
                newy = int(self.y/size) + y1[newdir]
                if maze[newy][newx] == 0:
                    self.dir = newdir
                    self.walking = 1
        else:
            self.x += x1[self.dir] * 4
            self.y += y1[self.dir] * 4
            if (self.x%size)==0 and (self.y%size)==0:
                self.walking = 0

        # 画面のスクロール処理
        if self.x - bgx < 160 :bgx -= 3
        if self.x - bgx >= WIDTH - 160 :bgx += 3
        if self.y - bgy < 160 :bgy -= 3
        if self.y - bgy >= HEIGHT - 160 : bgy += 3
        self.rect.left = self.x - bgx
        self.rect.top = self.y - bgy
        # 衝突判定
        hitlist = pygame.sprite.spritecollide(self,allgroup,False)
        if len(hitlist) >= 2:
            imagetext = myfont.render("GOAL!",True,WHITE)
            screen.blit(imagetext,(260,150))

#box
class Box(Spclass):
    def update(self):
        global bgx, bgy
        self.rect.left = self.x - bgx
        self.rect.top = self.y - bgy

# 迷路データ(仮)
bgdata = [
    "11111111111111111111",
    "1 1     1   1      1",
    "1   111 1 1 1111 1 1",
    "11111     1 1    1 1",
    "1   111111 1 1111 1",
    "1 1   1   1 1    1 1",
    "111 1   1 1   11 1 1",
    "1   11111 111 11 1 1",
    "1 1  1      1 1  1 1",
    "11111111111111111111"
]



def mazeprint(maze):  #数字で表現された面を●や◯に変換する関数
    c_dict={0:"□",  1:"■"}
    c_maze = [[c_dict[maze[j][i]] for i in range(width)] for j in range(height)]
    for i in range(height):
            print("".join(c_maze[i]) )
    print("")


#開始点を定める
wl = [[2*i+2,2*j+2] for i in range(int((width-1)/2)-1) for j in range(int((height-1)/2)-1)] #未探索リスト
stt = wl.pop(random.randint(0, len(wl)-1)) #ランダムに開始点を定める
ps = [stt]  #探索済みリスト
#print("start Point: ", stt)
maze[stt[1]][stt[0]] = 0  #壁(1)を通路(0)に書き換える
#mazeprint(maze)  #迷路出力

#探索する
dr =[[-1,0], [1,0], [0,-1], [0,1]] #探索方向のリスト

while(len(wl)>0):
    random.shuffle(dr)  #探索方向順をランダムに
    for i in range(4):  #このfor文内ではある座標sttの周辺４方向に対する探索のみ行う
        nxtx = stt[0]+dr[i][0]*2 #探索候補のx座標
        nxty = stt[1]+dr[i][1]*2 #探索候補のy座標
        if maze[nxty][nxtx]==1 :  #2マス先が通路でないとき
            wl.remove([nxtx,nxty])  #未探索リストから削除
            ps.append([nxtx,nxty])  #探索済みリストに追加
            maze[nxty][nxtx] = 0 #2マス先を通路に変更
            maze[nxty-dr[i][1]][nxtx-dr[i][0]] = 0 #1マス先を通路に変更
            break
            if i==3:
                ps.remove([nxtx,nxty])
        stt = ps[random.randint(0, len(ps)-1)]

#完成した迷路を出力
mazeprint(maze)

blockimage = pygame.image.load("block.png").convert()
bgimage = pygame.Surface((size*width,size*height))
bgimage.fill(NAVY)

#boxの座標x
#def box_x():
#    xbox = random.randint(2,width-3)
#    if xbox == 2: return xbox
#    elif xbox == (width-3): return int(xbox)
#    elif xbox % 2 == 0: return int(xbox)
xbox1 = random.randint(2,width-3)
if xbox1 == 2: pass
elif xbox1 == width-3: pass
elif xbox1 % 2 != 0: xbox1 += 1
xbox2 = random.randint(2,width-3)
if xbox2 == 2: pass
elif xbox2 == width-3: pass
elif xbox2 % 2 != 0: xbox2 += 1
#boxの座標y
#def box_y():
#    ybox = random.randint(2,height-3)
#    if ybox == 2: return ybox
#    elif ybox == (height-3): return int(ybox)
#    elif ybox % 2 == 0: return int(ybox)
ybox1 = random.randint(2,height-3)
if ybox1 == 2: pass
elif ybox1 == height-3: pass
elif ybox1 % 2 != 0: ybox1 += 1
ybox2 = random.randint(2,height-3)
if ybox2 == 2: pass
elif ybox2 == height-3: pass
elif ybox2 % 2 != 0: ybox2 +=1

# 迷路を描画する
for y in range(height):
    for x in range (width):
        if (maze[y][x] ==0): continue
        bgimage.blit(blockimage, (size*x,size*y))

allgroup = pygame.sprite.Group()
box = Box(size*xbox1, size*ybox1, "box.png")
allgroup.add(box)
player = Player(size*xbox2, size*ybox2, "tenshi32.png")   #default (2, 2)
allgroup.add(player)
endflag = 0

#main loop
while endflag == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: endflag = 1

    screen.fill(BLACK)
    # 迷路の表示
    screen.blit(bgimage, (-bgx,-bgy))
    allgroup.update()
    allgroup.draw(screen)
    myclock.tick(60)
    pygame.display.flip()

pygame.quit()
