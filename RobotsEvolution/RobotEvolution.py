import pygame
import random

FIELD_SIZE = 18
WALL_PROB = 0.3
N_ROBOTS_PER_PROG = 10
N_PROGRAMS = 3
GAME_SPEED = 4
scaleX = 40
scaleY = scaleX
N_ITEMS = 30
GameSteps = 0

pygame.font.init()
MyFont = pygame.font.SysFont('Comic Sans MS', 50)

pygame.init()
size = (800, 800)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("My Game")

#LOAD IMAGES
ImageFon = pygame.transform.scale(pygame.image.load(r'pic/fon.png'), (scaleX, scaleY))
ImageWall = pygame.transform.scale(pygame.image.load(r'pic/Rock2.png'), (scaleX, scaleY))
ImageRobot = pygame.transform.scale(pygame.image.load(r'pic/Robot1.png'), (scaleX, scaleY))
ImageRobotShoot = pygame.transform.scale(pygame.image.load(r'pic/Robot2.png'), (scaleX, scaleY))
ImageItemHP = pygame.transform.scale(pygame.image.load(r'pic/item_hp.jpg'), (scaleX, scaleY))
ImageItemEnergy = pygame.transform.scale(pygame.image.load(r'pic/item_energy.jpg'), (scaleX, scaleY))

#LOAD SOUNDS
SoundTake = pygame.mixer.Sound(r'sound/take.wav')

class Robot:
    x = 0
    y = 0
    hp = 10
    Energy = 50
    ViewDirection = 0
    ProgramType = 0
    LastAction = 'Pass'

    def __init__(self, ProgType):
        # create random coordinates in empty place
        self.x = random.randint(0, FIELD_SIZE - 1)
        self.y = random.randint(0, FIELD_SIZE - 1)
        while Field[self.x][self.y] > 0:
            self.x = random.randint(0, FIELD_SIZE - 1)
            self.y = random.randint(0, FIELD_SIZE - 1)

        # random direction
        self.ViewDirection = random.randint(0, 3)

        self.ProgramType = ProgType

    def Color(self):
        if self.ProgramType == 0:
            return 0, 0, 0
        elif self.ProgramType == 1:
            return 255, 0, 0
        elif self.ProgramType == 2:
            return 0, 255, 0

    def CellForward(self):
        xNew = self.x
        yNew = self.y
        if self.ViewDirection == 0:
            yNew += 1
        elif self.ViewDirection == 1:
            xNew += 1
        elif self.ViewDirection == 2:
            yNew -= 1
        elif self.ViewDirection == 3:
            xNew -= 1
        return xNew, yNew

    def View(self):
        xView, yView = self.CellForward()
        if (xView < 0) or (xView >= FIELD_SIZE) or (yView < 0) or (yView >= FIELD_SIZE):
            return 100                  # Out of Field
        elif Field[xView][yView] > 0:
            return Field[xView][yView]  # Wall
        for rbt in Robots:
            if (rbt.x==xView) and (rbt.y==yView):
                return -1               # Robot
        for it in Items:
            if it.x == xView and it.y == yView:
                return -2               # Item
        return 0                        # Empty space

    def IsItemHere(self):
        for it in Items:
            if it.x == self.x and it.y == self.y:
                return True
        return False

    def Action(self, decision):

        xNew, yNew = self.CellForward()

        if decision == 'Step Forward':
            # new coordinates
            # proove in field
            if (xNew < 0) or (xNew >= FIELD_SIZE) or (yNew < 0) or (yNew >= FIELD_SIZE):
                self.LastAction = 'Pass'
                return
            # proove empty space
            if Field[xNew][yNew] != 0:
                self.LastAction = 'Pass'
                return
            # proove other robots
            for rbt in Robots:
                if (rbt.x == xNew) and (rbt.y == yNew):
                    self.LastAction = 'Pass'
                    return
            self.LastAction = 'Step Forward'
            self.x = xNew
            self.y = yNew

        elif decision == 'Turn Left':
            self.ViewDirection += 1
            if self.ViewDirection > 3:
                self.ViewDirection = 0
            self.LastAction = 'Turn Left'

        elif decision == 'Turn Right':
            self.ViewDirection -= 1
            if self.ViewDirection < 0:
                self.ViewDirection = 3
            self.LastAction = 'Turn Right'

        elif decision == 'Shoot':
            if self.Energy < 1:
                self.LastAction = 'Pass'
                return
            self.LastAction = 'Shoot'
            self.Energy -= 1
            if (xNew < 0) or (xNew >= FIELD_SIZE) or (yNew < 0) or (yNew >= FIELD_SIZE):
                return
            elif Field[xNew][yNew] > 0:
                Field[xNew][yNew] -= 1
            else:
                # proove other robots
                for rbt in Robots:
                    if (rbt.x == xNew) and (rbt.y == yNew):
                        rbt.hp -= 1
                        return
        elif decision == 'Take':
            for it in Items:
                if it.x == self.x and it.y == self.y:
                    self.LastAction == 'Take'
                    #SoundTake.play()
                    if it.Type == 0:
                        self.Energy += 1
                    elif it.Type == 1:
                        self.hp += 1
                    Items.remove(it)

    def Decision_Era(self):
        rnd = random.randint(0, 5)
        if rnd == 0:
            return 'Pass'
        elif rnd == 1:
            return 'Step Forward'
        elif rnd == 2:
            return 'Turn Left'
        elif rnd == 3:
            return 'Turn Right'
        elif rnd == 4:
            return 'Shoot'
        elif rnd == 5:
            return 'Take'

    def Decision_WallDestructor(self):
        view = self.View()
        if view == 0 or view == -2:
            return 'Step Forward'
        elif (view == -1) or (view == 100):
            if random.randint(0, 1) == 0:
                return 'Turn Left'
            else:
                return 'Turn Right'
        elif view > 0:
            return 'Shoot'

