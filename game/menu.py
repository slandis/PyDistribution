import pygame as pg

from .utils import draw_text

BUTTON_HEIGHT = 30
MENU_WIDTH = 150

ITEM_BUTTON = 1
ITEM_HEADER = 2

BUTTON_HEADER = 1
BUTTON_RECENTER = 2
BUTTON_EXIT = 3

STATE_UNPRESSED = 1
STATE_PRESSED = 2
STATE_HOVER = 3

contextMenuItems = [
    {'type': ITEM_HEADER, 'id': BUTTON_HEADER, 'text': 'Tools', 'state': STATE_UNPRESSED},
    {'type': ITEM_BUTTON, 'id': BUTTON_RECENTER, 'text': 'Re-Center', 'state': STATE_UNPRESSED},
    {'type': ITEM_BUTTON, 'id': BUTTON_EXIT, 'text': 'Exit', 'state': STATE_UNPRESSED}
]

class ContextMenu:
    def __init__(self):
        self.display = False
        self.menuItems = contextMenuItems
        self.position = (0, 0)
    
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
            print('{},{}'.format(point, self.rect))

            if self.rect.collidepoint(point):
                print("Menu Hit Test True")
                return True
            
        return False

    def update(self, event):
        if self.display == True:
            i = 0

            for item in self.menuItems:
                rect = pg.Rect(self.rect.topleft[0], self.rect.topleft[1] + i, MENU_WIDTH, BUTTON_HEIGHT)

                if rect.collidepoint(event.pos) and item['type'] == ITEM_BUTTON:
                    print("Menu Item Hit Test True")
                    if event.type == pg.MOUSEBUTTONDOWN:
                        item['state'] = STATE_PRESSED
                    elif event.type == pg.MOUSEMOTION:
                        item['state'] = STATE_HOVER
                else:
                    item['state'] = STATE_UNPRESSED
                
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