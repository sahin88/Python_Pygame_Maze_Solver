import pygame
import queue
import time


class Maze:
    def __init__(self, width, height):
        pygame.init()
        self.height = 550
        self.width = 650
        self.grid = [['' for i in range(9)] for j in range(9)]
        self.orginal_grid = [[self.grid[x][y] for y in range(
            len(self.grid))] for x in range(len(self.grid))]
        self.font = pygame.font.SysFont('dejavuserif', 25)
        self.re_font = pygame.font.SysFont('dejavuserif', 55)
        self.color = (0, 0, 0)
        self.line_color = (0, 0, 0)
        self.buffer = 1
        self.background_color = (255, 255, 0)
        self.enter_background_color = (0, 255, 0)
        self.target_background_color = (255, 0, 0)
        self.right_way_color = (0, 0, 255)
        self.barier_color = (0, 0, 0)
        self.solutions = []
        self.start = False
        self.end = False
        self.start_coordinates = None

        self.main()

    def printMaze(self, posotions):

        x, y = self.start_coordinates

        for position in posotions:
            if position == "R":
                y += 1

            if position == 'L':
                y -= 1

            if position == 'U':
                x += 1

            if position == 'D':
                x -= 1
            if self.grid[x][y] != 'X':
                pygame.draw.rect(self.win, self.right_way_color, (
                    (y+1)*50 + self.buffer, (x+1)*50 + self.buffer, 50 - 2*self.buffer, 50 - 2*self.buffer))
            pygame.display.update()
            time.sleep(0.5)
        return self.grid

    def isValid(self, direction):
        maze = self.grid
        curr_x, curr_y = self.start_coordinates
        for dirs in direction:

            if dirs == 'R':
                curr_y += 1

                if curr_x < 0 or curr_x >= len(self.grid) or curr_y < 0 or curr_y >= len(self.grid[0]) or self.grid[curr_x][curr_y] == '#':
                    curr_y -= 1
                    return

            elif dirs == 'L':
                curr_y -= 1
                if curr_x < 0 or curr_x >= len(self.grid) or curr_y < 0 or curr_y >= len(self.grid) or self.grid[curr_x][curr_y] == '#':
                    curr_y += 1
                    return

            elif dirs == 'U':
                curr_x += 1
                if curr_x < 0 or curr_x >= len(self.grid) or curr_y < 0 or curr_y >= len(self.grid) or self.grid[curr_x][curr_y] == '#':
                    curr_x += 1
                    return

            else:
                curr_x -= 1

                if curr_x < 0 or curr_x >= len(self.grid) or curr_y < 0 or curr_y >= len(self.grid) or self.grid[curr_x][curr_y] == '#':
                    return
        return True

    def findStart(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == "O":
                    start = self.grid[i][j]
                    start = (i, j)

                    return start

    def checkTarget(self, positions):

        x, y = self.start_coordinates

        for position in positions:
            if position == "R":
                y += 1
                if self.grid[x][y] == 'X':
                    return True
            if position == 'L':
                y -= 1
                if self.grid[x][y] == 'X':
                    return True
            if position == 'U':
                x += 1
                if self.grid[x][y] == 'X':
                    return True
            if position == 'D':
                x -= 1
                if self.grid[x][y] == 'X':
                    return True
        return False

    def solve(self):

        qv = queue.Queue()
        qv.put('')

        while qv:
            vertex = qv.get()

            if self.checkTarget(vertex):
                return self.printMaze(vertex)

            for directions in ['R', 'L', 'D', 'U']:
                new_dirr = vertex+directions
                if self.isValid(new_dirr):
                    qv.put(new_dirr)

    def insert_item(self, position):
        pos_x, pos_y = position[1], position[0]
        print(pos_x, pos_y)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    print("event", event)

                    if (event.key == 49) and not self.start:
                        self.grid[pos_x-1][pos_y-1] = "O"
                        pygame.draw.rect(self.win, self.enter_background_color, (
                            position[0]*50 + self.buffer, position[1]*50 + self.buffer, 50 - 2*self.buffer, 50 - 2*self.buffer))
                        pygame.display.update()
                        self.start_coordinates = self.findStart()
                        self.start = True

                        return
                    if (event.key == 50) and not self.end:
                        self.grid[pos_x-1][pos_y-1] = "X"
                        pygame.draw.rect(self.win, self.target_background_color, (
                            position[0]*50 + self.buffer, position[1]*50 + self.buffer, 50 - 2*self.buffer, 50 - 2*self.buffer))
                        pygame.display.update()
                        self.end = True

                        return
                    if (event.key == 51):
                        self.grid[pos_x-1][pos_y-1] = "#"
                        pygame.draw.rect(self.win, self.barier_color, (
                            position[0]*50 + self.buffer, position[1]*50 + self.buffer, 50 - 2*self.buffer, 50 - 2*self.buffer))
                        pygame.display.update()
                        self.end = True
                        return
                    return

    def main(self):

        pygame.init()
        self.win = pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption("Maze Solver")
        self.win.fill(self.background_color)
        for i in range(10):

            pygame.draw.line(self.win, self.line_color,
                             (50+50*i, 50), (50+50*i, 500), 2)
            pygame.draw.line(self.win, self.line_color,
                             (50, 50+50*i), (500, 50+50*i), 2)

        pygame.display.update()

        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                value = self.font.render(
                    str(self.grid[x][y]), True, self.color)
                self.win.blit(value, ((y+1)*50+12, (x+1)*50+12))
        pygame.display.update()
        text = self.font.render('Find Path', True, (0, 0, 255))
        self.win.blit(text, (220, 570))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print(pos[0], pos[1])
                    if(50 <= pos[0] <= 500 and 50 <= pos[1] <= 500):
                        self.insert_item((pos[0]//50, pos[1]//50))
                        pygame.display.update()

                    elif (222 <= pos[0] <= 342 and 575 <= pos[1] <= 595):
                        self.solve()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()


clss = Maze(500, 500)
