import pygame
import time
import random
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


    
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Dodge")

BG = pygame.transform.scale(pygame.image.load("grass.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 40

PLAYER_VEL = 5
STAR_WIDTH = 20
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

# Load the player image
player_img = pygame.image.load("ant.jpg")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Load the star image
star_img = pygame.image.load("rain.jpg")
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))


def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    score_text = FONT.render(f"Score: {score}", 1, "black")
    
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    WIN.blit(player_img, (player.x, player.y))

    for star in stars:
        WIN.blit(star_img, (star.x, star.y))

    pygame.display.update()


def main():
    while True:
        run = True
        score = 0

        player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                             PLAYER_WIDTH, PLAYER_HEIGHT)
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False
        play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        while run:
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT,
                                       STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if play_again_button.collidepoint(event.pos):
                            run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
            if keys[pygame.K_UP] and player.y - PLAYER_VEL >=0:
                player.y -= PLAYER_VEL
            if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
                player.y += PLAYER_VEL

            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break

            if hit:
                break

            draw(player, elapsed_time, stars, round(elapsed_time))
            score = round(elapsed_time)

            pygame.display.update()

        lost_text = FONT.render(f"You Lost! Score: {score}", 1, "black")
        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
        pygame.display.update()

        restart_game = False  # Flag to control game restart

        while not restart_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # LEFT BUTTON MOUSE
                        if play_again_button.collidepoint(event.pos):
                            restart_game = True  # Set flag to restart game

            pygame.draw.rect(WIN, (0, 255, 0), play_again_button)
            play_again_text = FONT.render("Play Again", 1, "black")
            WIN.blit(play_again_text,
                     (play_again_button.x + play_again_button.width / 2 - play_again_text.get_width() / 2,
                      play_again_button.y + play_again_button.height / 2 - play_again_text.get_height() / 2))

            pygame.display.update()

        if restart_game:
            continue
if __name__ == "__main__":
    pygame.init()
    main()
    app.run(debug=True)







