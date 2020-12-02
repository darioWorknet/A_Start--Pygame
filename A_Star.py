# COMMANDS:
    # Left click  ------> create barrier
    # Right click ------> erase (reset to default)
    # Shift + click ----> set starting point
    # Ctrl + click -----> set end point
    # ENTER ------------> start A* ALGORITHM
    # Escape -----------> restart board

import pygame
import time
import math

#Initialize pygame
pygame.init()

# ENVIRONMENT
WIDTH = 800
HEIGHT = WIDTH
ROWS = 50

# PYGAME WINDOW
WIN = pygame.display.set_mode(( WIDTH, HEIGHT))
pygame.display.set_caption("A* from scratch")

# COLORS
LINE_COLOR = (100, 100, 100)
NORMAL = (250,  250, 240) 
BARRIER = (20, 20, 20)
START = (20,32, 108)
END = (200, 100, 255)
BORDER = (100,  100, 50)
VISITED = (200,  200, 150)
PATH = (20, 200, 10)


class Node:
    def __init__(self, row, col, width, rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.state = "Normal"
        self.color = self.get_color()
        self.width = width
        self.rows = rows
        self.G = 99999
        self.H = 99999

    def get_color(self):
        if self.state == "Normal":
            return NORMAL
        elif self.state == "Barrier":
            return BARRIER
        elif self.state == "Start":
            return START
        elif self.state == "End":
            return END
        elif self.state == "Border":
            return BORDER
        elif self.state == "Visited":
            return VISITED
        elif self.state == "Path":
            return PATH

    def get_width(self):
        return self.width

    def set_state(self, state):
        self.state = state
        self.color = self.get_color()

    def get_state(self):
        return self.state

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, nodes):
        self.neighbours = []
        # Get UP, DOWN, LEFT, RIGHT neighbours (Barries not allowed):
        if self.row != 0 and nodes[self.row - 1][self.col].get_state() != "Barrier": # UP
            self.neighbours.append(nodes[self.row - 1][self.col]) 
        if self.row < self.rows - 1 and nodes[self.row + 1][self.col].get_state() != "Barrier": # DOWN
            self.neighbours.append(nodes[self.row + 1][self.col]) 
        if self.col != 0 and nodes[self.row][self.col - 1].get_state() != "Barrier": # LEFT
            self.neighbours.append(nodes[self.row][self.col - 1]) 
        if self.col < self.rows - 1 and nodes[self.row][self.col + 1].get_state() != "Barrier": # RIGHT
            self.neighbours.append(nodes[self.row][self.col + 1])

    def set_parent(self, node):
        self.parent = node

    def restart_G(self):
        self.G = 0

    def set_G(self):
        self.G = self.parent.G + self.distance_to(self.parent)

    def set_H(self, node):
        self.H = self.distance_to(node) 

    def set_F(self):
        self.F = self.G + self.H

    def distance_to(self, node):
        x2, y2 = node.get_coords()
        return abs(self.x - x2) + abs(self.y - y2)

    def get_coords(self):
        return self.x, self.y


def a_star(draw, start_node, end_node, nodes):
    
    borders = []
    visited = []
    finished = False

    start_node.set_parent(start_node)
    start_node.restart_G()
    start_node.set_H(end_node)
    start_node.set_F()
    borders.append(start_node)

    iteration = 0

    while len(borders) != 0 and not finished:
        draw()
        iteration += 1
        borders.sort(key = lambda x: x.F, reverse=True)
        node = borders.pop()
        visited.append(node)
        node.set_state("Visited")
        print("Iteration:", iteration)
        print("Node G:", node.G)
        print("Node H:", node.H)
        print("Node F:", node.F)
        print("")

        if node == end_node:
            finished = True
            print("Solution found")
            #draw backwards path
            draw_path(end_node, start_node)

        else:
            #neighbours = node.get_neighbours(nodes)
            node.update_neighbours(nodes)
            for neighbour in node.neighbours:
                if neighbour not in visited and neighbour not in borders:
                    neighbour.set_parent(node)
                    neighbour.set_G()
                    neighbour.set_H(end_node)
                    neighbour.set_F()
                    neighbour.set_state("Border")
                    borders.append(neighbour)

        #time.sleep(0.05)
        draw()
    if not finished:
        print("No solution found")
    print("Exiting A star")


def draw_path(end_node, start_node):
    not_found = True
    node = end_node.parent
    end_node.set_state("End")

    while not_found:
        if node == start_node:
            print("found start_node")
            not_found = False
            node.set_state("Start")
        else:
            node.set_state("Path")
            node = node.parent



def make_nodes(rows, width):
    nodes = []
    size = width // rows
    for y in range(rows):
        nodes.append([])
        for x in range(rows):
            node = Node(y, x, size, rows)
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

def draw(win, rows, width, nodes):
    draw_nodes(win, nodes)
    draw_board(win, rows, width)
    pygame.display.update()



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
                    a_star(lambda: draw(win, rows, width, nodes), start, end, nodes)

            elif pygame.key.get_mods() & pygame.KMOD_SHIFT: # SHIFT + click --> START POSITION
                if pygame.mouse.get_pressed()[0]:
                    x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                    state = "Start"
                    restart_nodes_state(state, nodes)
                    nodes[y][x].set_state(state)
                    start = nodes[y][x]

            elif pygame.key.get_mods() & pygame.KMOD_CTRL: # CTRL + click --> END POSITION
                if pygame.mouse.get_pressed()[0]:
                    x, y = get_pos(pygame.mouse.get_pos(), width, rows)
                    state = "End"
                    restart_nodes_state(state, nodes)
                    nodes[y][x].set_state(state)
                    end = nodes[y][x]

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
        draw(win, rows, width, nodes)
        

main (WIN, WIDTH, ROWS)