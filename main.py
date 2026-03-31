import os
import time
import threading
from PIL import Image
from pynput import keyboard
import pyautogui
import random

pyautogui.FAILSAFE = False

WIDTH = 14
HEIGHT = 7

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYGROUND = os.path.join(BASE_DIR, "playground")
RESOURCE = os.path.join(BASE_DIR, "resources")


def load(name):
    return Image.open(os.path.join(RESOURCE, name)).resize((100, 100))

img_bg = load("background.png")
img_bird = load("bird.png")
img_pillar = load("piller.png")
food_pos = [5, 3]
velocity = 0
GRAVITY = 1
JUMP = -2
pillar_x = WIDTH - 1
pillar_gap_y = 3
GAP_SIZE = 2
passed = False


score = 0

running = True


def get_file_path(x, y):
    return os.path.join(PLAYGROUND, f"{y * WIDTH + x + 1}.png")

def draw():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            img_bg.save(get_file_path(x, y))

    for y in range(HEIGHT):
        if not (pillar_gap_y <= y < pillar_gap_y + GAP_SIZE):
            img_pillar.save(get_file_path(pillar_x, y))

    x, y = food_pos
    img_bird.save(get_file_path(x, y))
    pyautogui.press("f5")


def check_collision():
    x, y = food_pos
    
    if x == pillar_x:
        if not (pillar_gap_y <= y < pillar_gap_y + GAP_SIZE):
            return True
    return False

def game_loop():
    global velocity, food_pos, pillar_x, pillar_gap_y, running, score, passed

    while running:

        velocity += GRAVITY
        new_y = food_pos[1] + velocity

        if new_y < 0:
            new_y = 0
            velocity = 0
        elif new_y >= HEIGHT:
            new_y = HEIGHT - 1
            velocity = 0

        food_pos[1] = int(new_y)

        pillar_x -= 1

        if pillar_x < food_pos[0] and not passed:
            score += 1
            passed = True
            print("Score:", score)

        if pillar_x < 0:
            pillar_x = WIDTH - 1
            pillar_gap_y = random.randint(1, HEIGHT - GAP_SIZE - 1)
            passed = False

        if check_collision():
            running = False
            print("\n💀 GAME OVER")
            print("🏆 Final Score:", score)
            break

        draw()
        time.sleep(1)


def on_press(key):
    global running, velocity
    try:
        if hasattr(key, "char") and key.char == "p":
            running = False
            return False

        if key == keyboard.Key.space:
            velocity = JUMP
    except:
        pass

for y in range(HEIGHT):
    for x in range(WIDTH):
        img_bg.save(get_file_path(x, y))

draw()
threading.Thread(target=game_loop, daemon=True).start()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Exited")
