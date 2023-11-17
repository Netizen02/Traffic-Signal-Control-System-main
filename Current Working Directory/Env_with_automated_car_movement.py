import pygame
import sys
import random

# set up the window
pygame.init()
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Traffic Control Environment")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
DGREEN =  (0, 100, 0) 
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# define road dimensions
ROAD_WIDTH = WIDTH*0.075
ROAD_LENGTH = 300
INTERSECTION_SIZE = 100

class System:
    TrafficLights = []
    trafficlightVar = -1 # temp variable to keep count of traffic light
    Cars = []
    cars = 1 # No. of cars on the road


class TrafficLight:
    initial_color = RED
    def __init__(self, x, y, srNo, color = initial_color):
        self.x = x
        self.y = y
        self.srNo = srNo
        self.color = color
        global win
        if self not in System.TrafficLights:
            System.TrafficLights.append(self)

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x,self.y), (ROAD_WIDTH/4))

    def turn_green(self):
        self.color = GREEN
        pygame.draw.circle(win, self.color, (self.x,self.y), (ROAD_WIDTH/4))

    def turn_red(self):
        self.color = RED
        pygame.draw.circle(win, self.color, (self.x,self.y), (ROAD_WIDTH/4))

    def toggle_signal(self):
        if self.color == RED:
            self.turn_green()
        else:
            self.turn_red()


class Car:
    def __init__(self, spawnPosition, velocity, car_dimensions):
        self.position = spawnPosition #position is a list data type of size 2. position[0] is the x-coordinate. position[1] is the y-coordinate.  
        self.velocity = velocity #velocity is a list data type of size 2. velocity[0] is the x-axis. velocity[1] is the y-axis.
        self.car_dimensions = car_dimensions #car_dimensions is a list data type of size 2. car_dimensions[0] is the length. car_dimensions[1] is the breadth.
        global win
        if self not in System.Cars:
            System.Cars.append(self)

    def draw(self):
        pygame.draw.circle(win, BLUE, (self.position[0], self.position[1]),  (ROAD_WIDTH/8))
    
    def turn_right(self):
        if (self.velocity[0] == 0):
            while(self.velocity[1]>0):
                self.velocity[0] += 0.1
                self.velocity[1] -= 0.1
        elif (self.velocity[1] == 0):
            while(self.velocity[0]>0):
                self.velocity[0] -= 0.1
                self.velocity[1] += 0.1 
        


# Base environment functions
# draw roads, intersections and obstacles
def draw_environment():
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
    #create obstacles
    obstacle1 = pygame.Rect((ROAD_WIDTH), (ROAD_WIDTH), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)
    obstacle2 = pygame.Rect(((ROAD_WIDTH + WIDTH)/2), (ROAD_WIDTH), (WIDTH - (3*ROAD_WIDTH))/2, (HEIGHT - (3*ROAD_WIDTH))/2)
    obstacle3 = pygame.Rect((ROAD_WIDTH), ((ROAD_WIDTH + HEIGHT)/2), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)
    obstacle4 = pygame.Rect(((ROAD_WIDTH + WIDTH)/2), ((ROAD_WIDTH + HEIGHT)/2), (WIDTH - (3*ROAD_WIDTH))/2,(HEIGHT - (3*ROAD_WIDTH))/2)
 
    # draw obstacles
    pygame.draw.rect(win, DGREEN, obstacle1)
    pygame.draw.rect(win, DGREEN, obstacle2)
    pygame.draw.rect(win, DGREEN, obstacle3)
    pygame.draw.rect(win, DGREEN, obstacle4)

# Traffic signal functions
# create traffic signals at intersections
def create_trafficSignals():
    # create traffic signals
    TrafficLight(x=(WIDTH/2-0.25*ROAD_WIDTH), y=(HEIGHT/2+0.75*ROAD_WIDTH), srNo=0)
    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=((HEIGHT/2) - (ROAD_WIDTH/4)), srNo=1)
    TrafficLight(x=(WIDTH/2+0.25*ROAD_WIDTH), y=(HEIGHT/2-0.75*ROAD_WIDTH), srNo=2)
    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(HEIGHT/2+0.25*ROAD_WIDTH), srNo=3)

    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=(ROAD_WIDTH/4), srNo=4)
    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(ROAD_WIDTH*0.75), srNo=5)
    TrafficLight(x=(WIDTH/2-0.25*ROAD_WIDTH), y=(5*ROAD_WIDTH/4), srNo=6)

    TrafficLight(x=(WIDTH-0.25*ROAD_WIDTH), y=(HEIGHT/2-0.75*ROAD_WIDTH), srNo=7)
    TrafficLight(x=(WIDTH-0.75*ROAD_WIDTH), y=(HEIGHT/2+0.75*ROAD_WIDTH), srNo=8)
    TrafficLight(x=(WIDTH-1.25*ROAD_WIDTH), y=(HEIGHT/2-0.25*ROAD_WIDTH), srNo=9)

    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(HEIGHT-0.25*ROAD_WIDTH), srNo=10)
    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=(HEIGHT-0.75*ROAD_WIDTH), srNo=11)
    TrafficLight(x=(WIDTH/2+0.25*ROAD_WIDTH), y=(HEIGHT-1.25*ROAD_WIDTH), srNo=12)

    TrafficLight(x=(ROAD_WIDTH*0.25), y=(HEIGHT/2+0.75*ROAD_WIDTH), srNo=13)
    TrafficLight(x=(ROAD_WIDTH*0.75), y=(HEIGHT/2-0.75*ROAD_WIDTH), srNo=14)
    TrafficLight(x=(ROAD_WIDTH*1.25), y=(HEIGHT/2+0.25*ROAD_WIDTH), srNo=15)
