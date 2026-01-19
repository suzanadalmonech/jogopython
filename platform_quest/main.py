import random
import math

WIDTH = 800
HEIGHT = 450
GRAVITY = 0.6


class AnimatedActor:
    def __init__(self, frames, pos):
        self.frames = frames
        self.frame_index = 0
        self.actor = Actor(frames[0], pos)
        self.animation_timer = 0

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]
            self.animation_timer = 0

    def draw(self):
        self.actor.draw()


class Hero(AnimatedActor):
    def __init__(self):
        self.idle_frames = ["hero_idle_0", "hero_idle_1"]
        self.walk_frames = ["hero_walk_0", "hero_walk_1"]

        super().__init__(self.idle_frames, (100, 300))

        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        self.velocity_x = 0

        if keyboard.left:
            self.velocity_x = -3
            self.frames = self.walk_frames
        elif keyboard.right:
            self.velocity_x = 3
            self.frames = self.walk_frames
        else:
            self.frames = self.idle_frames

        if self.on_ground and keyboard.space:
            self.velocity_y = -12
            self.on_ground = False
            sounds.jump.play()

        self.velocity_y += GRAVITY

        self.actor.x += self.velocity_x
        self.actor.y += self.velocity_y

        if self.actor.y >= 300:
            self.actor.y = 300
            self.velocity_y = 0
            self.on_ground = True

        self.animate()


class Enemy(AnimatedActor):
    def __init__(self, left_limit, right_limit):
        # 🔥 AGORA COM 3 FRAMES
        self.idle_frames = [
            "enemy_idle_0",
            "enemy_idle_1",
            "enemy_idle_2"
        ]

        start_x = random.randint(left_limit, right_limit)
        super().__init__(self.idle_frames, (start_x, 300))

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = random.choice([-2, 2])

    def update(self):
        self.actor.x += self.speed

        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.speed *= -1

        self.animate()


hero = Hero()

enemies = [
    Enemy(300, 500),
    Enemy(550, 750)
]

game_state = "menu"
sound_enabled = True


start_button = Actor("button", center=(400, 220))
sound_button = Actor("button", center=(400, 280))
exit_button = Actor("button", center=(400, 340))


music.play("background")
music.set_volume(0.4)


def draw_menu():
    screen.fill((25, 25, 45))
    screen.draw.text(
        "PLATFORM QUEST",
        center=(400, 120),
        fontsize=60,
        color="white"
    )

    start_button.draw()
    sound_button.draw()
    exit_button.draw()

    screen.draw.text("Start Game", center=start_button.center, fontsize=32)
    screen.draw.text("Sound On / Off", center=sound_button.center, fontsize=32)
    screen.draw.text("Exit", center=exit_button.center, fontsize=32)


def draw():
    if game_state == "menu":
        draw_menu()
    else:
        screen.clear()
        hero.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    if game_state == "game":
        hero.update()

        for enemy in enemies:
            enemy.update()

            if hero.actor.colliderect(enemy.actor):
                sounds.hit.play()
                hero.actor.pos = (100, 300)


def on_mouse_down(pos):
    global game_state, sound_enabled

    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "game"

        elif sound_button.collidepoint(pos):
            sound_enabled = not sound_enabled
            music.set_volume(0.4 if sound_enabled else 0)

        elif exit_button.collidepoint(pos):
            quit()