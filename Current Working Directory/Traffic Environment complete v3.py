import pygame
import sys
import random

pygame.init()

# set up the window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Control Environment")

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


class System:
    TrafficLights = []
    Cars = []
    max_cars = 50
    total_cars = 0
    obstacles = []

    @staticmethod
    def add_car(car_obj):
        System.Cars.append(car_obj)
        System.total_cars += 1
    
    @staticmethod
    def get_loc(loc):
        for light in System.TrafficLights:
            if light.loc == loc:
                return light
            

class TrafficLight:
    def __init__(self, x, y, loc, start_col=GREEN):
        self.x = x
        self.y = y
        self.loc = loc
        self.col = start_col
        global win
        pygame.draw.circle(win, self.col, (self.x,self.y), (ROAD_WIDTH/4))
        # pygame.display.update()
        if self not in System.TrafficLights:
            System.TrafficLights.append(self)

    def draw(self):
        pygame.draw.circle(win, self.col, (self.x,self.y), (ROAD_WIDTH/4))

    def turn_green(self):
        self.col = GREEN
        pygame.draw.circle(win, self.col, (self.x,self.y), (ROAD_WIDTH/4))
        # pygame.display.update()

    def turn_red(self):
        self.col = RED
        pygame.draw.circle(win, self.col, (self.x,self.y), (ROAD_WIDTH/4))
        # pygame.display.update()

    def toggle_signal(self):
        if self.col == RED:
            self.turn_green()
        else:
            self.turn_red()

    def is_red(self):
        return self.col == RED