class Item:
    x = 0
    y = 0
    Type = 0
    Lvl = 0

    def __init__(self):
        # create random coordinates in empty place
        self.x = random.randint(0, FIELD_SIZE - 1)
        self.y = random.randint(0, FIELD_SIZE - 1)
        while Field[self.x][self.y] > 0:
            self.x = random.randint(0, FIELD_SIZE - 1)
            self.y = random.randint(0, FIELD_SIZE - 1)

        # random Type (0 - Energy;  1 - hp)
        self.Type = random.randint(0, 1)


# MAIN MENU ============================================================================================================

bgc = (255, 255, 255) #background color
textc = (0, 0, 0)
yellow = (255, 255, 0)

textx = 575
texty = 200

text2x = 575
text2y = 300

text3x = 575
text3y = 100

pygame.init()

font = pygame.font.Font('font.ttf', 32)
text = font.render('Play', True, textc, bgc)
text2 = font.render('Quit', True, textc, bgc)
text3 = font.render('Robot Evolution', True, textc, bgc)

textRect = text.get_rect()
textRect.center = (textx, texty)

textRect2 = text2.get_rect()
textRect2.center = (text2x, text2y)

textRect3 = text3.get_rect()
textRect3.center = (text3x, text3y)

sc = pygame.display.set_mode((1200, 900))
pygame.display.set_caption('Robot Evolution')
sc.fill(bgc)
pygame.display.update()

pygame.mixer.music.load(r'sound/menu.wav')
pygame.mixer.music.play(-1)

InMenu = True
while InMenu:
    pos = pygame.mouse.get_pos()
    mouseX = pos[0]
    mouseY = pos[1]
    #sc.fill(white)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                # print(pos)
                if ((mouseX >= textx-30) & (mouseX <= textx+30) & (mouseY >= texty - 15) & (mouseY <= texty + 15)):
                    InMenu = False
                if ((mouseX >= text2x-30) & (mouseX <= text2x+30) & (mouseY >= text2y - 15) & (mouseY <= text2y + 15)):
                    exit()

    if ((mouseX >= textx-30) & (mouseX <= textx+30) & (mouseY >= texty - 15) & (mouseY <= texty + 15)):
        text = font.render('Play', True, textc, yellow)
    else:
        text = font.render('Play', True, textc, bgc)
    sc.blit(text, textRect)

    if ((mouseX >= text2x-30) & (mouseX <= text2x+30) & (mouseY >= text2y - 15) & (mouseY <= text2y + 15)):
        text2 = font.render('Quit', True, textc, yellow)
    else:
        text2 = font.render('Quit', True, textc, bgc)
    sc.blit(text2, textRect2)

    pygame.display.flip()
    pygame.time.delay(20)
    sc.blit(text3, textRect3)


# GAME =================================================================================================================
pygame.mixer.music.stop()
pygame.mixer.music.load(r'sound/Untitled.wav')
pygame.mixer.music.play(-1)

# CREATE RANDOM FIELD
Field = [[0 for i in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
for i in range(FIELD_SIZE):
    for r in range(FIELD_SIZE):
        if random.random() < WALL_PROB:
            Field[i][r] = random.randint(1, 10)


# CREATE ITEMS
Items = []
for i in range(N_ITEMS):
    Items.append(Item())

# CREATE ROBOTS
Robots = []
for iProg in range(N_PROGRAMS):
    for iRob in range(N_ROBOTS_PER_PROG):
        Robots.append(Robot(iProg))


size = (scaleX*FIELD_SIZE, scaleY*FIELD_SIZE)
screen = pygame.display.set_mode(size)
Game = True
while Game:
    GameSteps += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                GAME_SPEED *= 2
                print('Game speed = ', GAME_SPEED)
            elif pygame.key.get_pressed()[pygame.K_KP_MINUS]:
                GAME_SPEED /= 2
                print('Game speed = ',  GAME_SPEED)
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                Game = False


    # Draw field
    screen.blit(pygame.transform.scale(ImageFon, (800, 800)), (0, 0))
    for x in range(FIELD_SIZE):
        for y in range(FIELD_SIZE):
            if Field[x][y] != 0:
                screen.blit(ImageWall, (x * scaleX, y * scaleY))

    # Draw tems
    for it in Items:
        if it.Type == 0:
            screen.blit(ImageItemEnergy, (it.x * scaleX, it.y * scaleY))
        elif it.Type == 1:
            screen.blit(ImageItemHP, (it.x * scaleX, it.y * scaleY))

    # For each robot
    for rbt in Robots:
        if rbt.hp < 1:
            Robots.remove(rbt)
        # decision
        if rbt.ProgramType == 0:
            decision = 'Pass'
        elif rbt.ProgramType == 1:
            decision = rbt.Decision_Era()
        elif rbt.ProgramType == 2:
            decision = rbt.Decision_WallDestructor()
        # action
        rbt.Action(decision)
        # draw
        ImRob = ImageRobot
        if rbt.LastAction == 'Shoot':
            ImRob = ImageRobotShoot
        screen.blit(pygame.transform.rotate(ImRob, 90*rbt.ViewDirection), (rbt.x * scaleX, rbt.y * scaleY))
        pygame.draw.circle(screen, rbt.Color(), (int((rbt.x+0.5) * scaleX), int((rbt.y+0.5) * scaleY)), int(scaleX*0.1))

    pygame.display.flip()
    clock.tick(GAME_SPEED)
