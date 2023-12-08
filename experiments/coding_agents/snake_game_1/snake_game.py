# Import libraries
import random
import curses

# Initialize the screen
s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Snake initial position
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Food initial position
food = [sh//2, sw//2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT

# Initial snake speed
speed = 100

# Function to get next key
def get_next_key(current_key):
    next_key = w.getch()
    
    # If no input is given, -1 is returned, and the snake keeps moving in the current direction
    return current_key if next_key == -1 else next_key

# Game loop
while True:
    next_key = get_next_key(key)

    # Direction restrictions added to prevent snake from moving in the opposite direction
    if next_key == curses.KEY_DOWN and key != curses.KEY_UP:
        key = next_key
    elif next_key == curses.KEY_UP and key != curses.KEY_DOWN:
        key = next_key
    elif next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT:
        key = next_key
    elif next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT:
        key = next_key

    if snake[0][0] in [0, sh] or \
        snake[0][1]  in [0, sw] or \
        snake[0] in snake[1:]:
        curses.endwin()
        quit()
    
    # Calculate the new head of the snake
    new_head = [snake[0][0], snake[0][1]]
    
    # Update snake direction based on key
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    
    snake.insert(0, new_head)

    # Check if the snake has gotten the food
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
        # Increase snake speed
        speed = max(10, speed - 10)
        w.timeout(speed)
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')
    
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
