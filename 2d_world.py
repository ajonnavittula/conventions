import pygame
import sys
import os
import math
import numpy as np
import time
import pickle


class Joystick(object):

    def __init__(self):
        self.gamepad = pygame.joystick.Joystick(0)
        self.gamepad.init()
        self.DEADBAND = 0.1

    def input(self):
        pygame.event.get()
        z1 = self.gamepad.get_axis(0)
        if abs(z1) < self.DEADBAND:
            z1 = 0.0
        z2 = self.gamepad.get_axis(1)
        if abs(z2) < self.DEADBAND:
            z2 = 0.0
        start = self.gamepad.get_button(1)
        stop = self.gamepad.get_button(0)
        return [z1, z2], start, stop


class Object(pygame.sprite.Sprite):

    def __init__(self, position, color):

        # create sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # initial conditions
        self.x = position[0]
        self.y = position[1]
        self.rect.x = (self.x * 500) + 100 - self.rect.size[0] / 2
        self.rect.y = (self.y * 500) + 100 - self.rect.size[1] / 2


class Player(pygame.sprite.Sprite):

    def __init__(self, position):

        # create sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill((255, 128, 0))
        self.rect = self.image.get_rect()

        # initial conditions
        self.x = position[0]
        self.y = position[1]
        self.rect.x = (self.x * 500) + 100 - self.rect.size[0] / 2
        self.rect.y = (self.y * 500) + 100 - self.rect.size[1] / 2

    def update(self, s):
        self.rect = self.image.get_rect(center=self.rect.center)
        self.x = s[0]
        self.y = s[1]
        self.rect.x = (self.x * 500) + 100 - self.rect.size[0] / 2
        self.rect.y = (self.y * 500) + 100 - self.rect.size[1] / 2


def main():

    filename = sys.argv[1]
    savename = "data/demos/" + filename + ".pkl"

    clock = pygame.time.Clock()
    pygame.init()
    fps = 30

    world = pygame.display.set_mode([700, 700])
    position_player = np.asarray([.1, .35])
    postition_blue = np.asarray([0.8, 0.4])
    postition_green = np.asarray([0.8, 0.3])
    postition_gray = np.asarray([0., 0.])
    obs_position = postition_blue.tolist() + postition_green.tolist() + postition_gray.tolist()


    player = Player(position_player)
    blue = Object(postition_blue, [0, 0, 255])
    green = Object(postition_green, [0, 255, 0])
    gray = Object(postition_gray, [128, 128, 128])

    sprite_list = pygame.sprite.Group()
    sprite_list.add(player)
    sprite_list.add(blue)
    sprite_list.add(green)
    sprite_list.add(gray)

    world.fill((0,0,0))
    sprite_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)

    demonstration = []
    sampletime = 5
    count = 0

    while True:

        q = np.asarray([player.x, player.y])
        # s = obs_position + q.tolist()
        s = q.tolist()

        stop = 0
        z1 = 0
        z2 = 0
        action = [0, 0]
        left = pygame.key.get_pressed()[pygame.K_LEFT]
        up = pygame.key.get_pressed()[pygame.K_UP]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        stop = pygame.key.get_pressed()[pygame.K_RETURN]
        
        z1 = right - left
        z2 = down - up

        action = [z1, z2]

        if stop:
            pickle.dump( demonstration, open( savename, "wb" ) )
            print(demonstration)
            print("[*] Done!")
            print("[*] I recorded this many datapoints: ", len(demonstration))
            pygame.quit(); sys.exit()

        q += np.asarray(action) * 0.01

        # dynamics
        player.update(q)

        # animate
        world.fill((0,0,0))
        sprite_list.draw(world)
        pygame.display.flip()
        clock.tick(fps)

        pygame.event.pump()
        # save
        if not count % sampletime:
            demonstration.append(s)
        count += 1

if __name__ == "__main__":
    main()