import os
import sys
import pygame
from pygame.constants import AUDIO_ALLOW_CHANNELS_CHANGE
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King

pygame.init()
pygame.mixer.init()

#  Setting up the window
screen_width = 600
screen_height = 600
mod = (screen_height + screen_width) // 16

# Loading sounds
move_sound = pygame.mixer.Sound("sounds\move.wav")
capture_sound = pygame.mixer.Sound("sounds\capture.wav")

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
chessBoard = pygame.image.load("img/chess_board.png")


#  Loading the black and white chess pieces
white_pieces = [pygame.image.load("img/white_pieces/wP.png"),
                pygame.image.load("img/white_pieces/wN.png"),
                pygame.image.load("img/white_pieces/wB.png"),
                pygame.image.load("img/white_pieces/wR.png"),
                pygame.image.load("img/white_pieces/wQ.png"),
                pygame.image.load("img/white_pieces/wK.png")]

black_pieces = [pygame.image.load("img/black_pieces/bP.png"),
                pygame.image.load("img/black_pieces/bN.png"),
                pygame.image.load("img/black_pieces/bB.png"),
                pygame.image.load("img/black_pieces/bR.png"),
                pygame.image.load("img/black_pieces/bQ.png"),
                pygame.image.load("img/black_pieces/bK.png")]


# Defines each king's position throughout the game
white_king = [7, 4]
black_king = [0, 4]

# Creates out the chess board


def createBoard(board, white_king, black_king, validlist):
    win.blit(chessBoard, (0, 0))
    highlightValid(validlist)
    highlightCheck(board, white_king, black_king)
    for i in range(len(board)):
        for j in range(len(board[i])):

            # Checks if the piece is black or white
            piece = abs(board[i][j]) - 1
            if board[i][j] > 0:
                win.blit(white_pieces[piece], (j * mod, i * mod))

            elif board[i][j] < 0:
                win.blit(black_pieces[piece], (j * mod, i * mod))


# Highlights the king if it is in check
def highlightCheck(board, white_king, black_king):
    inCheck = check(board, white_king, black_king)
    if inCheck != 0:
        if inCheck == 1:
            highlightRect(RED, white_king[0], white_king[1])

        elif inCheck == -1:
            highlightRect(RED, black_king[0], black_king[1])


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


# Moves a piece on the board(Drag and drop animation)
def movePiece(piece):
    pos = pygame.mouse.get_pos()
    if piece > 0:
        win.blit(white_pieces[piece - 1],
                 white_pieces[piece - 1].get_rect(center=pos))

    elif piece < 0:
        win.blit(black_pieces[abs(piece) - 1],
                 black_pieces[abs(piece) - 1].get_rect(center=pos))


# Animation for highliting a rectangle
def highlightRect(col, x, y):
    pygame.draw.rect(win, col, (y * mod, x * mod, mod, mod))
    if abs(x - y) % 2 == 0:
        pygame.draw.rect(
            win, TAN, (y * mod + 3, x * mod + 3, mod - 6, mod - 6))

    else:
        pygame.draw.rect(win, DARK_TAN, (y * mod + 3,
                                         x * mod + 3, mod - 6, mod - 6))


# Highlights all the valid moves for a side
def highlightValid(validlist):
    if not validlist:
        return

    for i in range(len(validlist)):
        highlightRect(YELLOW, validlist[i][2], validlist[i][3])

# Creates a piece with defined properties
# See "Pieces" class


def createPiece(board, piece, x, y):
    piece = abs(piece)
    pieceMap = {1: Pawn(board, x, y),
                2: Knight(board, x, y),
                3: Bishop(board, x, y),
                4: Rook(board, x, y),
                5: Queen(board, x, y),
                6: King(board, x, y)}

    return pieceMap[piece]

# Checks if a pawn can promote


def canPromote(x):
    if x == 0 or x == 7:
        return True

    return False

# Shortens the piece coordinates
# Ex: [x1, y1, x2, y2] --> [x2, y2]


def reduce(validlist):
    newList = []
    for i in validlist:
        newList.append([i[2], i[3]])

    return newList

# Finds all the squares "protected" by white


def validWhite(board):
    white = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                curr = createPiece(board, board[i][j], i, j)
                white += curr.validMoves()

    return white


# Finds all the squares "protected" by black
def validBlack(board):
    black = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] < 0:
                curr = createPiece(board, board[i][j], i, j)
                black += curr.validMoves()

    return black


# Checks if either of the kings are in check
def check(board, white_king, black_king):
    if black_king in reduce(validWhite(board)):
        return -1

    if white_king in reduce(validBlack(board)):
        return 1

    return 0


