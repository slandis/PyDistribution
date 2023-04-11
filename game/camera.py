import pygame as pg
from .settings import ZOOM_FACTOR, ZOOM_MAX, ZOOM_MIN
class Camera:
    def __init__(self, width, height, zoom):

        self.width = width
        self.height = height
        self.zoom = zoom

        self.scroll = pg.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.speed = 25

    def zoomIn(self):
        if self.zoom < ZOOM_MAX:
            self.zoom += ZOOM_FACTOR
        else:
            self.zoom = ZOOM_MAX

    def zoomOut(self):
        if self.zoom > ZOOM_MIN:
            self.zoom -= ZOOM_FACTOR
        else:
            self.zoom = ZOOM_MIN

    def update(self):
        mouse_pos = pg.mouse.get_pos()

        # x movement
        if mouse_pos[0] > self.width * 0.97:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:
            self.dx = self.speed
        else:
            self.dx = 0

        # y movement
        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.03:
            self.dy = self.speed
        else:
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy