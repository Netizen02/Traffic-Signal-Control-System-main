
import pygame, sys


class TrafficLight:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        # Draw the traffic light on the screen
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y, 20, 60))
        if self.color == "red":
            pygame.draw.circle(screen, (255, 0, 0), (self.x + 10, self.y + 10), 10)
        elif self.color == "yellow":
            pygame.draw.circle(screen, (255, 255, 0), (self.x + 10, self.y + 30), 10)
        elif self.color == "green":
            pygame.draw.circle(screen, (0, 255, 0), (self.x + 10, self.y + 50), 10)
    

class Vehicle:
    def __init__(self, x, y, speed, prevSpeed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.prevSpeed = prevSpeed

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        # Draw the obstacle on the screen
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Traffic Simulation")

vehicles = []

# Add some vehicles to the simulation
vehicles.append(Vehicle(0, 100, 0.25, 0.25, (255, 0, 0)))
vehicles.append(Vehicle(0, 117, 0.3, 0.3, (0, 255, 0)))
vehicles.append(Vehicle(0, 134, 0.2, 0.2, (0, 0, 255)))
vehicles.append(Vehicle(0, 151, 0.25, 0.25, (255, 0, 0)))
vehicles.append(Vehicle(0, 168, 0.3, 0.3, (0, 255, 0)))
vehicles.append(Vehicle(0, 185, 0.2, 0.2, (0, 0, 255)))

traffic_light = TrafficLight(500, 100, "green")

obstacles = []

# Add some obstacles to the simulation
obstacles.append(Obstacle(0, 80, 1000, 50))
obstacles.append(Obstacle(0, 200, 1000, 1000))

running = True

while running:      
    # Draw the obstacles on the screen
    screen.fill((255, 255, 255))
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Draw the vehicles on the screen
    screen.fill((255, 255, 255))
    for vehicle in vehicles:
        vehicle_surface = pygame.Surface((20, 10))
        vehicle_surface.fill(vehicle.color)
        screen.blit(vehicle_surface, (vehicle.x, vehicle.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # If the spacebar is pressed, toggle the traffic light's color
                if traffic_light.color == "red":
                        traffic_light.color = "green"
                elif traffic_light.color == "green":
                        traffic_light.color = "yellow"
                elif traffic_light.color == "yellow":
                        traffic_light.color = "red"

    # Update the position of each vehicle
    for vehicle in vehicles:
        vehicle.x += vehicle.speed
        # Check if the vehicle has gone off the screen
        if vehicle.x > screen.get_width():
            # Reset the vehicle's position to the left side of the screen
            vehicle.x = -20
        if traffic_light.color == "red":
            if vehicle.x < traffic_light.x:
                vehicle.speed = 0
            else: 
                vehicle.speed = vehicle.prevSpeed
        else:
            vehicle.speed = vehicle.prevSpeed

    # Draw the vehicles on the screen
    traffic_light.draw(screen)
    for vehicle in vehicles:
        vehicle_surface = pygame.Surface((20, 10))
        vehicle_surface.fill(vehicle.color)
        screen.blit(vehicle_surface, (vehicle.x, vehicle.y))


    pygame.display.update()




pygame.quit()
sys.exit()
