import pygame
from random import randint

class Cat:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.img_count = 0
        self.jumping = False
        self.jump_count = 9
        self.landed = False
        self.images = images

    def jump(self):
        if self.jump_count >= -9:
            neg = 1
            if self.jump_count < 0:
                neg = -1

            self.y -= (self.jump_count ** 2) * 0.5 * neg
            self.jump_count -= 1

        else:
            self.jump_count = 9
            self.jumping = False
            self.landed = True

    def draw(self, win):
        if self.jumping:
            if self.jump_count > 3:
                win.blit(self.images[6], (self.x, self.y))
            else:
                win.blit(self.images[7], (self.x, self.y))

        else:
            win.blit(self.images[self.img_count], (self.x, self.y))

        self.img_count += 1
        if self.img_count % 8 == 0:
            self.img_count = 0

    def collided(self, obstacle):
        obstacle_mask = obstacle.get_mask()
        cat_mask = pygame.mask.from_surface(self.images[self.img_count])

        offset = (self.x - obstacle.obstacles[0], round(self.y) - obstacle.y)

        collision_point = obstacle_mask.overlap(cat_mask, offset)

        if collision_point:
            return True

        return False


class Obstacle:
    def __init__(self, y, fps, image):
        self.y = y
        self.obstacles = [randint(800, 1200)]
        self.made = False
        self.image = image
        self.fps = fps

    def make_obstacle(self):
        if not self.made and self.obstacles[0] < 400:
            self.obstacles.append(randint(800, 1200))
            self.made = True

        if self.obstacles[0] + 150 < 0:
            self.obstacles.pop(0)
            self.made = False

    def draw(self, win):
        for i in range(len(self.obstacles)):
            win.blit(self.image, (self.obstacles[i], self.y))
            self.obstacles[i] -= self.fps

        self.make_obstacle()

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Background:
    def __init__(self, width, fps, image):
        self.bg1 = 0
        self.bg2 = 800
        self.fps = fps
        self.width = width
        self.image = image

    def move(self):
        self.bg1 -= self.fps
        self.bg2 -= self.fps

        if self.bg1 + self.width < 0:
            self.bg1 = self.width - self.fps

        if self.bg2 + self.width < 0:
            self.bg2 = self.width - self.fps

    def draw(self, win):
        win.blit(self.image, (self.bg1, 0))
        win.blit(self.image, (self.bg2, 0))
        self.move()