# draw the signal
def draw_signal():
    if len(System.TrafficLights) == 0:
        create_trafficSignals()
    else:    
        #draw_signals
        for light_obj in System.TrafficLights:
            light_obj.draw()


# Car functions
# choose spawn position
def chooseSpawnPosition():
    spawnPosition_1=[15 , 15]
    spawnPosition_2=[785 , 15]
    spawnPosition_3=[785 , 585]
    spawnPosition_4=[15 , 585]
    temp = random.randint(1,4)
    if temp == 1:
        return spawnPosition_1
    elif temp == 2:
        return spawnPosition_2
    elif temp == 3:
        return spawnPosition_3
    elif temp == 4:
        return spawnPosition_4
    
# give initial velocity
def initialVelocity(spawnPosition):
    spawnPosition_1=[15 , 15]
    spawnPosition_2=[785 , 15]
    spawnPosition_3=[785 , 585]
    spawnPosition_4=[15 , 585]
    #a = random.randint(1, 3)
    a = 2
    # speed of 3 is too fast for the code to pause and wait for the program to see if it 
    # is okay to cross
    initVelocity_1=[a , 0]
    initVelocity_2=[0 , a]
    initVelocity_3=[a*-1 , 0]
    initVelocity_4=[0 , a*-1]
    if spawnPosition == spawnPosition_1:
        return initVelocity_1
    elif spawnPosition == spawnPosition_2:
        return initVelocity_2
    elif spawnPosition == spawnPosition_3:
        return initVelocity_3
    elif spawnPosition == spawnPosition_4:
        return initVelocity_4

# create car function
def create_car():
    spawnPosition = chooseSpawnPosition()
    velocity = initialVelocity(spawnPosition)
    car_dimensions=[ROAD_WIDTH/4 , ROAD_WIDTH/4]
    Car(spawnPosition, velocity, car_dimensions)
# draw cars
def draw_cars():
    # Create car objects
    if (len(System.Cars) < System.cars) or (len(System.Cars) == 0):
        for i in range((System.cars - len(System.Cars))):
            create_car()
    elif len(System.Cars) > System.cars:
        for i in range(len(System.Cars) - System.cars):
            System.Cars.pop(0)
    else:
        # actually draw the cars when len(System.Cars) == System.cars
        for car_obj in System.Cars:
            car_obj.draw()
# move cars
def move_cars():
    traffic_light_detection()
    for car in System.Cars:
        car.position[0] = car.position[0] + car.velocity[0]
        car.position[1] = car.position[1] + car.velocity[1]
        if car.position[0] > win.get_width():
            car.position[0] = 0
        if car.position[1] > win.get_height():
            car.position[1] = 0
        if car.position[0] < 0:
            car.position[0] = win.get_width()
        if car.position[1] < 0:
            car.position[1] = win.get_height()
# detect collisions
def collision_detection():
    pass
