from cmu_112_graphics import *
import random

'''

█▀▀ ▄▀█ ▀█▀   █▀▀ █░░ ▄▀█ █▀ █▀
█▄▄ █▀█ ░█░   █▄▄ █▄▄ █▀█ ▄█ ▄█

'''

class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #player movement 
        self.gravity = 10
        self.jump = False

    def getLocation(self):
        return (self.x, self.y)
    
    def catCurrCol(self, blockSize):
        catCCol = (self.x // blockSize) + 1
        return int(catCCol)
    
    def catCurrRow(self, blockSize):
        catCRow = (self.y // blockSize)
        return int(catCRow) 
    
    def jumpMotion(self, yVel):
        if self.jump:
            self.y -= yVel
    
'''

█▀▀ █▄░█ █▀▀ █▀▄▀█ █▄█   █▀▀ █░░ ▄▀█ █▀ █▀
██▄ █░▀█ ██▄ █░▀░█ ░█░   █▄▄ █▄▄ █▀█ ▄█ ▄█

'''

class Enemy:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.maxCol = col + 4
        self.minCol = col - 4
    
    def getRowAndCol(self):
        return (self.row, self.col)

    def move(self, app): 
        if self.col < app.catCCol - 2:
            app.enemyCurrImage = app.enemyR
            self.col += 0.01
        else:
            self.col -= 0.01
            app.enemyCurrImage = app.enemyL

'''

█▀ ▀█▀ █▀█ █▄░█ █▀▀   █▀▀ █░░ ▄▀█ █▀ █▀
▄█ ░█░ █▄█ █░▀█ ██▄   █▄▄ █▄▄ █▀█ ▄█ ▄█

'''

class Stone:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def getRowAndCol(self):
        return (self.row, self.col)

'''

█▀▀ ▄▀█ █▀▄▀█ █▀▀   █▀ █▀▀ ▀█▀ █░█ █▀█
█▄█ █▀█ █░▀░█ ██▄   ▄█ ██▄ ░█░ █▄█ █▀▀

'''

def worldDimensions():
    row = 7
    col = 12
    blockSize = 100
    return (row, col, blockSize)

def playCatGame():
    r, c, bs = worldDimensions()
    width = 0
    height = 0
    for x in range(r):
        height += bs
    for y in range(c):
        width += bs
    runApp(width = width, height = height)

def appStarted(app):
    # game set up
    (app.rows, app.cols, app.blockSize) = worldDimensions()
    app.timerDelay = 0
    app.timer = 0
    app.seconds = 60
    app.scrollX = app.blockSize
    app.score = 0
    app.gameOver = False 
    app.winGame = False
    app.pause = False

    # map
    app.map = []
    numCols = random.randint(app.cols + 50, app.cols + 80)
    for _ in range(app.rows):
        temp = []
        for __ in range(numCols):
            temp.append(0)
        app.map.append(temp)
    app.scrollX = 0
    
    # background
    app.background = app.loadImage('background.png')
    
    # base blocks
    randMapGeneration(app)

    # cat 
    app.cat = Cat(app.width/2, app.blockSize) # implement cat gravity/collision
    app.yVel = 20
    importStripR = app.loadImage("catSpriteR.png")
    importStripL = app.loadImage("catSpriteL.png")
    app.stripScaledR = app.scaleImage(importStripR, 1/3)
    app.spritesR = [ ]
    for i in range(3):
        sprite = app.stripScaledR.crop((260*i, 20, 150+260*i, 220))
        app.spritesR.append(sprite)
    app.stripScaledL = app.scaleImage(importStripL, 1/3)
    app.spritesL = [ ]
    for i in range(3):
        sprite = app.stripScaledL.crop((260*i, 20, 150+260*i, 220))
        app.spritesL.append(sprite)
    app.spriteCounter = 0
    app.catCanPass = True
    app.catCanPassLeft = True
    app.catMoveRight = False
    app.catMoveLeft = False
    app.catCRol = 0
    app.catCCol = 0

    # stones
    app.stones = []
    for i in range(random.randint(8, 15)):
        choices = [3, 5]
        stoneRow = random.choice(choices)
        stoneCol = random.randint(10, len(app.map[stoneRow]) - 7)
        app.map[stoneRow][stoneCol] = random.randint(3, 6)
        currStone = Stone(stoneRow, stoneCol)
        app.stones.append(currStone)
    app.image3 = app.loadImage('rStone.png')
    app.image4 = app.loadImage('gStone.png')
    app.image5 = app.loadImage('yStone.png')
    app.image6 = app.loadImage('bStone.png')
    app.rStoneImage = app.scaleImage(app.image3, 1/3)
    app.gStoneImage = app.scaleImage(app.image4, 1/3)
    app.yStoneImage = app.scaleImage(app.image5, 1/3)
    app.bStoneImage = app.scaleImage(app.image6, 1/3)



    # enemies
    app.enemies = []
    for i in range(5):
        newEnemy = Enemy(5, random.randint(8, len(app.map[0])-7))
        app.enemies.append(newEnemy)
    app.image7 = app.loadImage('enemyR.png')
    app.image8 = app.loadImage('enemyL.png')
    app.enemyR = app.scaleImage(app.image7, 1/4)
    app.enemyL = app.scaleImage(app.image8, 1/4)
    app.enemyCurrImage = app.enemyR

'''

█▀▀ ▄▀█ █▀▄▀█ █▀▀   █▀▀ █▀█ █▄░█ ▀█▀ █▀█ █▀█ █░░ █░░
█▄█ █▀█ █░▀░█ ██▄   █▄▄ █▄█ █░▀█ ░█░ █▀▄ █▄█ █▄▄ █▄▄

'''

def keyPressed(app, event):
    if event.key == "r" or event.key == "R":
       appStarted(app) 
    if not app.gameOver:
        if (event.key == 'p') or (event.key == 'P'):
            app.pause = not app.pause
        if not app.pause:
            if event.key == 'Right' or event.key == "d" or event.key == "D":
                app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesR)
                app.catMoveRight = True
                app.catMoveLeft = False
                app.scrollX += 20
                if not app.catCanPass:
                    app.scrollX -= 20
                app.catCanPass = True
                app.cat.x = (app.scrollX + app.width/2)
            elif event.key == 'Left' or event.key == "a" or event.key == "A":
                app.catMoveLeft = True
                app.catMoveRight = False
                app.spriteCounter = (1 + app.spriteCounter) % len(app.spritesL)
                app.scrollX -= 20
                if (not app.catCanPass) or (not app.catCanPassLeft):
                    app.scrollX += 20
                app.catCanPass = True
                app.catCanPassLeft = True
                app.cat.x = (app.scrollX + app.width/2)
            elif (event.key == 'Space') or (event.key == 'Up') or event.key == "w" or event.key == 'W':
                app.cat.jump = True
            elif (event.key == 'g') or (event.key == 'G'):
                app.gameOver = True

# Jump Motion: https://youtu.be/am2Tb_tj8zM?t=347
def timerFired(app):
    if not app.gameOver:
        if not app.pause:
            # Cat Gravity
            app.catCCol = app.cat.catCurrCol(app.blockSize)
            app.catCRow = app.cat.catCurrRow(app.blockSize)
            catCHeight = getCurrHeight(app, app.catCCol)
            if not app.cat.jump:
                app.cat.y += app.cat.gravity
                if (app.cat.y + 10) > catCHeight:
                    app.cat.y = app.cat.y - app.cat.gravity
            
            # Cat jump
            if app.cat.jump:
                app.cat.jumpMotion(app.yVel)
                app.yVel -= 1
                if app.yVel < -20:
                    app.cat.jump = False 
                    app.yVel = 20
                while (app.cat.y) >= catCHeight:
                    app.cat.y = app.cat.y - app.cat.gravity
            catStoneCollision(app)
            catHorizontalCollision(app)
            catEnemyCollision(app)

            #Map Control
            if app.catCCol <= 7:
                app.catCanPassLeft = False
        
            for enemy in app.enemies:
                enemy.move(app)
            
            app.timer += 1
            if (app.timer % 30 == 0):
                app.seconds -= 1
                if (app.seconds <= 0):
                    app.gameOver = True
            
            
'''

█▀▄▀█ ▄▀█ █▀█   █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█
█░▀░█ █▀█ █▀▀   █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ ░█░ █▄█ █▀▄ 

'''

# Randomized Map Generation with 2d List of 0's and 1's: https://www.youtube.com/watch?v=neTvQEDhZZM&t=605s&ab_channel=ChronoABI
def randMapGeneration(app):
    platRow = 5
    for row in range(len(app.map)):
        if row > platRow:
            for col in range(len(app.map[row])):
                app.map[row][col] = 1

    for row in range(platRow - 1, len(app.map)-2):
        for col in range(0, len(app.map[0])):
            if (random.random() < 0.5) and (app.map[row][col] == 0):
                app.map[row][col] = 2
    
'''

█▀▀ █▀█ █░░ █░░ █ █▀ █ █▀█ █▄░█ █▀
█▄▄ █▄█ █▄▄ █▄▄ █ ▄█ █ █▄█ █░▀█ ▄█

'''

def getCurrHeight(app, currCol):
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            if (col == currCol - 1) and ((app.map[row][col] == 1) or (app.map[row][col] == 2)):
                return (row) * app.blockSize 

def catHorizontalCollision(app):
    for row in range(len(app.map)):
        for col in range(len(app.map[row])):
            if app.map[row][col] == 2 and app.catCRow == row and app.catCCol == col:
                app.catCanPass = False

def catStoneCollision(app):
    temp = []
    for i in range(len(app.stones)):
        sRow, sCol = app.stones[i].getRowAndCol()
        if (sRow == app.catCRow) and (sCol == app.catCCol - 2):
            app.map[sRow][sCol] = 0
            app.score += 1
        else:
            temp.append(app.stones[i])
    app.stones = temp
    if len(app.stones) == 0:
        app.winGame = True
        app.gameOver = True


def catEnemyCollision(app):
    for i in range(len(app.enemies)):
        eRow, eCol = app.enemies[i].getRowAndCol()
        # print(f"eRow {eRow} eCol {eCol}")
        # print(f"cRow {app.catCRow} cCol {app.catCCol}")
        if (eRow == app.catCRow) and (int(eCol + 2) == app.catCCol):
            app.gameOver = True
        
'''

█▀▄ █▀█ ▄▀█ █░█░█   █▀▀ █░█ █▄░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀
█▄▀ █▀▄ █▀█ ▀▄▀▄▀   █▀░ █▄█ █░▀█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█

'''

def generateMap(app, canvas):
    for row in range(len(app.map)):
        for col in range(len(app.map[row])):
            bs = app.blockSize
            x1 = ((col)*bs) - app.scrollX
            y1 = (row)*bs 
            x2 = ((col + 1)*bs) - app.scrollX
            y2 = (row + 1)*bs
            if app.map[row][col] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#8f705c", width=0)
                canvas.create_rectangle(x1, y1, x2, y1+15, fill="#9db89a", width=0)
            elif app.map[row][col] == 2:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#8f7463", width = 0)
                canvas.create_rectangle(x1, y1, x2, y1+15, fill="#9db89a", width=0)
            elif app.map[row][col] == 3:
                canvas.create_image(x2 + 50, y2 - 10, anchor='s', image=ImageTk.PhotoImage(app.rStoneImage))
            elif app.map[row][col] == 4:
                canvas.create_image(x2 + 50, y2 - 10, anchor='s', image=ImageTk.PhotoImage(app.gStoneImage))
            elif app.map[row][col] == 5:
                canvas.create_image(x2 + 50, y2 - 10, anchor='s', image=ImageTk.PhotoImage(app.yStoneImage))
            elif app.map[row][col] == 6:
                canvas.create_image(x2 + 50, y2 - 10, anchor='s', image=ImageTk.PhotoImage(app.bStoneImage))
            # else:
            #     canvas.create_rectangle(x1, y1, x2, y2, width = 1)

def drawCat(app, canvas):
    cx, cy = app.cat.getLocation()
    if app.catMoveLeft:
        sprite = app.spritesL[app.spriteCounter]
        canvas.create_image(app.width/2 + 30, cy + 10, image=ImageTk.PhotoImage(sprite))
    else:
        sprite = app.spritesR[app.spriteCounter]
        canvas.create_image(app.width/2 + 30, cy + 10, image=ImageTk.PhotoImage(sprite))

def drawEnemies(app, canvas):
    for enemy in app.enemies:
        bs = app.blockSize
        row, col = enemy.getRowAndCol()
        x2 = ((col + 1)*bs) - app.scrollX
        y2 = (row + 1)*bs
        canvas.create_image(x2, y2, anchor='s', image=ImageTk.PhotoImage(app.enemyCurrImage))


def drawScoreTimeAndGameOver(app, canvas):
    canvas.create_text(app.width/2, 10, anchor='n', text=f"Time Remaining: {app.seconds}s     Score: {app.score}",
                       font="Comic\ Sans\ MS 16 bold")
                       
    if app.gameOver:
        canvas.create_rectangle(app.width/2 - 350, app.height/2 - 75,
                                 app.width/2 + 350, app.height/2 + 75,
                                 fill="#f0b6b1", outline="#f5eee4", width=7)
        if app.winGame:
            canvas.create_text(app.width/2, app.height/2, anchor="c", text="You Won!  /ᐠ. ᴗ.ᐟ\ﾉ",
                            font="Comic\ Sans\ MS 25 bold", fill="#f5eee4")
        else:
            canvas.create_text(app.width/2, app.height/2, anchor="c", text="Better Luck Next Time  /ᐠ . ֑ . ᐟ\ﾉ",
                            font="Comic\ Sans\ MS 25 bold", fill="#f5eee4")

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    generateMap(app, canvas)
    drawCat(app, canvas)
    drawEnemies(app, canvas)
    drawScoreTimeAndGameOver(app, canvas)

#################################################
# main
#################################################

def main():
    playCatGame()

if __name__ == '__main__':
    main()