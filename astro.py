# Astro GAME

import pygame
import random
import sys
import os

# from livewires import games, color
from superwires import games, color


games.init(screen_width=640, screen_height=480, fps=50)


PROJECT_ROOT_INDIRECT = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')
PROJECT_ROOT = os.path.realpath(PROJECT_ROOT_INDIRECT)
FILE_SERVING_ROOT = os.path.join(PROJECT_ROOT, 'feat')
print(FILE_SERVING_ROOT)


class Explosion(games.Animation):
    """ Explosion animation """
    sound = games.load_sound(os.path.join(FILE_SERVING_ROOT, 'eksplozja.wav'))
    images = [
        os.path.join(FILE_SERVING_ROOT, "eksplozja1.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja2.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja3.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja4.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja5.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja6.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja7.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja8.bmp"),
        os.path.join(FILE_SERVING_ROOT, "eksplozja9.bmp")
    ]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images,
                                        x = x, y = y,
                                        repeat_interval = 4, n_repeats = 1,
                                        is_collideable = False)
        Explosion.sound.play()


class Ship(games.Sprite):
    """Sheep Object"""
    image = games.load_image(os.path.join(FILE_SERVING_ROOT, 'statek.bmp'))

    def __init__(self, game, x, y):
        """ Ship """
        super(Ship, self).__init__(image = Ship.image, x = x, y = y)
        self.game = game

    def update(self):
        """Control Ship"""
        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_DOWN):
            self.y +=1
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -=1
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x +=1

        # ship on screen
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        """ Destroy Ship """
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()
        self.game.end()


class Asteroid(games.Sprite):
    """ Asteroids """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {
        SMALL: games.load_image(os.path.join(FILE_SERVING_ROOT, 'asteroida_mala.bmp')),
        MEDIUM: games.load_image(os.path.join(FILE_SERVING_ROOT, 'asteroida_sred.bmp')),
        LARGE: games.load_image(os.path.join(FILE_SERVING_ROOT, 'asteroida_duza.bmp')),
      }

    SPEED = 2
    POINTS = 30

    total = 0

    def __init__(self, game, x, y, size):
        """ Asteroids """
        Asteroid.total += 1

        super(Asteroid, self).__init__(
            image = Asteroid.images[size],
            x=x,
            y=y,
            dx=0, #random.choice([1, -1]) * Asteroid.SPEED * random.random()/size,
            dy=random.randint(1, Asteroid.SPEED))

        self.game = game
        self.size = size

    def update(self):
        if self.top > games.screen.height:
            self.die()

    def die(self):
        """ Destroy """
        Asteroid.total -= 1

        self.game.score.value += Asteroid.POINTS
        self.game.score.right = games.screen.width - 10

        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()

        if Asteroid.total == 0:
            self.game.advance()


class Game(object):
    """Game"""
    def __init__(self):
        """ game init """
        # set level
        self.level = 0

        # sound load new level
        self.sound = games.load_sound(os.path.join(FILE_SERVING_ROOT, "poziom.wav"))

        # score
        self.score = games.Text(value = 0,
                                size = 30,
                                color = color.white,
                                top = 5,
                                right = games.screen.width - 10,
                                is_collideable = False)
        games.screen.add(self.score)

        self.ship = Ship(game = self,
                         x = games.screen.width/2,
                         y = games.screen.height/2)
        games.screen.add(self.ship)

    def play(self):
        """ play """
        print(os.path.join(FILE_SERVING_ROOT, "mglawica.jpg"))
        nebula_image = games.load_image(os.path.join(FILE_SERVING_ROOT, "mglawica.jpg"))
        games.screen.background = nebula_image

        # level 1
        self.advance()

        # play
        games.screen.mainloop()

    def advance(self):
        """ next level """
        self.level += 1

        for i in range(self.level):
            size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
            new_asteroid = Asteroid(game = self,
                                    x = random.randrange(games.screen.width),
                                    y = 0,
                                    size = size)
            games.screen.add(new_asteroid)

        # Shows level
        level_message = games.Message(value = "Poziom " + str(self.level),
                                      size = 40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = games.screen.width/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)

        # new level sound
        if self.level > 1:
            self.sound.play()

    def end(self):
        """ end game """
        # Show "The End"
        end_message = games.Message(value = "Koniec gry",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit,
                                    is_collideable = False)
        games.screen.add(end_message)

# main loop
def main():
    astrocrash = Game()
    astrocrash.play()
    done = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#start
main()
