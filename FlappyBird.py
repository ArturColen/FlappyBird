# Import libraries
import pygame
import os
import random

# Set the game screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800 

# Import the object images
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png'))),
]

# Set the score font 
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

# Create the bird class
class Bird:
    IMAGES = BIRD_IMAGES

    # Rotation animation
    MAXIMUM_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

    # Function for setting the attributes of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMAGES[0]

    # Function of the bird jump
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    # Function of the bird movement
    def move(self):
        # Calculate the displacement
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # Restrict the displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2
        
        self.y += displacement

        # Angle of the bird's fall
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAXIMUM_ROTATION:
                self.angle = self.MAXIMUM_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATION

    # Function for draw the bird
    def draw(self, screen):
        # Define which bird image to use
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]
        elif self.image_count >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        # Stop the bird's wing in the fall
        if self.angle <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2

        # Draw the image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=pos_center_image)
        screen.blit(rotated_image, rectangle.topleft)

    # Function to catch the bird's mask
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

# Create the pipe class
class Pipe:
    DISTANCE = 200
    SPEED = 5

    # Function for setting the attributes of the pipe
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.base_pos = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.BASE_PIPE = PIPE_IMAGE
        self.passed = False
        self.define_height()

    # Function for set the pipe height
    def define_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.TOP_PIPE.get_height()
        self.base_pos = self.height + self.DISTANCE

    # Function for move the pipe
    def move(self):
        self.x -= self.SPEED

    # Function for drawing the pipe
    def draw(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.top_pos))
        screen.blit(self.BASE_PIPE, (self.x, self.base_pos))

    # Function for checking collision between bird and pipe
    def colide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        top_distance = (self.x - bird.x, self.top_pos - round(bird.y))
        base_distance = (self.x - bird.x, self.base_pos - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        if base_point or top_point:
            return True
        else:
            return False

# Create the floor class
class Floor:
    SPEED = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    # Function for setting the attributes of the floor
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    # Function for moving the floor
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    # Function for drawing the floor
    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

# Function to draw the game screen
def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    # Put the score in the screen
    text = POINTS_FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    # Draw the floor in the screen
    floor.draw(screen)
    # Update the screen
    pygame.display.update()

# Function to execute the game
def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    rotating = True
    while rotating:
        clock.tick(30)

        # Interaction with the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rotating = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        # Move the objects
        for bird in birds:
            bird.move()
        floor.move()

        add_pipe = False
        remove_pipes = []

        # Action when the bird collides or passes through the pipe
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colide(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipes.append(pipe)

        # Add point when the bird is passing through the pipe
        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
        # Remove pipe after bird passes through it
        for pipe in remove_pipes:
            pipes.remove(pipe)

        # The bird dies if it touches the sky or the floor
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)

# Execute the game
if __name__ == '__main__':
    main()