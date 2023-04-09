import pygame as pg
from game.game import Game

def main():
    running = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement game
    game = Game(screen, clock)

    while running:
        game.run()

if __name__ == "__main__":
    main()