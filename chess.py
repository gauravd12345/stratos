import pygame
import pathlib

from pygame.constants import K_f, K_r

pygame.init()

#  Setting up the window
screen_width = 600
screen_height = 600
mod = (screen_height + screen_width) // 16

# Colors
RED = (255, 0, 0, 50)
GREEN = (0, 255, 0, 50)
BLUE = (0, 0, 255, 50)
WHITE = (255, 255, 255, 50)
BLACK = (0, 0, 0, 50)
YELLOW = (255, 255, 0, 50)
TAN = (240, 217, 181, 128)
DARK_TAN = (181, 136, 99, 128)

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess")

#  Loading the chess board
chessBoard = pygame.transform.scale(pygame.image.load("img/chess_board.png"), 
(screen_width, screen_height));

#  Loading the black and white chess pieces
white_pieces = [pygame.transform.scale(pygame.image.load("img/white_pieces/wP.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/white_pieces/wN.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/white_pieces/wB.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/white_pieces/wR.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/white_pieces/wQ.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/white_pieces/wK.png"), 
                (mod, mod))]


black_pieces = [pygame.transform.scale(pygame.image.load("img/black_pieces/bP.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/black_pieces/bN.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/black_pieces/bB.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/black_pieces/bR.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/black_pieces/bQ.png"), 
                (mod, mod)),
                pygame.transform.scale(pygame.image.load("img/black_pieces/bK.png"), 
                (mod, mod))]


# Creates out the chess board
def createBoard(board, validlist):
    win.blit(chessBoard, (0, 0))
    highlightValid(validlist)
    for i in range(len(board)):
        for j in range(len(board[i])):

            # Checks if the piece is black or white
            piece = abs(board[i][j]) - 1
            if board[i][j] > 0: 
                win.blit(white_pieces[piece], (j * mod, i * mod)) 

            elif board[i][j] < 0: 
                win.blit(black_pieces[piece], (j * mod, i * mod))


# Returns mouse coordinates
def getMousePos():
    y, x = pygame.mouse.get_pos() 
    x //= mod
    y //= mod  

    return x, y


# Checks if there is a piece under the mouse
def pieceUnderMouse(board):
    x, y = getMousePos()
    return board[x][y]
    

def highlightRect(x, y):
    pygame.draw.rect(win, YELLOW, (y * mod, x * mod, mod, mod))
    if abs(x - y) % 2 == 0:
        pygame.draw.rect(win, TAN, (y * mod + 3, x * mod + 3, mod - 6, mod - 6))

    else:
        pygame.draw.rect(win, DARK_TAN, (y * mod + 3, x * mod + 3, mod - 6, mod - 6))


def highlightValid(validlist):
    if not validlist:
        return

    for i in range(len(validlist)):
        highlightRect(validlist[i][0], validlist[i][1])


def restart(board):
    return [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  3,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 1,  1,  1,  1,  1,  1,  1,  1],
             [ 4,  2,  3,  5,  6,  3,  2,  4]]


def flipBoard(board):
    newBoard = []
    for i in range(len(board)):
        newRow = []
        for j in range(len(board[i])):
            newRow.append(board[7 - i][7 - j])

        newBoard.append(newRow)

    return newBoard


def createPiece(color, board, piece, x, y):
    piece = abs(piece)
    pieceMap = {1: Pawn(color, board, x, y),
                2: Knight(color, board, x, y),
                3: Bishop(color, board, x, y),
                4: Rook(color, board, x, y),
                5: Queen(color, board, x, y),
                6: King(color, board, x, y)}

    return pieceMap[piece]