class Car:
    def __init__(self, x, y, x_vel=0, y_vel=0, length=(ROAD_WIDTH/4), breadth=(ROAD_WIDTH/4), col=WHITE):
        self.x = x
        self.init_x = x
        self.y = y
        self.init_y = y
        self.lane = ''
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.length = length
        self.breadth = breadth
        self.col = col
        self.state = "Running"
        self.turn_inbound = False
        self.turn_direction = ''
        self.current_dir = ''
        self.start_dist = False
        self.turn_dist = 0
        self.waiting_time = 0
        self.dist_travelled = 0
        self.max_dist = random.choice([400,600,800,1000,1200,1400,1600,1800,2000]) #random.randint(10)
        self.change_speed(init=True)


        global win
        pygame.draw.rect(win, self.col, pygame.Rect(self.x, self.y, self.length, self.breadth))
        # pygame.display.update()
        # add logic to avoid same place spawning.
        if self not in System.Cars:
            System.add_car(self)

    def change_speed(self, init = False):
        min_change_dist, max_change_dist = 25, 100
        next_change_distance = random.randint(min_change_dist, max_change_dist)
        self.speed_checkpoint = self.dist_travelled + next_change_distance
        if not init:
            speed_choice = [0.75, 1, 1.25, 1.5]
            if self.x_vel != 0:
                self.x_vel *= random.choice(speed_choice)
            elif self.y_vel != 0:
                self.y_vel *= random.choice(speed_choice)

    def get_center(self):
        return (self.x + self.length/2, self.y + self.breadth/2)
    
    def turn_dist_calc(self):
        smaller_dist = ROAD_WIDTH/2
        bigger_dist = ROAD_WIDTH
        cur = self.current_dir
        dir = self.turn_direction
        turn_dict = {
            ('L','U'): bigger_dist,
            ('L','D'): smaller_dist,
            ('R','D'): bigger_dist,
            ('R','U'): smaller_dist,
            ('U','L'): smaller_dist,
            ('U','R'): bigger_dist,
            ('D','R'): smaller_dist,
            ('D','L'): bigger_dist,
        }
        return turn_dict[(cur,dir)]

    def update_pos(self):
        stop = self.check_signal_cross()
        if self.turn_inbound == True:
            if self.start_dist == True:
                self.turn_dist = 0
                self.start_dist = False
            dir = self.turn_direction
            intersect_dist = self.turn_dist_calc()
            
            if dir == "U":
                if self.turn_dist < intersect_dist and self.turn_dist+(abs(self.x_vel)+abs(self.y_vel)) > intersect_dist:
                    self.y_vel = -abs(self.x_vel)
                    self.x_vel = 0
                    self.turn_inbound = False
                else:
                    self.turn_dist += (abs(self.x_vel)+abs(self.y_vel))
                    self.go_forward()

            elif dir == "L":
                if self.turn_dist < intersect_dist and self.turn_dist+(abs(self.x_vel)+abs(self.y_vel)) > intersect_dist:
                    self.x_vel = -abs(self.y_vel)
                    self.y_vel = 0
                    self.turn_inbound = False
                else:
                    self.turn_dist += (abs(self.x_vel)+abs(self.y_vel))
                    self.go_forward()

            elif dir == "D":
                if self.turn_dist < intersect_dist and self.turn_dist+(abs(self.x_vel)+abs(self.y_vel)) > intersect_dist:
                    self.y_vel = abs(self.x_vel)
                    self.x_vel = 0
                    self.turn_inbound = False
                else:
                    self.turn_dist += (abs(self.x_vel)+abs(self.y_vel))
                    self.go_forward()

            elif dir == "R":
                if self.turn_dist < intersect_dist and self.turn_dist+(abs(self.x_vel)+abs(self.y_vel)) > intersect_dist:
                    self.x_vel = abs(self.y_vel)
                    self.y_vel = 0
                    self.turn_inbound = False
                else:
                    self.turn_dist += (abs(self.x_vel)+abs(self.y_vel))
                    self.go_forward()
        
        elif not stop:
            self.go_forward()
        

    def go_forward(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.dist_travelled += (abs(self.x_vel)+abs(self.y_vel))
        if (self.x > win.get_width() or self.y > win.get_height() or self.x < 0 or self.y < 0) or (self.dist_travelled >= self.max_dist):
            # removes car from environment
            del(System.Cars[System.Cars.index(self)])
            System.total_cars -= 1
            del(self)
        elif self.dist_travelled > self.speed_checkpoint:
            self.change_speed()

    def check_turn(self):
        pass

    def check_light(self, light, loc):
        directions = {
            "UL":['', 'U', 'D'],
            "UU":['', 'L', 'R'],
            "UR":['', 'U', 'D'],
            "LL":['', 'U', 'D'],
            "LD":['', 'L', 'R'],
            "LU":['', 'L', 'R'],
            "RR":['', 'U', 'D'],
            "RD":['', 'L', 'R'],
            "RU":['', 'L', 'R'],
            "DD":['', 'L', 'R'],
            "DR":['', 'U', 'D'],
            "DL":['', 'U', 'D'],
            "CU":['', 'L', 'R'],
            "CL":['', 'U', 'D'],
            "CD":['', 'L', 'R'],
            "CR":['', 'U', 'D'],
        }
        if light.is_red():
            if self.state == "Running":
                self.waiting_time = 0
                self.state = "Waiting"
                self.start_timer()
            return True
        else:
            if self.state == "Waiting":
                self.state = "Running"
                self.stop_timer()
                
            choices = directions[loc]
            turn = random.choice(choices)
            if turn != "":
                self.turn_inbound = True
                self.turn_direction = turn
                self.start_dist = True
                self.current_dir = loc[1]
                return True
            return False


    def check_signal_cross(self):
        xpos, ypos = self.get_center()
        
        if (xpos <= WIDTH/2-0.75*ROAD_WIDTH and xpos+self.x_vel > (WIDTH/2-0.75*ROAD_WIDTH)) and (ypos == ROAD_WIDTH/4):
            # Car at UR
            # check if red light at UR
            light = System.get_loc("UR")
            return self.check_light(light, "UR")
            
        elif (xpos >= WIDTH/2+0.75*ROAD_WIDTH and xpos+self.x_vel < (WIDTH/2+0.75*ROAD_WIDTH)) and (ypos == ROAD_WIDTH*0.75):
            # Car at UL
            # check if red light at UL
            light = System.get_loc("UL")
            return self.check_light(light, "UL")
        
        elif (ypos >= 5*ROAD_WIDTH/4 and ypos+self.y_vel < (5*ROAD_WIDTH/4)) and (xpos == WIDTH/2-0.25*ROAD_WIDTH):
            # Car at UU
            # check if red light at UU
            light = System.get_loc("UU")
            return self.check_light(light, "UU")
        
        elif (ypos <= HEIGHT/2-0.75*ROAD_WIDTH and ypos+self.y_vel > (HEIGHT/2-0.75*ROAD_WIDTH)) and (xpos == WIDTH-0.25*ROAD_WIDTH):
            # Car at RD
            # check if red light at RD
            light = System.get_loc("RD")
            return self.check_light(light, "RD")
        
        elif (xpos <= WIDTH-1.25*ROAD_WIDTH and xpos+self.x_vel > (WIDTH-1.25*ROAD_WIDTH)) and (ypos == HEIGHT/2-0.25*ROAD_WIDTH):
            # Car at RR
            # check if red light at RR
            light = System.get_loc("RR")
            return self.check_light(light, "RR")
        
        elif (ypos >= HEIGHT/2+0.75*ROAD_WIDTH and ypos+self.y_vel < (HEIGHT/2+0.75*ROAD_WIDTH)) and (xpos == WIDTH-0.75*ROAD_WIDTH):
            # Car at RU
            # check if red light at RU
            light = System.get_loc("RU")
            return self.check_light(light, "RU")
        
        elif (xpos >= WIDTH/2+0.75*ROAD_WIDTH and xpos+self.x_vel < (WIDTH/2+0.75*ROAD_WIDTH)) and (ypos == HEIGHT-0.25*ROAD_WIDTH):
            # Car at DL
            # check if red light at DL
            light = System.get_loc("DL")
            return self.check_light(light, "DL")
        
        elif (ypos <= HEIGHT-1.25*ROAD_WIDTH and ypos+self.y_vel > (HEIGHT-1.25*ROAD_WIDTH)) and (xpos == WIDTH/2+0.25*ROAD_WIDTH):
            # Car at DD
            # check if red light at DD
            light = System.get_loc("DD")
            return self.check_light(light, "DD")
        
        elif (xpos <= WIDTH/2-0.75*ROAD_WIDTH and xpos+self.x_vel > (WIDTH/2-0.75*ROAD_WIDTH)) and (ypos == HEIGHT-0.75*ROAD_WIDTH):
            # Car at DR
            # check if red light at DR
            light = System.get_loc("DR")
            return self.check_light(light, "DR")
        
        elif (ypos >= HEIGHT/2+0.75*ROAD_WIDTH and ypos+self.y_vel < (HEIGHT/2+0.75*ROAD_WIDTH)) and (xpos == ROAD_WIDTH*0.25):
            # Car at LU
            # check if red light at LU
            light = System.get_loc("LU")
            return self.check_light(light, "LU")
        
        elif (ypos <= HEIGHT/2-0.75*ROAD_WIDTH and ypos+self.y_vel > (HEIGHT/2-0.75*ROAD_WIDTH)) and (xpos == ROAD_WIDTH*0.75):
            # Car at LD
            # check if red light at LD
            light = System.get_loc("LD")
            return self.check_light(light, "LD")
        
        elif (xpos >= ROAD_WIDTH*1.25 and xpos+self.x_vel < (ROAD_WIDTH*1.25)) and (ypos == HEIGHT/2+0.25*ROAD_WIDTH):
            # Car at LL
            # check if red light at LL
            light = System.get_loc("LL")
            return self.check_light(light, "LL")
        
        elif (ypos >= HEIGHT/2+0.75*ROAD_WIDTH and ypos+self.y_vel < (HEIGHT/2+0.75*ROAD_WIDTH)) and (xpos == WIDTH/2-0.25*ROAD_WIDTH):
            # Car at CU
            # check if red light at CU
            light = System.get_loc("CU")
            return self.check_light(light, "CU")
        
        elif (xpos <= WIDTH/2-0.75*ROAD_WIDTH and xpos+self.x_vel > (WIDTH/2-0.75*ROAD_WIDTH)) and (ypos == (HEIGHT/2)-(ROAD_WIDTH/4)):
            # Car at CR
            # check if red light at CR
            light = System.get_loc("CR")
            return self.check_light(light, "CR")
        
        elif (xpos >= WIDTH/2+0.75*ROAD_WIDTH and xpos+self.x_vel < (WIDTH/2+0.75*ROAD_WIDTH)) and (ypos == (HEIGHT/2+0.25*ROAD_WIDTH)):
            # Car at CL
            # check if red light at CL
            light = System.get_loc("CL")
            return self.check_light(light, "CL")
        
        elif (ypos <= HEIGHT/2-0.75*ROAD_WIDTH and ypos+self.y_vel > (HEIGHT/2-0.75*ROAD_WIDTH)) and (xpos == WIDTH/2+0.25*ROAD_WIDTH):
            # Car at CD
            # check if red light at CD
            light = System.get_loc("CD")
            return self.check_light(light, "CD")
        
        return False


    def start_timer(self):
        self.clock=pygame.time.Clock()
        self.clock.tick()


    def stop_timer(self):
        self.clock.tick()
        self.waiting_time += self.clock.get_time()
        del(self.clock)
    
    
    
# create traffic signals
    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=(ROAD_WIDTH/4), loc='UR')
    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(ROAD_WIDTH*0.75), loc='UL')
    TrafficLight(x=(WIDTH/2-0.25*ROAD_WIDTH), y=(5*ROAD_WIDTH/4), loc='UU')

    TrafficLight(x=(WIDTH-0.25*ROAD_WIDTH), y=(HEIGHT/2-0.75*ROAD_WIDTH), loc='RD')
    TrafficLight(x=(WIDTH-1.25*ROAD_WIDTH), y=(HEIGHT/2-0.25*ROAD_WIDTH), loc='RR')
    TrafficLight(x=(WIDTH-0.75*ROAD_WIDTH), y=(HEIGHT/2+0.75*ROAD_WIDTH), loc='RU')

    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(HEIGHT-0.25*ROAD_WIDTH), loc='DL')
    TrafficLight(x=(WIDTH/2+0.25*ROAD_WIDTH), y=(HEIGHT-1.25*ROAD_WIDTH), loc='DD')
    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=(HEIGHT-0.75*ROAD_WIDTH), loc='DR')

    TrafficLight(x=(ROAD_WIDTH*0.25), y=(HEIGHT/2+0.75*ROAD_WIDTH), loc='LU')
    TrafficLight(x=(ROAD_WIDTH*0.75), y=(HEIGHT/2-0.75*ROAD_WIDTH), loc='LD')
    TrafficLight(x=(ROAD_WIDTH*1.25), y=(HEIGHT/2+0.25*ROAD_WIDTH), loc='LL')

    TrafficLight(x=(WIDTH/2-0.25*ROAD_WIDTH), y=(HEIGHT/2+0.75*ROAD_WIDTH), loc='CU')
    TrafficLight(x=(WIDTH/2-0.75*ROAD_WIDTH), y=((HEIGHT/2) - (ROAD_WIDTH/4)), loc='CR')
    TrafficLight(x=(WIDTH/2+0.75*ROAD_WIDTH), y=(HEIGHT/2+0.25*ROAD_WIDTH), loc='CL')
    TrafficLight(x=(WIDTH/2+0.25*ROAD_WIDTH), y=(HEIGHT/2-0.75*ROAD_WIDTH), loc='CD')


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

    for light_obj in System.TrafficLights:
        light_obj.draw()


