import pygame as pg
from .settings import TILE_SIZE, ZOOM_FACTOR, ZOOM_MIN, ZOOM_MAX
from .maps import gamemap1
from .tiles import defaultTiles

class World:

    def __init__(self, screen, mapSizeX, mapSizeY, tileMap = None):
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY
        self.screenSizeX, self.screenSizeY = screen.get_size()

        if tileMap == None:
            self.tileMap = gamemap1
        else:
            self.tileMap = tileMap

        self.columns, self.rows = len(self.tileMap[0]), len(self.tileMap)
        self.game_map = pg.Surface((screen.get_size()), pg.SRCALPHA)
        self.tile_height = 0
    
    def tileRect(self, column, row, tile_size):
        x = (column + row) * tile_size[0] // 2
        y = ((self.columns - column - 1) + row) * tile_size[1] // 2 
        return pg.Rect(x, y, *tile_size)

    def inverseMat2x2(self, m):
        a, b, c, d = m[0].x, m[0].y, m[1].x, m[1].y
        det = 1 / (a*d - b*c)
        return [(d*det, -b*det), (-c*det, a*det)]

    def transform(self, p, mat2x2):
        x = p[0] * mat2x2[0][0] + p[1] * mat2x2[1][0]
        y = p[0] * mat2x2[0][1] + p[1] * mat2x2[1][1]
        return pg.math.Vector2(x, y)
    
    def update(self, camera):
        pass

    def draw(self, screen, camera):
        self.game_map.fill((0, 0, 0))
    
        isometric_tiles = {}

        for key, color in defaultTiles.items():
            tile_surf = pg.Surface((TILE_SIZE * camera.zoom, TILE_SIZE * camera.zoom), pg.SRCALPHA)
            tile_surf.fill(color)
            tile_surf = pg.transform.rotate(tile_surf, 45)
            isometric_size = tile_surf.get_width()
            tile_surf = pg.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
            isometric_tiles[key] = tile_surf
    
        tile_size = (isometric_size, isometric_size // 2)
        self.tile_height = tile_size[1]
        
        offsetX = (screen.get_size()[0] + camera.scroll.x - isometric_size * self.columns) / 2
        offsetY = (screen.get_size()[1] + camera.scroll.y - (isometric_size // 2) * self.rows) / 2
    
        for column in range(self.columns):
            for row in range(self.rows):
                tile_surf = isometric_tiles[self.tileMap[row][column]]
                tile_rect = self.tileRect(column, row, tile_size)
                tile_rect.move_ip(offsetX, offsetY)
                self.game_map.blit(tile_surf, tile_rect)

        map_rect = self.game_map.get_rect(center = screen.get_rect().center)

        map_outline = [
            pg.math.Vector2(offsetX, (self.rows * tile_size[1]) / 2 + offsetY),
            pg.math.Vector2((self.columns * tile_size[0]) / 2 + offsetX, offsetY),
            pg.math.Vector2((self.columns * tile_size[0]) + offsetX, (self.rows * tile_size[1]) / 2 + offsetY),
            pg.math.Vector2((self.columns * tile_size[0]) / 2 + offsetX, (self.rows * tile_size[1]) + offsetY)
        ]

        self.origin = map_outline[0]
        x_axis = (map_outline[1] - map_outline[0]) / self.columns
        y_axis = (map_outline[3] - map_outline[0]) / self.rows
   
        point_to_grid = self.inverseMat2x2((x_axis, y_axis))
        
        m_pos = pg.mouse.get_pos()
        m_grid_pos = self.transform(pg.math.Vector2(m_pos) - self.origin, point_to_grid)
        m_col, m_row = int(m_grid_pos[0]), int(m_grid_pos[1])
            
        screen.fill((0, 0, 0))
        screen.blit(self.game_map, map_rect)
        pg.draw.lines(screen, (164, 164, 164), True, map_outline, 3)
    
        if 0 <= m_grid_pos[0] < self.columns and 0 <= m_grid_pos[1] < self.rows:
            tile_rect = self.tileRect(m_col, m_row, tile_size).move(map_rect.topleft)
            tile_rect.move_ip((offsetX, offsetY))
            pts = [tile_rect.midleft, tile_rect.midtop, tile_rect.midright, tile_rect.midbottom]
            pg.draw.lines(screen, (255, 255, 255), True, pts, 4)

        # Draw Crosshairs
        pg.draw.line(screen, (255, 255, 255), (0, screen.get_rect().centery), (screen.get_size()[0], screen.get_rect().centery))
        pg.draw.line(screen, (255, 255, 255), (screen.get_rect().centerx, 0), (screen.get_rect().centerx, screen.get_size()[1]))

        # Draw map outline points
        pg.draw.circle(screen, (255, 0, 0), (map_outline[0].x, map_outline[0].y), 5)
        pg.draw.circle(screen, (255, 0, 0), (map_outline[1].x, map_outline[1].y), 5)
        pg.draw.circle(screen, (255, 0, 0), (map_outline[2].x, map_outline[2].y), 5)
        pg.draw.circle(screen, (255, 0, 0), (map_outline[3].x, map_outline[3].y), 5)