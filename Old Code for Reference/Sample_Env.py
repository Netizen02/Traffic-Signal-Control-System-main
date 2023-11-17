import pygame
import random
import numpy as np

pygame.init()

size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Traffic Signal Control Game")


#mkaing signals using pygame
signal_width = 50
signal_height = 150
green_color = (0, 255, 0)
red_color = (255, 0, 0)


signal1 = pygame.Rect(200, 50, signal_width, signal_height)
signal2 = pygame.Rect(450, 300, signal_width, signal_height)


signal1_color = green_color
signal2_color = red_color

pygame.draw.rect(screen, signal1_color, signal1)
pygame.draw.rect(screen, signal2_color, signal2)

#making cars

car_width = 50
car_height = 50
car_color = (0, 0, 255)


car1 = pygame.Rect(0, 200, car_width, car_height)
car1_velocity = 5
car2 = pygame.Rect(650, 250, car_width, car_height)
car2_velocity = -5


pygame.draw.rect(screen, car_color, car1)
pygame.draw.rect(screen, car_color, car2)



#RL AGENT 

epsilon = 0.1
discount_factor = 0.9
learning_rate = 0.1
num_actions = 2

# Define RL algorithm functions
def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, num_actions - 1)
    else:
        return np.argmax(q_table[state])

def update_q_table(state, action, reward, next_state):
    q_table[state][action] += learning_rate * (reward + discount_factor * np.max(q_table[next_state]) - q_table[state][action])

# Initialize Q-table with zeros
q_table = np.zeros((num_states, num_actions))

# Loop through game episodes
for episode in range(num_episodes):
    # Reset game environment
    # ...
    # Loop through game steps
    for step in range(num_steps):
        # Choose action based on current state
        action = choose_action(state, epsilon)
        # Update game environment based on action
        # ...
        # Calculate reward and update Q-table
        reward = calculate_reward()
        update_q_table(state, action, reward, next_state)
        # Update current state
        state = next_state



#game looping
## Define game loop parameters
game_over = False
clock = pygame.time.Clock()

# Start game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    # Update game state
    update_game_state()

    # Draw game objects on screen
    draw_game
        


