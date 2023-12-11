# Import required modules
import random
import curses

# Initialize the screen
s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)

# Snake speed
speed = 100
w.timeout(speed)

# Snake initial position
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Initial food position
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
food = [sh//2, sw//2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI, curses.color_pair(1))

# Initial snake direction
key = curses.KEY_RIGHT

# Function to get the next key
def get_key(previous_key):
    next_key = w.getch()
    new_key = previous_key if next_key == -1 else next_key
    if (new_key == curses.KEY_DOWN and previous_key == curses.KEY_UP) or \
       (new_key == curses.KEY_UP and previous_key == curses.KEY_DOWN) or \
       (new_key == curses.KEY_LEFT and previous_key == curses.KEY_RIGHT) or \
       (new_key == curses.KEY_RIGHT and previous_key == curses.KEY_LEFT):
        return previous_key
    else:
        return new_key

# Function to get the next position of the snake head
def get_new_head_position(snake, key):
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    return new_head

# Function to increase snake speed
def increase_speed(current_speed):
    new_speed = max(10, int(current_speed * 0.9)) # 10% speed increase, should not go below 10ms
    return new_speed

# Main game loop
while True:
    # Get the next key
    key = get_key(key)

    # Check if the snake hit the boundary
    if snake[0][0] in [0, sh] or \
       snake[0][1]  in [0, sw] or \
       snake[0] in snake[1:]:
        curses.endwin()
        quit()

    # Generate the new position for the snake's head
    new_head = get_new_head_position(snake, key)

    # Insert the new position of the head
    snake.insert(0, new_head)

    # Check if the snake got the food
    if snake[0] == food:
        # Increase the speed
        speed = increase_speed(speed)
        w.timeout(speed)

        # Generate new food position
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(1))
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Add the new head of the snake
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
