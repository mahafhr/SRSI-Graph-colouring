import pygame
from pygame.locals import *
from graph import Graph

# Enter maximum resolution of game window
width = 800
height = 600

dot_width = 50
dot_radius = 16

coordinates = dict()

colour_map = {0: (0, 0, 0), 1: (50, 70, 255), 2: (255, 50, 50), 3: (50, 255, 80), 4: (255, 255, 50)}

def dist_squared(pair1, pair2):
    return (pair1[0] - pair2[0])**2 + (pair1[1] - pair2[1])**2


def nearest_vertex(click):
    # finds the vertex closest to click
    global coordinates
    return min(range(1, n+1), key = lambda v: dist_squared(click, coordinates[v]))

def colour_nodes(g):
    global coordinates
    for i in range(1, g.order()+1):
        if g.vertex_colour[i] in colour_map:
            pygame.draw.circle(screen, colour_map[g.vertex_colour[i]], coordinates[i], dot_radius)
    pygame.display.flip()

# Setup pygame screen
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Map colouring')

background = pygame.Surface(screen.get_size())
background = background.convert()

# Load tile image
image_map = pygame.image.load('australia.png')
dot = pygame.image.load('dot.png')

# Scale images
image_map = pygame.transform.scale(image_map, (width, height))
dot = pygame.transform.scale(dot, (dot_width, dot_width))


screen.blit(image_map, (0, 0))
pygame.display.flip()


# # Can use smoothing here. Smoothed tiles look more aesthetic, but perhaps not pixel-precise
# empty = pygame.transform.smoothscale(empty, (width/m, height/n))

phase = 1 # phase 1 is building the graph with left clicks, phase 2 is connecting the edges with right clicks
# phase 3 colours, phase 4 exits
n = 0

# This loop waits for mouse clicks and handles them
done = False
first_right_click = True
temp_vertex = 0

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            done = True
        elif event.type == KEYDOWN and event.key == K_SPACE:
            phase += 1
            print "Now in phase %d" % phase
            if phase == 2:
                g = Graph(n)
            elif phase == 3:
                # Choose colouring algorithm here
                g.colour_greedy("h")

                g.print_graph()
                colour_nodes(g)
            elif phase == 4:
                done = True
        elif event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and phase == 1:
                n += 1
                pos = pygame.mouse.get_pos()
                coordinates[n] = pos
                # pos_offset = (pos[0] - dot_width/2, pos[1] - dot_width/2)
                # screen.blit(dot, pos_offset)
                pygame.draw.circle(screen, (0, 0, 0), pos, dot_radius)
                pygame.display.flip()
            elif pygame.mouse.get_pressed()[2] and phase == 2:
                if first_right_click:
                    temp_vertex = nearest_vertex(pygame.mouse.get_pos())
                    first_right_click = False
                else:
                    pos = pygame.mouse.get_pos()
                    temp = nearest_vertex(pos)
                    g.add_edge(temp_vertex, temp)
                    first_right_click = True
                    #draw line
                    pygame.draw.line(screen, colour_map[0], coordinates[temp_vertex], coordinates[temp])
                    pygame.display.flip()


print "Program terminated."