pressed = 0
def toggle_key_press():
    global pressed
    pressed += 1
    if pressed == 3:
        pressed = 0

def show_cars():
    # display the cars
    for car in System.Cars:
        car_surface = pygame.Surface(((ROAD_WIDTH/4), (ROAD_WIDTH/4)))
        car_surface.fill(car.col)
        win.blit(car_surface, (car.x, car.y))

def update_cars():
    for car in System.Cars:
        car.update_pos()


def add_car():
    if System.total_cars < System.max_cars: # if cars dont exceed the max no
        # creating random pos for the car
        possible_locs = ['UU','UR','UL','LU','LL','LD','CU','CL','CR','CD','RU','RR','RD','DL','DR','DD']
        init_x_vel = 0.1
        init_y_vel = 0.1
        init_speed = [(0,-init_y_vel),(init_x_vel,0),(-init_x_vel,0),(0,-init_y_vel),(-init_x_vel,0),(0,init_y_vel),(0,-init_y_vel),(-init_x_vel,0),(init_x_vel,0),(0,init_y_vel),(0,-init_y_vel),(init_x_vel,0),(0,init_y_vel),(-init_x_vel,0),(init_x_vel,0),(0,init_y_vel)]
        loc_pos = random.randint(0,len(possible_locs)-1)
        loc_select = possible_locs[loc_pos]
        x_vel, y_vel = init_speed[loc_pos]
        spawn_locs = {
            'UR': ((ROAD_WIDTH*1.25),(ROAD_WIDTH/4)-ROAD_WIDTH/8),
            'UL': ((WIDTH-1.25*ROAD_WIDTH),(ROAD_WIDTH*0.75)-ROAD_WIDTH/8),
            'UU': ((WIDTH/2-0.25*ROAD_WIDTH)-ROAD_WIDTH/8,(HEIGHT/2-0.75*ROAD_WIDTH)),
            'RD': ((WIDTH-0.25*ROAD_WIDTH)-ROAD_WIDTH/8,(5*ROAD_WIDTH/4)),
            'RR': ((WIDTH/2+0.75*ROAD_WIDTH),(HEIGHT/2-0.25*ROAD_WIDTH)-ROAD_WIDTH/8),
            'RU': ((WIDTH-0.75*ROAD_WIDTH)-ROAD_WIDTH/8,(HEIGHT-1.25*ROAD_WIDTH)),
            'DL': ((WIDTH-1.25*ROAD_WIDTH),(HEIGHT-0.25*ROAD_WIDTH)-ROAD_WIDTH/8),
            'DD': ((WIDTH/2+0.25*ROAD_WIDTH)-ROAD_WIDTH/8,(HEIGHT/2+0.75*ROAD_WIDTH)),
            'DR': ((ROAD_WIDTH*1.25),(HEIGHT-0.75*ROAD_WIDTH)-ROAD_WIDTH/8),
            'LU': ((ROAD_WIDTH*0.25)-ROAD_WIDTH/8,(HEIGHT-1.25*ROAD_WIDTH)),
            'LD': ((ROAD_WIDTH*0.75)-ROAD_WIDTH/8,(5*ROAD_WIDTH/4)),
            'LL': ((WIDTH/2-0.75*ROAD_WIDTH),(HEIGHT/2+0.25*ROAD_WIDTH)-ROAD_WIDTH/8),
            'CU': ((WIDTH/2-0.25*ROAD_WIDTH)-ROAD_WIDTH/8,(HEIGHT-1.25*ROAD_WIDTH)),
            'CR': ((ROAD_WIDTH*1.25),((HEIGHT/2) - (ROAD_WIDTH/4))-ROAD_WIDTH/8),
            'CL': ((WIDTH-1.25*ROAD_WIDTH),(HEIGHT/2+0.25*ROAD_WIDTH)-ROAD_WIDTH/8),
            'CD': ((WIDTH/2+0.25*ROAD_WIDTH)-ROAD_WIDTH/8,(5*ROAD_WIDTH/4))
        }
        x,y = spawn_locs[loc_select]
        # add while loop to avoid same loc spawn 
        car1 = Car(x,y, x_vel,y_vel)


