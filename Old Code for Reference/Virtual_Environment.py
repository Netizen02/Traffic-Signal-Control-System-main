import pygame
import sys

pygame.init()

# set up the window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Environment")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# define road dimensions
ROAD_WIDTH = WIDTH*0.075
ROAD_LENGTH = 300
INTERSECTION_SIZE = 100

#create dividers: go to line 41

# create traffic signals: go to line 
# Traffic Signal Colour
s1 = RED
s2 = RED
s3 = RED
s4 = RED
s5 = RED
s6 = RED
s7 = RED
s8 = RED
s9 = RED
s10 = RED
s11 = RED
s12 = RED
s13 = RED
s14 = RED
s15 = RED
s16 = RED


# create obstacles
obstacle1 = pygame.Rect((ROAD_WIDTH), (ROAD_WIDTH), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)
obstacle2 = pygame.Rect(((ROAD_WIDTH + WIDTH)/2), (ROAD_WIDTH), (WIDTH - (3*ROAD_WIDTH))/2, (HEIGHT - (3*ROAD_WIDTH))/2)
obstacle3 = pygame.Rect((ROAD_WIDTH), ((ROAD_WIDTH + HEIGHT)/2), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)
obstacle4 = pygame.Rect(((ROAD_WIDTH + WIDTH)/2), ((ROAD_WIDTH + HEIGHT)/2), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)


# draw roads, intersections and signals
def draw_environment():
    win.fill(GREY)
    # create dividers
    pygame.draw.line(win, WHITE, ((ROAD_WIDTH/2), (ROAD_WIDTH/2)), (((WIDTH - ROAD_WIDTH)/2),(ROAD_WIDTH/2)))
    pygame.draw.line(win, WHITE, (((ROAD_WIDTH + WIDTH)/2),(ROAD_WIDTH/2)), ((WIDTH - (ROAD_WIDTH/2)),(ROAD_WIDTH/2)))
    pygame.draw.line(win, WHITE, ((WIDTH - (ROAD_WIDTH/2)),(ROAD_WIDTH/2)), ((WIDTH - (ROAD_WIDTH/2)), (HEIGHT-ROAD_WIDTH)/2))
    pygame.draw.line(win, WHITE, ((WIDTH - (ROAD_WIDTH/2)),(HEIGHT+ROAD_WIDTH)/2), ((WIDTH - (ROAD_WIDTH/2)),(HEIGHT-(ROAD_WIDTH/2))))
    pygame.draw.line(win, WHITE, ((WIDTH - (ROAD_WIDTH/2)),(HEIGHT - (ROAD_WIDTH/2))), (((ROAD_WIDTH + WIDTH)/2),(HEIGHT - (ROAD_WIDTH/2))))
    pygame.draw.line(win, WHITE, (((WIDTH - ROAD_WIDTH)/2),(HEIGHT - (ROAD_WIDTH/2))), ((ROAD_WIDTH/2),(HEIGHT - (ROAD_WIDTH/2))))
    pygame.draw.line(win, WHITE, ((ROAD_WIDTH/2),(HEIGHT-(ROAD_WIDTH/2))), ((ROAD_WIDTH/2),(HEIGHT+ROAD_WIDTH)/2))
    pygame.draw.line(win, WHITE, ((ROAD_WIDTH/2),(HEIGHT-ROAD_WIDTH)/2), ((ROAD_WIDTH/2),(ROAD_WIDTH/2)))
    pygame.draw.line(win, WHITE, ((WIDTH/2),(ROAD_WIDTH)), ((WIDTH/2),((HEIGHT-ROAD_WIDTH)/2)))
    pygame.draw.line(win, WHITE, ((ROAD_WIDTH),(HEIGHT/2)), (((WIDTH-ROAD_WIDTH)/2),(HEIGHT/2)))
    pygame.draw.line(win, WHITE, ((WIDTH/2),((HEIGHT+ROAD_WIDTH)/2)), ((WIDTH/2),(HEIGHT-ROAD_WIDTH)))
    pygame.draw.line(win, WHITE, (((WIDTH+ROAD_WIDTH)/2),(HEIGHT/2)), ((WIDTH-ROAD_WIDTH),(HEIGHT/2)))
    # draw obstacles
    pygame.draw.rect(win,GREEN, obstacle1)
    pygame.draw.rect(win,GREEN, obstacle2)
    pygame.draw.rect(win,GREEN, obstacle3)
    pygame.draw.rect(win,GREEN, obstacle4)
    # create traffic signals
    pygame.draw.circle(win,s1,((WIDTH/2-0.75*ROAD_WIDTH),(ROAD_WIDTH/4)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s2,((WIDTH/2+0.75*ROAD_WIDTH),(ROAD_WIDTH*0.75)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s3,((WIDTH/2-0.25*ROAD_WIDTH),(5*ROAD_WIDTH/4)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s4,((WIDTH-0.25*ROAD_WIDTH),(HEIGHT/2-0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH-1.25*ROAD_WIDTH),(HEIGHT/2-0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH-0.75*ROAD_WIDTH),(HEIGHT/2+0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH/2+0.75*ROAD_WIDTH),(HEIGHT-0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH/2+0.25*ROAD_WIDTH),(HEIGHT-1.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH/2-0.75*ROAD_WIDTH),(HEIGHT-0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH-1.25*ROAD_WIDTH),(HEIGHT/2-0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH-1.25*ROAD_WIDTH),(HEIGHT/2-0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s1,((WIDTH-1.25*ROAD_WIDTH),(HEIGHT/2-0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s10,((ROAD_WIDTH*0.25),(HEIGHT/2+0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s11,((ROAD_WIDTH*0.75),(HEIGHT/2-0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s12,((ROAD_WIDTH*1.25),(HEIGHT/2+0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s15,((WIDTH/2-0.25*ROAD_WIDTH),(HEIGHT/2+0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))    
    pygame.draw.circle(win,s13,((WIDTH/2-0.75*ROAD_WIDTH),((HEIGHT/2) - (ROAD_WIDTH/4))),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s12,((WIDTH/2+0.75*ROAD_WIDTH),(HEIGHT/2+0.25*ROAD_WIDTH)),(ROAD_WIDTH/4))
    pygame.draw.circle(win,s16,((WIDTH/2+0.25*ROAD_WIDTH),(HEIGHT/2-0.75*ROAD_WIDTH)),(ROAD_WIDTH/4))


    pygame.display.update()

# game loop
# gameover = False

# while not gameover:
#     pygame.

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    draw_environment()
