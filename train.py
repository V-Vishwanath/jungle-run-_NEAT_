import neat
import pygame
import pickle
from os import path
from objects import Cat, Obstacle, Background

CAT_IMAGES = [pygame.transform.scale(pygame.image.load(f'images/cat/cat{i}.png'), (150, 75)) for i in range(1, 9)]
OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load('images/obstacle.png'), (200, 120))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load('images/bg.jpg'), (800, 500))

win = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Jungle Run : Training')

pygame.font.init()
font = pygame.font.SysFont('comicsans', 40)

clock = pygame.time.Clock()


def eval_genome(genomes, config):
    nns = []
    gens = []
    cats = []
    scores = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nns.append(net)
        cats.append(Cat(50, 375, CAT_IMAGES))
        g.fitness = 0
        gens.append(g)
        scores.append(0)

    obs = Obstacle(350, 25, OBSTACLE_IMAGE)
    bg = Background(800, 25, BACKGROUND_IMG)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        bg.draw(win)
        obs.draw(win)

        if len(cats) == 0:
            break

        for index, cat in enumerate(cats):
            gens[index].fitness += 0.05
            output = nns[index].activate((cat.y, abs(cat.x - obs.obstacles[0])))

            if output[0] > 0.5:
                cat.jumping = True

            if cat.jumping:
                cat.jump()

            if cat.landed:
                scores[index] += 1
                for g in gens:
                    g.fitness += 1
                cat.landed = False

            if cat.collided(obs):
                gens.pop(index)
                nns.pop(index)
                cats.pop(index)
                scores.pop(index)

            cat.draw(win)

        if len(scores) > 0:
            score = max(scores)
            text = font.render(f'Score : {score}', 1, (255, 0, 0))
            win.blit(text, (50, 25))

            if score >= 500:
                with open('model_data/model_nn.pickle', 'wb') as f:
                    pickle.dump(nns[0], f)
                break

        text = font.render(f'Alive : {len(cats)}', 1, (0, 255, 0))
        win.blit(text, (50, 52))

        pygame.display.update()


def train():
    config_file = path.abspath('model_data/config.txt')
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file)

    pop = neat.Population(config)
    pop.run(eval_genome, 50)