def main():

    #  Representation of the chess board in an array
    #  Each number in the array represents a piece:
    #   
    #       0 - Empty Space
    #       1 - Pawn
    #       2 - Knight
    #       3 - Bishop
    #       4 - Rook
    #       5 - Queen
    #       6 - King
    #
    #  Positive values indicate white pieces
    #  Negative values indicate black pieces


    board = [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  3,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 1,  1,  1,  1,  1,  1,  1,  1],
             [ 4,  2,  3,  5,  6,  3,  2,  4]]


    # Important variables
    running = True 
    isClicked = False 
    
    curr = 0
    valid = []
    curr_piece = 0
    curr_x, curr_y = 0, 0

    # Setting a gameloop
    while running:

        # Stuff that will run in the background
        
        
        createBoard(board, valid) 
        
        piece = pieceUnderMouse(board) 
        x, y = getMousePos()    

        for event in pygame.event.get():
            state = pygame.key.get_pressed()
            if state[K_r]:
                board = restart(board)

            if state[K_f]:
                board = flipBoard(board)
                

            if event.type == pygame.QUIT:
                running = False
            
            # Checking if the mouse has been pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != 0 and not isClicked:

                    # Set the clicked piece as the current piece
                    curr_piece = piece
                    curr_x, curr_y = x, y
                    isClicked = True
                    
                    
            # Checking if the mouse has been released
            if event.type == pygame.MOUSEBUTTONUP:
                if isClicked:
                    
                    board[curr_x][curr_y] = curr_piece
                    print(curr_x, curr_y, x, y)
                    if [x, y] in valid:
                        
                        # Place the piece
                        Piece.placePiece(board, curr_x, curr_y, x, y)

        
                isClicked = False
                
                
        # If the mouse button is clicked
        if isClicked:
            board[curr_x][curr_y] = 0
            color = curr_piece // abs(curr_piece)
            curr = createPiece(color, board, curr_piece, curr_x, curr_y)

            valid = curr.validMoves()
            # Using drag n' drop functionality to move the piece
            Piece.movePiece(curr_piece)
        
        pygame.display.update()


# Setting up a Piece class
class Piece:
    def __init__(self, color, board, x, y):
        self.color = color
        self.board = board
        self.x = x
        self.y = y

    
    # Acts as a getter function
    def getVar(self):
        return self.color, self.board, self.x, self.y

    # Moves a piece on the board(Drag and drop)
    def movePiece(piece):
        pos = pygame.mouse.get_pos()
        if piece > 0:
            win.blit(white_pieces[piece - 1], 
                white_pieces[piece - 1].get_rect(center=pos))
        
        elif piece < 0:
            win.blit(black_pieces[abs(piece) - 1], 
                black_pieces[abs(piece) - 1].get_rect(center=pos))


    # Places a piece on the board
    def placePiece(board, x1, y1, x2, y2):
        board[x2][y2], board[x1][y1] = board[x1][y1], 0


class Pawn(Piece):

    # Generates valid moves for a pawn
    def validMoves(self):
        # Gets info about pawn at (x, y)
        color, board, x, y = Piece.getVar(self)

        # Checking if its positioned at original spot/hasn't moved yet
        validList = []
        if x == 1 or x == 6:
            end = 3
        
        else:
            end = 2

        for z in range(1, end):

            # Only checking for vertical moves
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7 and board[new_x][y] == 0:
                validList.append([new_x, y])

            else:
                break
        
        # Pawn capture functionality(checks left and right positions)
        if board[x - color][y - 1] * color < 0:
            validList.append([x - color, y - 1])

        if board[x - color][y + 1] * color < 0:
            validList.append([x - color, y + 1])

        return validList


class Knight(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        

        return validList


class Bishop(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if abs(i - x) == abs(j - y):
                    if [i, j] != [x, y]:
                        validList.append([i, j])

        return validList


class Rook(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if i == x or j == y:
                    if [i, j] != [x, y]:
                        validList.append([i, j])

        return validList


class Queen(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        b = Bishop(color, board, x, y)
        r = Rook(color, board, x, y)

        return b.validMoves() + r.validMoves()


class King(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        cor1, cor2 = x - 1, y - 1
        for i in range(3):
            for j in range(3):
                if 0 <= cor1 <= 7 and 0 <= cor2 <= 7: 
                    if board[cor1][cor2] * color <= 0:
                        if [cor1, cor2] != [x, y]:
                            validList.append([cor1, cor2])

                cor2 += 1

            cor1 += 1 
            cor2 = y - 1   

        return validList        

# Running the code
if __name__ == "__main__":
    main()
    pygame.quit()
   