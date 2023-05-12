import pygame
import random
from pygame.locals import *
from random import randint

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 400, 700
CANVA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sulifa")

BG = pygame.transform.scale(pygame.image.load("images/background.png"), (WIDTH, HEIGHT))

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

H_ITEMS = 50
W_ITEMS = 50

CLIPS = pygame.transform.scale(pygame.image.load('images/clips.png'), (W_ITEMS, H_ITEMS))
ROCK = pygame.transform.scale(pygame.image.load('images/rock.png'), (W_ITEMS, H_ITEMS))
PAPER = pygame.transform.scale(pygame.image.load('images/paper.png'), (W_ITEMS, H_ITEMS))

sound = pygame.mixer.Sound('sounds/music.mp3')
sound.play()


def move_and_draw(obj, x, y, vel_x, vel_y):
    x += vel_x
    y += vel_y
    if x < 0:
        x = 0
        vel_x = -vel_x
    elif x > 400 - obj.get_width():
        x = 400 - obj.get_width()
        vel_x = -vel_x
    if y < 0:
        y = 0
        vel_y = -vel_y
    elif y > 700 - obj.get_height():
        y = 700 - obj.get_height()
        vel_y = -vel_y
    CANVA.blit(obj, (x, y))
    return x, y, vel_x, vel_y

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def repel(obj1, obj2, dist):
    dx = obj1[0] - obj2[0]
    dy = obj1[1] - obj2[1]
    if dist > 0:
        force = 5 / (dist ** 2)
        obj1[2] += force * dx
        obj1[3] += force * dy
        obj2[2] -= force * dx
        obj2[3] -= force * dy

def main():
    run = True
    clips = []
    rock = []
    paper = []
    for i in range(random.randint(1, 10)):
        clips.append(
            [random.randint(50, 350), random.randint(50, 650), random.randint(-5, 5), random.randint(-5, 5)])
    for i in range(random.randint(1, 10)):
        rock.append(
            [random.randint(50, 350), random.randint(50, 650), random.randint(-5, 5), random.randint(-5, 5)])
    for i in range(random.randint(1, 10)):
        paper.append(
            [random.randint(50, 350), random.randint(50, 650), random.randint(-5, 5), random.randint(-5, 5)])

    while run:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        CANVA.blit(BG, (0, 0))

        for i, c in enumerate(clips):
            for j, other in enumerate(clips[i+1:] + rock + paper):
                dist = distance(c[0], c[1], other[0], other[1])
                if dist < 50:
                    repel(c, other, dist)

            c[0], c[1], c[2], c[3] = move_and_draw(CLIPS, c[0], c[1], c[2], c[3])

        for i, r in enumerate(rock):
            for j, other in enumerate(clips + rock[i+1:] + paper):
                dist = distance(r[0], r[1], other[0], other[1])
                if dist < 50:
                    repel(r, other, dist)

            r[0], r[1], r[2], r[3] = move_and_draw(ROCK, r[0], r[1], r[2], r[3])

        for i, p in enumerate(paper):
            for j, other in enumerate(clips + rock + paper[i+1:]):
                dist = distance(p[0], p[1], other[0], other[1])
                if dist < 50:
                    repel(p, other, dist)

            p[0], p[1], p[2], p[3] = move_and_draw(PAPER, p[0], p[1], p[2], p[3])

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()