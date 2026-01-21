import pgzrun
import random
import math

# Configuração da janela
WIDTH = 800
HEIGHT = 600

class Hero:
    def __init__(self):
        self.idle_frames = ["hero_idle_0", "hero_idle_1", "hero_idle_3"]
        self.walk_frames = ["hero_walk_0", "hero_walk_1", "hero_walk_3"]
        self.actor = Actor(self.idle_frames[0], (400, 300))
        self.frame_index = 0
        self.animation_timer = 0
        self.score = 0
        self.lives = 5
        self.invincibility_frames = 0

    def update(self):
        dx, dy = 0, 0
        is_moving = False
        move_speed = 5
        
        if keyboard.left and self.actor.left > 0:
            dx = -move_speed
            is_moving = True
        elif keyboard.right and self.actor.right < WIDTH:
            dx = move_speed
            is_moving = True
        if keyboard.up and self.actor.top > 0:
            dy = -move_speed
            is_moving = True
        elif keyboard.down and self.actor.bottom < HEIGHT:
            dy = move_speed
            is_moving = True

        self.actor.x += dx
        self.actor.y += dy

        self.animation_timer += 1
        current_animation = self.walk_frames if is_moving else self.idle_frames
        if self.animation_timer % 10 == 0:
            self.frame_index = (self.frame_index + 1) % 3
            self.actor.image = current_animation[self.frame_index]

class Enemy:
    def __init__(self):
        self.frames = ["enemy_idle_0", "enemy_idle_1", "enemy_idle_2"]
        self.actor = Actor(self.frames[0])
        self.actor.x = random.choice([50, 750])
        self.actor.y = random.randint(50, 550)
        self.angle = random.uniform(0, math.pi * 2)
        self.speed = 3
        self.frame_index = 0
        self.animation_timer = 0

    def move_logic(self):
        self.actor.x += math.cos(self.angle) * self.speed
        self.actor.y += math.sin(self.angle) * self.speed
        
        if self.actor.left < 0 or self.actor.right > WIDTH: self.angle = math.pi - self.angle
        if self.actor.top < 0 or self.actor.bottom > HEIGHT: self.angle = -self.angle

        self.animation_timer += 1
        if self.animation_timer % 12 == 0:
            self.frame_index = (self.frame_index + 1) % 3
            self.actor.image = self.frames[self.frame_index]

# --- INICIALIZAÇÃO ---
player = Hero()
enemies = [Enemy() for _ in range(4)]
coins = []
game_state = "MENU"
is_paused = False
sound_active = True

# Botões do Menu
start_button = Rect((300, 200), (200, 60))
sound_button = Rect((300, 300), (200, 60))
main_exit_button = Rect((300, 400), (200, 60))

# Botões In-game
ingame_exit_button = Rect((710, 10), (80, 30))
pause_button = Rect((620, 10), (80, 30))

def manage_game_coins():
    while len(coins) < 5:
        coins.append({"pos": (random.randint(50, 750), random.randint(50, 550))})

def draw():
    screen.clear()
    if game_state == "MENU":
        screen.fill((30, 30, 50))
        screen.draw.text("ADVENTURE EXPLORER", center=(400, 100), fontsize=60, color="white")
        screen.draw.filled_rect(start_button, "white")
        screen.draw.text("START GAME", center=start_button.center, color="black", fontsize=25)
        screen.draw.filled_rect(sound_button, "white")
        status = "ON" if sound_active else "OFF"
        screen.draw.text(f"SOUND: {status}", center=sound_button.center, color="black", fontsize=25)
        screen.draw.filled_rect(main_exit_button, "red")
        screen.draw.text("EXIT GAME", center=main_exit_button.center, color="white", fontsize=25)

    elif game_state == "PLAY":
        screen.fill((34, 139, 34))
        for coin in coins: screen.draw.filled_circle(coin["pos"], 8, "gold")
        for enemy in enemies: enemy.actor.draw()
        if player.invincibility_frames % 10 < 5: player.actor.draw()
        
        # --- HUD (Informações na tela) ---
        screen.draw.text(f"SCORE: {player.score}/100", (20, 15), fontsize=30, shadow=(1,1))
        screen.draw.text(f"LIVES: {player.lives}", (20, 45), fontsize=30, color="red", shadow=(1,1))
        
        # Botões
        screen.draw.filled_rect(ingame_exit_button, (180, 0, 0))
        screen.draw.text("EXIT", center=ingame_exit_button.center, fontsize=18, color="white")
        
        pause_color = (200, 200, 0) if not is_paused else (0, 0, 200)
        screen.draw.filled_rect(pause_button, pause_color)
        pause_text = "PAUSE" if not is_paused else "RESUME"
        screen.draw.text(pause_text, center=pause_button.center, fontsize=18, color="white")

        if is_paused:
            screen.draw.text("GAME PAUSED", center=(400, 300), fontsize=80, color="white", shadow=(2,2))

    elif game_state == "GAMEOVER" or game_state == "VICTORY":
        screen.fill((0, 0, 0))
        msg = "GAME OVER" if game_state == "GAMEOVER" else "YOU WIN!"
        color = "red" if game_state == "GAMEOVER" else "green"
        screen.draw.text(msg, center=(400, 300), fontsize=100, color=color)
        screen.draw.text("Press SPACE for Menu", center=(400, 450), fontsize=30)

def update():
    global game_state, coins, is_paused
    if game_state == "PLAY" and not is_paused:
        player.update()
        manage_game_coins()
        for enemy in enemies:
            enemy.move_logic()
            if player.actor.colliderect(enemy.actor) and player.invincibility_frames == 0:
                player.lives -= 1
                player.invincibility_frames = 60
                if sound_active: sounds.roboxel.play()
                if player.lives <= 0: game_state = "GAMEOVER"; music.stop()

        if player.invincibility_frames > 0: player.invincibility_frames -= 1

        for coin in coins[:]:
            if player.actor.collidepoint(coin["pos"]):
                coins.remove(coin)
                player.score += 10
                if sound_active: sounds.mistery.play()
                if player.score >= 100: game_state = "VICTORY"; music.stop()

    if (game_state == "GAMEOVER" or game_state == "VICTORY") and keyboard.space:
        reset_to_menu()

def on_mouse_down(pos):
    global game_state, sound_active, is_paused
    if game_state == "MENU":
        if start_button.collidepoint(pos):
            game_state = "PLAY"
            if sound_active: music.play("plimplom"); music.set_volume(0.3)
        elif sound_button.collidepoint(pos):
            sound_active = not sound_active
            if not sound_active: music.stop()
        elif main_exit_button.collidepoint(pos): exit()
        
    elif game_state == "PLAY":
        if ingame_exit_button.collidepoint(pos):
            reset_to_menu()
        elif pause_button.collidepoint(pos):
            is_paused = not is_paused

def reset_to_menu():
    global game_state, player, coins, is_paused
    music.stop()
    player = Hero()
    coins = []
    is_paused = False
    game_state = "MENU"

pgzrun.go()