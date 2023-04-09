import pygame as pg
from .settings import TILE_SIZE, ZOOM_FACTOR, MIN_ZOOM, MAX_ZOOM
from .maps import gamemap1
from .tiles import defaultTiles

class World:

    def __init__(self, mapSizeX, mapSizeY, screenSizeX, screenSizeY, gameMap = None):
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY
        self.screenSizeX = screenSizeX
        self.screenSizeY = screenSizeY

        if gameMap == None:
            self.gameMap = gamemap1
        else:
            self.gameMap = gameMap

        self.zoom_level = 1.0
        self.columns, self.rows = len(self.gameMap[0]), len(self.gameMap)
        self.p_col, self.p_row = 2, 2
    
    def tileRect(self, column, row, tile_size):
        x = (column + row) * tile_size[0] / 2
        y = ((self.columns - column - 1) + row) * tile_size[1] / 2

        return pg.Rect(x, y, *tile_size)

    def inverseMat2x2(self, m):
        a, b, c, d = m[0].x, m[0].y, m[1].x, m[1].y
        det = 1 / (a*d - b*c)

        return [(d*det, -b*det), (-c*det, a*det)]

    def transform(self, p, mat2x2):
        x = p[0] * mat2x2[0][0] + p[1] * mat2x2[1][0]
        y = p[0] * mat2x2[0][1] + p[1] * mat2x2[1][1]

        return pg.math.Vector2(x, y)
    
    def zoomIn(self):
        if (self.zoom_level + ZOOM_FACTOR) < MAX_ZOOM:
            self.zoom_level += ZOOM_FACTOR
        else:
            self.zoom_level = MAX_ZOOM

    def zoomOut(self):
        if (self.zoom_level - ZOOM_FACTOR) > MIN_ZOOM:
            self.zoom_level -= ZOOM_FACTOR
        else:
            self.zoom_level = MIN_ZOOM
    
    def update(self, camera):
        pass

    def draw(self, screen, camera):
        isometric_tiles = {}

        for key, color in defaultTiles.items():
            tile_surf = pg.Surface((TILE_SIZE * self.zoom_level, TILE_SIZE * self.zoom_level), pg.SRCALPHA)
            tile_surf.fill(color)
            tile_surf = pg.transform.rotate(tile_surf, 45)
            isometric_size = tile_surf.get_width()
            tile_surf = pg.transform.scale(tile_surf, (isometric_size, isometric_size / 2))
            isometric_tiles[key] = tile_surf

        tile_size = (isometric_size, isometric_size / 2)

        game_map = pg.Surface(((self.columns + self.rows) * isometric_size / 2,
                               (self.columns + self.rows) * isometric_size / 4),
                               pg.SRCALPHA)
        
        for column in range(self.columns):
            for row in range(self.rows):
                tile_surf = isometric_tiles[self.gameMap[row][column]]
                tile_rect = self.tileRect(column, row, tile_size)
                game_map.blit(tile_surf, tile_rect)

        map_rect = game_map.get_rect(center = screen.get_rect().center)
        map_outline = [
            pg.math.Vector2(0, self.columns * isometric_size / 4), 
            pg.math.Vector2(self.columns * isometric_size / 2, 0),
            pg.math.Vector2((self.columns + self.rows) * isometric_size / 2, self.rows * isometric_size / 4),
            pg.math.Vector2(self.rows * isometric_size / 2, (self.columns + self.rows) * isometric_size / 4)
        ]
        for pt in map_outline:
            pt += map_rect.topleft 

        self.origin = map_outline[0]
        x_axis = (map_outline[1] - map_outline[0]) / self.columns
        y_axis = (map_outline[3] - map_outline[0]) / self.rows

        point_to_grid = self.inverseMat2x2((x_axis, y_axis))
    
        p_position = self.transform((self.p_col + 0.5, self.p_row + 0.5), (x_axis, y_axis)) + self.origin
        m_pos = pg.mouse.get_pos()
        m_grid_pos = self.transform(pg.math.Vector2(m_pos) - self.origin, point_to_grid)
        m_col, m_row = int(m_grid_pos[0]), int(m_grid_pos[1])
            
        screen.fill((0, 0, 0))
        screen.blit(game_map, map_rect)
        pg.draw.lines(screen, (164, 164, 164), True, map_outline, 3)
        #pygame.draw.line(window, (255, 0, 0), origin, origin+x_axis, 3)
        #pygame.draw.line(window, (0, 255, 0), origin, origin+y_axis, 3)
        #pygame.draw.circle(window, (255, 255, 255), origin, 5)
        #pygame.draw.circle(window, (255, 0, 0), origin+x_axis, 5)
        #pygame.draw.circle(window, (0, 255, 0), origin+y_axis, 5)
        #window.blit(textO, textO.get_rect(topright = origin+(-5, 5)))   
        #window.blit(textX, textX.get_rect(bottomright = origin+x_axis+(-5, -5)))
        #window.blit(textY, textX.get_rect(topright = origin+y_axis+(-5, 5))) 
        pg.draw.ellipse(screen, (255, 255, 0),
                        (p_position[0]-16,
                         p_position[1]-8,
                         isometric_size * 0.5,
                         (isometric_size * 0.5) / 2))
        
        if 0 <= m_grid_pos[0] < self.columns and 0 <= m_grid_pos[1] < self.rows:
            tile_rect = self.tileRect(m_col, m_row, tile_size).move(map_rect.topleft)
            pts = [tile_rect.midleft, tile_rect.midtop, tile_rect.midright, tile_rect.midbottom]
            pg.draw.lines(screen, (255, 255, 255), True, pts, 4)