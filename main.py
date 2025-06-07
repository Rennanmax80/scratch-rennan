import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

# Game States
game_state = "menu"  # "menu", "playing"
sound_on = True

# Music
music.set_volume(0.3)
music.play("bg_music")

# Buttons
class Button:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def draw(self):
        screen.draw.filled_rect(self.rect, (0, 100, 200))
        screen.draw.text(self.text, center=self.rect.center, fontsize=32, color="white")

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Menu buttons
buttons = [
    Button(Rect(WIDTH//2 - 100, 200, 200, 50), "Start Game"),
    Button(Rect(WIDTH//2 - 100, 280, 200, 50), "Sound On/Off"),
    Button(Rect(WIDTH//2 - 100, 360, 200, 50), "Exit"),
]

# Hero class
class Hero:
    def __init__(self):
        self.actor = Actor("hero_idle0", (100, 500))
        self.vy = 0
        self.on_ground = False
        self.frame = 0
        self.anim_timer = 0

    def update(self):
        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame = (self.frame + 1) % 2

        if keyboard.left:
            self.actor.x -= 3
            self.actor.image = f"hero_run{self.frame}"
        elif keyboard.right:
            self.actor.x += 3
            self.actor.image = f"hero_run{self.frame}"
        else:
            self.actor.image = f"hero_idle{self.frame}"

        # Gravity
        self.vy += 0.5
        self.actor.y += self.vy

        # Ground collision
        if self.actor.y >= 500:
            self.actor.y = 500
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vy = -10
            if sound_on:
                sounds.jump.play()

    def draw(self):
        self.actor.draw()

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.actor = Actor("enemy_idle0", (x, y))
        self.direction = 1
        self.frame = 0
        self.anim_timer = 0

    def update(self):
        self.anim_timer += 1
        if self.anim_timer % 15 == 0:
            self.frame = (self.frame + 1) % 2
        self.actor.image = f"enemy_idle{self.frame}"

        self.actor.x += self.direction * 2
        if self.actor.left < 100 or self.actor.right > 700:
            self.direction *= -1

    def draw(self):
        self.actor.draw()

# Instantiate hero and enemies
hero = Hero()
enemies = [Enemy(random.randint(200, 600), 500) for _ in range(3)]

def draw():
    screen.clear()
    if game_state == "menu":
        screen.draw.text("Forest Run", center=(WIDTH//2, 100), fontsize=60, color="green")
        for btn in buttons:
            btn.draw()
    elif game_state == "playing":
        hero.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if hero.actor.colliderect(enemy.actor):
                if sound_on:
                    sounds.hit.play()
                print("Game Over")  # Pode ser substituído por lógica de fim de jogo

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == "menu":
        if buttons[0].is_clicked(pos):
            game_state = "playing"
        elif buttons[1].is_clicked(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("bg_music")
            else:
                music.stop()
        elif buttons[2].is_clicked(pos):
            exit()

def on_key_down(key):
    if key == keys.SPACE and game_state == "playing":
        hero.jump()

pgzrun.go()