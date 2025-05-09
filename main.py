from tkinter import *
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#89CFF0"
FOOD_COLOR = "#00FF00"
BACKGROUND_COLOR = "#000000"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag = "snake")
            self.squares.append(square)


class Food:
    
    def __init__(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE

            if[x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")


def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE


        # Handle wrapping (moving snake across screen edges)
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE  # Wrap to the right
    elif x >= GAME_WIDTH:
        x = 0  # Wrap to the left
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE  # Wrap to the bottom
    elif y >= GAME_HEIGHT:
        y = 0  # Wrap to the top
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score, SPEED
        score += 1

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        label.config(text="Score:{} High Score:{}".format(score, high_score))
        canvas.delete("food")
        food =  Food()

        #Decrease Speed to make the game harder over time
        if SPEED > 20:
            SPEED -= 1

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
 
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('colsolas',70), text="GAME OVER", fill="red", tag="gameover")
    
    # Delay button creation slightly to avoid UI issues
    window.after(100, show_restart_button)

def show_restart_button():
    # Create the restart button
    restart_button = Button(window, text="RESTART", font=('consolas', 20), command=restart_game)
    
    # Place it in the center of the window
    restart_button.place(relx=0.5, rely=0.7, anchor=CENTER)

    # Store reference so we can remove it later
    window.restart_button = restart_button

def restart_game():
    global snake, food, score, direction, SPEED
    #Reset score
    score = 0
    SPEED = 100
    direction = "down"
    label.config(text="Score:{} High Score:{}".format(score, high_score))

    #Remove restart button
    window.restart_button.destroy()

    #Clear canvas
    canvas.delete(ALL)

    #Recreate snake and food
    snake = Snake()
    food = Food()

    #Start game loop
    next_turn(snake, food)

def save_high_score(high_score):
    try:
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))  # Write the new high score into the file
    except Exception as e:
        print("Error saving high score:", e)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())  # Return the high score as an integer
    except FileNotFoundError:
        return 0  # If the file doesn't exist, return 0 as the default high score
    except Exception as e:
        print("Error reading high score:", e)
        return 0


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0 
high_score = load_high_score()
direction = 'down'

label= Label(window, text="Score:{} High Score:{}".format(score, high_score), font=('consolas',40))
label.pack()

canvas = Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Up>',lambda event: change_direction('up'))
window.bind('<Down>',lambda event: change_direction('down'))

snake = Snake()
food = Food()
next_turn(snake, food)


window.mainloop()