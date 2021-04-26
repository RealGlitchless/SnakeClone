import pygame as pg
import sys
import random
import ctypes

pg.init()

# Get window width and height and set to window size
size = width, height = 400, 400
gameHeight = 40

# Set windows size
display = pg.display.set_mode(size)

# Set title
pg.display.set_caption("Snake Clone")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Font
score_font = pg.font.SysFont("comicsansms", 24)

# Score
score = 0
highScore = 0


def Score(get_score):
    value = score_font.render("Your Score: " + str(get_score), True, green)
    display.blit(value, [0, 0])


def highscore(get_highscore):
    value = score_font.render("Highscore: " + str(get_highscore), True, green)
    display.blit(value, [200, 0])


def snake(snake_block, snake_list):
    for y in snake_list:
        pg.draw.rect(display, white, [y[0], y[1], snake_block, snake_block])


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


isRunning = True
while isRunning:
    # Place snake
    snake_x = 50
    tempSnake_x = 0
    snake_y = 50
    tempSnake_y = 0
    snakeBlock = 10

    # Set speed
    clock = pg.time.Clock()
    snakeSpeed = 15

    # Set snake list
    snakeList = []
    Length_of_snake = 1

    # Set placement randomizer of food
    food_x = round(random.randrange(0, width - snakeBlock) / 10.0) * 10.0
    food_y = round(random.randrange(gameHeight, height - snakeBlock) / 10.0) * 10.0

    gameOver = False
    while not gameOver:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

        # Get key pressed
        playerKey = pg.key.get_pressed()
        # If up arrow key is pressed
        if playerKey[pg.K_UP]:
            # Makes snake unable to make a 180
            if tempSnake_y >= snake_y:
                tempSnake_y = snake_y
                snake_y -= 10
                tempSnake_x = snake_x
            else:
                snake_y += 10

        # If down arrow is pressed
        elif playerKey[pg.K_DOWN]:
            # Makes snake unable to make a 180
            if tempSnake_y <= snake_y:
                tempSnake_y = snake_y
                snake_y += 10
                tempSnake_x = snake_x
            else:
                snake_y -= 10

        # If left arrow is pressed
        elif playerKey[pg.K_LEFT]:
            # Makes snake unable to make a 180
            if tempSnake_x >= snake_x:
                tempSnake_x = snake_x
                snake_x -= 10
                tempSnake_y = snake_y
            else:
                snake_x += 10

        # If right arrow is pressed
        elif playerKey[pg.K_RIGHT]:
            # Makes snake unable to make a 180
            if tempSnake_x <= snake_x:
                tempSnake_x = snake_x
                snake_x += 10
                tempSnake_y = snake_y
            else:
                snake_x -= 10

        # If no key is pressed continue in the same direction
        elif not playerKey[pg.K_UP] or \
                playerKey[pg.K_DOWN] or \
                playerKey[pg.K_LEFT] or \
                playerKey[pg.K_RIGHT]:
            # Prevents snake from moving when starting game
            if tempSnake_x != 0 or tempSnake_y != 0:
                if tempSnake_y > snake_y:
                    snake_y -= 10
                if tempSnake_y < snake_y:
                    snake_y += 10
                if tempSnake_x > snake_x:
                    snake_x -= 10
                if tempSnake_x < snake_x:
                    snake_x += 10

        # Check if snake has hit corners
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < gameHeight:
            gameOver = True
            score = (Length_of_snake - 1)

        # Check if snake has hit food
        if snake_x == food_x and snake_y == food_y:
            # If so, generates a new placement for food
            food_x = round(random.randrange(0, width - snakeBlock) / 10.0) * 10.0
            food_y = round(random.randrange(gameHeight, height - snakeBlock) / 10.0) * 10.0
            Length_of_snake += 1
            snakeSpeed += 0.5

        # Draw new frame with updated info
        display.fill(black)
        pg.draw.rect(display, red, [food_x, food_y, snakeBlock, snakeBlock])
        # Save snakes head in list
        snakeHead = [snake_x, snake_y]
        snakeList.append(snakeHead)
        if len(snakeList) > Length_of_snake:
            del snakeList[0]

        # Check if snake hits itself
        for x in snakeList[:-1]:
            if x == snakeHead:
                gameOver = True
                score = (Length_of_snake - 1)

        # Draw snake and tail
        snake(snakeBlock, snakeList)
        # Draw current score
        Score(Length_of_snake - 1)
        # Draw highscore
        highscore(highScore)
        # Update display
        pg.display.update()

        clock.tick(snakeSpeed)

    # If score is higher than old highscore then replace
    if score > highScore:
        highScore = score

    # Display popup with score and current highscore
    # If 'Yes' is pressed the game will start again
    # If 'No' is pressed the game will end
    choice = Mbox('Game Over!',
                  f'You scored {score}\n'
                  f'Your current highscore is {highScore}\n'
                  'Do you want to play again?', 4)

    YES = 6
    NO = 7
    if choice == YES:
        gameOver = False

    if choice == NO:
        isRunning = False
