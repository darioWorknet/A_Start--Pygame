# COMMANDS:
    # Left click  ------> create barrier
    # Right click ------> erase (reset to default)
    # Shift + click ----> set starting point
    # Ctrl + click -----> set finish point
    # ENTER ------------> start A* ALGORITHM
    # Escape -----------> restart board

import pygame

#Initialize pygame
pygame.init()

# ENVIRONMENT
WIDTH = 500
HEIGHT = WIDTH
ROWS = 20

# PYGAME WINDOW
WIN = pygame.display.set_mode(( WIDTH, HEIGHT))
pygame.display.set_caption("A* from scratch")

# COLORS
LINE_COLOR = (150, 200, 50)
NORMAL = (200,  200, 250)
BARRIER = (20, 20, 20)
START = (20,32, 108)
FINISH = (200, 100, 255)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.state = "Normal"
        self.color = self.get_color()
        self.width = width

    def get_color(self):
        if self.state == "Normal":
            return NORMAL
        elif self.state == "Barrier":
            return BARRIER
        elif self.state == "Start":
            return START
        elif self.state == "Finish":
            return FINISH

    def get_width(self):
        return self.width

    def set_state(self, state):
        self.state = state
        self.color = self.get_color()

    def get_state(self):
        return self.state

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))



def make_nodes(rows, width):
    nodes = []
    size = width // rows
    for y in range(rows):
        nodes.append([])
        for x in range(rows):
            node = Node(y, x, size)
            nodes[y].append(node)
    return nodes


def restart_nodes_state(state, nodes):
    for row_of_nodes in nodes:
        for node in row_of_nodes:
            if node.get_state() == state:
                node.set_state("Normal")


def draw_board(win, rows, width):
    gap = width // rows
    for x in range(1, rows):
        pygame.draw.line(win, LINE_COLOR, (gap*x, 0), (gap*x, width), 2) # Last item == line.weight = 1 by default
    for y in range(1, rows):
        pygame.draw.line(win, LINE_COLOR, (0, gap*y), (width, gap*y), 2)


def draw_nodes(win, nodes):
    for row_of_nodes in nodes:
        for node in row_of_nodes:
                node.draw(win)


def get_pos(posXY, width, rows):
    pos_x, pos_y = posXY
    node_width = width // rows
    x = pos_x // node_width
    y = pos_y // node_width
    return x, y


def main(win, width, rows):
    # List of nodes
    nodes = make_nodes(rows, width)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: # ESCAPE --> RESTART BOARD
                    nodes = make_nodes(rows, width)

                if event.key == pygame.K_RETURN: # ENTER --> START A* ALGORITHM
                    print("Enter pressed")

            elif pygame.key.get_mods() & pygame.KMOD_SHIFT: # SHIFT + click --> START POSITION
                if pygame.mouse.get_pressed()[0]:
                    x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                    state = "Start"
                    restart_nodes_state(state, nodes)
                    nodes[y][x].set_state(state)

            elif pygame.key.get_mods() & pygame.KMOD_CTRL: # CTRL + click --> FINISH POSITION
                if pygame.mouse.get_pressed()[0]:
                    x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                    state = "Finish"
                    restart_nodes_state(state, nodes)
                    nodes[y][x].set_state(state)

            elif pygame.mouse.get_pressed()[0]: # click  --> BARRIERS
                x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                state = "Barrier"
                nodes[y][x].set_state(state)

            elif pygame.mouse.get_pressed()[2]: # RIGHT click --> ERASER
                x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                state = "Normal"
                # Extends eraser surface
                for i in range (-1, 2):
                    for j in range (-1 ,2):
                        try:
                            nodes[y+i][x+j].set_state(state)
                        except:
                            nodes[y][x].set_state(state)

        # DRAWING
        draw_nodes(win, nodes)
        draw_board(win, rows, width)
        pygame.display.update()

        
main (WIN, WIDTH, ROWS)