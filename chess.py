
import math
import copy
import time
import random
import pygame
import numpy as np

BLUE = (100, 100, 200)

class EffectList():
    def __init__(self):
        self.effects = {
            'boardFog': False,
            'traitFog': False,
            'baseTraits': False,
            'societies': False}
    def setTrue(self, name):
        self.effects[name] = True

piece_table = {
    'P': [ [0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, -20, -20, 10, 10, 5],
           [5, -5, -10, 0, 0, -10, -5, 5], [0, 0, 0, 20, 20, 0, 0, 0],
           [5, 5, 10, 25, 25, 10, 5, 5], [10, 10, 20, 30, 30, 20, 10, 10],
           [50, 50, 50, 50, 50, 50, 50, 50], [0, 0, 0, 0, 0, 0, 0, 0] ],
    'N': [ [-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 0, 0, 0, -20, -40],
           [-30, 5, 10, 15, 15, 10, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30],
           [-30, 0, 10, 15, 15, 10, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30],
           [-40, -20, 0, 5, 5, 0, -20, -40], [-50, -40, -30, -30, -30, -30, -40, -50]],
    'B': [ [-20, -10, -10, -10, -10, -10, -10, -20], [-10, 5, 0, 0, 0, 0, 5, -10],
           [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 0, 10, 10, 10, 10, 0, -10],
           [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 5, 10, 10, 5, 0, -10],
           [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -10, -10, -10, -10, -20] ],
    'R': [ [0, 0, 0, 5, 5, 0, 0, 0], [-5, 0, 0, 0, 0, 0, 0, -5],
           [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5],
           [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5],
           [5, 10, 10, 10, 10, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0] ],
    'Q': [ [-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 5, 0, 0, 0, 0, -10],
           [-10, 5, 5, 5, 5, 5, 0, -10], [0, 0, 5, 5, 5, 5, 0, -5],
           [-5, 0, 5, 5, 5, 5, 0, -5], [-10, 0, 5, 5, 5, 5, 0, -10],
           [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20] ],
    'K': [ [20, 30, 10, 0, 0, 10, 30, 20], [20, 20, 0, 0, 0, 0, 20, 20],
           [-10, -20, -20, -20, -20, -20, -20, -10], [-20, -30, -30, -40, -40, -30, -30, -20],
           [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30],
           [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30] ],
    'KE': [ [-50, -40, -30, -20, -20, -30, -40, -50], [-30, -20, -10, 0, 0, -10, -20, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30], [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30], [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -20, -10, 0, 0, -10, -20, -30], [-50, -40, -30, -20, -20, -30, -40, -50] ]
    }

IMAGES = {}

surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
pygame.draw.polygon(surface, (200, 0, 0),
                    [(50, 35), (75, 20), (95, 50), (50, 90), (5, 50), (25, 20)])
IMAGES['Heart'] = surface

surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
pygame.draw.polygon(surface, (200, 200, 0),
                    [(30, 50), (60, 20), (80, 20), (80, 40), (50, 70), (60, 80), (55, 85), (40, 70), (25, 85),
                     (15, 75), (30, 60), (15, 45), (20, 40)])
IMAGES['Sword'] = surface