def check_changelights(event):
    global pressed, key1, key2
    if event.key == pygame.K_SPACE:
        pressed = 1
        print("Space Pressed")
    elif event.key == pygame.K_t:
        for light_obj in System.TrafficLights:
            if random.randint(1,2) == 1:
                light_obj.toggle_signal()
                
    elif pressed == 1:
        if event.key in [pygame.K_u, pygame.K_l, pygame.K_c, pygame.K_r, pygame.K_d]:
            toggle_key_press()
            key1 = event.key
    elif pressed == 2:
        toggle_key_press()
        key2 = event.key
        loc_converted = (chr(key1)+chr(key2)).upper()
        acceptable_keys = ['UU','UR','UL','LU','LL','LD','CU','CL','CR','CD','RU','RR','RD','DL','DR','DD']
        if loc_converted in acceptable_keys: #check if its the specified key we want 
            print(f'Key Identified: {loc_converted}')
            for light_obj in System.TrafficLights:
                if light_obj.loc == loc_converted:
                    light_obj.toggle_signal()
                    break

vel_toggle = 0
car_toggle = -1
def give_velocity():
    global vel_toggle, car_toggle
    # vel_toggle = (vel_toggle+1)%3
    if event.key == pygame.K_i:
        car_toggle = (car_toggle+1)%(len(System.Cars))
    elif event.key == pygame.K_z:
        System.Cars[car_toggle].y_vel = 0
        System.Cars[car_toggle].x_vel = 0
    elif event.key == pygame.K_x:
        vel_toggle = 1
    elif event.key == pygame.K_y:
        vel_toggle = 2
    elif event.key == pygame.K_p and vel_toggle == 1:
        vel_toggle = 0
        System.Cars[car_toggle].x_vel = 0.1
    elif event.key == pygame.K_n and vel_toggle == 1:
        vel_toggle = 0
        System.Cars[car_toggle].x_vel = -0.1    
    elif event.key == pygame.K_p and vel_toggle == 2:
        vel_toggle = 0
        System.Cars[car_toggle].y_vel = 0.1 
    elif event.key == pygame.K_n and vel_toggle == 2:
        vel_toggle = 0
        System.Cars[car_toggle].y_vel = -0.1 

class Obstacle:
    def __init__(self, x1,x2,y1,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        

running = True
while running:
    draw_environment()
    show_cars()
    add_car() # remove?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            check_changelights(event)
            if event.key == pygame.K_a:
                add_car()
            give_velocity()

    update_cars()
    show_cars()
    
    pygame.display.update()
    
pygame.quit()
sys.exit()



            
                
            
