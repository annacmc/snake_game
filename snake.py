"""
 Snake Game template, using classes.
 
 Derived from:
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
import pygame
import random
 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (222, 120, 31)
YELLOW = (237, 205, 54)
GREY = (149, 149, 149)

# Default snake colour
colour = WHITE

# Screen size
height = 600
width = 600
 
# Margin between each segment
segment_margin = 3
 
# Set the width and height of each snake segment
segment_width = min(height, width) / 40 - segment_margin
segment_height = min(height, width) / 40 - segment_margin

 
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0

# Set initial score
score = 0

game_ended = False

class Snake():
    """ Class to represent one snake. """

    # Constructor
    def __init__(self, type):
        self.segments = []
        self.spriteslist = pygame.sprite.Group()

        # Find a random spawn spot for the snake to begin that is within the available grid space
        startx = random.randrange(((segment_width + segment_margin)*15),(width-((segment_width + segment_margin)*10)),(segment_width + segment_margin))

        # Spawn Player snake in top range of grid, enemy snake in lower range of grid
        if type == "user":
            colour = WHITE
            starty = random.randrange(0,((segment_width + segment_margin)*15),(segment_width + segment_margin))

        elif type == "enemy":
            colour = ORANGE
            starty = random.randrange(((segment_width + segment_margin)*25),height,(segment_width + segment_margin))

        for i in range(15):
            x = startx - (i * (segment_width + segment_margin))
            y = starty

            segment = Segment(x, y, colour)
            self.segments.append(segment)
            self.spriteslist.add(segment)
            
    def move(self):

        global game_ended

        # Figure out where new segment will be
        x = self.segments[0].rect.x + x_change
        y = self.segments[0].rect.y + y_change
        
        # Don't move off the screen
        # At the moment a potential move off the screen means nothing happens, but it should end the game
        if 0 <= x <= width - segment_width and 0 <= y <= height - segment_height:
        
        # Insert new segment into the list
            segment = Segment(x, y, colour)
            self.segments.insert(0, segment)
            self.spriteslist.add(segment)

        # Get rid of last segment of the snake
        # .pop() command removes last item in list
            old_segment = self.segments.pop()
            self.spriteslist.remove(old_segment)

        else:
            game_ended = True

    def grow(self):  # grow snake by one segment each time it eats a piece of food
        # compare rect.x and rect.y positions of the last and second-to-last segments of the snake to
        # determine the direction in which the snake's tail should grow.


        # get difference between the last and second-to-last rect.x values
        xdelta = self.segments[-1].rect.x - self.segments[-2].rect.x
        ydelta = self.segments[-1].rect.y - self.segments[-2].rect.y

        # use difference between values to find correct location/direction to add segment
        x = self.segments[-1].rect.x + xdelta
        y = self.segments[-1].rect.y + ydelta

        # Create a new segment in the correct position and add it to the snake.
        segment = Segment(x, y, colour)
        self.segments.append(segment)
        self.spriteslist.add(segment)

    
class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of a snake. """

    # Constructor
    def __init__(self, x, y, colour):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(colour)
 
        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Food():
    """ Class to represent a group of randomly-placed food items. """

    # Constructor
    def __init__(self):
        self.food = []
        self.spriteslist = pygame.sprite.Group()
        for i in range(10):
            x = (segment_width + segment_margin) * random.randrange(width / (segment_width + segment_margin))
            y = (segment_width + segment_margin) * random.randrange(height / (segment_width + segment_margin))
            food_item = Food_item(x, y)
            self.food.append(food_item)
            self.spriteslist.add(food_item)

    # replenish method to replace eaten food
    def replenish(self):

        # add new food item to a random location
        x = (segment_width + segment_margin) * random.randrange(width / (segment_width + segment_margin))
        y = (segment_width + segment_margin) * random.randrange(height / (segment_width + segment_margin))

        # add food to sprites list & food list
        food_item = Food_item(x, y)

        # make sure that new food items do not land on the snake itself
        hit_list = pygame.sprite.spritecollide(food_item, my_snake.segments, False)

        #If the hit_list is not empty, recursively call the replenish() method to try again.
        if hit_list :
            self.replenish()
        elif not hit_list :
            self.food.append(food_item)
            self.spriteslist.add(food_item)


class Food_item(pygame.sprite.Sprite):
    """ Class to represent food sprites. """

    # Constructor
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstacle(pygame.sprite.Sprite):
    """ Class to represent one obstacle. """
    # Constructor
    def __init__(self):
        # Call the parent's constructor
        super().__init__()

        x = (segment_width + segment_margin) * random.randrange(width / (segment_width + segment_margin))
        y = (segment_width + segment_margin) * random.randrange(height / (segment_width + segment_margin))

        # Set height, width
        myheight = (segment_width + segment_margin) * random.randrange(4)
        mywidth = (segment_width + segment_margin) * random.randrange(8)

        #ensure obstacle doesnt run down into scoreboard
        if y + myheight >= height:
            y = (y - height)

        self.image = pygame.Surface([mywidth,myheight])
        self.image.fill(GREY)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Make sure that obstacles don't collide with the snake or enemy snake in its initial position.
        if pygame.sprite.spritecollide(self, my_snake.segments, False) or pygame.sprite.spritecollide(self, enemy_snake.segments, False):
            Obstacle()
        else:
            obstacles.add(self)


# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create a 600x600 sized screen
screen = pygame.display.set_mode([width, height+100])
 
# Set the title of the window
pygame.display.set_caption('Snake Game')
 
# Create an initial snake
my_snake = Snake("user")

# Create an enemy snake
enemy_snake = Snake("enemy")

# Create an initial food
my_food = Food()

# Create some obstacles
obstacles = pygame.sprite.Group()
# add some obstacles to the Group
for i in range(5):
    Obstacle()

 
clock = pygame.time.Clock()
done = False
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the direction based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    # move snake one step
    my_snake.move()

    # move enemy snake one step
    enemy_snake.ai_move()

    # did snake hit an obstacle?
    hit_list1 = pygame.sprite.spritecollide(my_snake.segments[0], obstacles, False)

    #did snake hit its own body
    hit_list2 = pygame.sprite.spritecollide(my_snake.segments[0], my_snake.segments[1:], False)

    if hit_list1 or hit_list2:
        game_ended = True

    # did the snake hit food
    hit_list3 = pygame.sprite.spritecollide(my_snake.segments[0], my_food.spriteslist, True)
    if hit_list3:
        my_snake.grow()
        my_food.replenish()
        score += 1

    # create a Font object from the system fonts
    font = pygame.font.SysFont("comicsansms", 35)

    # create an image (Surface) of the text for scoreboard
    text = font.render('Score = ' + str(score), True, (0, 0, 0))

    # create an image of the text for gameover notice
    finishtext = font.render('Game Over', True, (255, 0, 0))

    # get the bounding box for the image
    textrect = text.get_rect()

    # set the position of the scoreboard text
    textrect.centerx = 300
    textrect.centery = 650



    if game_ended == False:
        # -- Draw everything
        # Clear screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, [0, 600, 600, 150])
        my_snake.spriteslist.draw(screen)
        enemy_snake.spriteslist.draw(screen)
        my_food.spriteslist.draw(screen)
        obstacles.draw(screen)
        # blit (copy) the scorecard text image onto the screen
        screen.blit(text, textrect)
    elif game_ended == True:
        # Clear screen
        screen.fill(BLACK)
        # blit (copy) the scorecard text image onto the screen
        screen.blit(finishtext, textrect)


    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)


pygame.quit()
