import pygame
from pygame.constants import K_f, K_r
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King

pygame.init()
pygame.mixer.init()
#  Setting up the window
screen_width = 600
screen_height = 600
mod = (screen_height + screen_width) // 16
chess_sound = pygame.mixer.Sound("sounds/Chess_Move.wav")

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



white_king = [7, 4]
black_king = [0, 4]

# Creates out the chess board
def createBoard(board, validlist):
    win.blit(chessBoard, (0, 0))
    #availableBoxes(board)
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
    

# Moves a piece on the board(Drag and drop animation)
def movePiece(piece):
    pos = pygame.mouse.get_pos()
    if piece > 0:
        win.blit(white_pieces[piece - 1], 
            white_pieces[piece - 1].get_rect(center=pos))
    
    elif piece < 0:
        win.blit(black_pieces[abs(piece) - 1], 
            black_pieces[abs(piece) - 1].get_rect(center=pos))


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
        highlightRect(validlist[i][2], validlist[i][3])


def restart(board):
    return [[-4, -2, -3, -5, -6, -3, -2, -4],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
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

    board = newBoard


def createPiece(color, board, piece, x, y):
    piece = abs(piece)
    pieceMap = {1: Pawn(color, board, x, y),
                2: Knight(color, board, x, y),
                3: Bishop(color, board, x, y),
                4: Rook(color, board, x, y),
                5: Queen(color, board, x, y),
                6: King(color, board, x, y)}

    return pieceMap[piece]


def canPromote(x):
    if x == 0 or x == 7:
        return True
    
    return False

# Reduces validlist[0:3] to validlist[2:3]
# (It is done so due to how the program is made)
def reduce(validlist):
    newList = []
    for i in validlist:
        newList.append([i[2], i[3]])

    return newList


def availableBoxes(board):
    for i in range(len(board)):
        for j in range(len(board[i])):

            # Checks if the piece is black or white
            piece = board[i][j]
            if piece > 0: 
                pygame.draw.rect(win, BLACK, (j * mod, i * mod, mod, mod))

            elif piece < 0: 
                pygame.draw.rect(win, WHITE, (j * mod, i * mod, mod, mod))


# Finds all the squares "protected" by white
def validWhite(color, board):
    white = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                curr = createPiece(color, board, board[i][j], i, j)
                white += reduce(curr.validMoves())

    return white


# Finds all the squares "protected" by black
def validBlack(color, board):
    black = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] < 0:
                curr = createPiece(color, board, board[i][j], i, j)
                black += reduce(curr.validMoves())

    return black


# Checks if either of the kings are in check
def check(color, board, white_king, black_king):
    if black_king in validWhite(color, board):
        return True

    elif white_king in validBlack(color, board):
            return True

    return False

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

    board = [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0,  0,  0,  0],
             [ 1,  1,  1,  1,  1,  1,  1,  1],
             [ 4,  2,  3,  5,  6,  3,  2,  4]]


    # Important variables
    running = True 
    isClicked = False 
    
    curr = 0
    color = 1
    valid = []
    curr_piece = 10
    curr_x, curr_y = 10, 10

    # Setting a gameloop
    while running:

        # Stuff that will run in the background   
        createBoard(board, valid)     
        piece = pieceUnderMouse(board) 
        if curr_piece != 0:
            color = curr_piece // abs(curr_piece)
        x, y = getMousePos() 

        for event in pygame.event.get():
            state = pygame.key.get_pressed()
            if state[K_r]:
                board = restart(board)

            if state[K_f]:
                flipBoard(board)
                

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
                    if [curr_x, curr_y, x, y] in valid:
                        if abs(curr_piece) == 6:
                            if color > 0:
                                white_king = [x, y]

                            else:
                                black_king = [x, y]


                        # Place the piece
                        inCheck = check(color, board, white_king, black_king)   
                        if not inCheck:
                            Piece.placePiece(board, curr_x, curr_y, x, y)
                            pygame.mixer.Sound.play(chess_sound)
                            curr_piece = board[x][y]
                        
                        else:
                            print("King in check")
                
                isClicked = False
 
        
        # If the mouse button is clicked
        if isClicked: 
            board[curr_x][curr_y] = 0
            curr = createPiece(color, board, curr_piece, curr_x, curr_y)       
            valid = curr.validMoves()

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