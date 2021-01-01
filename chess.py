import pygame

pygame.init()

#  Setting up the window
screen_width = 480
screen_height = 480
mod = (screen_height + screen_width) // 16
YELLOW = (225, 225, 0, 128)

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
def createBoard(board):
    win.blit(chessBoard, (0, 0))
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
    
def hoverRect(board, x, y):
    pygame.draw.rect(win, YELLOW, (y * mod, x * mod, mod, mod))

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
    curr_piece = 0
    curr_x, curr_y = 0, 0

    # Setting a gameloop
    while running:

        # Stuff that will run in the background
        
        createBoard(board) 
        
        piece = pieceUnderMouse(board) 
        x, y = getMousePos()    

        for event in pygame.event.get():
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

                    # Place the piece
                    Piece.placePiece(board, curr_x, curr_y, x, y)
                    

                isClicked = False
                
                    

        # If the mouse button is clicked
        if isClicked:
            board[curr_x][curr_y] = 0
            color = curr_piece // abs(curr_piece)
            if abs(curr_piece) == 1:
                curr = Pawn(color, board, curr_x, curr_y)

            elif abs(curr_piece) == 2:
                curr = Knight(color, board, curr_x, curr_y)

            elif abs(curr_piece) == 3:
                curr = Bishop(color, board, curr_x, curr_y)

            elif abs(curr_piece) == 4:
                curr = Rook(color, board, curr_x, curr_y)

            elif abs(curr_piece) == 5:
                curr = Queen(color, board, curr_x, curr_y)

            elif abs(curr_piece) == 6:
                curr = King(color, board, curr_x, curr_y)

            curr.validMoves()
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
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, 3):
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7:
                validList.append([new_x, y])
                hoverRect(board, new_x, y)

            else:
                break

class Knight(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, 3):
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7:
                validList.append([new_x, y])
                hoverRect(board, new_x, y)

            else:
                break

class Bishop(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, x):
            if color > 0:
                new_x = x - z
                new_y = y - z
            
            else:
                new_x = x + z
                new_y = y + z

            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                validList.append([new_x, new_y])
                hoverRect(board, new_x, new_y)

            else:
                break

        

class Rook(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, 3):
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7:
                validList.append([new_x, y])
                hoverRect(board, new_x, y)

            else:
                break

class Queen(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, 3):
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7:
                validList.append([new_x, y])
                hoverRect(board, new_x, y)

            else:
                break

class King(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for z in range(1, 3):
            if color > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7:
                validList.append([new_x, y])
                hoverRect(board, new_x, y)

            else:
                break



# Running the code
if __name__ == "__main__":
    main()
    pygame.quit()
   