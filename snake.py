import numpy
import pygame
import random
import time
import colorsys




def hsv_to_rgb(h, s=1, v=1):
    r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def draw_grid():
    for x in range(0, windowWidth, cellSize):
        pygame.draw.line(window, backgroundColor,(x,0),(x,windowHeight))
    for y in range(0, windowHeight, cellSize):
        pygame.draw.line(window, backgroundColor,(0,y),(windowWidth,y))

def fillCell(x, y, color):
    pygame.draw.rect(window, color, pygame.Rect((x * cellSize) + 1, (y * cellSize) + 1, cellSize-1, cellSize-1))

def placeFruit(snake, newHead):
    possiblePlacements = []
    for x in range(rows):
        for y in range(cols):
            possiblePlacements.append((x,y))
    for tuple in snake:
        if tuple in possiblePlacements:
            possiblePlacements.remove(tuple)
    
    possiblePlacements.remove(newHead)

    newLocation = random.choice(possiblePlacements)
    
    return newLocation

def outOfBounds(newHead):
    return not(newHead[0] >= 0 and newHead[0] < cols and newHead[1] >= 0 and newHead[1] < rows)

    

def updateSnake(snake, fruit, direction):
    #do something
    global hue
    global gameScore

    gamecondition = True
    head = snake[0]
    neck = snake[1]
    tail = snake[len(snake) - 1]
    newHead = head

    if direction == "up":
        newHead = (head[0], head[1] - 1);
    elif direction == "down":
        newHead = (head[0], head[1] + 1);
    elif direction == "left":
        newHead = (head[0] - 1, head[1]);
    else:
        newHead = (head[0]+ 1, head[1]);


    if newHead == neck:
        if direction == "up":
            return updateSnake(snake, fruit, "down")
        elif direction == "down":
            return updateSnake(snake, fruit, "up")
        elif direction == "left":
            return updateSnake(snake, fruit, "right")
        else:
            return updateSnake(snake, fruit, "left")

    if newHead in snake or outOfBounds(newHead): #illegal move
        return (False, fruit)
    if newHead != fruit:
        fillCell(tail[0], tail[1], backgroundColor) #basically removing the tail...
        snake.pop()
    else:
        fruit = placeFruit(snake, newHead)
        fillCell(fruit[0], fruit[1], fruitColor)
        gameScore += 1

    hue = (hue + 20) % 360
    snakeColor = hsv_to_rgb(hue)

    fillCell(newHead[0], newHead[1], snakeColor) #and attaching back at the front
    snake.insert(0,newHead)    


    return (gamecondition, fruit)


def game(snake, fruit):
    global hue
    global gameScore

    for section in snake:
        hue = (hue + 20) % 360
        snakeColor = hsv_to_rgb(hue)
        fillCell(section[0], section[1], snakeColor)

    fillCell(fruit[0], fruit[1], fruitColor)

    running = True
    decision = "notyet"
    while running:
        pygame.display.update()
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN: #VIM MOTIONS H-J-K-L
                if event.key == pygame.K_q:
                    #quit the game
                    running = False
                elif event.key == pygame.K_k:
                    #move snake up
                    decision = "up"
                elif event.key == pygame.K_h:
                    #move snake left
                    decision = "left"
                elif event.key == pygame.K_j and decision != "notyet":
                    #move snake down
                    decision = "down"
                elif event.key == pygame.K_l:
                    #move snake right
                    decision = "right"


        if decision != "notyet" and running != False:
            (running, fruit) = updateSnake(snake, fruit, decision)
            pygame.display.update()
            time.sleep(0.13)
            clock.tick(512)
    
    print("\nGAME OVER!")
    print("SCORE: {}".format(gameScore))




#constants
windowHeight = 600
windowWidth = 600
rows = 20
cols = 20
cellSize = windowHeight // cols
backgroundColor = (15, 214, 71)
hue = 0
snakeColor = hsv_to_rgb(hue)

gameScore = 0


#Initialization
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((windowHeight, windowWidth))
window.fill(backgroundColor)

draw_grid()

#player cell
snake = [(2,1), (2,2)] #head is the first pair, last pair is the tail


#fruitCell
fruit = (5,5)
fruitColor = (242, 7, 11)


game(snake, fruit)