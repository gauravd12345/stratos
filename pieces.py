# Setting up a Piece class
class Piece:
    def __init__(self, board, x, y):
        self.color = abs(board[x][y]) // board[x][y]
        self.board = board
        self.x = x
        self.y = y
        


    
    # Getter function
    def getVar(self):
        return self.color, self.board, self.x, self.y


    # Places a piece on the board
    def placePiece(board, x1, y1, x2, y2, piece):
        board[x2][y2], board[x1][y1] = board[x1][y1], piece


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
            if board[x][y] > 0:
                new_x = x - z
            
            else:
                new_x = x + z

            if 0 <= new_x <= 7 and board[new_x][y] == 0:
                validList.append([x, y, new_x, y])

            else:
                break
        
        # Pawn capture functionality(checks left and right positions)
        try:
            if board[x - color][y - 1] * color < 0:
                validList.append([x, y, x - color, y - 1])

            if board[x - color][y + 1] * color < 0:
                validList.append([x, y, x - color, y + 1])

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
                        validList.append([x, y, i, j])

                elif abs(i - x) == 2 and abs(j - y) == 1:
                    if board[i][j] * color <= 0:
                        validList.append([x, y, i, j])

        return validList


class Bishop(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        validList = []

        try:
            # Top Left Diagonal
            for i in range(y + 1):
                if [x, y] != [x - i, y - i]:
                    if x - i >= 0 and y - i >= 0:
                        result = board[x - i][y - i] * color
                        if result <= 0:
                            validList.append([x, y, x - i, y - i])
                            if result < 0:               
                                break

                        else:
                            break

                    else:
                        break

        except:
            pass
        try:            
            # Top Right Diagonal
            for i in range(8 - y):     
                if [x, y] != [x - i, y + i]:
                    if x - i >= 0 and y + i >= 0:
                        result = board[x - i][y + i] * color
                        print(result)
                        if result <= 0:
                            validList.append([x, y, x - i, y + i])
                            if result < 0:
                                break

                        else:
                            break

                    else:
                        break
        except:
            pass
        try:
            # Bottom Left Diagonal
            for i in range(y + 1):         
                if [x, y] != [x + i, y - i]:
                    if x + i >= 0 and y - i >= 0:
                        result = board[x + i][y - i] * color
                        if result <= 0:
                            validList.append([x, y, x + i, y - i])
                            if result < 0:
                                break

                        else:
                            break
                    
                    else:
                        break

        except:
            pass    
        try:    
            # Bottom Right Diagonal
            for i in range(8 - y):
                result = board[x + i][y + i] * color
                if [x, y] != [x + i, y + i]:
                    if x + i >= 0 and y + i >= 0:
                        if result <= 0:
                            validList.append([x, y, x + i, y + i])
                            if result < 0:
                                break

                        else:
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
        
        # Left Horizontal
        for i in range(y + 1):
            if [x, y] != [x, y - i]:
                if y - i >= 0:
                    result = board[x][y - i] * color
                    if result <= 0:
                        validList.append([x, y, x, y - i])
                        if result < 0:               
                            break

                    else:
                        break
                
                else:
                    break
                
        # Right Horizontal
        for i in range(8 - y):
            if [x, y] != [x, y + i]:
                if y + i >= 0:
                    result = board[x][y + i] * color
                    if result <= 0:
                        validList.append([x, y, x, y + i])
                        if result < 0:               
                            break

                    else:
                        break

                else:
                    break

        # Top Vertical
        for i in range(x + 1):
            if [x, y] != [x - i, y]:
                result = board[x - i][y] * color
                if x - i >= 0:
                    if result <= 0:
                        validList.append([x, y, x - i, y])
                        if result < 0:               
                            break

                    else:
                        break

                else:
                    break

        # Bottom Vertical
        for i in range(8 - x):
            if [x, y] != [x + i, y]:
                result = board[x + i][y] * color
                if x + i >= 0:
                    if result <= 0:
                        validList.append([x, y, x + i, y])
                        if result < 0:               
                            break

                    else:
                        break

                else:
                    break

        return validList


class Queen(Piece):
    def validMoves(self):
        color, board, x, y = Piece.getVar(self)
        b = Bishop(board, x, y)
        r = Rook(board, x, y)

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
                            validList.append([x, y, cor1, cor2])

                cor2 += 1

            cor1 += 1 
            cor2 = y - 1   

        return validList        


