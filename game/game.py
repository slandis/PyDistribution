import pygame as pg
import math
import sys
from .world import World
from .settings import TILE_SIZE, ZOOM_MAX, ZOOM_MAX, ZOOM_FACTOR
from .utils import draw_text
from .camera import Camera
from .menu import ContextMenu

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.click_timer = 0

        # world
        self.world = World(self.screen, 50, 50)

        # camera
        self.camera = Camera(self.width, self.height, 1)

        # context menu
        self.cmenu = ContextMenu()

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
                    if self.cmenu.display == True:
                        self.cmenu.hide()
                    else:
                        pg.quit()
                        sys.exit()
                elif event.key == pg.K_c:
                    self.camera.scroll.update(0, 0)
                elif event.key == pg.K_z:
                    self.camera.zoom = 1.0
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:   # left button
                    if self.click_timer == 0:
                        self.click_timer = pg.time.get_ticks()

                        if self.cmenu.hit_test(event.pos):
                            self.cmenu.update(event)
                    else:
                        if pg.time.get_ticks() - self.click_timer < 500:
                            mx, my = event.pos
                            cx, cy = self.screen.get_rect().center

                            if cy < my:
                                scrollY = (my - cy) * -2
                            else:
                                scrollY = (cy - my) * 2

                            if cx < mx:
                                scrollX = (mx - cx) * -2
                            else:
                                scrollX = (cx - mx) * 2
                            
                            self.camera.scroll.update(scrollX, scrollY)
                            self.click_timer = 0
                        else:
                            self.click_timer = 0
                elif event.button == 3:
                    self.cmenu.show(event.pos)
                elif event.button == 4:
                    self.camera.zoomIn()
                    pass
                elif event.button == 5:
                    self.camera.zoomOut()
            elif event.type == pg.MOUSEMOTION:
                if self.cmenu.hit_test(event.pos):
                    self.cmenu.update(event)

    def update(self):
        self.camera.update()
        self.world.update(self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.cmenu.draw(self.screen)

        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )

        draw_text(
            self.screen,
            'Zoom={}'.format(round(self.camera.zoom, 2)),
            25,
            (255, 255, 255),
            (10, 30)
        )

        draw_text(
            self.screen,
            'Screen={}'.format(self.screen.get_size()),
            25,
            (255, 255, 255),
            (10, 50)
        )

        m_pos = pg.mouse.get_pos()

        draw_text(
            self.screen,
            'Mouse={}'.format(m_pos),
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

        draw_text(
            self.screen,
            'Scroll={}'.format(self.camera.scroll),
            25,
            (255, 255, 255),
            (10, 110)
        )
        draw_text(
            self.screen,
            'Map Height={}'.format(self.world.tile_height * self.world.columns / 2),
            25,
            (255, 255, 255),
            (10, 130)
        )

        pg.display.flip()