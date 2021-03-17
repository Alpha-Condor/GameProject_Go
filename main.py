# FRONT END
import pygame
import Go
from sys import exit

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_SIZE = (820, 820)
BACKGROUND = "GoBoard.jpg"


class Stone(Go.Stone):
    def __init__(self, board, point, color):
        super(Stone, self).__init__(board, point, color)
        self.coordinates = (5 + self.point[0] * 40, 5 + self.point[1] * 40)
        self.draw()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.coordinates, 20, 0)
        pygame.display.update()

    def remove(self):
        blit_cords = (self.coordinates[0] - 20, self.coordinates[1] - 20)
        area_rect = pygame.Rect(blit_cords, (40, 40))
        screen.blit(background, blit_cords, area_rect)
        pygame.display.update()
        super(Stone, self).remove()


class Board(Go.Board):
    def __init__(self):
        super(Board, self).__init__()
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.draw()

    def draw(self):
        pygame.draw.rect(background, BLACK, self.outline, 3)
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                cords = (165 + (240 * i), 165 + (240 * j))
                pygame.draw.circle(background, BLACK, cords, 5, 0)
        screen.blit(background, (0, 0))
        pygame.display.update()

    def update_liberties(self, added_stone=None):
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()


def main():
    while True:
        pygame.time.wait(250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and board.outline.collidepoint(event.pos):
                    x = int(round(((event.pos[0] - 5) / 40.0), 0))
                    y = int(round(((event.pos[1] - 5) / 40.0), 0))
                    stone = board.search(point=(x, y))
                    if stone:
                        stone.remove()
                    else:
                        added_stone = Stone(board, (x, y), board.get_turn())
                    board.update_liberties(added_stone)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Go Game')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    board = Board()
    main()
