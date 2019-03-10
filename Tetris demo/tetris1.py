import pygame
import random
import copy
import tetris_controls
#from tetris_bot import tetris_ai
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height




# SHAPE FORMATS
"""
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
"""
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
"""
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
"""
shapes = [I, O]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape




class move_pieces():
    def move_right(self, current_piece, grid):
        current_piece.x += 1
        if not(Tetris.valid_space(current_piece, grid)):
            current_piece.x -= 1

    def move_left(self, current_piece, grid):
            current_piece.x -= 1
            if not(Tetris.valid_space(current_piece, grid)):
                    current_piece.x += 1
    def move_down(self, current_piece, grid):
            current_piece.y += 1
            if not(Tetris.valid_space(current_piece, grid)):
                    current_piece.y -= 1
    def rotate(self, current_piece, grid):
            current_piece.rotation += 1
            if not(Tetris.valid_space(current_piece, grid)):
                    current_piece.rotation -= 1


class settings_GA():
    #GA SETTINGS
    genomes = []
    currentGenome = -1
    generation = 0

    archive = {'population_size':0,
    'currentGeneration':0,
    'fittest':[],
    'genomes':[]
}

    mutationRate = 0.05
    mutationStep = 0.2




class tetris_ai():



    def createInitialPopulation(self, population_size = 50):
        genomes = []
        for x in range(population_size):
            genome = {

                'id': random.uniform(0.0, 1.0),

                'weightedHoleCount': random.uniform(0.0, 1.0) * 0.5,

                'weightedRowsClearedCount': random.uniform(0.0, 1.0) - 0.5,

                'weightedRougness': random.uniform(0.0, 1.0) - 0.5,

                'roughness': random.uniform(0.0, 1.0) - 0.5
            }
        
            genomes.append(copy.deepcopy(genome))
        self.evaluateNextGenome(genomes)
        




    def run_genetic_algorithm(self, population_size = 50):




        settings_GA.archive['population_size'] = population_size


        self.createInitialPopulation(population_size)




    def evaluateNextGenome(self, genomes):
        settings_GA.currentGenome += 1
        if settings_GA.currentGenome == len(genomes):
            
            self.evolve()

        
    def evolve(self):
        print('Generation' + settings_GA.generation + 'evaluated')
        settings_GA.currentGenome = 0
        settings_GA.generation += 1
        Tetris.clear()



class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

class Tetris():

    def start(self):
        
        self.win = pygame.display.set_mode((s_width, s_height))
        pygame.display.set_caption('Tetris')
        self.main(self.win)

        
    def create_grid(self, locked_pos={}):  # *
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c

        #print(grid)
        return grid


    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions


    def valid_space(self, shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True


    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False


    def get_shape(self):
        return Piece(5, 0, random.choice(shapes))


    def check_hole(self, grid, hole_count):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == (0, 0, 0):
                    print('grid[i][j] ' + str(grid[i][j]))
                    if grid[i-1][j] != (0, 0, 0):
                        print ('grid[i-1][j] ' + str(grid[i-1][j]))
                        hole_count += 1
        return hole_count



    def draw_text_middle(self, surface, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


    def draw_grid(self, surface, grid):
        sx = top_left_x
        sy = top_left_y

        for i in range(len(grid)):
            pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


    def clear_rows(self, grid):

        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (0,0,0) not in row:
                inc += 1
                
                print('row found' + ' ' + str(inc))
        return inc
    """
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        
    """
        
    def draw_next_shape(self, shape, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255,255,255))

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

        surface.blit(label, (sx + 10, sy - 30))




    def draw_window(self, surface, grid, score=0, last_score = 0):
        surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

        # current score



        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

        self.draw_grid(surface, grid)
        #pygame.display.update()


    def move_score(self, grid, inc_weight, hole_count_weight):
        inc = self.clear_rows(grid)
        hole_count = self.check_hole(grid)

        final_score = inc_weight*inc + hole_count_weight*hole_count 

        return final_score



    def clear(self):
        grid = [
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        ]
        return grid


    def main(self, win):  # *
        locked_positions = {}
        grid = self.create_grid(locked_positions)
        

       # ai = False



        hole_count = 0
        change_piece = False
        run = True
        current_piece = self.get_shape()
        next_piece = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0

        while run:
            grid = self.create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()
            
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print('a')
                        if ai == False:
                            ai = True
                        else:
                            ai = False

                '''
                

            
            '''
            if ai == False:
                for event in pygame.event.get():
                    print('fucking ai')
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            tetris_controls.move_left(current_piece, grid)
                        if event.key == pygame.K_RIGHT:
                            tetris_controls.move_right(current_piece, grid)
                        if event.key == pygame.K_DOWN:
                            tetris_controls.move_down(current_piece, grid)
                        if event.key == pygame.K_UP:
                            tetris_controls.rotate(current_piece, grid)
            else:
                pass
            '''


            
            #ТУТ ПИСАТЬ КОД ДЛЯ АЛГОРИТМА

            #tetris_ai.run_genetic_algorithm(self)



            if level_time/1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005
            
            if fall_time/1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
            #and 
                if not (self.valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            shape_pos = self.convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = self.get_shape()
                change_piece = False
                print(grid)
                print ('rows: ' + str(self.clear_rows(grid)))
                print('holes: ' + str(self.check_hole(grid, hole_count)))
                

            self.draw_window(win, grid, score)
            self.draw_next_shape(next_piece, win)
            pygame.display.update()

            if self.check_lost(locked_positions):
                self.draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False

tetris_ai = tetris_ai()
Tetris = Tetris()
Tetris.start()