# detect traffic light
def traffic_light_detection():
    a = random.randint(1, 2)
    for car_obj in System.Cars:
        for light_obj in System.TrafficLights:
            # cars moving along the x-axis
            if (car_obj.position[0] == ((WIDTH/2-0.75*ROAD_WIDTH) - (ROAD_WIDTH/4) - 15)) and (car_obj.position[1] == (ROAD_WIDTH/4)):
                if (light_obj.srNo == 4):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH/2-0.75*ROAD_WIDTH) - (ROAD_WIDTH/4) - 15)) and (car_obj.position[1] == ((HEIGHT/2) - (ROAD_WIDTH/4))):
                if (light_obj.srNo == 1):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH-1.25*ROAD_WIDTH) - (ROAD_WIDTH/4) - 15)) and (car_obj.position[1] == (HEIGHT/2-0.25*ROAD_WIDTH)):
                if (light_obj.srNo == 9):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH/2-0.75*ROAD_WIDTH) - (ROAD_WIDTH/4) - 15)) and (car_obj.position[1] == (HEIGHT-0.75*ROAD_WIDTH)):
                if (light_obj.srNo == 11):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)) and (car_obj.position[1] == (ROAD_WIDTH*0.75)):
                if (light_obj.srNo == 5):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)) and (car_obj.position[1] == (HEIGHT/2+0.25*ROAD_WIDTH)):
                if (light_obj.srNo == 3):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((WIDTH/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)) and (car_obj.position[1] == (HEIGHT-0.25*ROAD_WIDTH)):
                if (light_obj.srNo == 10):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            elif (car_obj.position[0] == ((ROAD_WIDTH*1.25) + (ROAD_WIDTH/4) + 15)) and (car_obj.position[1] == (HEIGHT/2+0.25*ROAD_WIDTH)):
                if (light_obj.srNo == 15):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [a, 0] 
            # cars moving along the y-axis
            elif (car_obj.position[0] == (WIDTH/2-0.25*ROAD_WIDTH)) and (car_obj.position[1] == ((5*ROAD_WIDTH/4) + (ROAD_WIDTH/4) + 15)):
                if (light_obj.srNo == 6):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (ROAD_WIDTH*0.75)) and (car_obj.position[1] == ((HEIGHT/2-0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) - 15)):
                if (light_obj.srNo == 14):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (WIDTH/2+0.25*ROAD_WIDTH)) and (car_obj.position[1] == ((HEIGHT/2-0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) - 15)):
                if (light_obj.srNo == 2):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (WIDTH-0.25*ROAD_WIDTH)) and (car_obj.position[1] == ((HEIGHT/2-0.75*ROAD_WIDTH) - (ROAD_WIDTH/4) - 15)):
                if (light_obj.srNo == 7):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (ROAD_WIDTH*0.25)) and (car_obj.position[1] == ((HEIGHT/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)):
                if (light_obj.srNo == 13):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (WIDTH/2-0.25*ROAD_WIDTH)) and (car_obj.position[1] == ((HEIGHT/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)):
                if (light_obj.srNo == 0):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (WIDTH-0.75*ROAD_WIDTH)) and (car_obj.position[1] == ((HEIGHT/2+0.75*ROAD_WIDTH) + (ROAD_WIDTH/4) + 15)):
                if (light_obj.srNo == 8):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            elif (car_obj.position[0] == (WIDTH/2+0.25*ROAD_WIDTH)) and (car_obj.position[1] == ((HEIGHT-1.25*ROAD_WIDTH) + (ROAD_WIDTH/4) - 15)):
                if (light_obj.srNo == 12):
                    if (light_obj.color == RED):
                        car_obj.velocity = [0, 0]
                    if (light_obj.color == GREEN):
                        car_obj.velocity = [0, a] 
            
# automated movement
def automated_movement():
    pass


#Check if commands are coming    
pressed = 0
def toggle_key_press():
    global pressed
    pressed += 1
    if pressed == 3:
        pressed = 0

# one function to rule all keyboard inputs
def keyboard_input(event):
    global pressed, key1
    if event.key == pygame.K_SPACE:
        pressed = 1
        print("Space Pressed")
    elif pressed == 1:
        if event.key in [pygame.K_p, pygame.K_m, pygame.K_a, pygame.K_d]:
            toggle_key_press()
            key1 = event.key
        loc_converted = (chr(key1)).upper()
        print(loc_converted)
        acceptable_keys = ['P','M','A','D']
        if loc_converted in acceptable_keys: #check if its the specified key we want 
            print(f'Key Identified: {loc_converted}')
            # Add or Delete cars on the map
            if (loc_converted == "A") or (loc_converted == "D"):
                if loc_converted == "A":
                    System.cars += 1
                else:
                    System.cars -= 1
            # Change traffic light colour
            else:
                if loc_converted == "P":
                    System.trafficlightVar += 1
                elif loc_converted == "M":
                    System.trafficlightVar -= 1
                if (System.trafficlightVar < 0) or (System.trafficlightVar > 15):
                    if System.trafficlightVar < 0:
                        System.trafficlightVar = 15
                    else:
                        System.trafficlightVar = 0
                for light_obj in System.TrafficLights:
                    if light_obj.srNo == System.trafficlightVar:
                        print(System.trafficlightVar)
                        light_obj.toggle_signal()

running = True
while running:
    timer.tick(fps)
    win.fill(GREY)
    draw_environment()
    draw_signal()
    draw_cars()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keyboard_input(event)
    
    move_cars()
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()
