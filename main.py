'''
@author : Vishwa
@date : 29/04/2020
'''

import pygame
import pickle
from os import path
from objects import Cat, Obstacle, Background

CAT_IMAGES = [pygame.transform.scale(pygame.image.load(f'images/cat/cat{i}.png'), (150, 75)) for i in range(1, 9)]
OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load('images/obstacle.png'), (200, 120))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('images/bg.jpg'), (800, 500))

win = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Jungle Run')

pygame.font.init()
font = pygame.font.SysFont('comicsans', 40)

clock = pygame.time.Clock()

pygame.mixer.init()

cat = Cat(50, 375, CAT_IMAGES)
obs = Obstacle(350, 25, OBSTACLE_IMAGE)
bg = Background(800, 25, BACKGROUND_IMG)

score = 0
game_over = False


def game(ai_play=False):
    global game_over, score

    model = None
    music_played = False

    if ai_play:
        if not path.exists('model_data/model_nn.pickle'):
            from train import train
            train()

        with open('model_data/model_nn.pickle', 'rb') as f:
            model = pickle.load(f)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not ai_play and not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        cat.jumping = True
                        pygame.mixer.music.load('sounds/jump.mp3')
                        pygame.mixer.music.play()

        if not game_over:
            bg.draw(win)
            obs.draw(win)

            if ai_play:
                cat_pos = cat.y
                dist_from_obs = abs(cat.x - obs.obstacles[0])
                output = model.activate((cat_pos, dist_from_obs))

                if output[0] > 0.5:
                    cat.jumping = True
                    if not music_played:
                        pygame.mixer.music.load('sounds/jump.mp3')
                        pygame.mixer.music.play()
                        music_played = True

            if cat.jumping:
                cat.jump()

            if cat.landed:
                score += 1
                music_played = False
                cat.landed = False

            cat.draw(win)

            text = font.render(f'Score : {score}', 1, (255, 0, 0))
            win.blit(text, (50, 25))

            pygame.display.update()

            if cat.collided(obs):
                pygame.mixer.music.load('sounds/game-over.mp3')
                pygame.mixer.music.play()

                game_over = True

        clock.tick(25)


if __name__ == '__main__':
    # normal game : press space bar to jump
    # game()

    # AI playing the game
    game(True)
