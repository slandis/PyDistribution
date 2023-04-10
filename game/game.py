import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE, MIN_ZOOM, MAX_ZOOM, ZOOM_FACTOR
from .utils import draw_text
from .camera import Camera

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # world
        self.world = World(self.screen, 50, 50)

        # camera
        self.camera = Camera(self.width, self.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_a and self.world.p_col > 0:
                    self.world.p_col -= 1
                if event.key == pg.K_d and self.world.p_col < self.world.columns-1:
                    self.world.p_col += 1
                if event.key == pg.K_w and self.world.p_row > 0:
                    self.world.p_row -= 1
                if event.key == pg.K_s and self.world.p_row < self.world.rows-1:
                    self.world.p_row += 1
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    #self.world.zoomIn()
                    pass
                elif event.button == 5:
                    #self.world.zoomOut()
                    pass

    def update(self):
        self.camera.update()
        self.world.update(self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)

        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )

        draw_text(
            self.screen,
            'zoom={}'.format(round(self.world.zoom_level, 2)),
            25,
            (255, 255, 255),
            (10, 30)
        )

        draw_text(
            self.screen,
            'screenX={},screenY={}'.format(self.screen.get_size()[0],self.screen.get_size()[1]),
            25,
            (255, 255, 255),
            (10, 50)
        )

        m_pos = pg.mouse.get_pos()

        draw_text(
            self.screen,
            'mouseX={},mouseY={}'.format(m_pos[0], m_pos[1]),
            25,
            (255, 255, 255),
            (10, 70)
        )

        draw_text(
            self.screen,
            'Map Origin={}'.format(self.world.origin),
            25,
            (255, 255, 255),
            (10, 90)
        )

        pg.display.flip()