for colour in [3*(0,), 3*(255,), (200, 100, 100), (200, 150, 100), (200, 200, 100), (150, 200, 100), (120, 180, 150), (100, 100, 200), (100, 100, 100)]:
    IMAGES[colour] = {}

    surface = pygame.Surface(2*(100,))
    IMAGES['-'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, (35, 15, 30, 20))
    pygame.draw.rect(surface, colour, (45, 35, 10, 35))
    pygame.draw.rect(surface, colour, (40, 70, 20, 5))
    pygame.draw.rect(surface, colour, (30, 75, 40, 10))

    IMAGES[colour]['P'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.polygon(surface, colour,
                        [(30, 75), (50, 44), (50, 36), (38, 43), (36, 42),
                         (30, 45), (20, 40), (30, 29), (32, 23), (34, 21),
                         (40, 15), (50, 20), (65, 40), (70, 55), (70, 75)])
    pygame.draw.rect(surface, colour, (30, 75, 40, 15))
    IMAGES[colour]['N'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.polygon(surface, colour,
                        [(35, 30), (50, 15),
                         (53, 18), (45, 35), (57, 22),
                         (65, 30), (58, 40), (42, 40)])
    pygame.draw.rect(surface, colour, (42, 40, 16, 35))
    pygame.draw.rect(surface, colour, (35, 75, 30, 5))
    pygame.draw.rect(surface, colour, (30, 80, 40, 10))
    IMAGES[colour]['B'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, (47, 15, 6, 10))#
    pygame.draw.rect(surface, colour, (35, 15, 6, 10))#
    pygame.draw.rect(surface, colour, (59, 15, 6, 10))#
    pygame.draw.rect(surface, colour, (35, 25, 30, 15))
    pygame.draw.rect(surface, colour, (40, 40, 20, 35))
    pygame.draw.rect(surface, colour, (35, 75, 30, 5))
    pygame.draw.rect(surface, colour, (30, 80, 40, 10))
    IMAGES[colour]['R'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.polygon(surface, colour,
                        [(36, 15), (42, 20), (50, 10), (58, 20), (66, 15),
                         (58, 30), (42, 30)])
    pygame.draw.rect(surface, colour, (42, 30, 16, 45))
    pygame.draw.rect(surface, colour, (39, 40, 22, 10))
    pygame.draw.rect(surface, colour, (35, 73, 30, 7))
    pygame.draw.rect(surface, colour, (30, 80, 40, 10))
    IMAGES[colour]['Q'] = surface

    surface = pygame.Surface(2*(100,), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, (47, 5, 6, 20))
    pygame.draw.rect(surface, colour, (42, 12, 16, 8))

    pygame.draw.rect(surface, colour, (35, 25, 30, 18))
    pygame.draw.rect(surface, colour, (40, 40, 20, 35))
    pygame.draw.rect(surface, colour, (35, 75, 30, 5))
    pygame.draw.rect(surface, colour, (30, 80, 40, 10))
    IMAGES[colour]['K'] = surface

def play(songName):
    music = pygame.mixer.music.load(songName)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

#play('music.mp3')

class Piece():
    def __init__(self, colour, value, pos):
        self.colour = colour
        self.pos = np.array(pos)
        
        self.traits = []
        self.status = []
        
        self.value = value
        self.strength = 1
        self.life = 1
        
    def getSymbol(self):
        return '-'
    def getPos(self):
        return self.pos
    def getColour(self):
        return self.colour
    def getValue(self):
        return self.value*(self.getLife()/2 + 0.5)
    def getStrength(self):
        return self.strength
    def getLife(self):
        return self.life
    def attack(self, piece):
        piece.damage(self.strength)
    def damage(self, amt):
        self.life -= amt
    def weaken(self, amt):
        self.strength = max(1, self.strength-amt)
        print(f'{self.strength=}')
    def isAlive(self):
        return self.life > 0
    def isEnemy(self, piece):
        return self.getColour() != piece.getColour()
    def getActions(self, board):
        return []
    def move(self, board, new_pos):
        piece = board.getPiece(new_pos)
        if piece == None:
            self.pos = new_pos
        else:
            self.attack(piece)
            if not piece.isAlive():
                self.pos = new_pos
                piece.deathEffects(board, self.getColour())
                board.getPieces().remove(piece)
        self.moveEffects(board)
    def moveEffects(self, board):
        pass
    def deathEffects(self, board, killing_colour):
        pass
    
class Blocker(Piece):
    def __init__(self, pos):
        super().__init__(3*(100,), 0, pos)
    def isEnemy(self, piece):
        return False
    def getActions(self, board):
        return []

class Pawn(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 1, pos)
        self.hasMoved = False
    def getSymbol(self):
        return 'P'
    def getActions(self, board):
        moves = []

        x = 1
        if self.getColour() != board.getPlayerColour():
            x = -1

        if board.getPiece(self.getPos() + np.array((0, 1*x))) == None:
            moves = [(0, 1*x)]
            if not self.hasMoved and board.getPiece(self.getPos() + np.array((0, 2*x))) == None:
                moves.append((0, 2*x))
                
        for pos in [(1, 1*x), (-1, 1*x)]:
            p = board.getPiece(self.getPos() + np.array(pos))
            if p != None and p.isEnemy(self):
                moves.append(pos)

        return [self.getPos() + np.array(move) for move in moves]
    def promote(self, board):
        board.getPieces().append(Queen(self.getColour(), self.getPos()))
        board.getPieces().remove(self)
    def moveEffects(self, board):
        self.hasMoved = True
        if self.getPos()[1] == board.getUpper():
            self.promote(board)

class Knight(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 3, pos)
    def getSymbol(self):
        return 'N'
    def getActions(self, board):
        moves = []
        for pos in [(1, 2), (1, -2), (-1, 2), (-1, -2),
                    (2, 1), (-2, 1), (2, -1), (-2, -1)]:
            pos = self.getPos() + np.array(pos)
            p = board.getPiece(pos)
            if (pos<board.getLower()).any() or\
               (pos>board.getUpper()).any():
                continue
            if p != None and not p.isEnemy(self):
                continue
            moves.append(pos)
        return moves

class Bishop(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 3, pos)
    def getSymbol(self):
        return 'B'
    def getActions(self, board):
        moves = []
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            d = np.array(direction)
            for i in range(1, 12):
                pos = self.getPos() + d*i
                if (pos<board.getLower()).any() or\
                   (pos>board.getUpper()).any():
                    break
                p = board.getPiece(pos)
                if p != None:
                    if p.isEnemy(self):
                        moves.append(pos)
                    break
                moves.append(pos)
        return moves

class Rook(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 5, pos)
        self.hasMoved = False
    def getSymbol(self):
        return 'R'
    def getActions(self, board):
        moves = []
        for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            d = np.array(direction)
            for i in range(1, 12):
                pos = self.getPos() + d*i
                if (pos<board.getLower()).any() or\
                   (pos>board.getUpper()).any():
                    break
                p = board.getPiece(pos)
                if p != None:
                    if p.isEnemy(self):
                        moves.append(pos)
                    break
                moves.append(pos)
        return moves
    def moveEffects(self, board):
        self.hasMoved = True

class Queen(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 9, pos)
    def getSymbol(self):
        return 'Q'
    def getActions(self, board):
        moves = []
        for direction in [(0, 1), (1, 0), (-1, 0), (0, -1),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            d = np.array(direction)
            for i in range(1, 12):
                pos = self.getPos() + d*i
                if (pos<board.getLower()).any() or\
                   (pos>board.getUpper()).any():
                    break
                p = board.getPiece(pos)
                if p != None:
                    if p.isEnemy(self):
                        moves.append(pos)
                    break
                moves.append(pos)
        return moves

class King(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, 100, pos)
        self.hasMoved = False
    def getSymbol(self):
        return 'K'
    def getActions(self, board):
        moves = []
        for pos in [(0, 1), (1, 0), (-1, 0), (0, -1),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            pos = self.getPos() + np.array(pos)
            p = board.getPiece(pos)
            if (pos<board.getLower()).any() or\
               (pos>board.getUpper()).any():
                continue
            if p != None and not p.isEnemy(self):
                continue
            moves.append(pos)

        if not self.hasMoved:
            x = 1
            if board.getPlayerColour() == 3*(0,):
                x = -1
                
            if board.getPiece(self.getPos() + np.array((1*x, 0))) == None and \
               board.getPiece(self.getPos() + np.array((2*x, 0))) == None and \
               isinstance(board.getPiece(self.getPos() + np.array((3*x, 0))), Rook) and \
               not board.getPiece(self.getPos() + np.array((3*x, 0))).isEnemy(self):
                moves.append(self.getPos() + np.array((3*x, 0)))
            if board.getPiece(self.getPos() + np.array((-1*x, 0))) == None and \
               board.getPiece(self.getPos() + np.array((-2*x, 0))) == None and \
               board.getPiece(self.getPos() + np.array((-3*x, 0))) == None and \
               isinstance(board.getPiece(self.getPos() + np.array((-4*x, 0))), Rook)\
               and not board.getPiece(self.getPos() + np.array((-4*x, 0))).isEnemy(self):
                moves.append(self.getPos() + np.array((-4*x, 0)))
        return moves
    def move(self, board, new_pos):
        piece = board.getPiece(new_pos)
        if piece == None:
            self.pos = new_pos
        else:
            if piece.isEnemy(self):
                self.attack(piece)
                if not piece.isAlive():
                    self.pos = new_pos
                    board.getPieces().remove(piece)
            elif (piece.getPos() > self.getPos()).any():
                self.pos += np.array((2, 0))
                piece.pos = self.pos - np.array((1, 0))
            else:
                self.pos -= np.array((2, 0))
                piece.pos = self.pos + np.array((1, 0))
        self.moveEffects(board)
    def moveEffects(self, board):
        self.hasMoved = True

class Move():
    def __init__(self, piece, pos, colour, val):
        self.piece = piece
        self.pos = pos
        self.colour = colour
        self.value = val

class Evaluator():
    def __init__(self):
        #self.memory = set()
        self.memory = {(0,0), (7,0), (4,0), (5,0),
                       (3,3), (3,4), (4,3), (4,4), (2,2), (5,2)}
    def findRandom(self, board, colour, rboard = None, rcolour= None, compDecisions = [], playerDecisions = []):
        
        moves = self.getMoves(board, colour)
        keys = list(moves.keys())
        values = []
        while values == []:
            if len(keys) == 0:
                print('----- end random -----')
                return
            piece = keys[random.randint(0, len(keys) - 1)]
            values = moves[piece]
            keys.remove(piece)
        pos = values[random.randint(0, len(values) - 1)]
        victim = board.getPiece(pos)
        if isinstance(victim, Glyph):
            victim.getRule().getEffect()(rboard, rcolour)
            compDecisions.extend(victim.getRule().getDecisions())
            playerDecisions.extend(victim.getRule().getDecisions())
        piece.move(board, pos)
        
    def findNext(self, boardState, colour, moves_left, start_time, _piece = None, _pos = None, _capture = False):
        
        if (moves_left <= 0 and (not _capture or (time.time() - start_time) > 6)) or moves_left <= -1:
            mult = -1
            if not colour == boardState.getCompColour():
                mult = -1
            return Move(_piece, _pos, colour, random.randint(-1,1) + 2*mult*self.getMaterialPoints(boardState, colour) \
                        + mult*self.getPosAdjustment(boardState, colour)/50)
        
        best_move = Move(None, None, None, float('-inf'))
        moves = self.getMoves(boardState, colour)
        for piece in moves.keys():
            for pos in moves[piece]:
                fake_board = copy.deepcopy(boardState)
                fake_piece = fake_board.getPiece(piece.getPos())
                capture = fake_board.getPiece(pos) != None
                fake_piece.move(fake_board, pos)
                _next = self.findNext(fake_board, self.oppColour(colour),
                                      moves_left-0.5, start_time, fake_piece, pos, capture)
                if best_move.value < _next.value:
                    best_move = Move(piece, pos, colour, _next.value)
        best_move.value = -best_move.value
        return best_move
                
                        
    def findBestFog(self, boardState, colour, cont = 2, _piece = None, _pos = None, memory = []):

        if not cont:
            king_alive = False
            points = round(math.sqrt(len(self.getSeeing(boardState, colour))), 1)
            for piece in boardState.getPieces():
                
                # Material Value
                if piece.getColour() != colour:
                    points -= piece.getValue()
                    continue
                points += piece.getValue()
                
                # Position Value
                x, y = piece.getPos()
                points += piece_table[piece.getSymbol()][7 - y][x]/100

                
                if piece.getSymbol() != 'K':
                    continue
                king_alive = True
                continue


            if not king_alive:
                points = float('-inf')
            
            return Move(_piece, _pos, colour, points)

        # Actual Search
        if cont % 2:
            best_move = Move(None, None, None, float('inf'))

            if memory == []:
                return Move(None, None, None, float('-inf'))

            moves = {}
            for piece in boardState.getPieces():
                #print(piece.getPos(), memory)
                if piece.getColour() != self.oppColour(colour) or not \
                   np.any(np.all(piece.getPos() == memory, axis=1)):
                    continue
                moves[piece] = piece.getActions(boardState)
        else:
            best_move = Move(None, None, None, float('-inf'))
            moves = self.getMoves(boardState, colour)
            
        for piece in moves.keys():
            for pos in moves[piece]:
                fake_board = copy.deepcopy(boardState)
                fake_piece = fake_board.getPiece(piece.getPos())
                fake_piece.move(fake_board, pos)
                _next = self.findBestFog(fake_board, colour, cont-1, fake_piece, pos,
                                         memory + [a for a in fake_piece.getActions(boardState)\
                                                   if boardState.getPiece(a) != None \
                                                   and boardState.getPiece(a).getColour() == boardState.getPlayerColour()])
                if cont % 2 and best_move.value > _next.value:
                    best_move = Move(piece, pos, colour, _next.value)
                elif best_move.value < _next.value:
                    best_move = Move(piece, pos, colour, _next.value)
            
        return best_move

    def findBest(self, boardState, colour):
        if isinstance(boardState, Board):
            print("ERROR - Board not BoardState")
        start = time.time()
        
        if boardState.getEffectList().effects['boardFog']:

            # Handle Memory
            seeing = self.getSeeing(boardState, colour)
            for i in seeing:
                piece = boardState.getPiece(i)
                if piece != None and piece.getColour() == boardState.getPlayerColour():
                    self.memory.add((i[0], i[1]))
            #for i in self.memory:
            #    if not random.randint(0, 2) and i not in seeing:
            #        self.memory.remove(i)
                    
            bestMove = self.findBestFog(boardState, colour, memory = [np.array((pos[0], pos[1])) for pos in self.memory])
        else:
            bestMove = self.findNext(boardState, colour, 1, start)

            
        print('time-taken: ', round(time.time() - start, 2))
        print('bot-confidence: ', -round(bestMove.value - 7, 1))
        bestMove.piece.move(boardState, bestMove.pos)
        
    def getPosAdjustment(self, board, colour):
        adjustment = 0
        for piece in board.getPieces():
            if piece.getColour() == colour:
                x, y = piece.getPos()
                adjustment += piece_table[piece.getSymbol()][7 - y][x]
            elif piece.getSymbol() in 'PRNBQK':
                x, y = piece.getPos()
                adjustment -= piece_table[piece.getSymbol()][7 - y][x]
        return adjustment
    def getMaterialPoints(self, board, colour):
        king_alive = False
        points = 0
            
        for piece in board.getPieces():
            if piece.getColour() == colour:
                points += piece.getValue()
                if piece.getSymbol() == 'K':
                    king_alive = True
            elif piece.getSymbol() in 'PRNBQK':
                points -= piece.getValue()
        if not king_alive:
            return float('-inf')
        return points
    def oppColour(self, colour):
        if colour == 3*(0,):
            return 3*(255,)
        return 3*(0,)
    def getSeeing(self, board, colour):
        moves = []
        for piece in board.getPieces():
            if piece.getColour() != colour and piece.getColour() != BLUE:
                continue
            moves.append(piece.getPos())
            moves.extend(piece.getActions(board))
        return moves
    def getMoves(self, board, colour):
        moves = {}
        for piece in board.getPieces():
            if piece.getColour() != colour:
                continue
            moves[piece] = piece.getActions(board)
        return moves

class BoardState():
    def __init__(self, bounds, pieces, colour, effectList):
        self.lower = bounds[0]
        self.upper = bounds[1]
        self.pieces = pieces
        self.playerColour = colour
        self.effectList = effectList
    def getUpper(self):
        return self.upper
    def getLower(self):
        return self.lower
    def getPieces(self):
        return self.pieces
    def getPiece(self, pos):
        for p in self.getPieces():
            if (p.getPos() == pos).all():
                return p
    def getPlayerColour(self):
        return self.playerColour
    def getCompColour(self):
        if self.getPlayerColour() == 3*(0,):
            return 3*(255,)
        return 3*(0,)
    def getEffectList(self):
        return self.effectList
    
class Board():
    def __init__(self, dims, pieces = [Pawn(3*(255,), (0,1)), Pawn(3*(0,), (0,6)),
                                       Pawn(3*(255,), (1,1)), Pawn(3*(0,), (1,6)),
                                       Pawn(3*(255,), (2,1)), Pawn(3*(0,), (2,6)),
                                       Pawn(3*(255,), (3,1)), Pawn(3*(0,), (3,6)),
                                       Pawn(3*(255,), (4,1)), Pawn(3*(0,), (4,6)),
                                       Pawn(3*(255,), (5,1)), Pawn(3*(0,), (5,6)),
                                       Pawn(3*(255,), (6,1)), Pawn(3*(0,), (6,6)),
                                       Pawn(3*(255,), (7,1)), Pawn(3*(0,), (7,6)),
                                       Knight(3*(255,), (1,0)), Knight(3*(0,), (1,7)),
                                       Knight(3*(255,), (6,0)), Knight(3*(0,), (6,7)),
                                       Bishop(3*(255,), (2,0)), Bishop(3*(0,), (2,7)),
                                       Bishop(3*(255,), (5,0)), Bishop(3*(0,), (5,7)),
                                       Rook(3*(255,), (0,0)), Rook(3*(0,), (0,7)),
                                       Rook(3*(255,), (7,0)), Rook(3*(0,), (7,7)),
                                       Queen(3*(255,), (3,0)), Queen(3*(0,), (3,7)),
                                       King(3*(255,), (4,0)), King(3*(0,), (4,7))],
                 bounds = (0, 7), pos = 0):
        self.screen_dims = dims
        if pos == 0:
            pos = 2*(dims[1]*1//5,)
        self.surface = pygame.Surface(2*(dims[1]*3//5,))
        self.rect = self.surface.get_rect(topleft=pos)
        self.tileSize = self.surface.get_width()//8
        self.lower = bounds[0]
        self.upper = bounds[1]

        if random.randint(0, 1):
            self.playerColour = 3*(255,)
        else:
            self.playerColour = 3*(255,)
            
        _pieces = []
        for p in pieces:
            _pieces.append(p)
        print(len(pieces))
        self.boardState = BoardState(bounds, _pieces, self.playerColour, EffectList())
        

    def getBoardState(self):
        return self.boardState
    def getUpper(self):
        return self.upper
    def getLower(self):
        return self.lower
    def getRect(self):
        return self.rect
    def getPlayerColour(self):
        return self.playerColour
    def getCompColour(self):
        if self.getPlayerColour() == 3*(0,):
            return 3*(255,)
        return 3*(0,)
    def getCoordFromClick(self, pos):
        x,y = pos
        x -= self.rect.x
        y -= self.rect.y
        x //= self.tileSize
        y //= self.tileSize
        y = 7 - y
        return np.array((x, y))
    def getPieceFromClick(self, pos):
        return self.getBoardState().getPiece(self.getCoordFromClick(pos))
    def draw(self, evalu, win):
        self.surface.fill(3*(0,))
        
        for i in range(self.getUpper() + 1):
            for j in range(self.getUpper() + 1):
                if (i+j)%2 == 0:
                    colour = 3*(155,)
                else:
                    colour = 3*(100,)
                pygame.draw.rect(self.surface, colour,
                                 (i*self.tileSize, j*self.tileSize,
                                  self.tileSize, self.tileSize))

        for piece in self.getBoardState().getPieces():
            x, y = piece.getPos()
            if piece.getSymbol() == '-':
                new_surface = pygame.transform.scale(IMAGES[piece.getSymbol()], 2*(self.tileSize,))
            else:
                new_surface = pygame.transform.scale(IMAGES[piece.getColour()][piece.getSymbol()], 2*(self.tileSize,))

            # piece attributes
            _x = 2
            if piece.getLife() > 1:
                for i in range(piece.getLife()-1):
                    new_surface.blit(pygame.transform.scale(IMAGES['Heart'], 2*(self.tileSize//5,)),
                                     (_x, self.tileSize*4//5 - 2))
                    _x += self.tileSize//5 + 2
            if piece.getStrength() > 1:
                for i in range(piece.getStrength()-1):
                    new_surface.blit(pygame.transform.scale(IMAGES['Sword'], 2*(self.tileSize//5,)),
                                     (_x, self.tileSize*4//5 - 2))
                    _x += self.tileSize//5 + 2
                    
            self.surface.blit(new_surface, (x*self.tileSize, (self.getUpper() - y)*self.tileSize))

        # Effects
        if self.getBoardState().getEffectList().effects['boardFog']:
            seeing = evalu.getSeeing(self.getBoardState(), self.getPlayerColour())
            for i in range(self.getUpper() + 1):
                for j in range(self.getUpper() + 1):
                    if len([x for x in seeing if ((i, j) == x).all()]) == 0:
                        pygame.draw.rect(self.surface, 3*(140,),
                                         (i*self.tileSize, (self.getUpper() - j)*self.tileSize,
                                          self.tileSize, self.tileSize))

        win.blit(self.surface, self.rect.topleft)
        
class Overhead():
    def __init__(self, dims, pos = 0):
        self.screen_dims = dims
        if pos == 0:
            pos = (dims[0]*3//8, 0)
        self.surface = pygame.Surface((dims[0]*1//4, dims[1]*1//10))
        self.rect = self.surface.get_rect(topleft=pos)
        self.lightSize = self.surface.get_height()//2
        self.light = 2
    def setLight(self, light):
        self.light = light
    def draw(self, win):
        self.surface.fill(3*(100,))
        if self.light == 4:
            self.surface.fill(3*(0,))
        if self.light > 0 and self.light < 4:
            pygame.draw.rect(self.surface, 3*(255,),
                             ((2*self.light-1)*self.surface.get_width()//7, self.lightSize//2,
                              self.lightSize, self.lightSize))
            
        win.blit(self.surface, self.rect.topleft)
    
class Rule():
    def __init__(self, title, text, effect = (lambda bState, color: None), decisions = []):
        self.effect = effect
        self.title = title
        self.text = text
        self.decisions = decisions
    def getInfo(self):
        return (self.title, self.text)
    def getEffect(self):
        return self.effect
    def getDecisions(self):
        return self.decisions

class Glyph(Piece):
    def __init__(self, colour, pos, rule = None):
        super().__init__(colour, 0, pos)
        if rule == None:
            self.rule = Rule(chr(50 + random.randint(0,50)), chr(50 + random.randint(0,50))+chr(50 + random.randint(0,50)))
        else:
            self.rule = rule
    def getSymbol(self):
        return 'P'
    def getRule(self):
        return self.rule
    def getActions(self, board):
        return []
    def deathEffects(self, board, colour):
        pass
        
class Footer():
    def __init__(self, dims, pos = 0):
        self.screen_dims = dims
        if pos == 0:
            pos = (dims[0]*1//3, dims[1]*9//10)
        self.surface = pygame.Surface((dims[0]*1//3, dims[1]*1//10))
        self.rect = self.surface.get_rect(topleft=pos)
        self.title = ''
        self.text = ''
        
    def updateText(self, info):
        self.title, self.text = info
    def draw(self, win):
        self.surface.fill(3*(50,))

        text = pygame.font.SysFont('comicsans', 30, True).render(self.title, 1, (220,220,220))
        self.surface.blit(text, (10, 10))
        text = pygame.font.SysFont('comicsans', 18, True).render(self.text, 1, (220,220,220))
        self.surface.blit(text, (10, 40))

        win.blit(self.surface, self.rect.topleft)

class GameManager():
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_dims = [info.current_w, info.current_h]
        self.board = Board(self.screen_dims)
        self.side = Board(self.screen_dims,
                          pieces = [Knight(BLUE, (3, 0)), Blocker((2, 2)), Blocker((4, 2)),
                                    Glyph((200, 100, 100), (1, 1), Rule("Board", "It's time we realise that the battlefield isn't just a flat square")),
                                    Glyph((200, 100, 100), (5, 1), Rule("Pieces","It's time we realise that your subjects are not just pieces")),
                                    Glyph((200, 100, 100), (3, 2), Rule("Societies","Choose which class gets priority",
                                               decisions = [Rule("Peasents", "Pawns get 1 armour",
                                                                 lambda bState, color: ([piece.damage(-1) for piece in bState.getPieces()\
                                                                                       if isinstance(piece, Pawn) and piece.getColour() == color],
                                                                                        bState.getEffectList().setTrue('societies'))),
                                                            Rule("Nobles", "Minor and Major pieces get 1 armour",
                                                                 lambda bState, color: ([piece.damage(-1) for piece in bState.getPieces()\
                                                                                       if not isinstance(piece, Pawn) and piece.getColour() == color],
                                                                                        bState.getEffectList().setTrue('societies')))])),
                                    Glyph((200, 100, 100), (2, 3), Rule("Hills and Valleys", "Players can place 3 hills and 3 valleys on their side of the board",
                                               decisions = [Rule("Hills and Valleys", "Place 3 hills and 3 valleys on your side of the board",
                                                                 lambda bState, color: None)])),# Haven't figured out how i'm doing this one
                                    Glyph((200, 100, 100), (6, 3), Rule("Individualism", "Pieces can now acquire traits",
                                                                 lambda bState, color: bState.getEffectList().setTrue('baseTraits'))),
                                    Glyph((200, 150, 100), (4, 3), Rule("Knighthood", "Knights have +1 armour and +1 damage",
                                                                 lambda bState, color: ([piece.damage(-1) for piece in bState.getPieces()\
                                                                                       if isinstance(piece, Knight)],
                                                                                      [piece.weaken(-1) for piece in bState.getPieces()\
                                                                                       if isinstance(piece, Knight)]))),
                                    Glyph((200, 150, 100), (0, 3), Rule("Fortifications", "Rooks have +2 armour",
                                                                 lambda bState, color: [piece.damage(-2) for piece in bState.getPieces()\
                                                                                       if isinstance(piece, Rook)])),
                                    Glyph((200, 150, 100), (2, 1), Rule("Armour", "All pieces have +1 armour",
                                                                 lambda bState, color: [piece.damage(-1) for piece in bState.getPieces()])),
                                    Glyph((200, 150, 100), (2, 4), Rule("Fog of War", "Can only see the tiles you can move to",
                                                                 lambda bState, color: bState.getEffectList().setTrue('boardFog'))),
                                    Glyph((200, 150, 100), (2, 4), Rule("Long Live the King", "Kings gain +2 Armour",
                                                                 lambda bState, color: [piece.damage(-2) for piece in bState.getPieces()\
                                                                                       if isinstance(piece, King)])),
                                    Glyph((200, 150, 100), (4, 4), Rule("Morale", "Pieces can get low or high morale",
                                                                 lambda bState, color: bState.getEffectList().setTrue('Morale'))),
                                    Glyph((200, 150, 100), (4, 4), Rule("FoodnStuff", "",
                                                                 lambda bState, color: None)),
                                    Glyph((200, 150, 100), (4, 4), Rule("Territory?", "",
                                                                 lambda bState, color: None)),
                                    Glyph((200, 150, 100), (4, 4), Rule("Crusades", "",
                                                                 lambda bState, color: None)),
                                    Glyph((200, 150, 100), (4, 4), Rule("Artillary", "",
                                                                 lambda bState, color: None))
                                    ],
                          pos = (self.screen_dims[0] - self.screen_dims[1]*4//5, self.screen_dims[1]*1//5))
        self.overhead = Overhead(self.screen_dims)
        self.footer = Footer(self.screen_dims)
        self.side.getBoardState().getEffectList()#.setTrue('boardFog') #####
        self.selectedPiece = None

        self.eval = Evaluator()
        self.playerTurn = True
        self.playerDecisions = []
        self.compDecisions = []
        self.mainBoard = True
        self.move_no = 0
        
        self.mainLoop()

    def mainLoop(self):
        end = False
        while not end:
            end = self.update()
            self.redraw()
        pygame.quit()
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if self.playerTurn:
                    self.playerTurn = False
                    moved = self.handle_player_move(pos)
                    if moved:
                        if self.move_no % 3 == 0 and self.mainBoard:
                            self.mainBoard = False
                            self.overhead.setLight(3)
                        else:
                            self.overhead.setLight(4)
                            self.redraw()
                            self.move_no += 1
                            self.handle_comp_move()
                            self.mainBoard = True
                            self.overhead.setLight(2)
                    self.playerTurn = True
                
    def handle_comp_move(self):
        if self.compDecisions != []:
            print(f'{self.compDecisions=}')
            decision = self.compDecisions[random.randint(0, len(self.compDecisions)-1)]
            print(f'{decision=}')
            decision.getEffect()(self.board.getBoardState(), self.board.getCompColour())
            self.compDecisions = []
        self.eval.findBest(self.board.getBoardState(), self.board.getCompColour())
        if self.move_no % 3 == 0:
            self.eval.findRandom(self.side.getBoardState(), BLUE, self.board.getBoardState(),
                                 self.board.getCompColour(), self.compDecisions, self.playerDecisions)
        self.move_no += 1
    def handle_player_move(self, pos):
        if self.side.getRect().collidepoint(pos):
            piece = self.side.getPieceFromClick(pos)
            if isinstance(piece, Glyph):
                self.footer.updateText(piece.getRule().getInfo())
        if self.board.getRect().collidepoint(pos) and self.mainBoard:
            piece = self.board.getPieceFromClick(pos)
            tile_pos = self.board.getCoordFromClick(pos)
            if self.selectedPiece == None:
                self.selectedPiece = piece
            elif len([action for action in self.selectedPiece.getActions(self.board.getBoardState())\
                      if (tile_pos == action).all() and \
                      self.selectedPiece.getColour() == self.board.getPlayerColour()]) > 0:
                if piece != None and self.board.getBoardState().getEffectList().effects['boardFog']:
                    self.eval.memory.add((tile_pos[0], tile_pos[1]))
                self.selectedPiece.move(self.board.getBoardState(), tile_pos)
                self.selectedPiece = None
                return True
            else:
                self.selectedPiece = piece
        elif self.side.getRect().collidepoint(pos) and not self.mainBoard:
            piece = self.side.getPieceFromClick(pos)
            tile_pos = self.side.getCoordFromClick(pos)
            if self.selectedPiece == None:
                self.selectedPiece = piece
            elif len([action for action in self.selectedPiece.getActions(self.side.getBoardState())\
                      if (tile_pos == action).all()]) > 0:
                if piece != None:
                    piece.getRule().getEffect()(self.board.getBoardState(), self.board.getPlayerColour())
                    self.compDecisions.extend(piece.getRule().getDecisions())
                    self.playerDecisions.extend(piece.getRule().getDecisions())
                self.selectedPiece.move(self.side.getBoardState(), tile_pos)
                self.selectedPiece = None
                return True
            else:
                self.selectedPiece = piece
            if isinstance(self.selectedPiece, Pawn):
                self.selectedPiece = None
        
                    
                        
    def redraw(self):
        self.window.fill((0,0,0))
        self.board.draw(self.eval, self.window)
        self.side.draw(self.eval, self.window)
        self.overhead.draw(self.window)
        self.footer.draw(self.window)
        pygame.display.update()

def main():
    pygame.display.set_caption("Chess-v2.0")
    GameManager()

pygame.init()
main()

