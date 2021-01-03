

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
        try:
            if board[x - color][y - 1] * color < 0:
                validList.append([x - color, y - 1])

            if board[x - color][y + 1] * color < 0:
                validList.append([x - color, y + 1])

        except:
            pass

        return validList


class Knight(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if abs(i - x) == 1 and abs(j - y) == 2:
                    if board[i][j] * color <= 0:
                        validList.append([i, j])

                elif abs(i - x) == 2 and abs(j - y) == 1:
                    if board[i][j] * color <= 0:
                        validList.append([i, j])

        return validList


class Bishop(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        try:
            for i in range(y + 1):
                if [x, y] != [x - i, y - i]:
                    result = board[x - i][y - i] * color
                    if result <= 0:
                        validList.append([x - i, y - i])
                        if result < 0:               
                            break

                    else:
                        break

            for i in range(y + 1):         
                if [x, y] != [x + i, y - i]:
                    result = board[x + i][y - i] * color
                    if result <= 0:
                        validList.append([x + i, y - i])
                        if result < 0:
                            break

                    else:
                        break

            for i in range(8 - y):
                result = board[x - i][y + i] * color
                if [x, y] != [x - i, y + i]:
                    if result <= 0:
                        validList.append([x - i, y + i])
                        if result < 0:
                            break

                    else:
                        break

            for i in range(8 - y):
                result = board[x + i][y + i] * color
                if [x, y] != [x + i, y + i]:
                    if result <= 0:
                        validList.append([x + i, y + i])
                        if result < 0:
                            break

                    else:
                        break
        except:
            pass

        return validList


class Rook(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []
        try:
            for i in range(y + 1):
                if [x, y] != [x, y - i]:
                    result = board[x][y - i] * color
                    if result <= 0:
                        validList.append([x, y - i])
                        if result < 0:               
                            break

                    else:
                        break

            for i in range(x + 1):
                if [x, y] != [x - i, y]:
                    result = board[x - i][y] * color
                    if result <= 0:
                        validList.append([x - i, y])
                        if result < 0:               
                            break

                    else:
                        break
            
            for i in range(8 - y):
                if [x, y] != [x, y + i]:
                    result = board[x][y + i] * color
                    if result <= 0:
                        validList.append([x, y + i])
                        if result < 0:               
                            break

                    else:
                        break

            for i in range(8 - x):
                if [x, y] != [x + i, y]:
                    result = board[x + i][y] * color
                    if result <= 0:
                        validList.append([x + i, y])
                        if result < 0:               
                            break

                    else:
                        break

        except:
            pass

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