"""
def castle():
    
    # Black side castling
    if x == 0:
        if board[x][y - 1] == 0 and board[x][y - 2] == 0 and board[x][y - 3] == 0:
            validList.append([x, y, x, y - 2])

        if board[x][y + 1] == 0 and board[x][y + 2] == 0:
            validList.append([x, y, x, y + 2])

    # White side castling
    if x == 7:
        if board[x][y + 1] == 0 and board[x][y + 2] == 0:
            validList.append([x, y, x, y + 2])

        if board[x][y - 1] == 0 and board[x][y - 2] == 0 and board[x][y - 3] == 0:
            validList.append([x, y, x, y - 2])  
"""
'''
# Creates a short "animation" for promotion
def promoteBox(color):
    new_y = int((mod // 2) * 7)
    off = (mod * 8) // 60
    dim = mod + 2 * off

    
    # Drawing the selectable promotions
    for i in range(4):
        pygame.draw.rect(win, WHITE, ((2 * i * mod) + mod // 2 - off, 
        new_y - off, dim, dim))
        if color > 0: 
            win.blit(white_pieces[i + 1], ((2 * i * mod) + mod // 2,
             new_y)) 

        elif color < 0: 
            win.blit(black_pieces[i + 1], ((2 * i * mod) + mod // 2, 
            new_y))

'''


def main(white_king, black_king):
    '''
      Representation of the chess board in an array
      Each number in the array represents a piece:

           0 - Empty Space
           1 - Pawn
           2 - Knight
           3 - Bishop
           4 - Rook
           5 - Queen
           6 - King

      Positive values indicate white pieces
      Negative values indicate black pieces

    '''
    # Chess board
    board = [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [1,  1,  1,  1,  1,  1,  1,  1],
             [4,  2,  3,  5,  6,  3,  2,  4]]

    # Important variables
    running = True
    isClicked = False

    curr = 0
    color = 1
    valid = []
    cm = False
    counter = 1
    curr_piece = 10
    canCastle = False
    curr_x, curr_y = 10, 10

    # Setting a gameloop
    while running:

        # Stuff that will run in the background
        createBoard(board, white_king, black_king, valid)
        piece = pieceUnderMouse(board)
        if curr_piece != 0:
            color = curr_piece // abs(curr_piece)
        x, y = getMousePos()

        for event in pygame.event.get():

            # Exits program
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
                    # Animation stuff
                    board[curr_x][curr_y] = curr_piece
                    lastPiece = board[x][y]
                    capture = board[x][y]
                    # Checks if the desired move is valid
                    if [curr_x, curr_y, x, y] in valid:
                        # Update the king's positions
                        if abs(curr_piece) == 6:
                            if color > 0:
                                white_king = [x, y]

                            else:
                                black_king = [x, y]

                        Piece.placePiece(board, curr_x, curr_y, x, y, 0)
                        inCheck = check(board, white_king, black_king)
                        counter *= -1

                        if inCheck != 0:
                            """
                            This part checks if there is a checkmate or not

                            It looks one move into the future to determine if 
                            a side has any possible moves that can be played
                            """
                            if inCheck > 0:
                                val = validWhite(board)

                            else:
                                val = validBlack(board)

                            count = 0

                            # Looping through all the possible moves
                            for i in val:

                                x1, y1, x2, y2 = i
                                last = board[x2][y2]

                                """
                                Here, we simulate all the possible moves that a side can
                                play by taking its "validMove" list and placing all of the 
                                moves on the board, one by one.

                                We then check if the king is in check if that move is played
                                and then reset the move so as to not disturb the game   
                                """
                                Piece.placePiece(board, x1, y1, x2, y2, 0)
                                if abs(board[x2][y2]) == 6:
                                    if color < 0:
                                        white_king = [x2, y2]

                                    elif color > 0:
                                        black_king = [x2, y2]

                                inCheck = check(board, white_king, black_king)
                                if inCheck != 0:
                                    count += 1

                                # Reseting the moves
                                Piece.placePiece(board, x2, y2, x1, y1, last)
                                if abs(board[x1][y1]) == 6:
                                    if color < 0:
                                        white_king = [x1, y1]

                                    elif color > 0:
                                        black_king = [x1, y1]

                            # Checking for checkmate
                            if count == len(val):
                                cm = True

                            else:
                                cm = False

                        # If a side puts itself in check
                        if color == inCheck:
                            Piece.placePiece(
                                board, x, y, curr_x, curr_y, lastPiece)
                            counter *= -1

                        elif color != inCheck:
                            if cm:
                                sys.exit()

                            if capture == 0:
                                pygame.mixer.Sound.play(move_sound)

                            else:
                                pygame.mixer.Sound.play(capture_sound)
                            curr_piece = board[x][y]

                isClicked = False

        # If the mouse button is clicked
        if isClicked:
            board[curr_x][curr_y] = curr_piece
            curr = createPiece(board, curr_piece, curr_x, curr_y)
            valid = curr.validMoves()
            board[curr_x][curr_y] = 0

            # Using drag n' drop functionality to move the piece
            movePiece(curr_piece)

        else:
            # Pawn Promotion functionality
            if abs(curr_piece) == 1 and curr_piece == piece:
                pr = 5
                if canPromote(x):
                    board[x][y] = pr * color
                    curr_piece = board[x][y]

        pygame.display.update()


# Running the code
if __name__ == "__main__":
    main(white_king, black_king)
    pygame.quit()
