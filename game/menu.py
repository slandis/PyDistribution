import pygame as pg
import sys
from .IEvent import IEvent
from .utils import draw_text

BUTTON_HEIGHT = 30
MENU_WIDTH = 150

ITEM_BUTTON = 1
ITEM_HEADER = 2

BUTTON_HEADER = 1
BUTTON_RECENTER = 2
BUTTON_EXIT = 3

STATE_NORMAL = 1
STATE_PRESSED = 2
STATE_HOVER = 3

class ContextMenu(IEvent):
    menuItems = [
        {'type': ITEM_HEADER, 'name': 'HEADER', 'text': 'Tools', 'state': STATE_NORMAL, 'callback': None},
        {'type': ITEM_BUTTON, 'name': 'btnRecenter', 'text': 'Re-Center', 'state': STATE_NORMAL, 'callback': 'btnRecenter_click'},
        {'type': ITEM_BUTTON, 'name': 'btnExit', 'text': 'Exit', 'state': STATE_NORMAL, 'callback': 'btnExit_click'}
    ]

    def __init__(self):
        self.display = False
        #self.menuItems = self.contextMenuItems
        self.position = (0, 0)

    def cb(self, item, *args, **kwargs):
        func_name = item['callback']

        if func_name and hasattr(self, func_name):
            return getattr(self, func_name)(*args, **kwargs)
        else:
            return None

    def btnRecenter_click(self, camera):
        camera.scroll = pg.Vector2(0, 0)

    def btnExit_click(self, args):
        pg.quit()
        sys.exit()

    def show(self, position):
        self.position = position
        self.display = True

        #self.surface = pg.Surface((MENU_WIDTH, len(self.menuItems) * BUTTON_HEIGHT))
        self.rect = pg.Rect(0, 0, MENU_WIDTH, len(self.menuItems) * BUTTON_HEIGHT)
        self.rect.move_ip(position)

    def hide(self):
        self.display = False

    def hit_test(self, point):
        if self.display == True:
            if self.rect.collidepoint(point):
                return True
            
        return False
    
    def menuClick(self, pos, args):
        if self.display == True:
            i = 0

            for item in self.menuItems:
                rect = pg.Rect(self.rect.topleft[0], self.rect.topleft[1] + i, MENU_WIDTH, BUTTON_HEIGHT)

                if rect.collidepoint(pos) and item['type'] == ITEM_BUTTON:
                    item['state'] = STATE_NORMAL
                    self.cb(item, args)
                    self.hide()
                
                i += BUTTON_HEIGHT

    def menuHover(self, pos):
        if self.display == True:
            i = 0

            for item in self.menuItems:
                rect = pg.Rect(self.rect.topleft[0], self.rect.topleft[1] + i, MENU_WIDTH, BUTTON_HEIGHT)

                if rect.collidepoint(pos) and item['type'] == ITEM_BUTTON:
                    item['state'] = STATE_HOVER
                else:
                    item['state'] = STATE_NORMAL
                
                i += BUTTON_HEIGHT

    def draw(self, screen):
        if self.display == True:
            pts1 = [self.rect.topleft, self.rect.topright, self.rect.bottomright]
            pts2 = [self.rect.bottomright, self.rect.bottomleft, self.rect.topleft]
            pg.draw.lines(screen, (170, 170, 170), True, pts1, 2)
            pg.draw.lines(screen, (30, 30, 30), True, pts2, 2)

            i = 0

            for item in self.menuItems:
                rect = pg.Rect(0, i, MENU_WIDTH, BUTTON_HEIGHT)
                rect.move_ip(self.position)
                surface = pg.Surface((MENU_WIDTH, BUTTON_HEIGHT))

                color = (200, 200, 200)

                if item['state'] == STATE_HOVER:
                    color = (80, 80, 80)
                
                surface.fill(color)
                pg.draw.rect(surface, color, rect)
                pg.draw.rect(surface, (20, 20, 20), rect, 1)
                screen.blit(surface, rect)
                draw_text(screen, item['text'], 20, (255, 255, 255), (rect.topleft[0]+7, rect.topleft[1]+7))

                i += BUTTON_HEIGHT
        else:
            pass